/**
 * @file main.cpp
 * @brief CAE Solver Demo — Entry point.
 *
 * Demonstrates a complete FEA workflow:
 *   1. Generate a beam mesh
 *   2. Define material and boundary conditions
 *   3. Solve for displacements
 *   4. Post-process stresses
 *   5. Export results
 */

#include "solver/FEASolver.h"
#include "mesh/MeshGenerator.h"
#include "mesh/MeshRefinement.h"
#include "utils/Logger.h"

#include <iostream>
#include <iomanip>

using namespace cae;

void printBanner() {
    std::cout << R"(
  ╔═══════════════════════════════════════════════════════╗
  ║     CAE Solver Demo — Finite Element Analysis        ║
  ║     Mock Project for GitHub Copilot Enterprise Demo   ║
  ╚═══════════════════════════════════════════════════════╝
)" << std::endl;
}

void printResult(const SolverResult& result) {
    std::cout << "\n── Results ────────────────────────────────────────\n"
              << "  Converged:          " << (result.converged ? "YES" : "NO") << "\n"
              << "  Iterations:         " << result.iterations << "\n"
              << "  Residual:           " << std::scientific << result.residual_norm << "\n"
              << "  Solve time:         " << std::fixed << std::setprecision(3)
                                          << result.solve_time_seconds << " s\n"
              << "  Max displacement:   " << std::scientific << result.max_displacement << " m\n"
              << "  Max von Mises:      " << result.max_von_mises_stress << " Pa\n"
              << "  Strain energy:      " << result.total_strain_energy << " J\n"
              << "───────────────────────────────────────────────────\n";
}

int main(int argc, char* argv[]) {
    printBanner();

    // ── Step 1: Create mesh ─────────────────────────────────────
    LOG_INFO("Step 1: Generating beam mesh...");

    // Cantilever beam: 10m × 1m × 1m, 20×5×5 elements = 500 hex8 elements
    int nx = 20, ny = 5, nz = 5;
    if (argc > 1) nx = std::atoi(argv[1]);
    if (argc > 2) ny = std::atoi(argv[2]);
    if (argc > 3) nz = std::atoi(argv[3]);

    auto mesh = MeshGenerator::createBeam(10.0, 1.0, 1.0, nx, ny, nz);
    mesh->printSummary();

    // ── Step 2: Define material ─────────────────────────────────
    LOG_INFO("Step 2: Defining material properties...");

    Material steel;
    steel.name = "Structural Steel";
    steel.youngs_modulus = 200e9;     // 200 GPa
    steel.poisson_ratio = 0.3;
    steel.density = 7850;             // kg/m³
    steel.yield_strength = 250e6;     // 250 MPa
    steel.thermal_expansion = 12e-6;  // 1/K

    std::cout << "  Material: " << steel.name << "\n"
              << "  E = " << steel.youngs_modulus / 1e9 << " GPa\n"
              << "  ν = " << steel.poisson_ratio << "\n"
              << "  ρ = " << steel.density << " kg/m³\n";

    // ── Step 3: Create solver and apply BCs ─────────────────────
    LOG_INFO("Step 3: Setting up solver and boundary conditions...");

    FEASolver solver(mesh, steel);

    SolverConfig config;
    config.tolerance = 1e-8;
    config.max_iterations = 5000;
    config.use_preconditioner = true;
    config.verbose = false;
    solver.configure(config);

    // Fix left face (x=0): all displacements = 0
    auto fixed_nodes = mesh->findNodesOnPlane(
        Point3D(0, 0, 0),    // Point on plane
        Point3D(1, 0, 0),    // Normal (X direction)
        0.001                // Tolerance
    );
    LOG_INFO("  Fixed {} nodes on left face (x=0)", fixed_nodes.size());

    for (int nid : fixed_nodes) {
        solver.addBC({nid, BCType::DISPLACEMENT, 0, 0, 0, true, true, true});
    }

    // Apply downward force on right face (x=10m)
    auto loaded_nodes = mesh->findNodesOnPlane(
        Point3D(10.0, 0, 0), // Point on plane
        Point3D(1, 0, 0),    // Normal
        0.001
    );
    LOG_INFO("  Loaded {} nodes on right face (x=10m)", loaded_nodes.size());

    double total_force = -10000.0;  // -10 kN downward
    double force_per_node = total_force / loaded_nodes.size();
    for (int nid : loaded_nodes) {
        solver.addBC({nid, BCType::FORCE, 0, force_per_node, 0});
    }

    // ── Step 4: Solve ───────────────────────────────────────────
    LOG_INFO("Step 4: Solving K·u = f ...");

    solver.setProgressCallback([](int iter, double residual) {
        if (iter % 500 == 0) {
            LOG_INFO("  CG iteration {}: residual = {:.2e}", iter, residual);
        }
    });

    SolverResult result = solver.solve();
    printResult(result);

    // ── Step 5: Check against analytical solution ───────────────
    if (result.converged) {
        LOG_INFO("Step 5: Comparing with analytical solution...");

        // Euler-Bernoulli beam theory:
        // δ_max = F·L³ / (3·E·I)
        // I = b·h³/12 for rectangular cross-section
        double L = 10.0, b = 1.0, h = 1.0;
        double I = b * h * h * h / 12.0;
        double F = -total_force;  // Positive for formula
        double analytical_deflection = F * L * L * L / (3.0 * steel.youngs_modulus * I);

        std::cout << "\n  Analytical max deflection: " << std::scientific
                  << analytical_deflection << " m\n"
                  << "  FEA max displacement:      " << result.max_displacement << " m\n"
                  << "  Relative error:            "
                  << std::abs(result.max_displacement - analytical_deflection) / analytical_deflection * 100.0
                  << " %\n";

        // Check yield
        if (result.max_von_mises_stress > steel.yield_strength) {
            LOG_WARN("⚠️  Max von Mises stress ({:.1f} MPa) exceeds yield strength ({:.1f} MPa)!",
                     result.max_von_mises_stress / 1e6, steel.yield_strength / 1e6);
        } else {
            LOG_INFO("✅ Max von Mises stress ({:.1f} MPa) is within yield strength ({:.1f} MPa)",
                     result.max_von_mises_stress / 1e6, steel.yield_strength / 1e6);
        }
    }

    // ── Step 6: Export ──────────────────────────────────────────
    LOG_INFO("Step 6: Exporting results...");
    mesh->exportVTK("beam_mesh.vtk");
    LOG_INFO("  Mesh exported to beam_mesh.vtk");

    std::cout << "\n✅ Analysis complete.\n";
    return result.converged ? 0 : 1;
}
