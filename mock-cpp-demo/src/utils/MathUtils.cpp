/**
 * @file MathUtils.cpp
 * @brief Math utility implementations for FEA computations.
 */

#include "utils/MathUtils.h"
#include <cstring>
#include <stdexcept>

namespace cae {
namespace math {

void denseMatVec(const std::vector<double>& A, int rows, int cols,
                 const std::vector<double>& x, std::vector<double>& y) {
    y.assign(rows, 0.0);
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            y[i] += A[i * cols + j] * x[j];
        }
    }
}

double determinant3x3(const double* m) {
    return m[0] * (m[4] * m[8] - m[5] * m[7])
         - m[1] * (m[3] * m[8] - m[5] * m[6])
         + m[2] * (m[3] * m[7] - m[4] * m[6]);
}

bool invert3x3(const double* m, double* inv) {
    double det = determinant3x3(m);
    if (std::abs(det) < 1e-30) return false;

    double inv_det = 1.0 / det;

    inv[0] =  (m[4] * m[8] - m[5] * m[7]) * inv_det;
    inv[1] = -(m[1] * m[8] - m[2] * m[7]) * inv_det;
    inv[2] =  (m[1] * m[5] - m[2] * m[4]) * inv_det;
    inv[3] = -(m[3] * m[8] - m[5] * m[6]) * inv_det;
    inv[4] =  (m[0] * m[8] - m[2] * m[6]) * inv_det;
    inv[5] = -(m[0] * m[5] - m[2] * m[3]) * inv_det;
    inv[6] =  (m[3] * m[7] - m[4] * m[6]) * inv_det;
    inv[7] = -(m[0] * m[7] - m[1] * m[6]) * inv_det;
    inv[8] =  (m[0] * m[4] - m[1] * m[3]) * inv_det;

    return true;
}

void gaussQuadratureHex(int order,
                        std::vector<std::array<double, 3>>& points,
                        std::vector<double>& weights) {
    points.clear();
    weights.clear();

    if (order == 1) {
        // 1-point rule: centroid
        points.push_back({0.0, 0.0, 0.0});
        weights.push_back(8.0);
    } else if (order == 2) {
        // 2×2×2 Gauss-Legendre (8 points)
        double g = 1.0 / std::sqrt(3.0);  // ≈ 0.5773
        double coords[] = {-g, g};
        for (double xi : coords) {
            for (double eta : coords) {
                for (double zeta : coords) {
                    points.push_back({xi, eta, zeta});
                    weights.push_back(1.0);
                }
            }
        }
    } else if (order == 3) {
        // 3×3×3 Gauss-Legendre (27 points)
        double g1 = std::sqrt(3.0 / 5.0);  // ≈ 0.7746
        double coords[] = {-g1, 0.0, g1};
        double wts[] = {5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0};
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                for (int k = 0; k < 3; ++k) {
                    points.push_back({coords[i], coords[j], coords[k]});
                    weights.push_back(wts[i] * wts[j] * wts[k]);
                }
            }
        }
    }
}

void gaussQuadratureTet(int order,
                        std::vector<std::array<double, 3>>& points,
                        std::vector<double>& weights) {
    points.clear();
    weights.clear();

    if (order == 1) {
        // 1-point centroid rule
        points.push_back({0.25, 0.25, 0.25});
        weights.push_back(1.0 / 6.0);
    } else if (order == 2) {
        // 4-point rule
        double a = (5.0 + 3.0 * std::sqrt(5.0)) / 20.0;
        double b = (5.0 - std::sqrt(5.0)) / 20.0;
        points.push_back({a, b, b});
        points.push_back({b, a, b});
        points.push_back({b, b, a});
        points.push_back({b, b, b});
        for (int i = 0; i < 4; ++i) weights.push_back(1.0 / 24.0);
    }
}

