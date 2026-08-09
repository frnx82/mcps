#pragma once
/**
 * @file MeshRefinement.h
 * @brief Adaptive mesh refinement based on error estimators.
 */

#include "mesh/MeshGenerator.h"
#include <vector>
#include <memory>

namespace cae {

/// Error estimator types for adaptive refinement
enum class ErrorEstimator {
    ZIENKIEWICZ_ZHU,    ///< ZZ error estimator (stress recovery)
    KELLY,              ///< Kelly error indicator (jump in normal derivatives)
    RESIDUAL_BASED      ///< Element residual-based estimator
};

/// Refinement strategy
enum class RefinementStrategy {
    UNIFORM,            ///< Refine all elements
    ADAPTIVE,           ///< Refine only elements above error threshold
    GRADED              ///< Gradual refinement toward high-error regions
};

/**
 * @class MeshRefinement
 * @brief Adaptive mesh refinement for FEA accuracy improvement.
 *
 * Workflow:
 *   1. Solve on coarse mesh
 *   2. Estimate error per element
 *   3. Mark elements for refinement
 *   4. Refine mesh
 *   5. Repeat until target accuracy reached
 */
class MeshRefinement {
public:
    MeshRefinement();
    ~MeshRefinement();

    /// Estimate error per element using stress recovery
    /// @param displacements Solution vector from solver
    /// @return Error indicator per element (0 = perfect, larger = more error)
    std::vector<double> estimateError(const Mesh& mesh,
                                      const std::vector<double>& displacements,
                                      ErrorEstimator estimator = ErrorEstimator::ZIENKIEWICZ_ZHU);

    /// Mark elements for refinement based on error threshold
    /// @param errors Error per element from estimateError()
    /// @param threshold Elements with error > threshold * max_error are marked
    /// @return Indices of elements to refine
    std::vector<int> markForRefinement(const std::vector<double>& errors,
                                       double threshold = 0.3);

    /// Refine mesh by splitting marked elements
    /// @param mesh Original mesh
    /// @param marked_elements Indices of elements to split
    /// @return New refined mesh
    std::shared_ptr<Mesh> refine(const Mesh& mesh,
                                  const std::vector<int>& marked_elements,
                                  RefinementStrategy strategy = RefinementStrategy::ADAPTIVE);

    /// Perform one complete adaptive refinement cycle
    /// @return true if refinement improved accuracy below target
    bool adaptiveRefine(std::shared_ptr<Mesh>& mesh,
                        const std::vector<double>& displacements,
                        double target_error = 0.01);

    /// Set maximum refinement level (prevents infinite refinement)
    void setMaxRefinementLevel(int level) { m_max_level = level; }

    /// Get current refinement level
    int getCurrentLevel() const { return m_current_level; }

private:
    int m_max_level = 5;
    int m_current_level = 0;

    /// Split a hexahedral element into 8 sub-elements
    void splitHex8(const Mesh& mesh, int elem_id,
                   std::shared_ptr<Mesh>& refined_mesh);

    /// Split a tetrahedral element into 8 sub-tetrahedra
    void splitTet4(const Mesh& mesh, int elem_id,
                   std::shared_ptr<Mesh>& refined_mesh);

    /// Ensure mesh conformity at refinement boundaries (hanging nodes)
    void resolveHangingNodes(std::shared_ptr<Mesh>& mesh);
};

} // namespace cae
