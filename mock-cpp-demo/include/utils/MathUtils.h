#pragma once
/**
 * @file MathUtils.h
 * @brief Math utilities for vector/matrix operations used throughout the solver.
 */

#include <vector>
#include <cmath>
#include <cassert>

namespace cae {
namespace math {

/// Dot product of two vectors
inline double dot(const std::vector<double>& a, const std::vector<double>& b) {
    assert(a.size() == b.size());
    double sum = 0.0;
    for (size_t i = 0; i < a.size(); ++i) {
        sum += a[i] * b[i];
    }
    return sum;
}

/// L2 norm of a vector
inline double norm(const std::vector<double>& v) {
    return std::sqrt(dot(v, v));
}

/// Scale vector: a *= scalar
inline void scale(std::vector<double>& a, double scalar) {
    for (auto& val : a) val *= scalar;
}

/// Vector addition: result = a + b
inline std::vector<double> add(const std::vector<double>& a,
                                const std::vector<double>& b) {
    assert(a.size() == b.size());
    std::vector<double> result(a.size());
    for (size_t i = 0; i < a.size(); ++i) {
        result[i] = a[i] + b[i];
    }
    return result;
}

/// AXPY: y = alpha * x + y  (BLAS-style)
inline void axpy(double alpha, const std::vector<double>& x, std::vector<double>& y) {
    assert(x.size() == y.size());
    for (size_t i = 0; i < x.size(); ++i) {
        y[i] += alpha * x[i];
    }
}

/// Dense matrix-vector product: y = A * x
/// A is stored row-major as A[row * cols + col]
void denseMatVec(const std::vector<double>& A, int rows, int cols,
                 const std::vector<double>& x, std::vector<double>& y);

/// Compute determinant of a 3×3 matrix (stored as 9 doubles, row-major)
double determinant3x3(const double* m);

/// Invert a 3×3 matrix. Returns false if singular.
bool invert3x3(const double* m, double* inv);

/// Gauss quadrature points and weights for hexahedral elements
/// @param order Quadrature order (1, 2, or 3)
/// @param points Output: quadrature point coordinates (ξ, η, ζ)
/// @param weights Output: quadrature weights
void gaussQuadratureHex(int order,
                        std::vector<std::array<double, 3>>& points,
                        std::vector<double>& weights);

/// Gauss quadrature for tetrahedral elements
void gaussQuadratureTet(int order,
                        std::vector<std::array<double, 3>>& points,
                        std::vector<double>& weights);

/// Shape functions for 8-node hexahedron at natural coordinates (ξ, η, ζ)
/// @param xi Natural coordinates [-1, 1]³
/// @param N Output: shape function values (8 values)
/// @param dNdxi Output: shape function derivatives (8 × 3 = 24 values)
void hexShapeFunctions(double xi, double eta, double zeta,
                       double N[8], double dNdxi[8][3]);

/// Compute Jacobian matrix from shape function derivatives and node coordinates
/// @param dNdxi Shape function derivatives (8×3)
/// @param coords Node coordinates (8×3)
/// @param J Output: 3×3 Jacobian matrix
/// @return Determinant of J
double computeJacobian(const double dNdxi[8][3],
                       const double coords[8][3],
                       double J[3][3]);

/// Compute B-matrix (strain-displacement) for 3D solid element
/// @param dNdx Shape function derivatives in physical coordinates (8×3)
/// @param B Output: 6×24 B-matrix (6 strain components × 24 DOFs)
void computeBMatrix(const double dNdx[8][3], double B[6][24]);

/// Compute elasticity matrix D for isotropic material
/// @param E Young's modulus
/// @param nu Poisson's ratio
/// @param D Output: 6×6 elasticity matrix
void computeElasticityMatrix(double E, double nu, double D[6][6]);

/// Compute von Mises stress from stress tensor components
/// σ_vm = √(0.5 × ((σ₁-σ₂)² + (σ₂-σ₃)² + (σ₃-σ₁)² + 6(τ₁₂² + τ₂₃² + τ₁₃²)))
double vonMisesStress(const double stress[6]);

} // namespace math
} // namespace cae
