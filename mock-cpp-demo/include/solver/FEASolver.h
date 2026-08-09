#pragma once
/**
 * @file FEASolver.h
 * @brief Finite Element Analysis solver for structural mechanics.
 *
 * Supports linear static analysis with various element types.
 * Uses sparse matrix storage (CSR format) for large-scale problems.
 *
 * Thread Safety: Solver is NOT thread-safe. Create one instance per thread.
 * Memory: For N nodes × 3 DOF, peak memory ≈ nnz(K) × 16 bytes.
 */

#include <vector>
#include <string>
#include <memory>
#include <functional>

namespace cae {

// Forward declarations
class SparseMatrix;
class Mesh;

/// Boundary condition types
enum class BCType {
    DISPLACEMENT,  ///< Fixed displacement (Dirichlet)
    FORCE,         ///< Applied force (Neumann)
    PRESSURE,      ///< Surface pressure load
    TEMPERATURE    ///< Thermal boundary condition
};

/// Represents a single boundary condition
struct BoundaryCondition {
    int node_id;            ///< Node where BC is applied
    BCType type;            ///< Type of boundary condition
    double value_x = 0.0;   ///< Value in X direction
    double value_y = 0.0;   ///< Value in Y direction
    double value_z = 0.0;   ///< Value in Z direction
    bool fixed_x = false;   ///< Whether X DOF is constrained
    bool fixed_y = false;   ///< Whether Y DOF is constrained
    bool fixed_z = false;   ///< Whether Z DOF is constrained
};

/// Material properties for isotropic linear elastic material
struct Material {
    std::string name;
    double youngs_modulus;   ///< Young's modulus (Pa)
    double poisson_ratio;    ///< Poisson's ratio (dimensionless, 0 < ν < 0.5)
    double density;          ///< Density (kg/m³)
    double yield_strength;   ///< Yield strength for von Mises check (Pa)
    double thermal_expansion;///< Coefficient of thermal expansion (1/K)
};

/// Result of a solver run
struct SolverResult {
    bool converged = false;
    int iterations = 0;
    double residual_norm = 0.0;
    double max_displacement = 0.0;
    double max_von_mises_stress = 0.0;
    double total_strain_energy = 0.0;
    std::vector<double> displacements;   ///< [ux0, uy0, uz0, ux1, uy1, uz1, ...]
    std::vector<double> stresses;        ///< Von Mises stress per element
    std::vector<double> reactions;       ///< Reaction forces at constrained DOFs
    double solve_time_seconds = 0.0;
};

/// Solver configuration
struct SolverConfig {
    double tolerance = 1e-8;         ///< Convergence tolerance
    int max_iterations = 10000;      ///< Maximum CG iterations
    bool use_preconditioner = true;  ///< Use Jacobi preconditioner
    bool use_openmp = true;          ///< Enable OpenMP parallelism
    int num_threads = 0;             ///< 0 = auto-detect
    bool verbose = false;            ///< Print iteration progress
};

/**
 * @class FEASolver
 * @brief Main solver class for linear static finite element analysis.
 *
 * Workflow:
 *   1. Create solver with mesh and material
 *   2. Apply boundary conditions
 *   3. Assemble global stiffness matrix
 *   4. Solve the system K·u = f
 *   5. Post-process (stresses, reactions)
 *
 * Example:
 * @code
 *   auto mesh = MeshGenerator::createBeam(10.0, 1.0, 1.0, 20, 5, 5);
 *   Material steel{"Steel", 200e9, 0.3, 7850, 250e6, 12e-6};
 *
 *   FEASolver solver(mesh, steel);
 *   solver.addBC({0, BCType::DISPLACEMENT, 0, 0, 0, true, true, true});
 *   solver.addBC({100, BCType::FORCE, 0, -1000, 0});
 *
 *   SolverResult result = solver.solve();
 *   if (result.converged) {
 *       std::cout << "Max displacement: " << result.max_displacement << " m\n";
 *   }
 * @endcode
 */
class FEASolver {
public:
    /// Construct solver with mesh and material
    FEASolver(std::shared_ptr<Mesh> mesh, const Material& material);
    ~FEASolver();

    /// Configure solver parameters
    void configure(const SolverConfig& config);

    /// Add a boundary condition
    void addBC(const BoundaryCondition& bc);

    /// Clear all boundary conditions
    void clearBCs();

    /// Assemble global stiffness matrix from element stiffness matrices
    /// This is the most computationally expensive step for large models.
    /// Time complexity: O(num_elements × element_dof²)
    void assemble();

    /// Solve the system K·u = f using Conjugate Gradient method
    /// @return SolverResult with displacements, stresses, and convergence info
    SolverResult solve();

    /// Post-process: compute stresses from displacements
    void computeStresses(SolverResult& result);

    /// Post-process: compute reaction forces at constrained DOFs
    void computeReactions(SolverResult& result);

    /// Get the number of degrees of freedom
    int getNumDOF() const;

    /// Get the number of non-zero entries in the stiffness matrix
    int getNumNonZeros() const;

    /// Set a progress callback for long-running solves
    void setProgressCallback(std::function<void(int iteration, double residual)> cb);

private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;

    /// Compute element stiffness matrix for a hexahedral element
    void computeElementStiffness(int elem_id, std::vector<double>& ke);

    /// Apply Dirichlet boundary conditions via penalty method
    void applyDirichletBCs();

    /// Conjugate Gradient solver with Jacobi preconditioner
    bool conjugateGradient(const SparseMatrix& A,
                           const std::vector<double>& b,
                           std::vector<double>& x,
                           double tol, int maxIter);
};

} // namespace cae
