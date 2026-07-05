---
title: "Iterative Solvers (Conjugate Gradient)"
description: "Large sparse linear systems, quadratic form minimization, Krylov subspaces, A-conjugacy derivations, and preconditioning."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Linear Algebra: Matrices", "Linear Algebra: Orthogonality and Projections", "Optimization: Gradient Descent"]
---

<h1 align="center"> Chapter 99: Iterative Solvers (Conjugate Gradient) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Symmetric Positive-Definite (SPD) Matrix:** A symmetric matrix $\mathbf{A}$ satisfying $\mathbf{v}^T\mathbf{A}\mathbf{v} > 0$ for all non-zero vectors $\mathbf{v}$.
* **Krylov Subspace:** The vector space spanned by the images of a vector under successive powers of a matrix: $\mathcal{K}_k(\mathbf{A}, \mathbf{v}) = \text{span}\{\mathbf{v}, \mathbf{A}\mathbf{v}, \dots, \mathbf{A}^{k-1}\mathbf{v}\}$.

</div>

## 1. Conceptual Hook

Solving linear systems of equations $\mathbf{A}\mathbf{x} = \mathbf{b}$ is a core calculation in machine learning. However, when $\mathbf{A}$ is a massive, sparse matrix with millions of dimensions, direct solvers (like Gaussian elimination or Cholesky decomposition) become computationally impossible. Inverting the matrix requires $O(d^3)$ operations and destroys the computational efficiency of sparsity.

Standard gradient descent can approximate the solution iteratively but suffers from a "short-term memory" problem. In narrow, steep valleys, gradient descent takes steps perpendicular to the contours, leading to a slow, zig-zagging trajectory that repeats updates along previously explored directions.

The **Conjugate Gradient (CG)** method solves this memory problem.

Instead of taking steps along the steepest descent direction, CG generates a sequence of search directions that are mutually orthogonal with respect to the matrix $\mathbf{A}$ (called **$\mathbf{A}$-conjugate directions**). This geometric constraint guarantees that the minimization achieved along one search direction is never undone by subsequent updates. As a result, the algorithm eliminates redundant updates, guaranteeing convergence to the exact solution of a $d$-dimensional linear system in at most $d$ steps.

---

## 2. Formal Definition

We wish to solve the linear system:
$$\mathbf{A}\mathbf{x} = \mathbf{b}$$
where $\mathbf{A} \in \mathbb{R}^{d \times d}$ is a symmetric, positive-definite (SPD) matrix. Solving this system is mathematically equivalent to locating the unique global minimizer of the strictly convex quadratic function:
$$f(\mathbf{x}) = \frac{1}{2} \mathbf{x}^T \mathbf{A} \mathbf{x} - \mathbf{b}^T \mathbf{x}$$

### A-Conjugacy
Two non-zero vectors $\mathbf{p}_i, \mathbf{p}_j \in \mathbb{R}^d$ are defined as **$\mathbf{A}$-conjugate** (or $\mathbf{A}$-orthogonal) if:
$$\mathbf{p}_i^T \mathbf{A} \mathbf{p}_j = 0 \quad \forall i \neq j$$

### The Conjugate Gradient Algorithm
Starting from an initial guess $\mathbf{x}^{(0)}$, we compute the initial residual (which is the negative gradient of $f$):
$$\mathbf{r}^{(0)} = \mathbf{b} - \mathbf{A}\mathbf{x}^{(0)}$$
and set the initial search direction:
$$\mathbf{p}^{(0)} = \mathbf{r}^{(0)}$$

For iteration steps $k = 0, 1, 2, \dots$:
1.  **Calculate Primal Step Size ($\alpha_k$):**
    Minimize $f\left(\mathbf{x}^{(k)} + \alpha_k \mathbf{p}^{(k)}\right)$ along the direction $\mathbf{p}^{(k)}$:
    $$\alpha_k = \frac{\mathbf{r}^{(k)T} \mathbf{r}^{(k)}}{\mathbf{p}^{(k)T} \mathbf{A} \mathbf{p}^{(k)}}$$
2.  **Update Primal State Vector:**
    $$\mathbf{x}^{(k+1)} = \mathbf{x}^{(k)} + \alpha_k \mathbf{p}^{(k)}$$
3.  **Update Residual Vector:**
    $$\mathbf{r}^{(k+1)} = \mathbf{r}^{(k)} - \alpha_k \mathbf{A}\mathbf{p}^{(k)}$$
    If $\|\mathbf{r}^{(k+1)}\|_2 < \text{tolerance}$, terminate.
4.  **Calculate Conjugacy Coefficient ($\beta_k$):**
    Using the Fletcher-Reeves formula to enforce $\mathbf{A}$-conjugacy:
    $$\beta_k = \frac{\mathbf{r}^{(k+1)T} \mathbf{r}^{(k+1)}}{\mathbf{r}^{(k)T} \mathbf{r}^{(k)}}$$
