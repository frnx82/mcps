#pragma once
/**
 * @file MeshGenerator.h
 * @brief Mesh generation for structured and unstructured finite element meshes.
 *
 * Supports:
 *   - 2D triangular and quadrilateral meshes
 *   - 3D tetrahedral and hexahedral meshes
 *   - Parametric shapes (beam, plate, cylinder, sphere)
 *   - Import from external mesh files (.inp, .msh)
 */

#include <vector>
#include <array>
#include <memory>
#include <string>

namespace cae {

/// 3D point
struct Point3D {
    double x = 0.0;
    double y = 0.0;
    double z = 0.0;

    Point3D() = default;
    Point3D(double x_, double y_, double z_) : x(x_), y(y_), z(z_) {}

    Point3D operator+(const Point3D& other) const { return {x + other.x, y + other.y, z + other.z}; }
    Point3D operator-(const Point3D& other) const { return {x - other.x, y - other.y, z - other.z}; }
    Point3D operator*(double s) const { return {x * s, y * s, z * s}; }
    double dot(const Point3D& other) const { return x * other.x + y * other.y + z * other.z; }
    Point3D cross(const Point3D& other) const {
        return {y * other.z - z * other.y,
                z * other.x - x * other.z,
                x * other.y - y * other.x};
    }
    double norm() const;
    Point3D normalized() const;
};

/// Element types
enum class ElementType {
    TRI3,    ///< 3-node triangle (2D)
    QUAD4,   ///< 4-node quadrilateral (2D)
    TET4,    ///< 4-node tetrahedron (3D)
    HEX8,    ///< 8-node hexahedron (3D)
    TET10,   ///< 10-node quadratic tetrahedron (3D)
    HEX20    ///< 20-node quadratic hexahedron (3D)
};

/// A finite element
struct Element {
    int id;
    ElementType type;
    std::vector<int> node_ids;  ///< Connectivity: indices into node array
    int material_id = 0;        ///< Material assignment
};

/**
 * @class Mesh
 * @brief Container for a finite element mesh.
 *
 * A mesh consists of:
 *   - Nodes: 3D coordinates
 *   - Elements: connectivity (which nodes form each element)
 *   - Surface info: boundary faces for applying loads
 */
class Mesh {
public:
    Mesh();
    ~Mesh();

    /// Add a node, returns node index
    int addNode(const Point3D& point);
    int addNode(double x, double y, double z);

    /// Add an element, returns element index
    int addElement(ElementType type, const std::vector<int>& node_ids);

    /// Get node coordinates
    const Point3D& getNode(int index) const;
    Point3D& getNode(int index);

    /// Get element
    const Element& getElement(int index) const;

    /// Counts
    int numNodes() const { return static_cast<int>(m_nodes.size()); }
    int numElements() const { return static_cast<int>(m_elements.size()); }

    /// Compute mesh quality metrics
    double minElementQuality() const;   ///< Worst element quality (0=degenerate, 1=perfect)
    double avgElementQuality() const;   ///< Average element quality
    double minEdgeLength() const;       ///< Shortest edge in the mesh
    double maxEdgeLength() const;       ///< Longest edge in the mesh

    /// Compute element volume (3D) or area (2D)
    double elementVolume(int elem_id) const;

    /// Find surface nodes (nodes on the boundary)
    std::vector<int> findSurfaceNodes() const;

    /// Find nodes within a bounding box
    std::vector<int> findNodesInBox(const Point3D& min, const Point3D& max) const;

    /// Find nodes on a plane (within tolerance)
    std::vector<int> findNodesOnPlane(const Point3D& point, const Point3D& normal,
                                      double tolerance = 1e-6) const;

    /// Print mesh summary
    void printSummary() const;

    /// Export to VTK format for visualization
    void exportVTK(const std::string& filename) const;

private:
    std::vector<Point3D> m_nodes;
    std::vector<Element> m_elements;
};

/**
 * @class MeshGenerator
 * @brief Factory for creating standard mesh geometries.
 */
class MeshGenerator {
public:
    /// Create a beam mesh (hexahedral elements)
    /// @param length  Beam length in X direction
    /// @param width   Beam width in Y direction
    /// @param height  Beam height in Z direction
    /// @param nx, ny, nz  Number of elements in each direction
    static std::shared_ptr<Mesh> createBeam(double length, double width, double height,
                                             int nx, int ny, int nz);

    /// Create a plate mesh (quadrilateral shell elements)
    static std::shared_ptr<Mesh> createPlate(double length, double width,
                                              int nx, int ny);

    /// Create a cylinder mesh
    static std::shared_ptr<Mesh> createCylinder(double radius, double height,
                                                 int n_radial, int n_height);

    /// Create a sphere mesh (tetrahedral elements)
    static std::shared_ptr<Mesh> createSphere(double radius, int refinement_level);

    /// Import mesh from Abaqus .inp file
    static std::shared_ptr<Mesh> importINP(const std::string& filename);

    /// Import mesh from Gmsh .msh file
    static std::shared_ptr<Mesh> importGMSH(const std::string& filename);
};

} // namespace cae
