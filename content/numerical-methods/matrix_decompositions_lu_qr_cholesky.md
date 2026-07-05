---
title: "Matrix Decompositions (LU, QR, Cholesky)"
description: "Matrix factorizations, lower and upper triangular systems, orthogonal matrices, forward and backward substitutions, and Cholesky algorithms."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Linear Algebra: Matrices", "Linear Algebra: Matrix Inverse", "Linear Algebra: Orthogonality and Projections"]
---

<h1 align="center"> Chapter 100: Matrix Decompositions (LU, QR, Cholesky) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Triangular Systems:** Systems of equations where the coefficient matrix is lower or upper triangular, allowing for fast back-solving.
* **Orthonormal Vectors:** Vectors of unit length that are mutually perpendicular to one another.

</div>

## 1. Conceptual Hook

In linear algebra, a matrix represents a complex system of linear transformations. However, working with a raw matrix directly is often computationally expensive and numerically unstable. Solving large systems of equations $\mathbf{A}\mathbf{x} = \mathbf{b}$ or inverting massive covariance matrices requires significant processor cycles.

**Matrix decomposition** (or factorization) is the mathematical practice of breaking a matrix down into a product of simpler, structured matrices—specifically triangular, orthogonal, or diagonal matrices.

Think of a matrix as a complex cabinet of files. If the files are piled in a chaotic heap, finding any document requires searching the entire room. Matrix decompositions organize the heap:
*   **LU Decomposition** splits the matrix into lower and upper triangular folders.
*   **QR Decomposition** extracts orthogonal vectors, ensuring no redundant information exists.
*   **Cholesky Decomposition** takes advantage of symmetry, storing only "half" of the data to solve systems in half the time.

By organizing the matrix structure, we convert complex linear algebra operations into fast, sequential steps.

---

## 2. Formal Definition

### 1. LU Decomposition
Let $\mathbf{A} \in \mathbb{R}^{d \times d}$ be a square matrix. The LU factorization of $\mathbf{A}$ is:
$$\mathbf{A} = \mathbf{L}\mathbf{U}$$
where:
*   **$\mathbf{L} \in \mathbb{R}^{d \times d}$:** A unit lower triangular matrix, meaning $L_{ij} = 0$ for $i < j$ and the diagonal entries are unit values ($L_{ii} = 1$).
*   **$\mathbf{U} \in \mathbb{R}^{d \times d}$:** An upper triangular matrix, meaning $U_{ij} = 0$ for $i > j$.

*Note on Pivoting:* For numerical stability, row swaps are tracked via a permutation matrix $\mathbf{P}$, yielding:
$$\mathbf{P}\mathbf{A} = \mathbf{L}\mathbf{U}$$

### 2. QR Decomposition
Let $\mathbf{A} \in \mathbb{R}^{m \times d}$ be a matrix with $m \ge d$. The QR factorization of $\mathbf{A}$ is:
$$\mathbf{A} = \mathbf{Q}\mathbf{R}$$
where:
*   **$\mathbf{Q} \in \mathbb{R}^{m \times m}$:** An orthogonal matrix whose columns form an orthonormal basis for the column space of $\mathbf{A}$, satisfying $\mathbf{Q}^T\mathbf{Q} = \mathbf{I}$.
*   **$\mathbf{R} \in \mathbb{R}^{m \times d}$:** An upper triangular matrix.

### 3. Cholesky Decomposition
Let $\mathbf{A} \in \mathbb{R}^{d \times d}$ be a symmetric, positive-definite matrix ($\mathbf{A} = \mathbf{A}^T$ and $\mathbf{w}^T\mathbf{A}\mathbf{w} > 0$ for all $\mathbf{w} \neq \mathbf{0}$). The Cholesky factorization of $\mathbf{A}$ is:
$$\mathbf{A} = \mathbf{L}\mathbf{L}^T$$
where $\mathbf{L} \in \mathbb{R}^{d \times d}$ is a lower triangular matrix with strictly positive diagonal entries ($L_{ii} > 0$).

---

## 3. Illustrative Derivation

