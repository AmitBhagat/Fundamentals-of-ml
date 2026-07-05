---
title: "Critical Points"
description: "Gradient vanishing criteria, classification of stationary points, Lagrange multipliers, and saddle point geometry."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Matrices", "Partial Derivatives", "Gradient", "Hessian Matrix"]
---

<h1 align="center"> Chapter 32: Critical Points </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Gradient Vector:** Understanding that $\nabla f(x) = \mathbf{0}$ represents a flat local slope.
* **Hessian Matrix:** Knowing how second-order derivatives define local curvature.

</div>

## 1. Conceptual Hook

When training a machine learning model, our goal is to find the parameter settings that produce the lowest possible error on our task. We do this by adjusting weights to slide down the loss landscape. But how do we know when we have reached the bottom? How do we identify the potential endpoints of our optimization process? We look for **critical points**.

A critical point is any coordinate in the parameter space where the gradient of the function is exactly zero: $\nabla f(x) = \mathbf{0}$. At these locations, the local surface is temporarily flat, meaning that small steps in any direction yield no immediate change in the output. These points represent the mathematical junctions of optimization: they are the candidates for local minima (the valleys we want), local maxima (the peaks we avoid), and saddle points (deceptive flat zones). Identifying and classifying these points is essential to understanding whether our models have successfully converged.

---

## 2. Formal Definition

Let $f: U \to \mathbb{R}$ be a scalar-valued function defined on an open set $U \subseteq \mathbb{R}^n$. A point $x^* \in U$ is defined as a **critical point** (or stationary point) of $f$ if:
1.  The gradient of $f$ at $x^*$ is the zero vector:
    $$\nabla f(x^*) = \mathbf{0}$$
    which implies that all first-order partial derivatives vanish simultaneously:
    $$\frac{\partial f}{\partial x_i}(x^*) = 0 \quad \forall i = 1, 2, \dots, n$$
2.  Or if the function $f$ is not differentiable at $x^*$.

### Classification via the Hessian
If $f$ is twice-differentiable at a critical point $x^*$ where $\nabla f(x^*) = \mathbf{0}$, we can classify the point using the eigenvalues of the Hessian matrix $H_f(x^*)$:
*   **Local Minimum:** $H_f(x^*) \succ 0$ (positive definite, all eigenvalues $\lambda_i > 0$).
*   **Local Maximum:** $H_f(x^*) \prec 0$ (negative definite, all eigenvalues $\lambda_i < 0$).
*   **Saddle Point:** $H_f(x^*)$ is indefinite (has both positive and negative eigenvalues).

---

## 3. Illustrative Derivation

### Derivation of the Lagrange Multiplier Method
In machine learning, we often optimize objectives under constraints (for example, keeping weight vectors unit norm, or bounding margins in SVMs). We derive how critical points are identified in constrained systems using the **Method of Lagrange Multipliers**.

Suppose we want to find the critical points of a function $f(x)$ subject to an equality constraint $g(x) = c$, where $f, g: \mathbb{R}^n \to \mathbb{R}$ are differentiable.

*Proof:*
1.  **Geometric Tangency Condition:**
    At a constrained optimum $x^*$, the contour curve of $f(x)$ must be tangent to the constraint curve $g(x) = c$. If they were not tangent, they would cross, meaning we could move along the constraint curve to increase or decrease $f(x)$.
2.  **Collinearity of Gradients:**
    Since the contours are tangent at $x^*$, their normal vectors must point in the same (or exact opposite) direction. The gradient vector is always orthogonal to its contour lines. Therefore, the gradient of the objective $\nabla f(x^*)$ and the gradient of the constraint $\nabla g(x^*)$ must be collinear:
    $$\nabla f(x^*) = \lambda \nabla g(x^*)$$
    where $\lambda \in \mathbb{R}$ is the scaling factor, known as the **Lagrange multiplier**.

3.  **The Lagrangian Function:**
    We can unify this collinearity condition and the constraint equation into a single unconstrained function called the **Lagrangian**, $\mathcal{L}: \mathbb{R}^n \times \mathbb{R} \to \mathbb{R}$:
    $$\mathcal{L}(x, \lambda) = f(x) - \lambda(g(x) - c)$$
4.  **Finding Critical Points of $\mathcal{L}$:**
    We find the critical points of this unconstrained function by setting its gradient with respect to both $x$ and $\lambda$ to zero:
    *   Gradient w.r.t $x$:
        $$\nabla_x \mathcal{L}(x, \lambda) = \nabla f(x) - \lambda \nabla g(x) = \mathbf{0} \implies \nabla f(x) = \lambda \nabla g(x)$$
    *   Partial derivative w.r.t $\lambda$:
        $$\frac{\partial \mathcal{L}}{\partial \lambda} = -(g(x) - c) = 0 \implies g(x) = c$$
