/**
 * @file FEASolver.cpp
 * @brief Implementation of the Finite Element Analysis solver.
 */

#include "solver/FEASolver.h"
#include "solver/SparseMatrix.h"
#include "mesh/MeshGenerator.h"
#include "utils/MathUtils.h"
#include "utils/Logger.h"

#include <chrono>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <numeric>

#ifdef _OPENMP
#include <omp.h>
#endif

namespace cae {

// ── Implementation details (PIMPL) ──────────────────────────────

struct FEASolver::Impl {
    std::shared_ptr<Mesh> mesh;
    Material material;
    SolverConfig config;
    std::vector<BoundaryCondition> boundary_conditions;
    SparseMatrix stiffness_matrix;
    std::vector<double> force_vector;
    bool assembled = false;
    std::function<void(int, double)> progress_callback;
};

// ── Constructor / Destructor ────────────────────────────────────

FEASolver::FEASolver(std::shared_ptr<Mesh> mesh, const Material& material)
    : m_impl(std::make_unique<Impl>())
{
    m_impl->mesh = std::move(mesh);
    m_impl->material = material;

    // Validate material properties
    if (material.youngs_modulus <= 0) {
        throw std::invalid_argument("Young's modulus must be positive");
    }
    if (material.poisson_ratio <= 0 || material.poisson_ratio >= 0.5) {
        throw std::invalid_argument("Poisson's ratio must be in (0, 0.5)");
    }

    LOG_INFO("FEASolver created: {} nodes, {} elements",
             m_impl->mesh->numNodes(), m_impl->mesh->numElements());
}

FEASolver::~FEASolver() = default;

// ── Configuration ───────────────────────────────────────────────

void FEASolver::configure(const SolverConfig& config) {
    m_impl->config = config;

#ifdef _OPENMP
    if (config.num_threads > 0) {
        omp_set_num_threads(config.num_threads);
    }
    LOG_INFO("OpenMP enabled: {} threads", omp_get_max_threads());
#else
    if (config.use_openmp) {
        LOG_WARN("OpenMP requested but not available — running single-threaded");
    }
#endif
}

// ── Boundary Conditions ─────────────────────────────────────────

void FEASolver::addBC(const BoundaryCondition& bc) {
    if (bc.node_id < 0 || bc.node_id >= m_impl->mesh->numNodes()) {
        throw std::out_of_range("BC node_id out of range: " + std::to_string(bc.node_id));
    }
    m_impl->boundary_conditions.push_back(bc);
    m_impl->assembled = false;  // Invalidate assembly
}

void FEASolver::clearBCs() {
    m_impl->boundary_conditions.clear();
    m_impl->assembled = false;
}

// ── Assembly ────────────────────────────────────────────────────

void FEASolver::assemble() {
    auto start = std::chrono::high_resolution_clock::now();

    int num_nodes = m_impl->mesh->numNodes();
    int num_dof = num_nodes * 3;  // 3 DOF per node (ux, uy, uz)
    int num_elements = m_impl->mesh->numElements();

    LOG_INFO("Assembling stiffness matrix: {} DOFs, {} elements", num_dof, num_elements);

    // Initialize global stiffness matrix and force vector
    m_impl->stiffness_matrix = SparseMatrix(num_dof, num_dof);
    m_impl->force_vector.assign(num_dof, 0.0);

    // Estimate non-zeros: each hex8 element contributes 24×24 = 576 entries
    // but many are shared, so roughly nnz ≈ num_elements × 200
    m_impl->stiffness_matrix.reserve(static_cast<size_t>(num_elements) * 200);

    // ── Assemble element stiffness matrices ─────────────────────
    // This is the most expensive step: O(num_elements × 24²)
    //
    // For each element:
    //   1. Get element node coordinates
    //   2. Compute element stiffness matrix ke (24×24 for hex8)
    //   3. Scatter ke into global K using connectivity

#ifdef _OPENMP
    #pragma omp parallel for schedule(dynamic, 64)
#endif
    for (int e = 0; e < num_elements; ++e) {
        // Element stiffness matrix (24×24 for 8-node hex with 3 DOF/node)
        std::vector<double> ke(24 * 24, 0.0);
        computeElementStiffness(e, ke);

        const Element& elem = m_impl->mesh->getElement(e);
        int elem_dof = static_cast<int>(elem.node_ids.size()) * 3;

        // Scatter element stiffness into global matrix
        for (int i = 0; i < elem_dof; ++i) {
            int global_i = elem.node_ids[i / 3] * 3 + (i % 3);
            for (int j = 0; j < elem_dof; ++j) {
                int global_j = elem.node_ids[j / 3] * 3 + (j % 3);
                double val = ke[i * elem_dof + j];
                if (std::abs(val) > 1e-15) {
#ifdef _OPENMP
                    #pragma omp critical
#endif
                    m_impl->stiffness_matrix.addValue(global_i, global_j, val);
                }
            }
        }
    }

    m_impl->stiffness_matrix.finalize();

    // ── Apply force boundary conditions ─────────────────────────
    for (const auto& bc : m_impl->boundary_conditions) {
        if (bc.type == BCType::FORCE) {
            int base = bc.node_id * 3;
            m_impl->force_vector[base + 0] += bc.value_x;
            m_impl->force_vector[base + 1] += bc.value_y;
            m_impl->force_vector[base + 2] += bc.value_z;
        }
    }

    // ── Apply displacement (Dirichlet) boundary conditions ──────
    applyDirichletBCs();

    m_impl->assembled = true;

    auto end = std::chrono::high_resolution_clock::now();
    double elapsed = std::chrono::duration<double>(end - start).count();
    LOG_INFO("Assembly complete: {} non-zeros, {:.2f}s, {:.1f} MB",
             m_impl->stiffness_matrix.nonZeros(), elapsed,
             m_impl->stiffness_matrix.memoryUsage() / 1e6);
}

void FEASolver::computeElementStiffness(int elem_id, std::vector<double>& ke) {
    const Element& elem = m_impl->mesh->getElement(elem_id);

    // Get node coordinates for this element
    int num_nodes = static_cast<int>(elem.node_ids.size());
    double coords[8][3] = {};  // Max 8 nodes for hex8
    for (int n = 0; n < num_nodes; ++n) {
        const Point3D& pt = m_impl->mesh->getNode(elem.node_ids[n]);
        coords[n][0] = pt.x;
        coords[n][1] = pt.y;
        coords[n][2] = pt.z;
    }

    // Compute elasticity matrix D (6×6)
    double D[6][6] = {};
    math::computeElasticityMatrix(m_impl->material.youngs_modulus,
                                  m_impl->material.poisson_ratio, D);

    // Gauss quadrature (2×2×2 for hex8)
    std::vector<std::array<double, 3>> gauss_pts;
    std::vector<double> gauss_wts;
    math::gaussQuadratureHex(2, gauss_pts, gauss_wts);

    int elem_dof = num_nodes * 3;

    // ── Numerical integration over element ──────────────────────
    for (size_t gp = 0; gp < gauss_pts.size(); ++gp) {
        double xi  = gauss_pts[gp][0];
        double eta = gauss_pts[gp][1];
        double zeta = gauss_pts[gp][2];
        double w = gauss_wts[gp];

        // Shape functions and derivatives
        double N[8], dNdxi[8][3];
        math::hexShapeFunctions(xi, eta, zeta, N, dNdxi);

        // Jacobian: maps natural → physical coordinates
        double J[3][3];
        double detJ = math::computeJacobian(dNdxi, coords, J);

        if (detJ <= 0.0) {
            LOG_WARN("Negative Jacobian in element {} at Gauss point {} (detJ={:.2e})",
                     elem_id, gp, detJ);
            continue;
        }

        // Transform derivatives to physical coordinates: dNdx = J^{-1} · dNdxi
        double Jinv[3][3];
        double J_flat[9] = {J[0][0], J[0][1], J[0][2],
                            J[1][0], J[1][1], J[1][2],
                            J[2][0], J[2][1], J[2][2]};
        double Jinv_flat[9];
        math::invert3x3(J_flat, Jinv_flat);

        double dNdx[8][3] = {};
        for (int n = 0; n < num_nodes; ++n) {
            for (int i = 0; i < 3; ++i) {
                for (int j = 0; j < 3; ++j) {
                    dNdx[n][i] += Jinv_flat[i * 3 + j] * dNdxi[n][j];
                }
            }
        }

        // B-matrix (strain-displacement): 6 × 24
        double B[6][24] = {};
        math::computeBMatrix(dNdx, B);

        // ke += B^T · D · B · detJ · w
        // B is 6×24, D is 6×6, so B^T·D·B is 24×24
        for (int i = 0; i < elem_dof; ++i) {
            for (int j = 0; j < elem_dof; ++j) {
                double sum = 0.0;
                for (int k = 0; k < 6; ++k) {
                    for (int l = 0; l < 6; ++l) {
                        sum += B[k][i] * D[k][l] * B[l][j];
                    }
                }
                ke[i * elem_dof + j] += sum * detJ * w;
            }
        }
    }
}

void FEASolver::applyDirichletBCs() {
    // Penalty method: set K(i,i) = large_number, f(i) = large_number * prescribed_value
    // This avoids modifying the matrix structure while enforcing u(i) ≈ prescribed_value
    const double penalty = 1e20 * m_impl->material.youngs_modulus;

    for (const auto& bc : m_impl->boundary_conditions) {
        if (bc.type != BCType::DISPLACEMENT) continue;

        int base = bc.node_id * 3;
        if (bc.fixed_x) {
            m_impl->stiffness_matrix.setDiagonal(base + 0, penalty);
            m_impl->force_vector[base + 0] = penalty * bc.value_x;
        }
        if (bc.fixed_y) {
            m_impl->stiffness_matrix.setDiagonal(base + 1, penalty);
            m_impl->force_vector[base + 1] = penalty * bc.value_y;
        }
        if (bc.fixed_z) {
            m_impl->stiffness_matrix.setDiagonal(base + 2, penalty);
            m_impl->force_vector[base + 2] = penalty * bc.value_z;
        }
    }
}

// ── Solver ──────────────────────────────────────────────────────

SolverResult FEASolver::solve() {
    if (!m_impl->assembled) {
        assemble();
    }

    SolverResult result;
    auto start = std::chrono::high_resolution_clock::now();

    int num_dof = getNumDOF();
    LOG_INFO("Solving: {} DOFs, {} non-zeros, tol={:.1e}",
             num_dof, getNumNonZeros(), m_impl->config.tolerance);

    // Initial guess: zero displacement
    result.displacements.assign(num_dof, 0.0);

    // Solve K·u = f using Conjugate Gradient
    result.converged = conjugateGradient(
        m_impl->stiffness_matrix,
        m_impl->force_vector,
        result.displacements,
        m_impl->config.tolerance,
        m_impl->config.max_iterations
    );

    auto end = std::chrono::high_resolution_clock::now();
    result.solve_time_seconds = std::chrono::duration<double>(end - start).count();

    // Compute max displacement
    result.max_displacement = 0.0;
    for (int i = 0; i < m_impl->mesh->numNodes(); ++i) {
        double ux = result.displacements[i * 3 + 0];
        double uy = result.displacements[i * 3 + 1];
        double uz = result.displacements[i * 3 + 2];
        double mag = std::sqrt(ux * ux + uy * uy + uz * uz);
        result.max_displacement = std::max(result.max_displacement, mag);
    }

    // Post-process
    if (result.converged) {
        computeStresses(result);
        computeReactions(result);
    }

    LOG_INFO("Solve {}: {:.3f}s, {} iterations, max_disp={:.6e} m",
             result.converged ? "converged" : "FAILED",
             result.solve_time_seconds, result.iterations,
             result.max_displacement);

    return result;
}

bool FEASolver::conjugateGradient(const SparseMatrix& A,
                                   const std::vector<double>& b,
                                   std::vector<double>& x,
                                   double tol, int maxIter) {
    int n = static_cast<int>(b.size());

    // r = b - A*x  (initially x=0, so r=b)
    std::vector<double> r = b;
    std::vector<double> Ax(n, 0.0);
    A.multiply(x, Ax);
    for (int i = 0; i < n; ++i) r[i] -= Ax[i];

    // Jacobi preconditioner: M = diag(A)
    std::vector<double> z(n);
    if (m_impl->config.use_preconditioner) {
        for (int i = 0; i < n; ++i) {
            double diag = A.getDiagonal(i);
            z[i] = (std::abs(diag) > 1e-15) ? r[i] / diag : r[i];
        }
    } else {
        z = r;
    }

    std::vector<double> p = z;
    double rz = math::dot(r, z);
    double b_norm = math::norm(b);
    if (b_norm < 1e-15) b_norm = 1.0;

    std::vector<double> Ap(n);

    for (int iter = 0; iter < maxIter; ++iter) {
        A.multiply(p, Ap);
        double pAp = math::dot(p, Ap);
        if (std::abs(pAp) < 1e-30) break;

        double alpha = rz / pAp;

        // x = x + alpha * p
        // r = r - alpha * A*p
#ifdef _OPENMP
        #pragma omp parallel for simd
#endif
        for (int i = 0; i < n; ++i) {
            x[i] += alpha * p[i];
            r[i] -= alpha * Ap[i];
        }

        double r_norm = math::norm(r);
        double relative_residual = r_norm / b_norm;

        if (m_impl->config.verbose && iter % 100 == 0) {
            LOG_DEBUG("CG iter {}: residual = {:.6e}", iter, relative_residual);
        }
        if (m_impl->progress_callback && iter % 50 == 0) {
            m_impl->progress_callback(iter, relative_residual);
        }

        if (relative_residual < tol) {
            LOG_INFO("CG converged in {} iterations (residual={:.2e})", iter + 1, relative_residual);
            return true;
        }

        // Preconditioner
        if (m_impl->config.use_preconditioner) {
            for (int i = 0; i < n; ++i) {
                double diag = A.getDiagonal(i);
                z[i] = (std::abs(diag) > 1e-15) ? r[i] / diag : r[i];
            }
        } else {
            z = r;
        }

        double rz_new = math::dot(r, z);
        double beta = rz_new / rz;
        rz = rz_new;

        for (int i = 0; i < n; ++i) {
            p[i] = z[i] + beta * p[i];
        }
    }

    LOG_ERROR("CG did NOT converge after {} iterations", maxIter);
    return false;
}

// ── Post-processing ─────────────────────────────────────────────

void FEASolver::computeStresses(SolverResult& result) {
    int num_elements = m_impl->mesh->numElements();
    result.stresses.resize(num_elements, 0.0);
    result.total_strain_energy = 0.0;

    for (int e = 0; e < num_elements; ++e) {
        const Element& elem = m_impl->mesh->getElement(e);
        int num_nodes = static_cast<int>(elem.node_ids.size());

        // Get element displacements
        std::vector<double> ue(num_nodes * 3);
        for (int n = 0; n < num_nodes; ++n) {
            int gid = elem.node_ids[n];
            ue[n * 3 + 0] = result.displacements[gid * 3 + 0];
            ue[n * 3 + 1] = result.displacements[gid * 3 + 1];
            ue[n * 3 + 2] = result.displacements[gid * 3 + 2];
        }

        // Evaluate stress at element centroid (ξ=η=ζ=0)
        double coords[8][3] = {};
        for (int n = 0; n < num_nodes; ++n) {
            const Point3D& pt = m_impl->mesh->getNode(elem.node_ids[n]);
            coords[n][0] = pt.x;
            coords[n][1] = pt.y;
            coords[n][2] = pt.z;
        }

        double N[8], dNdxi[8][3];
        math::hexShapeFunctions(0, 0, 0, N, dNdxi);

        double J[3][3];
        math::computeJacobian(dNdxi, coords, J);

        double J_flat[9] = {J[0][0], J[0][1], J[0][2],
                            J[1][0], J[1][1], J[1][2],
                            J[2][0], J[2][1], J[2][2]};
        double Jinv[9];
        math::invert3x3(J_flat, Jinv);

        double dNdx[8][3] = {};
        for (int n = 0; n < num_nodes; ++n) {
            for (int i = 0; i < 3; ++i) {
                for (int j = 0; j < 3; ++j) {
                    dNdx[n][i] += Jinv[i * 3 + j] * dNdxi[n][j];
                }
            }
        }

        double B[6][24] = {};
        math::computeBMatrix(dNdx, B);

        // strain = B · ue
        double strain[6] = {};
        for (int i = 0; i < 6; ++i) {
            for (int j = 0; j < num_nodes * 3; ++j) {
                strain[i] += B[i][j] * ue[j];
            }
        }

        // stress = D · strain
        double D[6][6] = {};
        math::computeElasticityMatrix(m_impl->material.youngs_modulus,
                                      m_impl->material.poisson_ratio, D);
        double stress[6] = {};
        for (int i = 0; i < 6; ++i) {
            for (int j = 0; j < 6; ++j) {
                stress[i] += D[i][j] * strain[j];
            }
        }

        result.stresses[e] = math::vonMisesStress(stress);

        // Strain energy: U_e = 0.5 · ue^T · ke · ue ≈ 0.5 · strain^T · stress · V_e
        double vol = m_impl->mesh->elementVolume(e);
        double se = 0.0;
        for (int i = 0; i < 6; ++i) se += strain[i] * stress[i];
        result.total_strain_energy += 0.5 * se * vol;
    }

    result.max_von_mises_stress = *std::max_element(result.stresses.begin(),
                                                     result.stresses.end());
    LOG_INFO("Post-processing: max von Mises = {:.4e} Pa, strain energy = {:.4e} J",
             result.max_von_mises_stress, result.total_strain_energy);
}

void FEASolver::computeReactions(SolverResult& result) {
    int num_dof = getNumDOF();
    result.reactions.assign(num_dof, 0.0);

    // R = K · u - f
    m_impl->stiffness_matrix.multiply(result.displacements, result.reactions);
    for (int i = 0; i < num_dof; ++i) {
        result.reactions[i] -= m_impl->force_vector[i];
    }
}

// ── Accessors ───────────────────────────────────────────────────

int FEASolver::getNumDOF() const {
    return m_impl->mesh->numNodes() * 3;
}

int FEASolver::getNumNonZeros() const {
    return static_cast<int>(m_impl->stiffness_matrix.nonZeros());
}

void FEASolver::setProgressCallback(std::function<void(int, double)> cb) {
    m_impl->progress_callback = std::move(cb);
}

} // namespace cae
