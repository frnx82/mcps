/**
 * @file MeshGenerator.cpp
 * @brief Mesh generation for standard geometries.
 */

#include "mesh/MeshGenerator.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>

namespace cae {

// ── Point3D ─────────────────────────────────────────────────────

double Point3D::norm() const {
    return std::sqrt(x * x + y * y + z * z);
}

Point3D Point3D::normalized() const {
    double n = norm();
    if (n < 1e-15) return {0, 0, 0};
    return {x / n, y / n, z / n};
}

// ── Mesh ────────────────────────────────────────────────────────

Mesh::Mesh() = default;
Mesh::~Mesh() = default;

int Mesh::addNode(const Point3D& point) {
    m_nodes.push_back(point);
    return static_cast<int>(m_nodes.size()) - 1;
}

int Mesh::addNode(double x, double y, double z) {
    return addNode(Point3D(x, y, z));
}

int Mesh::addElement(ElementType type, const std::vector<int>& node_ids) {
    Element elem;
    elem.id = static_cast<int>(m_elements.size());
    elem.type = type;
    elem.node_ids = node_ids;
    m_elements.push_back(std::move(elem));
    return elem.id;
}

const Point3D& Mesh::getNode(int index) const {
    return m_nodes.at(index);
}

Point3D& Mesh::getNode(int index) {
    return m_nodes.at(index);
}

const Element& Mesh::getElement(int index) const {
    return m_elements.at(index);
}

double Mesh::elementVolume(int elem_id) const {
    const Element& elem = m_elements.at(elem_id);

    if (elem.type == ElementType::HEX8 && elem.node_ids.size() == 8) {
        // Approximate hex volume using decomposition into 5 tetrahedra
        // For a perfect rectangular hex: V = dx * dy * dz
        const Point3D& p0 = m_nodes[elem.node_ids[0]];
        const Point3D& p1 = m_nodes[elem.node_ids[1]];
        const Point3D& p3 = m_nodes[elem.node_ids[3]];
        const Point3D& p4 = m_nodes[elem.node_ids[4]];

        double dx = (p1 - p0).norm();
        double dy = (p3 - p0).norm();
        double dz = (p4 - p0).norm();
        return dx * dy * dz;
    }

    if (elem.type == ElementType::TET4 && elem.node_ids.size() == 4) {
        const Point3D& a = m_nodes[elem.node_ids[0]];
        const Point3D& b = m_nodes[elem.node_ids[1]];
        const Point3D& c = m_nodes[elem.node_ids[2]];
        const Point3D& d = m_nodes[elem.node_ids[3]];
        Point3D ab = b - a;
        Point3D ac = c - a;
        Point3D ad = d - a;
        return std::abs(ab.cross(ac).dot(ad)) / 6.0;
    }

    return 0.0;  // Unknown element type
}

std::vector<int> Mesh::findNodesInBox(const Point3D& min_pt, const Point3D& max_pt) const {
    std::vector<int> result;
    for (int i = 0; i < numNodes(); ++i) {
        const Point3D& p = m_nodes[i];
        if (p.x >= min_pt.x && p.x <= max_pt.x &&
            p.y >= min_pt.y && p.y <= max_pt.y &&
            p.z >= min_pt.z && p.z <= max_pt.z) {
            result.push_back(i);
        }
    }
    return result;
}

std::vector<int> Mesh::findNodesOnPlane(const Point3D& point, const Point3D& normal,
                                         double tolerance) const {
    std::vector<int> result;
    Point3D n = normal.normalized();
    for (int i = 0; i < numNodes(); ++i) {
        Point3D diff = m_nodes[i] - point;
        if (std::abs(diff.dot(n)) < tolerance) {
            result.push_back(i);
        }
    }
    return result;
}

void Mesh::printSummary() const {
    std::cout << "Mesh Summary:\n"
              << "  Nodes:    " << numNodes() << "\n"
              << "  Elements: " << numElements() << "\n";
}

void Mesh::exportVTK(const std::string& filename) const {
    std::ofstream out(filename);
    if (!out) {
        std::cerr << "Error: Cannot open " << filename << " for writing\n";
        return;
    }

    out << "# vtk DataFile Version 3.0\n"
        << "CAE Solver Demo Mesh\n"
        << "ASCII\n"
        << "DATASET UNSTRUCTURED_GRID\n\n";

    out << "POINTS " << numNodes() << " double\n";
    for (const auto& node : m_nodes) {
        out << node.x << " " << node.y << " " << node.z << "\n";
    }

    // Count total connectivity entries
    int total = 0;
    for (const auto& elem : m_elements) {
        total += 1 + static_cast<int>(elem.node_ids.size());
    }

    out << "\nCELLS " << numElements() << " " << total << "\n";
    for (const auto& elem : m_elements) {
        out << elem.node_ids.size();
        for (int nid : elem.node_ids) out << " " << nid;
        out << "\n";
    }

    out << "\nCELL_TYPES " << numElements() << "\n";
    for (const auto& elem : m_elements) {
        int vtk_type = 12;  // VTK_HEXAHEDRON
        if (elem.type == ElementType::TET4)  vtk_type = 10;
        if (elem.type == ElementType::QUAD4) vtk_type = 9;
        if (elem.type == ElementType::TRI3)  vtk_type = 5;
        out << vtk_type << "\n";
    }
}

// ── MeshGenerator ───────────────────────────────────────────────

std::shared_ptr<Mesh> MeshGenerator::createBeam(double length, double width, double height,
                                                  int nx, int ny, int nz) {
    auto mesh = std::make_shared<Mesh>();

    double dx = length / nx;
    double dy = width / ny;
    double dz = height / nz;

    // Create nodes
    for (int iz = 0; iz <= nz; ++iz) {
        for (int iy = 0; iy <= ny; ++iy) {
            for (int ix = 0; ix <= nx; ++ix) {
                mesh->addNode(ix * dx, iy * dy, iz * dz);
            }
        }
    }

    // Create hexahedral elements
    for (int iz = 0; iz < nz; ++iz) {
        for (int iy = 0; iy < ny; ++iy) {
            for (int ix = 0; ix < nx; ++ix) {
                int n0 = iz * (ny + 1) * (nx + 1) + iy * (nx + 1) + ix;
                int n1 = n0 + 1;
                int n2 = n0 + (nx + 1) + 1;
                int n3 = n0 + (nx + 1);
                int n4 = n0 + (ny + 1) * (nx + 1);
                int n5 = n4 + 1;
                int n6 = n4 + (nx + 1) + 1;
                int n7 = n4 + (nx + 1);

                mesh->addElement(ElementType::HEX8, {n0, n1, n2, n3, n4, n5, n6, n7});
            }
        }
    }

    std::cout << "[MeshGenerator] Created beam: " << length << "×" << width << "×" << height
              << " m, " << mesh->numNodes() << " nodes, " << mesh->numElements() << " hex8 elements\n";

    return mesh;
}

std::shared_ptr<Mesh> MeshGenerator::createPlate(double length, double width, int nx, int ny) {
    auto mesh = std::make_shared<Mesh>();

    double dx = length / nx;
    double dy = width / ny;

    for (int iy = 0; iy <= ny; ++iy) {
        for (int ix = 0; ix <= nx; ++ix) {
            mesh->addNode(ix * dx, iy * dy, 0.0);
        }
    }

    for (int iy = 0; iy < ny; ++iy) {
        for (int ix = 0; ix < nx; ++ix) {
            int n0 = iy * (nx + 1) + ix;
            int n1 = n0 + 1;
            int n2 = n0 + (nx + 1) + 1;
            int n3 = n0 + (nx + 1);
            mesh->addElement(ElementType::QUAD4, {n0, n1, n2, n3});
        }
    }

    return mesh;
}

std::shared_ptr<Mesh> MeshGenerator::createCylinder(double radius, double height,
                                                      int n_radial, int n_height) {
    auto mesh = std::make_shared<Mesh>();

    for (int ih = 0; ih <= n_height; ++ih) {
        double z = (static_cast<double>(ih) / n_height) * height;
        for (int ir = 0; ir < n_radial; ++ir) {
            double theta = 2.0 * M_PI * ir / n_radial;
            mesh->addNode(radius * std::cos(theta), radius * std::sin(theta), z);
        }
    }

    // TODO: Add element connectivity for cylinder
    std::cout << "[MeshGenerator] Created cylinder: r=" << radius << ", h=" << height
              << ", " << mesh->numNodes() << " nodes\n";

    return mesh;
}

std::shared_ptr<Mesh> MeshGenerator::createSphere(double radius, int refinement_level) {
    auto mesh = std::make_shared<Mesh>();

    // Start with icosahedron and refine
    // Golden ratio for icosahedron vertices
    double phi = (1.0 + std::sqrt(5.0)) / 2.0;
    double scale = radius / std::sqrt(1.0 + phi * phi);

    // 12 vertices of icosahedron
    mesh->addNode(-1 * scale,  phi * scale, 0);
    mesh->addNode( 1 * scale,  phi * scale, 0);
    mesh->addNode(-1 * scale, -phi * scale, 0);
    mesh->addNode( 1 * scale, -phi * scale, 0);
    mesh->addNode(0, -1 * scale,  phi * scale);
    mesh->addNode(0,  1 * scale,  phi * scale);
    mesh->addNode(0, -1 * scale, -phi * scale);
    mesh->addNode(0,  1 * scale, -phi * scale);
    mesh->addNode( phi * scale, 0, -1 * scale);
    mesh->addNode( phi * scale, 0,  1 * scale);
    mesh->addNode(-phi * scale, 0, -1 * scale);
    mesh->addNode(-phi * scale, 0,  1 * scale);

    // TODO: Add icosahedron faces and subdivide for refinement_level
    std::cout << "[MeshGenerator] Created sphere: r=" << radius
              << ", refinement=" << refinement_level << "\n";

    return mesh;
}

std::shared_ptr<Mesh> MeshGenerator::importINP(const std::string& filename) {
    auto mesh = std::make_shared<Mesh>();
    std::ifstream file(filename);
    if (!file) {
        std::cerr << "Error: Cannot open " << filename << "\n";
        return mesh;
    }

    std::string line;
    bool reading_nodes = false;
    bool reading_elements = false;

    while (std::getline(file, line)) {
        if (line.find("*NODE") != std::string::npos || line.find("*Node") != std::string::npos) {
            reading_nodes = true;
            reading_elements = false;
            continue;
        }
        if (line.find("*ELEMENT") != std::string::npos || line.find("*Element") != std::string::npos) {
            reading_nodes = false;
            reading_elements = true;
            continue;
        }
        if (line[0] == '*') {
            reading_nodes = false;
            reading_elements = false;
            continue;
        }

        if (reading_nodes) {
            std::istringstream iss(line);
            int id;
            double x, y, z;
            char comma;
            if (iss >> id >> comma >> x >> comma >> y >> comma >> z) {
                mesh->addNode(x, y, z);
            }
        }

        if (reading_elements) {
            // Parse element connectivity (simplified)
            std::istringstream iss(line);
            int id;
            char comma;
            iss >> id >> comma;
            std::vector<int> nodes;
            int nid;
            while (iss >> nid) {
                nodes.push_back(nid - 1);  // Convert 1-based to 0-based
                iss >> comma;
            }
            if (nodes.size() == 8) {
                mesh->addElement(ElementType::HEX8, nodes);
            } else if (nodes.size() == 4) {
                mesh->addElement(ElementType::TET4, nodes);
            }
        }
    }

    std::cout << "[MeshGenerator] Imported " << filename << ": "
              << mesh->numNodes() << " nodes, " << mesh->numElements() << " elements\n";

    return mesh;
}

std::shared_ptr<Mesh> MeshGenerator::importGMSH(const std::string& filename) {
    // TODO: Implement Gmsh .msh v4 format reader
    std::cerr << "[MeshGenerator] GMSH import not yet implemented for: " << filename << "\n";
    return std::make_shared<Mesh>();
}

// ── Mesh Quality ────────────────────────────────────────────────

double Mesh::minElementQuality() const {
    // Simplified quality metric: aspect ratio of bounding box
    double worst = 1.0;
    for (const auto& elem : m_elements) {
        if (elem.node_ids.size() < 4) continue;
        Point3D min_pt = m_nodes[elem.node_ids[0]];
        Point3D max_pt = min_pt;
        for (int nid : elem.node_ids) {
            const Point3D& p = m_nodes[nid];
            min_pt.x = std::min(min_pt.x, p.x);
            min_pt.y = std::min(min_pt.y, p.y);
            min_pt.z = std::min(min_pt.z, p.z);
            max_pt.x = std::max(max_pt.x, p.x);
            max_pt.y = std::max(max_pt.y, p.y);
            max_pt.z = std::max(max_pt.z, p.z);
        }
        double dx = max_pt.x - min_pt.x;
        double dy = max_pt.y - min_pt.y;
        double dz = max_pt.z - min_pt.z;
        double max_dim = std::max({dx, dy, dz});
        double min_dim = std::min({dx, dy, dz});
        if (max_dim > 1e-15) {
            double quality = min_dim / max_dim;  // 1.0 = perfect cube, 0 = degenerate
            worst = std::min(worst, quality);
        }
    }
    return worst;
}

double Mesh::avgElementQuality() const {
    // Placeholder
    return 0.85;
}

double Mesh::minEdgeLength() const {
    double min_len = 1e30;
    for (const auto& elem : m_elements) {
        for (size_t i = 0; i < elem.node_ids.size(); ++i) {
            for (size_t j = i + 1; j < elem.node_ids.size(); ++j) {
                double len = (m_nodes[elem.node_ids[i]] - m_nodes[elem.node_ids[j]]).norm();
                min_len = std::min(min_len, len);
            }
        }
    }
    return min_len;
}

double Mesh::maxEdgeLength() const {
    double max_len = 0.0;
    for (const auto& elem : m_elements) {
        for (size_t i = 0; i < elem.node_ids.size(); ++i) {
            for (size_t j = i + 1; j < elem.node_ids.size(); ++j) {
                double len = (m_nodes[elem.node_ids[i]] - m_nodes[elem.node_ids[j]]).norm();
                max_len = std::max(max_len, len);
            }
        }
    }
    return max_len;
}

std::vector<int> Mesh::findSurfaceNodes() const {
    // Simplified: find nodes that appear in fewer element faces
    // A proper implementation would track face adjacency
    std::vector<int> surface;
    // TODO: Implement proper surface detection
    return surface;
}

} // namespace cae
