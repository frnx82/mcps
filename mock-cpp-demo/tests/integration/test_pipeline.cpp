/**
 * @file test_pipeline.cpp
 * @brief Integration test: full analysis pipeline.
 */

#include "solver/FEASolver.h"
#include "mesh/MeshGenerator.h"
#include "mesh/MeshRefinement.h"
#include "utils/Logger.h"

#include <iostream>
#include <cassert>
#include <cmath>

using namespace cae;

int main() {
    std::cout << "\n── Integration Test: Full Pipeline ────────────\n";

    // Step 1: Create mesh
    auto mesh = MeshGenerator::createBeam(5.0, 0.5, 0.5, 10, 3, 3);
    assert(mesh->numNodes() > 0);
    assert(mesh->numElements() > 0);

    // Step 2: Define material
    Material aluminum;
    aluminum.name = "Aluminum 6061-T6";
    aluminum.youngs_modulus = 69e9;
    aluminum.poisson_ratio = 0.33;
    aluminum.density = 2700;
    aluminum.yield_strength = 276e6;

    // Step 3: Solve
    FEASolver solver(mesh, aluminum);

    auto fixed = mesh->findNodesOnPlane(Point3D(0, 0, 0), Point3D(1, 0, 0), 0.001);
    for (int nid : fixed) {
        solver.addBC({nid, BCType::DISPLACEMENT, 0, 0, 0, true, true, true});
    }

    auto loaded = mesh->findNodesOnPlane(Point3D(5.0, 0, 0), Point3D(1, 0, 0), 0.001);
    for (int nid : loaded) {
        solver.addBC({nid, BCType::FORCE, 0, -500.0 / loaded.size(), 0});
    }

    SolverResult result = solver.solve();

    // Verify
    assert(result.converged);
    assert(result.max_displacement > 0);
    assert(result.max_von_mises_stress > 0);
    assert(result.solve_time_seconds > 0);

    // Step 4: Adaptive refinement
    MeshRefinement refiner;
    auto errors = refiner.estimateError(*mesh, result.displacements);
    auto marked = refiner.markForRefinement(errors);

    std::cout << "  Mesh:          " << mesh->numNodes() << " nodes, "
              << mesh->numElements() << " elements\n"
              << "  Converged:     YES (" << result.iterations << " iterations)\n"
              << "  Max displ:     " << result.max_displacement << " m\n"
              << "  Max stress:    " << result.max_von_mises_stress / 1e6 << " MPa\n"
              << "  Marked refine: " << marked.size() << " elements\n";

    // Step 5: Export
    mesh->exportVTK("/tmp/test_pipeline.vtk");

    std::cout << "\n✅ Integration test PASSED\n";
    return 0;
}
