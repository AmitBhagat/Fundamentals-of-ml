---
title: "Positive Definite Matrices"
description: "Quadratic forms, spectral decomposition, Sylvester's criterion, Cholesky factorization, and optimization stability."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Vector Spaces", "Matrices", "Eigenvalues and Eigenvectors"]
---

<h1 align="center"> Chapter 23: Positive Definite Matrices </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Symmetric Matrices:** Familiarity with matrices where $A = A^T$.
* **Eigenvalues:** Understanding scaling factors along characteristic directions.

</div>

## 1. Conceptual Hook

In machine learning optimization, we are constantly navigating high-dimensional loss landscapes to find the lowest point. But how do we know if we have landed in a stable valley, a peak, or a treacherous saddle point? The mathematical structure that guarantees stability is the **positive definite matrix**.

A symmetric matrix is positive definite if it defines a quadratic energy function that remains strictly positive in all non-zero directions. Geometrically, it represents a perfect, upward-opening bowl. This shape ensures that optimization algorithms like Gradient Descent can safely converge to a unique, stable global minimum. From multivariate Gaussian distributions and Gaussian Process regression to support vector machine kernels and Hessian curvature, positive definiteness is the mathematical backbone of model stability and optimization.

---

## 2. Formal Definition

Let $A \in \mathbb{R}^{n \times n}$ be a real symmetric matrix ($A = A^T$).
*   **Positive Definite ($A \succ 0$):** $A$ is positive definite if the scalar result of its quadratic form is strictly positive for every non-zero vector $x \in \mathbb{R}^n$:
    $$x^T A x > 0 \quad \forall x \in \mathbb{R}^n \setminus \{\mathbf{0}\}$$
*   **Positive Semi-Definite ($A \succeq 0$):** $A$ is positive semi-definite if the quadratic form is non-negative for all vectors:
    $$x^T A x \ge 0 \quad \forall x \in \mathbb{R}^n$$

### Equivalent Characterizations
For a real symmetric matrix $A$, the following statements are equivalent:
1.  **Positive Definiteness:** $A \succ 0$.
2.  **Positive Eigenvalues:** All eigenvalues $\lambda_i$ of $A$ are strictly positive:
    $$\lambda_i > 0 \quad \forall i=1, \dots, n$$
3.  **Sylvester's Criterion:** All principal minors of $A$ (the determinants of its top-left submatrices) are strictly positive.
4.  **Cholesky Decomposition:** $A$ can be decomposed uniquely as:
    $$A = L L^T$$
    where $L$ is a lower triangular matrix with strictly positive diagonal entries.

---

## 3. Illustrative Derivation

### Equivalence of Positive Definiteness and Positive Eigenvalues
We prove that a symmetric matrix $A \in \mathbb{R}^{n \times n}$ is positive definite if and only if all of its eigenvalues are strictly positive.

*Proof:*
Since $A$ is symmetric, by the Spectral Theorem, there exists an orthogonal matrix $Q \in \mathbb{R}^{n \times n}$ ($Q^T Q = I_n$) of eigenvectors such that:
$$A = Q \Lambda Q^T$$
where $\Lambda = \text{diag}(\lambda_1, \lambda_2, \dots, \lambda_n)$ is the diagonal matrix of eigenvalues.

Let us evaluate the quadratic form $x^T A x$ for any non-zero vector $x \in \mathbb{R}^n$:
$$x^T A x = x^T (Q \Lambda Q^T) x = (Q^T x)^T \Lambda (Q^T x)$$
Let $y = Q^T x$. Since $Q^T$ is invertible (orthogonal), if $x \neq 0$, then $y \neq 0$.
Expanding the diagonal product:
$$x^T A x = y^T \Lambda y = \sum_{i=1}^n \lambda_i y_i^2$$

1.  **Forward Direction ($\lambda_i > 0 \implies A \succ 0$):**
    Assume $\lambda_i > 0$ for all $i=1, \dots, n$. Since $y \neq 0$, there exists at least one component $y_j \neq 0$, meaning $y_j^2 > 0$. Since all other terms $y_i^2 \ge 0$ and $\lambda_i > 0$:
    $$\sum_{i=1}^n \lambda_i y_i^2 > 0 \implies x^T A x > 0$$
    Thus, $A$ is positive definite.

2.  **Reverse Direction ($A \succ 0 \implies \lambda_i > 0$):**
    Assume $A$ is positive definite ($x^T A x > 0$ for all $x \neq 0$). Let $q_i$ be the $i$-th eigenvector of $A$ corresponding to eigenvalue $\lambda_i$. Since $q_i$ is a basis vector, $q_i \neq 0$. Evaluate the quadratic form using $x = q_i$:
    $$q_i^T A q_i = q_i^T (\lambda_i q_i) = \lambda_i (q_i^T q_i) = \lambda_i \|q_i\|_2^2$$
    By positive definiteness, $q_i^T A q_i > 0$. Since $\|q_i\|_2^2 > 0$:
    $$\lambda_i \|q_i\|_2^2 > 0 \implies \lambda_i > 0$$
    This holds for all eigenvalues $\lambda_i$. Thus, all eigenvalues are strictly positive. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: A Positive Definite Matrix
