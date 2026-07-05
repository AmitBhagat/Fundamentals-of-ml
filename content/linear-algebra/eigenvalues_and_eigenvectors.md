---
title: "Eigenvalues and Eigenvectors"
description: "Spectral theory, coordinate-free linear operators, characteristic polynomials, real symmetric matrices, and the Spectral Theorem."
complexity: "Advanced"
estimated_time: "45 min"
prerequisites: ["Linear Algebra: Vector Spaces", "Linear Algebra: Linear Transformations", "Linear Algebra: Inner Products"]
---

<h1 align="center"> Chapter 14: Eigenvalues and Eigenvectors </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Linear Transformations:** Matrix representations of linear maps $T: V \to V$ on a vector space $V$.
* **Determinants and Kernels:** Comprehending the operator null space $\ker(T)$ and how singular operators have vanishing determinants.
* **Inner Product Spaces:** Familiarity with the standard inner product $\langle u, v \rangle = u^T v$ in $\mathbb{R}^n$ and orthogonal projections.

</div>

## 1. Conceptual Hook

Think of eigenvalues and eigenvectors as the **natural resonance axes of a physical system**, like a drumhead or a guitar string.

When you strike a drumhead, the resulting vibrations appear chaotic. The surface deforms, waves propagate in all directions, and the shape changes dynamically. However, any complex vibration is actually a superposition of **standing waves**—modes of vibration where the drumhead moves purely up and down without traveling or warping sideways.

The **eigenvectors** are these fundamental standing wave patterns (the natural shapes of resonance). The transformation (striking the drum) only scales the amplitude of these patterns; it does not alter their spatial shape. The **eigenvalues** represent the resonant frequencies (the scaling factor of the amplitude).

In machine learning, instead of physical vibrations, we "strike" high-dimensional datasets with covariance matrices or graph Laplacians. The eigenvectors reveal the stable, non-warping modes of the data, while the eigenvalues tell us the energy or variance concentrated in those directions.

---

## 2. Formal Definition

Let $V$ be a vector space over a field $F$ (typically $\mathbb{R}$ or $\mathbb{C}$). A linear operator is a map $T: V \to V$.

### Coordinate-Free Definition
A non-zero vector $v \in V \setminus \{0\}$ is an **eigenvector** of $T$ if there exists a scalar $\lambda \in F$ (the **eigenvalue**) such that:
$$T(v) = \lambda v$$
This definition is coordinate-free; it does not depend on choosing a basis for $V$.

### Matrix Representation and the Characteristic Equation
If $V$ is finite-dimensional ($d = \dim V$), we represent $T$ as a square matrix $\mathbf{A} \in F^{d \times d}$ under a chosen basis. The operator equation becomes:
$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v} \iff (\mathbf{A} - \lambda \mathbf{I})\mathbf{v} = \mathbf{0}$$
For a non-zero vector $\mathbf{v}$ to exist in the null space of $(\mathbf{A} - \lambda \mathbf{I})$, the matrix operator must be singular. Thus, the eigenvalues are the roots of the **characteristic polynomial**:
$$p(\lambda) = \det(\mathbf{A} - \lambda \mathbf{I}) = 0$$

### The Spectral Theorem for Real Symmetric Matrices
Let $\mathbf{A} \in \mathbb{R}^{d \times d}$ be a symmetric matrix ($\mathbf{A} = \mathbf{A}^T$). The **Spectral Theorem** guarantees that:
1.  All eigenvalues of $\mathbf{A}$ are real: $\lambda_i \in \mathbb{R}$.
2.  Eigenvectors corresponding to distinct eigenvalues are orthogonal.
3.  $\mathbf{A}$ is orthogonally diagonalizable:
    $$\mathbf{A} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^T = \sum_{i=1}^{d} \lambda_i \mathbf{q}_i \mathbf{q}_i^T$$
    where $\mathbf{Q}$ is an orthogonal matrix ($\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$) whose columns $\mathbf{q}_i$ are the orthonormal eigenvectors of $\mathbf{A}$.

> **Gotcha:** If a matrix is non-symmetric, it might not have a complete set of $d$ linearly independent eigenvectors (known as a **deficient** matrix). In such cases, diagonalization fails. For real symmetric matrices, completeness and orthogonality are mathematically guaranteed.

---

## 3. Illustrative Derivation

### Proof: Properties of Symmetric Matrix Spectra
We prove that (1) all eigenvalues of a real symmetric matrix are real, and (2) eigenvectors corresponding to distinct eigenvalues are orthogonal.

