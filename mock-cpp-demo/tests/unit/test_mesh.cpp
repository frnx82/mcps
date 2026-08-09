/**
 * @file test_mesh.cpp
 * @brief Unit tests for mesh generation and quality.
 */

#include "mesh/MeshGenerator.h"
#include "mesh/MeshRefinement.h"

#include <iostream>
#include <cassert>
#include <cmath>

using namespace cae;

static int passed = 0, failed = 0;

#define RUN_TEST(name) do { \
    std::cout << "  Running " << #name << "... "; \
    try { name(); std::cout << "OK\n"; passed++; } \
    catch (const std::exception& e) { std::cout << "FAILED: " << e.what() << "\n"; failed++; } \
} while(0)

#define EXPECT(cond) if (!(cond)) throw std::runtime_error(#cond)

void test_plate_mesh() {
    auto mesh = MeshGenerator::createPlate(5.0, 3.0, 10, 6);
    EXPECT(mesh->numNodes() == 77);   // (10+1) × (6+1)
    EXPECT(mesh->numElements() == 60); // 10 × 6
}

void test_element_volume() {
    auto mesh = MeshGenerator::createBeam(2.0, 1.0, 1.0, 2, 1, 1);
    // Each element: 1.0 × 1.0 × 1.0 = 1.0 m³
    double vol = mesh->elementVolume(0);
    EXPECT(std::abs(vol - 1.0) < 0.01);
}

void test_mesh_quality() {
    auto mesh = MeshGenerator::createBeam(1.0, 1.0, 1.0, 2, 2, 2);
    double quality = mesh->minElementQuality();
    EXPECT(quality > 0.99);  // Perfect cubes should have quality ≈ 1.0
}

void test_find_nodes_in_box() {
    auto mesh = MeshGenerator::createBeam(10.0, 1.0, 1.0, 10, 2, 2);
    auto nodes = mesh->findNodesInBox(Point3D(0, 0, 0), Point3D(1.0, 1.0, 1.0));
    EXPECT(nodes.size() > 0);
}

void test_vtk_export() {
    auto mesh = MeshGenerator::createBeam(1.0, 1.0, 1.0, 2, 2, 2);
    mesh->exportVTK("/tmp/test_mesh.vtk");
    // Just check it doesn't crash
}

void test_refinement_marking() {
    MeshRefinement refiner;
    std::vector<double> errors = {0.1, 0.5, 0.2, 0.8, 0.05, 0.9};
    auto marked = refiner.markForRefinement(errors, 0.5);
    // Elements with error > 0.5 * max(0.9) = 0.45 should be marked
    EXPECT(marked.size() >= 2);  // At least elements 3 and 5
}

void test_point3d_operations() {
    Point3D a(1, 2, 3);
    Point3D b(4, 5, 6);

    Point3D sum = a + b;
    EXPECT(std::abs(sum.x - 5.0) < 1e-10);
    EXPECT(std::abs(sum.y - 7.0) < 1e-10);
    EXPECT(std::abs(sum.z - 9.0) < 1e-10);

    double d = a.dot(b);
    EXPECT(std::abs(d - 32.0) < 1e-10);  // 1*4 + 2*5 + 3*6

    Point3D c = a.cross(b);
    EXPECT(std::abs(c.x - (-3.0)) < 1e-10);
    EXPECT(std::abs(c.y - 6.0) < 1e-10);
    EXPECT(std::abs(c.z - (-3.0)) < 1e-10);
}

int main() {
    std::cout << "\n── Mesh Tests ────────────────────────────────\n";

    RUN_TEST(test_plate_mesh);
    RUN_TEST(test_element_volume);
    RUN_TEST(test_mesh_quality);
    RUN_TEST(test_find_nodes_in_box);
    RUN_TEST(test_vtk_export);
    RUN_TEST(test_refinement_marking);
    RUN_TEST(test_point3d_operations);

    std::cout << "\n" << passed << " passed, " << failed << " failed\n";
    return failed > 0 ? 1 : 0;
}