Let $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$. Check if $A \succ 0$.
1.  **Calculate Eigenvalues:**
    $$\det(A - \lambda I) = \det\begin{pmatrix} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{pmatrix} = (2 - \lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0$$
    $$(\lambda - 3)(\lambda - 1) = 0 \implies \lambda_1 = 3, \quad \lambda_2 = 1$$
    Since both eigenvalues are strictly positive ($3 > 0$ and $1 > 0$), $A$ is positive definite.
2.  **Check Cholesky Decomposition:**
    We seek $L = \begin{pmatrix} l_{11} & 0 \\ l_{21} & l_{22} \end{pmatrix}$ such that $L L^T = A$:
    $$\begin{pmatrix} l_{11} & 0 \\ l_{21} & l_{22} \end{pmatrix} \begin{pmatrix} l_{11} & l_{21} \\ 0 & l_{22} \end{pmatrix} = \begin{pmatrix} l_{11}^2 & l_{11} l_{21} \\ l_{11} l_{21} & l_{21}^2 + l_{22}^2 \end{pmatrix} = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$$
    *   $l_{11}^2 = 2 \implies l_{11} = \sqrt{2}$
    *   $l_{11} l_{21} = 1 \implies l_{21} = \frac{1}{\sqrt{2}}$
    *   $l_{21}^2 + l_{22}^2 = 2 \implies \frac{1}{2} + l_{22}^2 = 2 \implies l_{22}^2 = \frac{3}{2} \implies l_{22} = \sqrt{\frac{3}{2}}$
    Since a unique lower-triangular $L$ with positive diagonal elements exists, $A \succ 0$.

### Example 2: An Indefinite Matrix
Let $B = \begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$.
1.  **Calculate Eigenvalues:**
    $$\det(B - \lambda I) = (1 - \lambda)^2 - 4 = \lambda^2 - 2\lambda - 3 = 0 \implies (\lambda - 3)(\lambda + 1) = 0 \implies \lambda_1 = 3, \quad \lambda_2 = -1$$
    Since one eigenvalue is negative, $B$ is indefinite.
2.  **Verify using a test vector:**
    Let $x = \begin{bmatrix} 1 \\ -1 \end{bmatrix}$. The quadratic form is:
    $$x^T B x = \begin{bmatrix} 1, & -1 \end{bmatrix} \begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix} \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 1, & -1 \end{bmatrix} \begin{bmatrix} 1(1) + 2(-1) \\ 2(1) + 1(-1) \end{bmatrix} = \begin{bmatrix} 1, & -1 \end{bmatrix} \begin{bmatrix} -1 \\ 1 \end{bmatrix} = -2$$
    Since the quadratic form yields a negative value, $B$ is not positive definite.

---

## 5. Applied ML Context

1.  **Covariance Matrices:** By definition, empirical covariance matrices $\Sigma = \frac{1}{n} X^T X$ are always positive semi-definite ($A \succeq 0$). If features are linearly independent, $\Sigma \succ 0$. This ensures that the variance of any linear combination of features is strictly non-negative: $\text{Var}(w^T x) = w^T \Sigma w \ge 0$.
2.  **Optimization Stability (The Hessian):** In multivariate optimization, a critical point $x^*$ is a local minimum if the gradient $\nabla f(x^*) = 0$ and the Hessian matrix $H(x^*) = \nabla^2 f(x^*)$ is positive definite ($H(x^*) \succ 0$). This guarantees the landscape curves upwards in all directions.
3.  **Kernel Methods (SVMs):** By Mercer's Theorem, a function $k(x, y)$ is a valid kernel if and only if the Gram matrix $K_{ij} = k(x_i, x_j)$ is positive semi-definite for any set of input vectors. This ensures that the kernel corresponds to a dot product in a valid Hilbert space.
4.  **Gaussian Process Regression:** GPs define distributions over functions, parameterized by a kernel covariance matrix $K$. This matrix must be positive definite to ensure the multivariate Gaussian probability density function is mathematically defined.
5.  **Cholesky Sampling:** To sample from a multivariate normal distribution $\mathcal{N}(\mu, \Sigma)$, we compute the Cholesky factorization $\Sigma = L L^T$. We then draw standard normal samples $z \sim \mathcal{N}(0, I)$ and transform them: $x = \mu + Lz$. Cholesky decomposition requires $\Sigma \succ 0$.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here showing the 3D graph of quadratic forms $f(x, y) = \begin{bmatrix} x, & y \end{bmatrix} A \begin{bmatrix} x \\ y \end{bmatrix}$ to illustrate definiteness:
*   **Positive Definite ($A \succ 0$):** Show a 3D parabolic **bowl** opening upwards. The minimum is at the origin $(0, 0, 0)$, and any step away from the center results in a positive height.
*   **Negative Definite ($A \prec 0$):** Show an inverted 3D parabolic **dome** opening downwards, where any step away from the origin results in a negative height.
*   **Indefinite Matrix:** Show a **saddle point** (hyperbolic paraboloid), where moving along one axis curves upwards (positive eigenvalues) while moving along another axis curves downwards (negative eigenvalues). Label the origin as the saddle point.
