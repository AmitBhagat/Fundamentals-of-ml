---
title: "Orthogonality and Projections"
description: "Orthogonal subspaces, vector projections, derivation of the projection matrix, and Ordinary Least Squares."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Vector Spaces", "Matrices", "Dot Product"]
---

<h1 align="center"> Chapter 21: Orthogonality and Projections </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Dot Product:** Understanding the algebraic and geometric definition of vector inner products.
* **Vector Subspaces:** Knowing how matrices span coordinate spaces.

</div>

## 1. Conceptual Hook

In machine learning, we are often forced to work in restricted spaces. A linear model might try to predict continuous labels using only a few features, or we might want to compress a 1000-dimensional embedding down to 2 dimensions for visualization. How do we find the "best possible representation" of our original data within these restricted subspaces? We use **projections**.

A projection is the mathematical way of finding the "closest fit" in a restricted space. Imagine shining a flashlight directly above a vector: the shadow it casts onto the floor (the subspace) is its projection. To make this shadow as accurate as possible, the error vector (the distance from the original vector to the shadow) must be completely perpendicular, or **orthogonal**, to the floor. In ML, this geometric optimization is what enables Ordinary Least Squares regression to find optimal parameters and PCA to project data onto variance-aligned coordinates.

---

## 2. Formal Definition

Let $V$ be an inner product space.
*   **Orthogonality:** Two vectors $u, v \in V$ are **orthogonal** (written $u \perp v$) if and only if their inner product is zero:
    $$\langle u, v \rangle = 0 \iff u^T v = 0$$
*   **Orthogonal Complement:** For a subspace $W \subseteq V$, the orthogonal complement $W^\perp$ is the set of all vectors in $V$ that are orthogonal to every vector in $W$:
    $$W^\perp = \{ v \in V \mid \langle v, w \rangle = 0 \quad \forall w \in W \}$$
*   **Orthogonal Projection:** The orthogonal projection of a vector $y \in V$ onto a subspace $W$ is the unique vector $\hat{y} \in W$ such that the error vector $e = y - \hat{y}$ is orthogonal to $W$:
    $$(y - \hat{y}) \in W^\perp \iff \langle y - \hat{y}, w \rangle = 0 \quad \forall w \in W$$
    We denote this projection vector as:
    $$\hat{y} = \text{proj}_W(y)$$

If the subspace $W$ is spanned by a single non-zero vector $u$, the projection of $y$ onto $u$ simplifies to:
$$\text{proj}_u(y) = \left( \frac{y^T u}{\|u\|_2^2} \right) u$$

---

## 3. Illustrative Derivation

### Derivation of the Multi-Dimensional Projection Matrix
In linear regression, we project a target vector $y \in \mathbb{R}^n$ onto the column space of a feature matrix $X \in \mathbb{R}^{n \times d}$. We derive the closed-form projection matrix.

Let $W = \text{col}(X)$ be the subspace spanned by the columns of $X$. We assume the columns of $X$ are linearly independent. Any vector $\hat{y} \in W$ can be represented as a linear combination of the columns of $X$:
$$\hat{y} = X\beta$$
where $\beta \in \mathbb{R}^d$ is the coordinate vector of coefficients.

The orthogonal projection criteria requires the error vector $e = y - \hat{y} = y - X\beta$ to be orthogonal to the spanning subspace $W$. Since $W$ is spanned by the columns of $X$, the error vector must be orthogonal to each column of $X$. This can be written compactly as:
$$X^T e = 0$$
$$X^T (y - X\beta) = 0$$

Distributing the transpose matrix:
$$X^T y - X^T X \beta = 0$$
$$X^T X \beta = X^T y$$
These are the **normal equations**. Since the columns of $X$ are linearly independent, the Gram matrix $X^T X \in \mathbb{R}^{d \times d}$ is invertible:
$$\beta = (X^T X)^{-1} X^T y$$

Substituting this optimal coefficient vector $\beta$ back into our equation for $\hat{y}$:
$$\hat{y} = X \beta = X (X^T X)^{-1} X^T y$$
We define the **projection matrix** (or "hat matrix") $H$ as:
$$H = X (X^T X)^{-1} X^T$$
such that $\hat{y} = Hy$. 

### Properties of the Projection Matrix $H$
We prove that $H$ is:
1.  **Symmetric:**
    $$H^T = \left( X (X^T X)^{-1} X^T \right)^T = (X^T)^T \left( (X^T X)^{-1} \right)^T X^T = X (X^T X)^{-1} X^T = H$$