5.  **Generate Next Conjugate Search Direction:**
    $$\mathbf{p}^{(k+1)} = \mathbf{r}^{(k+1)} + \beta_k \mathbf{p}^{(k)}$$

---

## 3. Illustrative Derivation

### Derivation of the Conjugate Parameter Updates
We derive the orthogonality of residuals ($\mathbf{r}^{(i)T} \mathbf{r}^{(j)} = 0$) and conjugacy of search directions ($\mathbf{p}^{(i)T} \mathbf{A} \mathbf{p}^{(j)} = 0$) for the first update step ($k = 1$).

*Proof:*
Let $\mathbf{p}^{(0)} = \mathbf{r}^{(0)} = \mathbf{b} - \mathbf{A}\mathbf{x}^{(0)}$.
1.  **Prove Residual Orthogonality ($\mathbf{r}^{(0)T} \mathbf{r}^{(1)} = 0$):**
    The residual update is $\mathbf{r}^{(1)} = \mathbf{r}^{(0)} - \alpha_0 \mathbf{A}\mathbf{p}^{(0)}$.
    Multiply by $\mathbf{r}^{(0)T}$:
    $$\mathbf{r}^{(0)T} \mathbf{r}^{(1)} = \mathbf{r}^{(0)T} \left( \mathbf{r}^{(0)} - \alpha_0 \mathbf{A}\mathbf{p}^{(0)} \right) = \mathbf{r}^{(0)T} \mathbf{r}^{(0)} - \alpha_0 \mathbf{r}^{(0)T} \mathbf{A}\mathbf{p}^{(0)}$$
    Substitute $\mathbf{p}^{(0)} = \mathbf{r}^{(0)}$ and the step size expression $\alpha_0 = \frac{\mathbf{r}^{(0)T}\mathbf{r}^{(0)}}{\mathbf{p}^{(0)T}\mathbf{A}\mathbf{p}^{(0)}}$:
    $$\mathbf{r}^{(0)T} \mathbf{r}^{(1)} = \mathbf{r}^{(0)T} \mathbf{r}^{(0)} - \left( \frac{\mathbf{r}^{(0)T}\mathbf{r}^{(0)}}{\mathbf{r}^{(0)T}\mathbf{A}\mathbf{r}^{(0)}} \right) \mathbf{r}^{(0)T}\mathbf{A}\mathbf{r}^{(0)} = \mathbf{r}^{(0)T} \mathbf{r}^{(0)} - \mathbf{r}^{(0)T} \mathbf{r}^{(0)} = 0$$
The residuals are orthogonal after the first update step.

2.  **Enforce search direction conjugacy ($\mathbf{p}^{(1)T} \mathbf{A} \mathbf{p}^{(0)} = 0$):**
    We write the next direction as $\mathbf{p}^{(1)} = \mathbf{r}^{(1)} + \beta_0 \mathbf{p}^{(0)}$. We require:
    $$\mathbf{p}^{(1)T} \mathbf{A} \mathbf{p}^{(0)} = 0 \implies \left( \mathbf{r}^{(1)} + \beta_0 \mathbf{p}^{(0)} \right)^T \mathbf{A} \mathbf{p}^{(0)} = 0 \implies \mathbf{r}^{(1)T} \mathbf{A} \mathbf{p}^{(0)} + \beta_0 \mathbf{p}^{(0)T} \mathbf{A} \mathbf{p}^{(0)} = 0$$
    Solve for the coefficient $\beta_0$:
    $$\beta_0 = -\frac{\mathbf{r}^{(1)T} \mathbf{A} \mathbf{p}^{(0)}}{\mathbf{p}^{(0)T} \mathbf{A} \mathbf{p}^{(0)}}$$

3.  **Simplify the numerator expression:**
    From $\mathbf{r}^{(1)} = \mathbf{r}^{(0)} - \alpha_0 \mathbf{A}\mathbf{p}^{(0)}$, we rearrange terms to isolate $\mathbf{A}\mathbf{p}^{(0)}$:
    $$\mathbf{A}\mathbf{p}^{(0)} = \frac{1}{\alpha_0} \left( \mathbf{r}^{(0)} - \mathbf{r}^{(1)} \right)$$
    Substitute this into the numerator of our $\beta_0$ equation:
    $$\mathbf{r}^{(1)T} \mathbf{A}\mathbf{p}^{(0)} = \frac{1}{\alpha_0} \mathbf{r}^{(1)T} \left( \mathbf{r}^{(0)} - \mathbf{r}^{(1)} \right) = \frac{1}{\alpha_0} \left( \mathbf{r}^{(1)T}\mathbf{r}^{(0)} - \mathbf{r}^{(1)T}\mathbf{r}^{(1)} \right)$$
    Since $\mathbf{r}^{(1)T}\mathbf{r}^{(0)} = 0$:
    $$\mathbf{r}^{(1)T} \mathbf{A}\mathbf{p}^{(0)} = -\frac{\mathbf{r}^{(1)T}\mathbf{r}^{(1)}}{\alpha_0}$$