### Derivation of Forward and Backward Substitution Algorithms
We derive how solving the linear system $\mathbf{A}\mathbf{x} = \mathbf{b}$ via $\mathbf{A} = \mathbf{L}\mathbf{U}$ is accomplished, proving that triangular systems reduce solving complexity from $O(d^3)$ to $O(d^2)$.

*Proof:*
Let $\mathbf{A}\mathbf{x} = \mathbf{b}$. Substitute $\mathbf{A} = \mathbf{L}\mathbf{U}$:
$$\mathbf{L}\mathbf{U}\mathbf{x} = \mathbf{b}$$
Define the intermediate vector $\mathbf{y} = \mathbf{U}\mathbf{x}$. The system splits into two triangular phases:
1.  Solve $\mathbf{L}\mathbf{y} = \mathbf{b}$ for $\mathbf{y}$.
2.  Solve $\mathbf{U}\mathbf{x} = \mathbf{y}$ for $\mathbf{x}$.

1.  **Forward Substitution Phase ($\mathbf{L}\mathbf{y} = \mathbf{b}$):**
    Because $\mathbf{L}$ is lower triangular:
    $$\begin{bmatrix} 
    L_{11} & 0 & \dots & 0 \\
    L_{21} & L_{22} & \dots & 0 \\
    \vdots & \vdots & \ddots & \vdots \\
    L_{d1} & L_{d2} & \dots & L_{dd}
    \end{bmatrix} \begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_d \end{bmatrix} = \begin{bmatrix} b_1 \\ b_2 \\ \vdots \\ b_d \end{bmatrix}$$
    We solve sequentially from top to bottom:
    $$y_1 = \frac{b_1}{L_{11}}$$
    $$y_i = \frac{b_i - \sum_{j=1}^{i-1} L_{ij} y_j}{L_{ii}} \quad \text{for } i = 2, 3, \dots, d$$
    The number of multiplications and subtractions at step $i$ is $i-1$. Summing operations over all $d$ rows yields:
    $$\text{Operations}_{Forward} = \sum_{i=1}^{d} (i-1) = \frac{d(d-1)}{2} \approx \frac{1}{2} d^2$$

2.  **Backward Substitution Phase ($\mathbf{U}\mathbf{x} = \mathbf{y}$):**
    Because $\mathbf{U}$ is upper triangular:
    $$\begin{bmatrix} 
    U_{11} & U_{12} & \dots & U_{1d} \\
    0 & U_{22} & \dots & U_{2d} \\
    \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & \dots & U_{dd}
    \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_d \end{bmatrix} = \begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_d \end{bmatrix}$$
    We solve sequentially from bottom to top:
    $$x_d = \frac{y_d}{U_{dd}}$$
    $$x_i = \frac{y_i - \sum_{j=i+1}^{d} U_{ij} x_j}{U_{ii}} \quad \text{for } i = d-1, d-2, \dots, 1$$
    Summing operations yields:
    $$\text{Operations}_{Backward} = \sum_{i=1}^{d} (d-i) = \frac{d(d-1)}{2} \approx \frac{1}{2} d^2$$

3.  **Calculate Total Complexity:**
    $$\text{Total Operations} \approx \frac{1}{2} d^2 + \frac{1}{2} d^2 = d^2 = O(d^2) \quad \blacksquare$$
This proves that solving a factored system takes $O(d^2)$ operations, which is significantly faster than standard Gaussian elimination or direct matrix inversion, which cost $O(d^3)$.

---

## 4. Concrete Examples

### Example 1: LU Factorization
We decompose the matrix $\mathbf{A} = \begin{bmatrix} 2 & 3 \\ 8 & 21 \end{bmatrix}$.
We set $L_{11} = 1, L_{22} = 1, L_{12} = 0$:
$$\begin{bmatrix} 2 & 3 \\ 8 & 21 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ L_{21} & 1 \end{bmatrix} \begin{bmatrix} U_{11} & U_{12} \\ 0 & U_{22} \end{bmatrix} = \begin{bmatrix} U_{11} & U_{12} \\ L_{21}U_{11} & L_{21}U_{12} + U_{22} \end{bmatrix}$$

1.  **Solve first row:**
    $$U_{11} = 2 \quad \text{and} \quad U_{12} = 3$$
2.  **Solve second row, first column:**
    $$L_{21} U_{11} = 8 \implies L_{21} \cdot 2 = 8 \implies L_{21} = 4$$
