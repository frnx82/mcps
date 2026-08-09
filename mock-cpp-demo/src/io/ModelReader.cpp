/**
 * @file ModelReader.cpp
 * @brief File I/O for reading/writing CAE model files.
 */

#include "mesh/MeshGenerator.h"
#include "utils/Logger.h"
#include <fstream>
#include <sstream>
#include <vector>

namespace cae {
namespace io {

/**
 * Read a simple CSV node file.
 * Format: node_id, x, y, z
 */
bool readNodesCSV(const std::string& filename, Mesh& mesh) {
    std::ifstream file(filename);
    if (!file) {
        LOG_ERROR("Cannot open node file: {}", filename);
        return false;
    }

    std::string line;
    int count = 0;
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;

        std::istringstream iss(line);
        int id;
        double x, y, z;
        char comma;
        if (iss >> id >> comma >> x >> comma >> y >> comma >> z) {
            mesh.addNode(x, y, z);
            count++;
        }
    }

    LOG_INFO("Read {} nodes from {}", count, filename);
    return count > 0;
}

/**
 * Write solver results to a CSV file.
 * Format: node_id, ux, uy, uz, displacement_magnitude
 */
bool writeResultsCSV(const std::string& filename,
                     const Mesh& mesh,
                     const std::vector<double>& displacements) {
    std::ofstream file(filename);
    if (!file) {
        LOG_ERROR("Cannot open output file: {}", filename);
        return false;
    }

    file << "# node_id, ux, uy, uz, magnitude\n";
    for (int i = 0; i < mesh.numNodes(); ++i) {
        double ux = displacements[i * 3 + 0];
        double uy = displacements[i * 3 + 1];
        double uz = displacements[i * 3 + 2];
        double mag = std::sqrt(ux * ux + uy * uy + uz * uz);
        file << i << ", " << ux << ", " << uy << ", " << uz << ", " << mag << "\n";
    }

    LOG_INFO("Wrote {} displacement results to {}", mesh.numNodes(), filename);
    return true;
}

} // namespace io
} // namespace cae
