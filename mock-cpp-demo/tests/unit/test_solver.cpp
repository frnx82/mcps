/**
 * @file test_solver.cpp
 * @brief Unit tests for the FEA solver.
 *
 * Uses a simple assert-based test framework (no external dependencies).
 */

#include "solver/FEASolver.h"
#include "solver/SparseMatrix.h"
#include "mesh/MeshGenerator.h"
#include "utils/MathUtils.h"

#include <iostream>
#include <cassert>
#include <cmath>
#include <string>

#define TEST(name) void name(); \
    static struct name##_register { \
        name##_register() { tests.push_back({#name, name}); } \
    } name##_instance; \
    void name()

#define ASSERT_NEAR(a, b, tol) \
    if (std::abs((a) - (b)) > (tol)) { \
        std::cerr << "FAIL: " << #a << " = " << (a) << ", expected " << (b) \
                  << " ± " << (tol) << " at " << __FILE__ << ":" << __LINE__ << "\n"; \
        test_failed = true; \
    }

#define ASSERT_TRUE(expr) \
    if (!(expr)) { \
        std::cerr << "FAIL: " << #expr << " at " << __FILE__ << ":" << __LINE__ << "\n"; \
        test_failed = true; \
    }

using namespace cae;

static bool test_failed = false;
static std::vector<std::pair<std::string, void(*)()>> tests;

// ── Test: Sparse Matrix ─────────────────────────────────────────

void test_sparse_matrix_basic() {
    SparseMatrix mat(3, 3);
    mat.addValue(0, 0, 4.0);
    mat.addValue(0, 1, -1.0);
    mat.addValue(1, 0, -1.0);
    mat.addValue(1, 1, 4.0);
    mat.addValue(1, 2, -1.0);
    mat.addValue(2, 1, -1.0);
    mat.addValue(2, 2, 4.0);
    mat.finalize();

    ASSERT_NEAR(mat.getValue(0, 0), 4.0, 1e-10);
    ASSERT_NEAR(mat.getValue(0, 1), -1.0, 1e-10);
    ASSERT_NEAR(mat.getValue(1, 1), 4.0, 1e-10);
    ASSERT_NEAR(mat.getValue(2, 2), 4.0, 1e-10);
    ASSERT_NEAR(mat.getValue(0, 2), 0.0, 1e-10);  // Not stored
}

void test_sparse_matrix_multiply() {
    SparseMatrix mat(2, 2);
    mat.addValue(0, 0, 2.0);
    mat.addValue(0, 1, 1.0);
    mat.addValue(1, 0, 1.0);
    mat.addValue(1, 1, 3.0);
    mat.finalize();

    std::vector<double> x = {1.0, 2.0};
    std::vector<double> y;
    mat.multiply(x, y);

    ASSERT_NEAR(y[0], 4.0, 1e-10);  // 2*1 + 1*2
    ASSERT_NEAR(y[1], 7.0, 1e-10);  // 1*1 + 3*2
}

void test_sparse_matrix_duplicate_add() {
    SparseMatrix mat(2, 2);
    mat.addValue(0, 0, 1.0);
    mat.addValue(0, 0, 2.0);  // Duplicate — should sum
    mat.addValue(0, 0, 3.0);
    mat.finalize();

    ASSERT_NEAR(mat.getValue(0, 0), 6.0, 1e-10);  // 1 + 2 + 3
}

// ── Test: Math Utils ────────────────────────────────────────────

void test_dot_product() {
    std::vector<double> a = {1.0, 2.0, 3.0};
    std::vector<double> b = {4.0, 5.0, 6.0};
    ASSERT_NEAR(math::dot(a, b), 32.0, 1e-10);  // 1*4 + 2*5 + 3*6
}

void test_vector_norm() {
    std::vector<double> v = {3.0, 4.0};
    ASSERT_NEAR(math::norm(v), 5.0, 1e-10);
}

void test_determinant_3x3() {
    double m[] = {1, 2, 3, 0, 4, 5, 1, 0, 6};
    double det = math::determinant3x3(m);
    ASSERT_NEAR(det, 22.0, 1e-10);
}

void test_invert_3x3() {
    // Identity matrix
    double I[] = {1, 0, 0, 0, 1, 0, 0, 0, 1};
    double inv[9];
    ASSERT_TRUE(math::invert3x3(I, inv));
    for (int i = 0; i < 9; ++i) {
        ASSERT_NEAR(inv[i], I[i], 1e-10);
    }
}

void test_von_mises_uniaxial() {
    // Pure uniaxial stress: σ_vm = |σ₁₁|
    double stress[] = {100e6, 0, 0, 0, 0, 0};  // 100 MPa in X
    double vm = math::vonMisesStress(stress);
    ASSERT_NEAR(vm, 100e6, 1.0);  // Should be 100 MPa
}

void test_elasticity_matrix_symmetry() {
    double D[6][6];
    math::computeElasticityMatrix(200e9, 0.3, D);
    // D should be symmetric
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            ASSERT_NEAR(D[i][j], D[j][i], 1e-3);
        }
    }
}