Solving this system of equations yields the critical points of the constrained system. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Unconstrained Local Minimum
Find and classify the critical points of the function $f(x, y) = x^2 + 2y^2 - 4x - 8y + 6$.
1.  **Find the Gradient:**
    $$\nabla f(x, y) = \begin{bmatrix} 2x - 4 \\ 4y - 8 \end{bmatrix}$$
2.  **Set the Gradient to zero:**
    $$2x - 4 = 0 \implies x = 2$$
    $$4y - 8 = 0 \implies y = 2$$
    The only critical point is $x^* = (2, 2)$.
3.  **Compute the Hessian:**
    $$H_f(x, y) = \begin{pmatrix} \frac{\partial^2 f}{\partial x^2} & \frac{\partial^2 f}{\partial x \partial y} \\ \frac{\partial^2 f}{\partial y \partial x} & \frac{\partial^2 f}{\partial y^2} \end{pmatrix} = \begin{pmatrix} 2 & 0 \\ 0 & 4 \end{pmatrix}$$
4.  **Evaluate at $x^*$:**
    $H_f(2, 2) = \begin{pmatrix} 2 & 0 \\ 0 & 4 \end{pmatrix}$. The eigenvalues are $\lambda_1 = 2$ and $\lambda_2 = 4$.
    Since both eigenvalues are strictly positive, the Hessian is positive definite, confirming $(2, 2)$ is a strict local minimum.

### Example 2: Constrained Minimization
Minimize the objective function $f(x, y) = x^2 + y^2$ subject to the equality constraint $x + y = 2$.
1.  **Formulate the Lagrangian:**
    $$\mathcal{L}(x, y, \lambda) = x^2 + y^2 - \lambda(x + y - 2)$$
2.  **Find the partial derivatives and set to zero:**
    $$\frac{\partial \mathcal{L}}{\partial x} = 2x - \lambda = 0 \implies x = \frac{\lambda}{2}$$
    $$\frac{\partial \mathcal{L}}{\partial y} = 2y - \lambda = 0 \implies y = \frac{\lambda}{2}$$
    $$\frac{\partial \mathcal{L}}{\partial \lambda} = -(x + y - 2) = 0 \implies x + y = 2$$
3.  **Solve the system:**
    Substitute $x$ and $y$ expressions into the constraint:
    $$\frac{\lambda}{2} + \frac{\lambda}{2} = 2 \implies \lambda = 2$$
    $$\implies x = 1, \quad y = 1$$
The constrained critical point is at $(1, 1)$ with a minimum value of $f(1, 1) = 2$.

---

## 5. Applied ML Context

1.  **SGD Convergence Limits:** First-order optimizers (like SGD) iteratively update network parameters to find coordinates where the gradient of the loss function vanishes: $\nabla L(\theta) \approx \mathbf{0}$, indicating convergence at a critical point.
2.  **Ordinary Least Squares (OLS) Solution:** In linear regression, we solve for parameters by setting the gradient of the sum of squared residuals to zero: $\nabla_{\mathbf{w}} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 = \mathbf{0}$. This leads to the normal equations: $\mathbf{X}^T \mathbf{X} \mathbf{w} = \mathbf{X}^T \mathbf{y}$.
3.  **Saddle Point Bottlenecks:** In deep learning, the vast majority of high-dimensional critical points are saddle points rather than local minima. Optimizers like Adam introduce momentum to "roll through" these flat regions where standard gradient descent stalls.
4.  **Support Vector Machines (SVMs):** Setting up the optimal separating hyperplane under margin constraints requires solving a dual Lagrangian objective. The support vectors correspond to the critical points of this constrained quadratic program.
5.  **Principal Component Analysis (PCA):** Finding principal components involves maximizing variance subject to weight vector orthnormal constraints. The eigenvectors of the covariance matrix are the critical points of this constrained Lagrangian formulation.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the three types of critical points:
*   Show three side-by-side 3D plots:
    1.  **Local Minimum:** A smooth bowl shape. Draw a flat tangent plane touching the very bottom. Label the gradient as $\nabla f = \mathbf{0}$ and indicate the curvature is positive upwards in all directions ($H \succ 0$).
    2.  **Local Maximum:** A smooth dome shape. Draw a flat tangent plane touching the peak. Label the gradient as $\nabla f = \mathbf{0}$ and indicate the curvature is negative downwards in all directions ($H \prec 0$).
    3.  **Saddle Point:** A classic horse-saddle shape. Draw a flat tangent plane touching the center. Label the gradient as $\nabla f = \mathbf{0}$. Draw a green line curving upwards along one axis (positive eigenvalue) and a red line curving downwards along the other axis (negative eigenvalue).
*   Use this visualization to emphasize that a zero gradient alone is not enough to identify a minimum; we must check the second-order curvature.