4.  **Assemble the final expression for $\beta_0$:**
    $$\beta_0 = -\frac{-\mathbf{r}^{(1)T}\mathbf{r}^{(1)} / \alpha_0}{\mathbf{p}^{(0)T} \mathbf{A} \mathbf{p}^{(0)}} = \frac{\mathbf{r}^{(1)T}\mathbf{r}^{(1)}}{\alpha_0 \mathbf{p}^{(0)T} \mathbf{A} \mathbf{p}^{(0)}}$$
    Substitute $\alpha_0 \mathbf{p}^{(0)T} \mathbf{A} \mathbf{p}^{(0)} = \mathbf{r}^{(0)T} \mathbf{r}^{(0)}$ into the denominator:
    $$\beta_0 = \frac{\mathbf{r}^{(1)T}\mathbf{r}^{(1)}}{\mathbf{r}^{(0)T}\mathbf{r}^{(0)}} \quad \blacksquare$$

This unrolls the recursive definition, proving how conjugacy is preserved at each step.

---

## 4. Concrete Examples

### Example 1: 1D Linear System
Solve the system $4x = 8 \implies A = 4, b = 8$, starting from initial guess $x_0 = 0$.
1.  **Calculate initial residual and search direction:**
    $$r_0 = b - A x_0 = 8 - 4 \cdot 0 = 8 \implies p_0 = 8$$
2.  **Calculate step size:**
    $$\alpha_0 = \frac{r_0^2}{p_0 A p_0} = \frac{8^2}{8 \cdot 4 \cdot 8} = \frac{64}{256} = 0.25$$
3.  **Update parameter state:**
    $$x_1 = x_0 + \alpha_0 p_0 = 0 + 0.25 \cdot 8 = 2$$
The algorithm converges to the exact solution $x^* = 2$ in a single iteration.

### Example 2: 2D Decoupled Linear System
Solve system $\mathbf{A}\mathbf{x} = \mathbf{b}$ where $\mathbf{A} = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}$ and $\mathbf{b} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}$, starting from $\mathbf{x}^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}^T$.
1.  **Calculate initial residual and search direction:**
    $$\mathbf{r}^{(0)} = \begin{bmatrix} 2 \\ 2 \end{bmatrix} - \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix} \begin{bmatrix} 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 2 \\ 2 \end{bmatrix} \implies \mathbf{p}^{(0)} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}$$
2.  **Calculate step size:**
    $$\alpha_0 = \frac{\mathbf{r}^{(0)T}\mathbf{r}^{(0)}}{\mathbf{p}^{(0)T}\mathbf{A}\mathbf{p}^{(0)}} = \frac{2^2 + 2^2}{\begin{bmatrix} 2 & 2 \end{bmatrix} \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix} \begin{bmatrix} 2 \\ 2 \end{bmatrix}} = \frac{8}{16} = 0.5$$
3.  **Update parameter state:**
    $$\mathbf{x}^{(1)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} + 0.5 \begin{bmatrix} 2 \\ 2 \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
Since $\mathbf{A}\mathbf{x}^{(1)} = \begin{bmatrix} 2 \\ 2 \end{bmatrix} = \mathbf{b}$, the algorithm converges in a single step.

---

## 5. Applied ML Context

1.  **Hessian-Free Optimization:** Deep learning optimization methods use CG to solve the Newton step equation $\mathbf{H}\Delta \mathbf{w} = -\nabla f$ iteratively. This avoids the need to explicitly compute or store the massive Hessian matrix.
2.  **Gaussian Process Regressions:** Training GPs requires solving covariance systems $(K + \sigma^2 I)\boldsymbol{\alpha} = \mathbf{y}$. CG approximates the solution vector $\boldsymbol{\alpha}$ in $O(N^2)$ time per iteration, bypassing the expensive $O(N^3)$ matrix inversion.
3.  **Linear Support Vector Machines:** The dual optimization objectives of large-scale linear SVM classifiers are solved using CG iterations.
4.  **Graph Laplacian Label Propagation:** In semi-supervised manifold learning, CG solves the sparse linear equations used to propagate class labels across high-dimensional graph edges.
5.  **Collaborative Filtering (ALS):** In Alternating Least Squares recommender systems, CG computes user and item latent vector updates quickly when latent factor dimensions are high.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here comparing Gradient Descent and CG trajectories:
*   Draw a contour plot of a narrow 2D quadratic valley:
    *   Show concentric ellipses representing level curves of constant loss.
*   Trace two optimization paths starting from the same coordinate:
    1.  **Gradient Descent Path (zig-zagging line):** Shows updates oscillating back and forth across the steep ravine walls, taking many steps to reach the center.
    2.  **Conjugate Gradient Path (two-step line):** Shows the first step descending along one axis, and the second step pointing exactly along the conjugate axis, reaching the global minimum in exactly two steps.
*   Add a caption explaining that standard gradient descent repeats updates along previously explored directions, whereas Conjugate Gradient uses conjugate search directions to solve a $d$-dimensional system in at most $d$ steps.