void test_hex_shape_functions_partition_of_unity() {
    // Sum of all shape functions should = 1 at any point
    double N[8], dNdxi[8][3];
    math::hexShapeFunctions(0.5, -0.3, 0.7, N, dNdxi);
    double sum = 0.0;
    for (int i = 0; i < 8; ++i) sum += N[i];
    ASSERT_NEAR(sum, 1.0, 1e-12);
}

// ── Test: Mesh Generator ────────────────────────────────────────

void test_beam_mesh_creation() {
    auto mesh = MeshGenerator::createBeam(10.0, 1.0, 1.0, 4, 2, 2);
    // (4+1) × (2+1) × (2+1) = 45 nodes
    ASSERT_TRUE(mesh->numNodes() == 45);
    // 4 × 2 × 2 = 16 elements
    ASSERT_TRUE(mesh->numElements() == 16);
}

void test_beam_mesh_dimensions() {
    auto mesh = MeshGenerator::createBeam(10.0, 2.0, 3.0, 10, 4, 6);
    // Check corner nodes
    const Point3D& origin = mesh->getNode(0);
    ASSERT_NEAR(origin.x, 0.0, 1e-10);
    ASSERT_NEAR(origin.y, 0.0, 1e-10);
    ASSERT_NEAR(origin.z, 0.0, 1e-10);
}

void test_find_nodes_on_plane() {
    auto mesh = MeshGenerator::createBeam(10.0, 1.0, 1.0, 10, 2, 2);
    auto nodes = mesh->findNodesOnPlane(Point3D(0, 0, 0), Point3D(1, 0, 0), 0.001);
    // Nodes on x=0 plane: (2+1) × (2+1) = 9
    ASSERT_TRUE(nodes.size() == 9);
}

// ── Test: Solver (small problem) ────────────────────────────────

void test_solver_cantilever_beam() {
    // Small cantilever beam: 1 element
    auto mesh = MeshGenerator::createBeam(1.0, 0.1, 0.1, 1, 1, 1);

    Material steel;
    steel.name = "Steel";
    steel.youngs_modulus = 200e9;
    steel.poisson_ratio = 0.3;
    steel.density = 7850;
    steel.yield_strength = 250e6;

    FEASolver solver(mesh, steel);

    // Fix left face
    auto fixed = mesh->findNodesOnPlane(Point3D(0, 0, 0), Point3D(1, 0, 0), 0.001);
    for (int nid : fixed) {
        solver.addBC({nid, BCType::DISPLACEMENT, 0, 0, 0, true, true, true});
    }

    // Apply force on right face
    auto loaded = mesh->findNodesOnPlane(Point3D(1.0, 0, 0), Point3D(1, 0, 0), 0.001);
    for (int nid : loaded) {
        solver.addBC({nid, BCType::FORCE, 0, -100.0 / loaded.size(), 0});
    }

    SolverResult result = solver.solve();
    ASSERT_TRUE(result.converged);
    ASSERT_TRUE(result.max_displacement > 0);
    ASSERT_TRUE(result.max_von_mises_stress > 0);
}

// ── Main ────────────────────────────────────────────────────────

int main() {
    // Register tests manually (no macro magic for simplicity)
    tests.push_back({"test_sparse_matrix_basic", test_sparse_matrix_basic});
    tests.push_back({"test_sparse_matrix_multiply", test_sparse_matrix_multiply});
    tests.push_back({"test_sparse_matrix_duplicate_add", test_sparse_matrix_duplicate_add});
    tests.push_back({"test_dot_product", test_dot_product});
    tests.push_back({"test_vector_norm", test_vector_norm});
    tests.push_back({"test_determinant_3x3", test_determinant_3x3});
    tests.push_back({"test_invert_3x3", test_invert_3x3});
    tests.push_back({"test_von_mises_uniaxial", test_von_mises_uniaxial});
    tests.push_back({"test_elasticity_matrix_symmetry", test_elasticity_matrix_symmetry});
    tests.push_back({"test_hex_shape_functions_partition_of_unity", test_hex_shape_functions_partition_of_unity});
    tests.push_back({"test_beam_mesh_creation", test_beam_mesh_creation});
    tests.push_back({"test_beam_mesh_dimensions", test_beam_mesh_dimensions});
    tests.push_back({"test_find_nodes_on_plane", test_find_nodes_on_plane});
    tests.push_back({"test_solver_cantilever_beam", test_solver_cantilever_beam});

    int passed = 0, failed = 0;
    for (const auto& [name, func] : tests) {
        test_failed = false;
        std::cout << "  Running " << name << "... ";
        try {
            func();
            if (test_failed) {
                std::cout << "FAILED\n";
                failed++;
            } else {
                std::cout << "OK\n";
                passed++;
            }
        } catch (const std::exception& e) {
            std::cout << "EXCEPTION: " << e.what() << "\n";
            failed++;
        }
    }

    std::cout << "\n" << passed << " passed, " << failed << " failed, "
              << (passed + failed) << " total\n";
    return failed > 0 ? 1 : 0;
}