2.  **Idempotent:** Projecting a vector that is already in the subspace should not change it ($H^2 = H$):
    $$H^2 = H \cdot H = \left( X (X^T X)^{-1} X^T \right) \left( X (X^T X)^{-1} X^T \right)$$
    Grouping terms:
    $$H^2 = X (X^T X)^{-1} \left( X^T X \right) (X^T X)^{-1} X^T = X (I_d) (X^T X)^{-1} X^T = X (X^T X)^{-1} X^T = H \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: 1D Vector Projection and Orthogonality Check
Project $y = \begin{bmatrix} 4 \\ 3 \end{bmatrix}$ onto the line spanned by $u = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
1.  **Compute the projection:**
    $$\hat{y} = \text{proj}_u(y) = \left( \frac{y^T u}{u^T u} \right) u = \left( \frac{4(1) + 3(1)}{1^2 + 1^2} \right) \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \frac{7}{2} \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3.5 \\ 3.5 \end{bmatrix}$$
2.  **Calculate the error vector $e$:**
    $$e = y - \hat{y} = \begin{bmatrix} 4 \\ 3 \end{bmatrix} - \begin{bmatrix} 3.5 \\ 3.5 \end{bmatrix} = \begin{bmatrix} 0.5 \\ -0.5 \end{bmatrix}$$
3.  **Verify orthogonality ($e^T u = 0$):**
    $$e^T u = (0.5)(1) + (-0.5)(1) = 0.5 - 0.5 = 0$$
The error vector is orthogonal to the target line, confirming $\hat{y}$ is the closest point on the line to $y$.

### Example 2: Projection Matrix Application
Let $X = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$. Construct $H$ and project $y = \begin{bmatrix} 3 \\ 1 \end{bmatrix}$.
1.  **Compute $X^T X$ and its inverse:**
    $$X^T X = \begin{bmatrix} 1, & 2 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = 1 + 4 = 5 \implies (X^T X)^{-1} = \frac{1}{5}$$
2.  **Construct $H = X(X^T X)^{-1} X^T$:**
    $$H = \begin{bmatrix} 1 \\ 2 \end{bmatrix} \left( \frac{1}{5} \right) \begin{bmatrix} 1, & 2 \end{bmatrix} = \frac{1}{5} \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix} = \begin{pmatrix} 0.2 & 0.4 \\ 0.4 & 0.8 \end{pmatrix}$$
3.  **Apply $H$ to $y$:**
    $$\hat{y} = H y = \begin{pmatrix} 0.2 & 0.4 \\ 0.4 & 0.8 \end{pmatrix} \begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} 0.2(3) + 0.4(1) \\ 0.4(3) + 0.8(1) \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$$
    This matches the analytical projection formula: $\frac{3(1) + 1(2)}{5} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = 1 \begin{bmatrix} 1 \\ 2 \end{bmatrix}$.

---

## 5. Applied ML Context

1.  **Ordinary Least Squares (OLS):** Linear regression fits parameter weights $\beta$ to minimize residual sum of squares. Geometrically, the prediction vector $\hat{y} = X\beta$ is the orthogonal projection of the label vector $y$ onto the column space of the feature matrix $X$.
2.  **Gram-Schmidt Orthogonalization:** In signal processing and embedding setups, this algorithm converts a set of linearly independent vectors into an orthonormal basis by sequentially projecting and subtracting overlapping components.
3.  **Support Vector Machines (SVMs):** The margin width separating classes is calculated as the orthogonal projection of the vector difference between support vectors onto the weight vector $w$ representing the hyperplane's normal.
4.  **PCA (Principal Component Analysis):** PCA reduces dimensions by projecting data points onto the subspace spanned by the covariance matrix's top $k$ eigenvectors, minimizing the reconstruction error.
5.  **Subspace Clustering:** High-dimensional data points are grouped by projecting them onto different low-dimensional subspaces, identifying local linear structures (e.g., in computer vision tracking).

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating 3D orthogonal projections:
*   Show a 3D coordinate system.
*   Draw a flat 2D plane $W$ passing through the origin.
*   Plot a vector $y$ starting from the origin and pointing diagonally upwards, out of the plane.
*   Draw the projection vector $\hat{y}$ lying entirely on the plane $W$.
*   Draw the error vector $e = y - \hat{y}$ starting from the tip of $\hat{y}$ and ending at the tip of $y$. Draw a right-angle symbol ($90^\circ$) between the plane $W$ and the error vector $e$ to emphasize that the shortest distance to the subspace must be orthogonal.