*Proof:*
Let $\mathbf{A} \in \mathbb{R}^{d \times d}$ be a symmetric matrix ($\mathbf{A} = \mathbf{A}^T$).

1.  **Prove eigenvalues are real ($\lambda_i \in \mathbb{R}$):**
    Suppose $\lambda \in \mathbb{C}$ is an eigenvalue of $\mathbf{A}$ with eigenvector $\mathbf{v} \in \mathbb{C}^d \setminus \{\mathbf{0}\}$:
    $$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$
    Taking the conjugate transpose (Hermitian conjugate, denoted by $^H$) of both sides:
    $$(\mathbf{A}\mathbf{v})^H = (\lambda \mathbf{v})^H \implies \mathbf{v}^H \mathbf{A}^H = \bar{\lambda} \mathbf{v}^H$$
    Since $\mathbf{A}$ is real and symmetric, $\mathbf{A}^H = \overline{\mathbf{A}}^T = \mathbf{A}^T = \mathbf{A}$. Thus:
    $$\mathbf{v}^H \mathbf{A} = \bar{\lambda} \mathbf{v}^H$$
    Post-multiply both sides of this equation by $\mathbf{v}$:
    $$\mathbf{v}^H \mathbf{A} \mathbf{v} = \bar{\lambda} \mathbf{v}^H \mathbf{v} \quad \text{(Equation 1)}$$
    Now, pre-multiply our original eigenvector equation $\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$ by $\mathbf{v}^H$:
    $$\mathbf{v}^H \mathbf{A} \mathbf{v} = \lambda \mathbf{v}^H \mathbf{v} \quad \text{(Equation 2)}$$
    Equating Equation 1 and Equation 2 yields:
    $$\lambda \mathbf{v}^H \mathbf{v} = \bar{\lambda} \mathbf{v}^H \mathbf{v} \implies (\lambda - \bar{\lambda}) \mathbf{v}^H \mathbf{v} = 0$$
    Since $\mathbf{v}$ is a non-zero vector, its inner product is strictly positive: $\mathbf{v}^H \mathbf{v} = \sum_{i=1}^d |v_i|^2 > 0$. Thus:
    $$\lambda - \bar{\lambda} = 0 \implies \lambda = \bar{\lambda}$$
    Since the eigenvalue equals its complex conjugate, $\lambda$ must be a real number ($\lambda \in \mathbb{R}$).

2.  **Prove distinct eigenvectors are orthogonal ($\mathbf{v}_1^T \mathbf{v}_2 = 0$):**
    Let $\mathbf{A}\mathbf{v}_1 = \lambda_1 \mathbf{v}_1$ and $\mathbf{A}\mathbf{v}_2 = \lambda_2 \mathbf{v}_2$ with $\lambda_1 \neq \lambda_2$.
    Consider the inner product product expansion:
    $$\lambda_1 \mathbf{v}_1^T \mathbf{v}_2 = (\mathbf{A}\mathbf{v}_1)^T \mathbf{v}_2 = \mathbf{v}_1^T \mathbf{A}^T \mathbf{v}_2$$
    Since $\mathbf{A}$ is symmetric ($\mathbf{A}^T = \mathbf{A}$):
    $$\lambda_1 \mathbf{v}_1^T \mathbf{v}_2 = \mathbf{v}_1^T \mathbf{A} \mathbf{v}_2 = \mathbf{v}_1^T (\lambda_2 \mathbf{v}_2) = \lambda_2 \mathbf{v}_1^T \mathbf{v}_2$$
    Rearranging terms:
    $$(\lambda_1 - \lambda_2) \mathbf{v}_1^T \mathbf{v}_2 = 0$$
    Since the eigenvalues are distinct ($\lambda_1 - \lambda_2 \neq 0$), we conclude:
    $$\mathbf{v}_1^T \mathbf{v}_2 = 0 \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Spectral Decomposition of a Symmetric Matrix
We decompose the symmetric matrix $\mathbf{A} = \begin{bmatrix} 3 & 2 \\ 2 & 3 \end{bmatrix}$.
1.  **Solve the Characteristic Equation:**
    $$\det(\mathbf{A} - \lambda \mathbf{I}) = \det \begin{bmatrix} 3-\lambda & 2 \\ 2 & 3-\lambda \end{bmatrix} = (3-\lambda)^2 - 4 = 0$$
    $$\lambda^2 - 6\lambda + 5 = 0 \implies (\lambda - 5)(\lambda - 1) = 0$$
    The eigenvalues are $\lambda_1 = 5$ and $\lambda_2 = 1$.
