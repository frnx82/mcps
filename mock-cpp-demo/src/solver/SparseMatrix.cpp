/**
 * @file SparseMatrix.cpp
 * @brief CSR sparse matrix implementation.
 */

#include "solver/SparseMatrix.h"
#include <algorithm>
#include <iostream>
#include <cassert>
#include <cmath>

#ifdef _OPENMP
#include <omp.h>
#endif

namespace cae {

SparseMatrix::SparseMatrix() = default;

SparseMatrix::SparseMatrix(int rows, int cols)
    : m_rows(rows), m_cols(cols)
{
    m_row_ptr.assign(rows + 1, 0);
}

SparseMatrix::~SparseMatrix() = default;

void SparseMatrix::reserve(size_t nnz_estimate) {
    m_triplets.reserve(nnz_estimate);
}

void SparseMatrix::addValue(int row, int col, double value) {
    assert(!m_finalized && "Cannot add values after finalize()");
    assert(row >= 0 && row < m_rows);
    assert(col >= 0 && col < m_cols);
    m_triplets.push_back({row, col, value});
}

void SparseMatrix::finalize() {
    // Sort triplets by (row, col)
    std::sort(m_triplets.begin(), m_triplets.end(),
              [](const Triplet& a, const Triplet& b) {
                  return (a.row < b.row) || (a.row == b.row && a.col < b.col);
              });

    // Merge duplicates and build CSR
    m_values.clear();
    m_col_index.clear();
    m_row_ptr.assign(m_rows + 1, 0);

    if (m_triplets.empty()) {
        m_finalized = true;
        return;
    }

    int prev_row = m_triplets[0].row;
    int prev_col = m_triplets[0].col;
    double sum = m_triplets[0].value;

    for (size_t i = 1; i < m_triplets.size(); ++i) {
        if (m_triplets[i].row == prev_row && m_triplets[i].col == prev_col) {
            sum += m_triplets[i].value;  // Merge duplicate
        } else {
            if (std::abs(sum) > 1e-15) {
                m_values.push_back(sum);
                m_col_index.push_back(prev_col);
                m_row_ptr[prev_row + 1]++;
            }
            prev_row = m_triplets[i].row;
            prev_col = m_triplets[i].col;
            sum = m_triplets[i].value;
        }
    }
    // Last entry
    if (std::abs(sum) > 1e-15) {
        m_values.push_back(sum);
        m_col_index.push_back(prev_col);
        m_row_ptr[prev_row + 1]++;
    }

    // Cumulative sum for row_ptr
    for (int i = 1; i <= m_rows; ++i) {
        m_row_ptr[i] += m_row_ptr[i - 1];
    }

    // Free triplets
    m_triplets.clear();
    m_triplets.shrink_to_fit();

    m_finalized = true;
}

double SparseMatrix::getValue(int row, int col) const {
    assert(m_finalized);
    for (int k = m_row_ptr[row]; k < m_row_ptr[row + 1]; ++k) {
        if (m_col_index[k] == col) return m_values[k];
        if (m_col_index[k] > col) break;  // Sorted, so no point continuing
    }
    return 0.0;
}

void SparseMatrix::setDiagonal(int index, double value) {
    assert(m_finalized);
    for (int k = m_row_ptr[index]; k < m_row_ptr[index + 1]; ++k) {
        if (m_col_index[k] == index) {
            m_values[k] = value;
            return;
        }
    }
    // Diagonal entry not found — this shouldn't happen for FEA matrices
    // but handle gracefully
    std::cerr << "[SparseMatrix] Warning: diagonal entry (" << index << "," << index
              << ") not in sparsity pattern\n";
}

double SparseMatrix::getDiagonal(int index) const {
    assert(m_finalized);
    for (int k = m_row_ptr[index]; k < m_row_ptr[index + 1]; ++k) {
        if (m_col_index[k] == index) return m_values[k];
    }
    return 0.0;
}

void SparseMatrix::multiply(const std::vector<double>& x, std::vector<double>& y) const {
    assert(m_finalized);
    assert(static_cast<int>(x.size()) == m_cols);
    y.assign(m_rows, 0.0);

#ifdef _OPENMP
    #pragma omp parallel for schedule(static)
#endif
    for (int i = 0; i < m_rows; ++i) {
        double sum = 0.0;
        for (int k = m_row_ptr[i]; k < m_row_ptr[i + 1]; ++k) {
            sum += m_values[k] * x[m_col_index[k]];
        }
        y[i] = sum;
    }
}

void SparseMatrix::multiplySymmetric(const std::vector<double>& x, std::vector<double>& y) const {
    // For symmetric matrices where only upper triangle is stored
    assert(m_finalized);
    y.assign(m_rows, 0.0);

    for (int i = 0; i < m_rows; ++i) {
        for (int k = m_row_ptr[i]; k < m_row_ptr[i + 1]; ++k) {
            int j = m_col_index[k];
            double v = m_values[k];
            y[i] += v * x[j];
            if (i != j) {
                y[j] += v * x[i];  // Symmetric contribution
            }
        }
    }
}

size_t SparseMatrix::memoryUsage() const {
    return m_values.size() * sizeof(double)
         + m_col_index.size() * sizeof(int)
         + m_row_ptr.size() * sizeof(int)
         + m_triplets.size() * sizeof(Triplet);
}

void SparseMatrix::printPattern(int max_rows) const {
    int rows_to_print = std::min(m_rows, max_rows);
    int cols_to_print = std::min(m_cols, max_rows);

    std::cout << "Sparsity pattern (" << m_rows << "x" << m_cols
              << ", nnz=" << nonZeros() << "):\n";
    for (int i = 0; i < rows_to_print; ++i) {
        for (int j = 0; j < cols_to_print; ++j) {
            std::cout << (std::abs(getValue(i, j)) > 1e-15 ? "█" : "·");
        }
        std::cout << "\n";
    }
}

} // namespace cae
