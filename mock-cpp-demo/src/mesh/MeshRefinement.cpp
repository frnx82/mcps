/**
 * @file MeshRefinement.cpp
 * @brief Adaptive mesh refinement implementation.
 */

#include "mesh/MeshRefinement.h"
#include "utils/Logger.h"
#include <algorithm>
#include <cmath>
#include <numeric>

namespace cae {

MeshRefinement::MeshRefinement() = default;
MeshRefinement::~MeshRefinement() = default;

std::vector<double> MeshRefinement::estimateError(const Mesh& mesh,
                                                   const std::vector<double>& displacements,
                                                   ErrorEstimator estimator) {
    int num_elements = mesh.numElements();
    std::vector<double> errors(num_elements, 0.0);

    // Simplified Zienkiewicz-Zhu error estimator:
    // Compare element stress (constant per element) with
    // smoothed nodal stress (averaged from neighboring elements).
    // The difference indicates discretization error.

    // Step 1: Compute element centroid stresses (already done in solver)
    // Step 2: Average stresses at nodes
    // Step 3: Error = ||σ_element - σ_smoothed||

    // For this demo, use a placeholder that flags elements with
    // large stress gradients
    for (int e = 0; e < num_elements; ++e) {
        // Compute a simple error indicator based on element size
        // Larger elements in high-stress regions need refinement
        double vol = mesh.elementVolume(e);
        double h = std::cbrt(vol);  // Characteristic element size

        // Error indicator ∝ h² × |∇σ|
        // Since we don't have the full stress field here, use displacement gradient
        const Element& elem = mesh.getElement(e);
        double max_disp = 0.0;
        double min_disp = 1e30;
        for (int nid : elem.node_ids) {
            if (nid * 3 + 2 < static_cast<int>(displacements.size())) {
                double ux = displacements[nid * 3 + 0];
                double uy = displacements[nid * 3 + 1];
                double uz = displacements[nid * 3 + 2];
                double mag = std::sqrt(ux * ux + uy * uy + uz * uz);
                max_disp = std::max(max_disp, mag);
                min_disp = std::min(min_disp, mag);
            }
        }

        // Error ∝ element size × displacement gradient
        errors[e] = h * h * (max_disp - min_disp);
    }

    LOG_INFO("Error estimation complete: max={:.4e}, avg={:.4e}",
             *std::max_element(errors.begin(), errors.end()),
             std::accumulate(errors.begin(), errors.end(), 0.0) / num_elements);

    return errors;
}

std::vector<int> MeshRefinement::markForRefinement(const std::vector<double>& errors,
                                                    double threshold) {
    if (errors.empty()) return {};

    double max_error = *std::max_element(errors.begin(), errors.end());
    double cutoff = threshold * max_error;

    std::vector<int> marked;
    for (size_t i = 0; i < errors.size(); ++i) {
        if (errors[i] > cutoff) {
            marked.push_back(static_cast<int>(i));
        }
    }

    LOG_INFO("Marked {} / {} elements for refinement (threshold={:.2f}, cutoff={:.4e})",
             marked.size(), errors.size(), threshold, cutoff);

    return marked;
}

std::shared_ptr<Mesh> MeshRefinement::refine(const Mesh& mesh,
                                              const std::vector<int>& marked_elements,
                                              RefinementStrategy strategy) {
    if (m_current_level >= m_max_level) {
        LOG_WARN("Maximum refinement level {} reached — skipping", m_max_level);
        return std::make_shared<Mesh>(mesh);
    }

    auto refined = std::make_shared<Mesh>();

    // Copy existing nodes
    for (int i = 0; i < mesh.numNodes(); ++i) {
        refined->addNode(mesh.getNode(i));
    }

    // Process each element
    std::vector<bool> is_marked(mesh.numElements(), false);
    for (int idx : marked_elements) {
        is_marked[idx] = true;
    }

    for (int e = 0; e < mesh.numElements(); ++e) {
        if (is_marked[e] && strategy != RefinementStrategy::UNIFORM) {
            // Split this element
            const Element& elem = mesh.getElement(e);
            if (elem.type == ElementType::HEX8) {
                splitHex8(mesh, e, refined);
            } else if (elem.type == ElementType::TET4) {
                splitTet4(mesh, e, refined);
            } else {
                // Copy unsupported element types unchanged
                refined->addElement(elem.type, elem.node_ids);
            }
        } else if (strategy == RefinementStrategy::UNIFORM) {
            const Element& elem = mesh.getElement(e);
            if (elem.type == ElementType::HEX8) {
                splitHex8(mesh, e, refined);
            } else {
                refined->addElement(elem.type, elem.node_ids);
            }
        } else {
            // Copy unmarked elements
            const Element& elem = mesh.getElement(e);
            refined->addElement(elem.type, elem.node_ids);
        }
    }

    // Fix hanging nodes at refinement boundaries
    if (strategy == RefinementStrategy::ADAPTIVE) {
        resolveHangingNodes(refined);
    }

    m_current_level++;

    LOG_INFO("Refinement level {}: {} → {} nodes, {} → {} elements",
             m_current_level, mesh.numNodes(), refined->numNodes(),
             mesh.numElements(), refined->numElements());

    return refined;
}

void MeshRefinement::splitHex8(const Mesh& mesh, int elem_id,
                                std::shared_ptr<Mesh>& refined_mesh) {
    const Element& elem = mesh.getElement(elem_id);

    // Split hex8 into 8 smaller hex8 elements
    // Add midpoint nodes on edges, faces, and center
    Point3D nodes[8];
    for (int i = 0; i < 8; ++i) {
        nodes[i] = mesh.getNode(elem.node_ids[i]);
    }

    // Center point
    Point3D center{0, 0, 0};
    for (int i = 0; i < 8; ++i) {
        center.x += nodes[i].x / 8.0;
        center.y += nodes[i].y / 8.0;
        center.z += nodes[i].z / 8.0;
    }
    int center_id = refined_mesh->addNode(center);

    // Edge midpoints (12 edges)
    int mid[12];
    int edges[][2] = {{0,1},{1,2},{2,3},{3,0},{4,5},{5,6},{6,7},{7,4},{0,4},{1,5},{2,6},{3,7}};
    for (int e = 0; e < 12; ++e) {
        Point3D mp = (nodes[edges[e][0]] + nodes[edges[e][1]]) * 0.5;
        mid[e] = refined_mesh->addNode(mp);
    }

    // Face centers (6 faces) — simplified
    // In a full implementation, we'd create proper sub-elements here
    // For the demo, just add the center node to show the concept

    // TODO: Create proper 8 sub-hex connectivity
    // This is left intentionally incomplete to demonstrate Copilot's
    // ability to suggest the correct connectivity pattern
}

void MeshRefinement::splitTet4(const Mesh& mesh, int elem_id,
                                std::shared_ptr<Mesh>& refined_mesh) {
    const Element& elem = mesh.getElement(elem_id);

    // Split tet4 into 8 sub-tetrahedra using edge midpoints
    Point3D nodes[4];
    for (int i = 0; i < 4; ++i) {
        nodes[i] = mesh.getNode(elem.node_ids[i]);
    }

    // 6 edge midpoints
    int mid[6];
    int edges[][2] = {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};
    for (int e = 0; e < 6; ++e) {
        Point3D mp = (nodes[edges[e][0]] + nodes[edges[e][1]]) * 0.5;
        mid[e] = refined_mesh->addNode(mp);
    }

    // TODO: Create 8 sub-tet connectivity
    // This is left intentionally incomplete for Copilot demo
}

void MeshRefinement::resolveHangingNodes(std::shared_ptr<Mesh>& mesh) {
    // Hanging nodes occur when a refined element shares a face with
    // an unrefined element. The midpoint node on the shared face is
    // a "hanging" node — not in the unrefined element's connectivity.
    //
    // Resolution strategies:
    // 1. Constrain hanging nodes (MPC: multi-point constraints)
    // 2. Split the neighboring unrefined element (cascading refinement)
    //
    // TODO: Implement hanging node resolution
    LOG_WARN("Hanging node resolution not implemented — mesh may have compatibility issues");
}

bool MeshRefinement::adaptiveRefine(std::shared_ptr<Mesh>& mesh,
                                     const std::vector<double>& displacements,
                                     double target_error) {
    auto errors = estimateError(*mesh, displacements);
    double max_error = *std::max_element(errors.begin(), errors.end());

    if (max_error < target_error) {
        LOG_INFO("Target error {:.4e} achieved (max error = {:.4e})", target_error, max_error);
        return true;
    }

    auto marked = markForRefinement(errors);
    if (marked.empty()) {
        LOG_WARN("No elements marked for refinement despite error > target");
        return false;
    }

    mesh = refine(*mesh, marked);
    return false;  // Need to re-solve and check again
}

} // namespace cae