2.  **Determine orthonormal eigenvectors:**
    *   For $\lambda_1 = 5$:
        $$\begin{bmatrix} -2 & 2 \\ 2 & -2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies x_1 = x_2 \implies \mathbf{q}_1 = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
    *   For $\lambda_2 = 1$:
        $$\begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies x_1 = -x_2 \implies \mathbf{q}_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$
    Note that $\mathbf{q}_1^T \mathbf{q}_2 = 0$ (orthogonal).
3.  **Reconstruct using the Spectral Theorem:**
    $$\mathbf{Q} = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}, \quad \mathbf{\Lambda} = \begin{bmatrix} 5 & 0 \\ 0 & 1 \end{bmatrix}$$
    $$\mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^T = \frac{1}{2} \begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} 5 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix} = \frac{1}{2} \begin{bmatrix} 5 & -1 \\ 5 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix} = \begin{bmatrix} 3 & 2 \\ 2 & 3 \end{bmatrix} = \mathbf{A}$$

### Example 2: Eigenspectrum of a Non-Symmetric Matrix
We find the eigenvalues and eigenvectors for the non-symmetric matrix $\mathbf{B} = \begin{bmatrix} 0 & 1 \\ -2 & 3 \end{bmatrix}$.
1.  **Solve the Characteristic Equation:**
    $$\det(\mathbf{B} - \lambda \mathbf{I}) = \det \begin{bmatrix} -\lambda & 1 \\ -2 & 3-\lambda \end{bmatrix} = -\lambda(3-\lambda) + 2 = \lambda^2 - 3\lambda + 2 = 0 \implies (\lambda - 2)(\lambda - 1) = 0$$
    The eigenvalues are $\lambda_1 = 2$ and $\lambda_2 = 1$.
2.  **Determine eigenvectors:**
    *   For $\lambda_1 = 2$:
        $$\begin{bmatrix} -2 & 1 \\ -2 & 1 \end{bmatrix} \mathbf{v}_1 = \mathbf{0} \implies \mathbf{v}_1 = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$$
    *   For $\lambda_2 = 1$:
        $$\begin{bmatrix} -1 & 1 \\ -2 & 2 \end{bmatrix} \mathbf{v}_2 = \mathbf{0} \implies \mathbf{v}_2 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
    *Note:* The eigenvectors $\mathbf{v}_1$ and $\mathbf{v}_2$ are not orthogonal ($\mathbf{v}_1^T \mathbf{v}_2 = 1\cdot1 + 2\cdot1 = 3 \neq 0$), because $\mathbf{B}$ is not symmetric.

---

## 5. Applied ML Context

1.  **Principal Component Analysis (PCA):** Finding eigenvectors of the symmetric covariance matrix $\boldsymbol{\Sigma} = \frac{1}{n} \mathbf{X}^T \mathbf{X}$. The eigenvectors represent directions of maximum variance (principal components), used for dimension reduction.
2.  **Spectral Graph Theory and GNNs:** The normalized Graph Laplacian $\mathbf{L}_{sym} = \mathbf{I} - \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$ is symmetric. Its eigenvectors define the graph Fourier basis, enabling graph convolutions.
3.  **Google PageRank:** Modeling internet browsing as a Markov chain. The PageRank score is the stationary distribution vector, which is the dominant eigenvector (eigenvalue $\lambda = 1$) of the hyperlink transition matrix.
4.  **Deep Landscape Hessian Spectrum:** Checking the eigenvalues of the Hessian matrix $\nabla^2 L(\boldsymbol{\theta})$ to analyze loss landscape curvature. A large condition number $\lambda_{max} / \lambda_{min}$ indicates steep ravines.
5.  **Kernel PCA and Spectral Clustering:** Decomposing affinity and kernel matrices using eigenvectors to perform non-linear dimensionality reduction and cluster data.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating eigenvector scaling under transformation:
*   Draw two 2D grids side-by-side:
    1.  **Original Space:** Draw a unit circle centered at the origin, with two coordinate arrows $\mathbf{v}_1$ and $\mathbf{v}_2$ pointing along different directions.
    2.  **Transformed Space:** Draw an ellipse representing the grid after transformation by a matrix.
*   Show that while most vectors on the unit circle have rotated and shifted, the arrows representing eigenvectors $\mathbf{v}_1$ and $\mathbf{v}_2$ still point in their original directions, only stretched in length by their corresponding eigenvalues $\lambda_1$ and $\lambda_2$.
*   Add a caption explaining that eigenvectors are the invariant directions of a linear transformation that do not rotate during mapping, undergoing only scaling by a factor equal to their eigenvalue.