3.  **Solve second row, second column:**
    $$L_{21} U_{12} + U_{22} = 21 \implies 4 \cdot 3 + U_{22} = 21 \implies U_{22} = 9$$
Result:
$$\mathbf{L} = \begin{bmatrix} 1 & 0 \\ 4 & 1 \end{bmatrix} \quad \text{and} \quad \mathbf{U} = \begin{bmatrix} 2 & 3 \\ 0 & 9 \end{bmatrix}$$

### Example 2: Cholesky Factorization
We decompose the symmetric, positive-definite matrix $\mathbf{A} = \begin{bmatrix} 4 & 12 \\ 12 & 37 \end{bmatrix}$.
We solve for $\mathbf{L} = \begin{bmatrix} L_{11} & 0 \\ L_{21} & L_{22} \end{bmatrix}$ satisfying $\mathbf{A} = \mathbf{L}\mathbf{L}^T$:
$$\begin{bmatrix} 4 & 12 \\ 12 & 37 \end{bmatrix} = \begin{bmatrix} L_{11} & 0 \\ L_{21} & L_{22} \end{bmatrix} \begin{bmatrix} L_{11} & L_{21} \\ 0 & L_{22} \end{bmatrix} = \begin{bmatrix} L_{11}^2 & L_{11}L_{21} \\ L_{21}L_{11} & L_{21}^2 + L_{22}^2 \end{bmatrix}$$

1.  **Solve first column diagonal:**
    $$L_{11}^2 = 4 \implies L_{11} = 2$$
2.  **Solve first column off-diagonal:**
    $$L_{11} L_{21} = 12 \implies 2 \cdot L_{21} = 12 \implies L_{21} = 6$$
3.  **Solve second column diagonal:**
    $$L_{21}^2 + L_{22}^2 = 37 \implies 6^2 + L_{22}^2 = 37 \implies L_{22}^2 = 37 - 36 = 1 \implies L_{22} = 1$$
Result:
$$\mathbf{L} = \begin{bmatrix} 2 & 0 \\ 6 & 1 \end{bmatrix}$$

---

## 5. Applied ML Context

1.  **Stable OLS Solutions via QR:** Decomposing the feature matrix $\mathbf{X} = \mathbf{Q}\mathbf{R}$ allows solving for weights via $\mathbf{R}\boldsymbol{\beta} = \mathbf{Q}^T\mathbf{y}$. This avoids computing the Gramian inverse $(\mathbf{X}^T\mathbf{X})^{-1}$, which is numerically unstable.
2.  **Gaussian Process Regression:** GPs require solving covariance matrix inversions. Cholesky decomposition $\boldsymbol{\Sigma} = \mathbf{L}\mathbf{L}^T$ is used to solve linear systems and compute the covariance log-determinant.
3.  **Newton-Raphson Optimization Step:** In second-order optimizers, the Hessian matrix is factored using LU or Cholesky to compute the update direction vector $\Delta \mathbf{w} = -\mathbf{H}^{-1}\nabla f$.
4.  **Latent Semantic Analysis (NLP):** QR factorization is used as a preprocessing step to orthogonalize feature spaces before running singular value decompositions.
5.  **State-Space Kalman Filtering:** In real-time tracking, Cholesky decomposition is performed at each time step to update hidden state covariances under measurement updates.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating matrix factorization geometries:
*   Draw a central square matrix $\mathbf{A}$ splitting into three pathways:
    1.  **LU Split:** Show $\mathbf{A}$ factorized into lower triangular $\mathbf{L}$ (elements shaded bottom-left) and upper triangular $\mathbf{U}$ (elements shaded top-right).
    2.  **QR Split:** Show $\mathbf{A}$ factorized into orthogonal $\mathbf{Q}$ (illustrated as mutually perpendicular axis vectors) and upper triangular $\mathbf{R}$.
    3.  **Cholesky Split:** Show symmetric $\mathbf{A}$ factorized into lower triangular $\mathbf{L}$ and its reflected transpose $\mathbf{L}^T$.
*   Add a caption explaining that matrix decompositions factorize a single complex transformation into structured, triangular, or orthogonal components, reducing computational complexity.