void hexShapeFunctions(double xi, double eta, double zeta,
                       double N[8], double dNdxi[8][3]) {
    // 8-node hexahedron shape functions
    // N_i = (1/8)(1 + xi_i·ξ)(1 + eta_i·η)(1 + zeta_i·ζ)
    double xi_n[]   = {-1, 1, 1, -1, -1, 1, 1, -1};
    double eta_n[]  = {-1, -1, 1, 1, -1, -1, 1, 1};
    double zeta_n[] = {-1, -1, -1, -1, 1, 1, 1, 1};

    for (int i = 0; i < 8; ++i) {
        double xi_factor   = 1.0 + xi_n[i] * xi;
        double eta_factor  = 1.0 + eta_n[i] * eta;
        double zeta_factor = 1.0 + zeta_n[i] * zeta;

        N[i] = 0.125 * xi_factor * eta_factor * zeta_factor;

        dNdxi[i][0] = 0.125 * xi_n[i]   * eta_factor * zeta_factor;
        dNdxi[i][1] = 0.125 * xi_factor  * eta_n[i]  * zeta_factor;
        dNdxi[i][2] = 0.125 * xi_factor  * eta_factor * zeta_n[i];
    }
}

double computeJacobian(const double dNdxi[8][3],
                       const double coords[8][3],
                       double J[3][3]) {
    std::memset(J, 0, 9 * sizeof(double));
    for (int n = 0; n < 8; ++n) {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                J[i][j] += dNdxi[n][i] * coords[n][j];
            }
        }
    }
    double J_flat[9] = {J[0][0], J[0][1], J[0][2],
                        J[1][0], J[1][1], J[1][2],
                        J[2][0], J[2][1], J[2][2]};
    return determinant3x3(J_flat);
}

void computeBMatrix(const double dNdx[8][3], double B[6][24]) {
    // B-matrix maps nodal displacements to strains:
    // ε = B · u
    // For 3D solid: 6 strain components (εxx, εyy, εzz, γxy, γyz, γxz)
    //               24 DOFs (8 nodes × 3 DOF)
    std::memset(B, 0, 6 * 24 * sizeof(double));

    for (int n = 0; n < 8; ++n) {
        int col = n * 3;

        // εxx = ∂u/∂x
        B[0][col + 0] = dNdx[n][0];

        // εyy = ∂v/∂y
        B[1][col + 1] = dNdx[n][1];

        // εzz = ∂w/∂z
        B[2][col + 2] = dNdx[n][2];

        // γxy = ∂u/∂y + ∂v/∂x
        B[3][col + 0] = dNdx[n][1];
        B[3][col + 1] = dNdx[n][0];

        // γyz = ∂v/∂z + ∂w/∂y
        B[4][col + 1] = dNdx[n][2];
        B[4][col + 2] = dNdx[n][1];

        // γxz = ∂u/∂z + ∂w/∂x
        B[5][col + 0] = dNdx[n][2];
        B[5][col + 2] = dNdx[n][0];
    }
}

void computeElasticityMatrix(double E, double nu, double D[6][6]) {
    // Isotropic linear elasticity (Hooke's law in 3D)
    // D = (E / ((1+ν)(1-2ν))) × [matrix]
    std::memset(D, 0, 36 * sizeof(double));

    double factor = E / ((1.0 + nu) * (1.0 - 2.0 * nu));

    D[0][0] = D[1][1] = D[2][2] = factor * (1.0 - nu);
    D[0][1] = D[0][2] = D[1][0] = D[1][2] = D[2][0] = D[2][1] = factor * nu;
    D[3][3] = D[4][4] = D[5][5] = factor * (1.0 - 2.0 * nu) / 2.0;
}

double vonMisesStress(const double stress[6]) {
    // σ_vm = √(0.5 × ((σ₁-σ₂)² + (σ₂-σ₃)² + (σ₃-σ₁)² + 6(τ₁₂² + τ₂₃² + τ₁₃²)))
    double s11 = stress[0], s22 = stress[1], s33 = stress[2];
    double s12 = stress[3], s23 = stress[4], s13 = stress[5];

    return std::sqrt(0.5 * ((s11 - s22) * (s11 - s22)
                          + (s22 - s33) * (s22 - s33)
                          + (s33 - s11) * (s33 - s11)
                          + 6.0 * (s12 * s12 + s23 * s23 + s13 * s13)));
}

} // namespace math
} // namespace cae
