---
title: "Matrix Inverse"
description: "Invertibility, determinants, uniqueness proofs, and solving linear systems in machine learning."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Scalars", "Vectors", "Matrices", "Matrix Multiplication"]
---

<h1 align="center"> Chapter 18: Matrix Inverse </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Matrix Multiplication:** Knowing how matrices compose linear transformations.
* **Determinants:** Understanding the area scaling factor of a matrix transformation.

</div>

## 1. Conceptual Hook

If a matrix represents a forward transformation of space—such as rotating, shearing, or projecting a coordinate system—the **matrix inverse** is the ultimate "undo" button. It represents the unique transformation that reverses the forward mapping, perfectly restoring the data to its starting coordinates.

In machine learning, we rely on the inverse to reconstruct original signals from mixed outputs (ICA), compute optimal parameters analytically (Ordinary Least Squares), and navigate loss landscapes using curvature information (Newton's method). However, an inverse exists if and only if the forward transformation preserves all information. If a matrix collapses our data onto a flat line or point, the details are lost forever—making the matrix singular and non-invertible.

---

## 2. Formal Definition

Let $A \in \mathbb{R}^{n \times n}$ be a square matrix. The matrix $A$ is said to be **invertible** (or **non-singular**) if there exists a square matrix $B \in \mathbb{R}^{n \times n}$ such that:
$$AB = BA = I_n$$
where $I_n$ is the $n \times n$ identity matrix. If such a matrix $B$ exists, it is unique and is denoted as the **inverse** of $A$:
$$B = A^{-1}$$

### Core Algebraic Properties
*   **Reversal of Products:** If $A$ and $B$ are invertible matrices of the same size, their product $AB$ is invertible, and:
    $$(AB)^{-1} = B^{-1} A^{-1}$$
*   **Transpose of Inverse:** If $A$ is invertible, its transpose is also invertible, and:
    $$(A^T)^{-1} = (A^{-1})^T$$
*   **Determinant of Inverse:** If $A$ is invertible, its determinant is non-zero, and:
    $$\det(A^{-1}) = \frac{1}{\det(A)}$$

---

## 3. Illustrative Derivation

### Proof of Uniqueness of the Matrix Inverse
**Theorem:** If a matrix $A \in \mathbb{R}^{n \times n}$ is invertible, its inverse $A^{-1}$ is unique.

*Proof:*
Assume that $B$ and $C$ are both valid inverses of $A$. By definition of the matrix inverse, this means:
$$AB = BA = I_n \quad \text{and} \quad AC = CA = I_n$$
Let us evaluate the product $CAB$ in two different ways using the associative property of matrix multiplication:
1. Grouping $C$ and $A$:
   $$(CA)B = I_n B = B$$
2. Grouping $A$ and $B$:
   $$C(AB) = C I_n = C$$
Since $(CA)B = C(AB)$ by associativity:
$$B = C$$
Thus, the inverse is unique. $\blacksquare$

### Derivation of the $2 \times 2$ Inverse Formula
Let $A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$. We seek a matrix $A^{-1} = \begin{pmatrix} w & x \\ y & z \end{pmatrix}$ such that $A A^{-1} = I_2$:
$$\begin{pmatrix} a & b \\ c & d \end{pmatrix} \begin{pmatrix} w & x \\ y & z \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$$
This yields two systems of linear equations:
*   **System 1 (Column 1):**
    $$aw + by = 1$$
    $$cw + dy = 0 \implies w = -\frac{d}{c} y \quad (\text{if } c \neq 0)$$
    Substituting $w$ into the first equation:
    $$a \left(-\frac{d}{c} y\right) + by = 1 \implies y \left(b - \frac{ad}{c}\right) = 1 \implies y \left(\frac{bc - ad}{c}\right) = 1$$
    $$y = -\frac{c}{ad - bc}, \quad w = \frac{d}{ad - bc}$$
*   **System 2 (Column 2):**
    $$ax + bz = 0 \implies x = -\frac{b}{a} z \quad (\text{if } a \neq 0)$$
    $$cx + dz = 1$$
    Solving similarly yields:
    $$x = -\frac{b}{ad - bc}, \quad z = \frac{a}{ad - bc}$$

Combining these terms into matrix form:
$$A^{-1} = \frac{1}{ad - bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$
The term $ad - bc$ is the determinant of $A$, denoted $\det(A)$. If $\det(A) = 0$, we cannot divide by it, proving that the inverse exists if and only if $\det(A) \neq 0$. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Inverting a Bundled Pricing Matrix
Solve for the individual prices of features given mixed bundles:
$$A = \begin{pmatrix} 3 & 1 \\ 2 & 1 \end{pmatrix}, \quad b = \begin{bmatrix} 7 \\ 5 \end{bmatrix}$$
1.  **Calculate the determinant:**
    $$\det(A) = (3)(1) - (1)(2) = 1$$
2.  **Compute the inverse $A^{-1}$:**
    $$A^{-1} = \frac{1}{1} \begin{pmatrix} 1 & -1 \\ -2 & 3 \end{pmatrix} = \begin{pmatrix} 1 & -1 \\ -2 & 3 \end{pmatrix}$$
3.  **Solve the system $x = A^{-1} b$:**
    $$x = \begin{pmatrix} 1 & -1 \\ -2 & 3 \end{pmatrix} \begin{bmatrix} 7 \\ 5 \end{bmatrix} = \begin{bmatrix} 1(7) - 1(5) \\ -2(7) + 3(5) \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$$
This confirms the unique components have prices of $2$ and $1$.

### Example 2: Singular (Non-Invertible) Matrix
Let $A = \begin{pmatrix} 4 & 2 \\ 2 & 1 \end{pmatrix}$.
1.  **Compute the determinant:**
    $$\det(A) = (4)(1) - (2)(2) = 0$$
2.  **Analyze geometrically:**
    The columns of $A$ are collinear: $\begin{bmatrix} 2 \\ 1 \end{bmatrix} = 0.5 \begin{bmatrix} 4 \\ 2 \end{bmatrix}$. The matrix collapses the 2D plane onto a 1D line. Information along the orthogonal direction is compressed to zero, meaning we cannot reconstruct unique input coordinates from output points. The matrix is singular and cannot be inverted.

---

## 5. Applied ML Context

1.  **Ordinary Least Squares (OLS) Regression:** The analytical solution for parameter weights $\beta$ is computed using the normal equations: $\beta = (X^T X)^{-1} X^T y$. This requires the covariance matrix $X^T X$ to be invertible.
2.  **Newton-Raphson Optimization:** Unlike standard gradient descent, Newton's method uses second-order curvature information. The parameters are updated by multiplying the gradient by the inverse Hessian matrix: $\theta_{t+1} = \theta_t - H^{-1} \nabla L(\theta_t)$.
3.  **Independent Component Analysis (ICA):** In blind source separation, we observe mixed signals $x = As$. ICA works by estimating an un-mixing matrix $W \approx A^{-1}$ to isolate the independent source signals: $s \approx Wx$.
4.  **Gaussian Process Regression:** Computing the predictive distribution of a Gaussian process requires inverting the kernel covariance matrix $K(X, X)$. Because inverting large matrices is $O(n^3)$ complex, this is the primary computational bottleneck of GPs.
5.  **Normalizing Flows:** This generative modeling framework maps complex target distributions back to simple isotropic Gaussians using a chain of invertible neural network layers, requiring the inverse mapping to generate new data points from Gaussian noise.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating matrix inversion vs. collapse:
*   **Invertible Mapping:** Show a 2D coordinate grid transformed by a matrix $A$ (shearing it). Show a reverse arrow labeled $A^{-1}$ pulling the sheared grid back into its original, perpendicular square configuration.
*   **Singular Mapping (No Inverse):** Show the same 2D grid collapsed onto a single 1D line by the matrix $A = \begin{pmatrix} 4 & 2 \\ 2 & 1 \end{pmatrix}$. Show that multiple points (e.g., $[1, 1]^T$ and $[0, 3]^T$) map to the exact same output point on the line, illustrating that we cannot map back uniquely (a vertical projection line showing loss of a dimension).
