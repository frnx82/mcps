#pragma once
/**
 * @file SparseMatrix.h
 * @brief Compressed Sparse Row (CSR) matrix for FEA stiffness matrices.
 *
 * FEA stiffness matrices are symmetric positive definite and very sparse.
 * For a model with 100K nodes (300K DOFs), the full matrix would be
 * 300K × 300K = 90 billion entries. In CSR format, we only store the
 * non-zero entries — typically 50-200 per row for hexahedral elements.
 */

#include <vector>
#include <cstddef>

namespace cae {

/**
 * @class SparseMatrix
 * @brief CSR (Compressed Sparse Row) sparse matrix.
 *
 * Storage format:
 *   values[]     — non-zero values, row by row
 *   col_index[]  — column index for each value
 *   row_ptr[]    — index into values[] where each row starts
 *
 * For an N×N matrix with nnz non-zeros:
 *   Memory = nnz × sizeof(double) + nnz × sizeof(int) + (N+1) × sizeof(int)
 */
class SparseMatrix {
public:
    SparseMatrix();
    SparseMatrix(int rows, int cols);
    ~SparseMatrix();

    /// Reserve space for expected number of non-zeros
    void reserve(size_t nnz_estimate);

    /// Add value to position (i, j). If entry exists, adds to it.
    /// Thread-safe ONLY if different threads write to different rows.
    void addValue(int row, int col, double value);

    /// Finalize the matrix structure (must call after all addValue() calls)
    /// Sorts column indices within each row and merges duplicates.
    void finalize();

    /// Get value at (row, col). Returns 0 if not stored.
    double getValue(int row, int col) const;

    /// Set diagonal entry (used for Dirichlet BC penalty method)
    void setDiagonal(int index, double value);

    /// Get diagonal value (used for Jacobi preconditioner)
    double getDiagonal(int index) const;

    /// Matrix-vector product: y = A * x
    /// This is the innermost loop of the CG solver — must be fast.
    /// Parallelized with OpenMP when available.
    void multiply(const std::vector<double>& x, std::vector<double>& y) const;

    /// Symmetric matrix-vector product (only upper triangle stored)
    void multiplySymmetric(const std::vector<double>& x, std::vector<double>& y) const;

    /// Dimensions
    int rows() const { return m_rows; }
    int cols() const { return m_cols; }
    size_t nonZeros() const { return m_values.size(); }

    /// Memory usage in bytes
    size_t memoryUsage() const;

    /// Print sparsity pattern (for debugging small matrices)
    void printPattern(int max_rows = 20) const;

    /// CSR data access (for direct solver interfaces like PARDISO/MKL)
    const double* values() const { return m_values.data(); }
    const int* colIndex() const { return m_col_index.data(); }
    const int* rowPtr() const { return m_row_ptr.data(); }

private:
    int m_rows = 0;
    int m_cols = 0;

    std::vector<double> m_values;     ///< Non-zero values
    std::vector<int>    m_col_index;  ///< Column indices
    std::vector<int>    m_row_ptr;    ///< Row pointers (size = m_rows + 1)

    bool m_finalized = false;

    /// Temporary storage for incremental assembly (before finalize)
    struct Triplet {
        int row, col;
        double value;
    };
    std::vector<Triplet> m_triplets;
};

} // namespace cae
