---
title: "Convex Optimization and Duality"
description: "Lagrange duality, KKT optimality conditions, and the dual formulation of Support Vector Machines."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Multivariate Calculus", "Linear Algebra", "Positive Definiteness"]
---

<h1 align="center"> Chapter 86: Convex Optimization </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Multivariate Calculus:** Directional derivatives, gradients $\nabla f(x)$, and Hessian matrices $\nabla^2 f(x)$.
* **Symmetric Matrices:** Understanding positive semi-definite (PSD) operators.
* **Set Theory:** Distinguishing between convex and non-convex sets.

</div>

## 1. Conceptual Hook

In machine learning, training a model is essentially an optimization task. We want to find the parameter configuration that minimizes prediction error. However, optimization landscapes are often treacherous—filled with false valleys (local minima), flat plains (saddle points), and steep cliffs. If we start in the wrong spot, gradient descent can easily get stuck. Convex optimization is the gold standard because it deals with a highly cooperative geometry.

Think of convex optimization as finding the absolute lowest spot on a tightly stretched trampoline.

No matter where you place a marble on the trampoline, it will roll smoothly along the slope and settle at the exact spot where the bowling ball rests. There are no ridges or false bottoms to trap it. This trampoline is a **convex objective function**, and the bowling ball's resting spot is the **global minimum**.

If we place wooden planks under the trampoline (representing **constraints**), the marble will roll to the lowest allowed point resting against the planks. The mathematics of locating this constrained optimal point is governed by **Lagrange Duality** and the **Karush-Kuhn-Tucker (KKT) conditions**.

---

## 2. Formal Definition

### Convex Sets and Functions
A set $\mathcal{C} \subseteq \mathbb{R}^n$ is **convex** if for all $x, y \in \mathcal{C}$ and any $\theta \in [0, 1]$:
$$\theta x + (1 - \theta)y \in \mathcal{C}$$

A function $f: \mathcal{C} \to \mathbb{R}$ is **convex** if its domain $\mathcal{C}$ is a convex set and for all $x, y \in \mathcal{C}$ and $\theta \in [0, 1]$:
$$f(\theta x + (1 - \theta)y) \le \theta f(x) + (1 - \theta)f(y)$$

If $f$ is twice continuously differentiable, convexity is equivalent to its Hessian matrix $\nabla^2 f(x)$ being positive semi-definite (PSD) for all $x \in \mathcal{C}$:
$$\mathbf{v}^T \nabla^2 f(x) \mathbf{v} \ge 0 \quad \forall \mathbf{v} \in \mathbb{R}^n$$

### General Constrained Optimization
Consider the primal optimization problem:
$$\min_{x \in \mathbb{R}^n} f_0(x) \quad \text{subject to} \quad f_i(x) \le 0 \quad (i=1, \dots, m), \quad h_j(x) = 0 \quad (j=1, \dots, r)$$

We define the **Lagrangian** $\mathcal{L}: \mathbb{R}^n \times \mathbb{R}^m \times \mathbb{R}^r \to \mathbb{R}$ as:
$$\mathcal{L}(x, \lambda, \nu) = f_0(x) + \sum_{i=1}^m \lambda_i f_i(x) + \sum_{j=1}^r \nu_j h_j(x)$$
where $\lambda_i \ge 0$ are the Lagrange multipliers for the inequality constraints, and $\nu_j \in \mathbb{R}$ are the multipliers for the equality constraints.

The **Lagrange Dual Function** $g: \mathbb{R}^m \times \mathbb{R}^r \to \mathbb{R}$ is:
$$g(\lambda, \nu) = \inf_{x \in \mathbb{R}^n} \mathcal{L}(x, \lambda, \nu)$$

The **dual optimization problem** is:
$$\max_{\lambda, \nu} g(\lambda, \nu) \quad \text{subject to} \quad \lambda \ge 0$$

### Weak and Strong Duality
Let $p^*$ be the primal optimal value, and $d^*$ be the dual optimal value. **Weak duality** always holds: $d^* \le p^*$. Under **Slater's Constraint Qualification** (if the primal is convex and there exists a strictly feasible point), **strong duality** holds: $d^* = p^*$.

### Karush-Kuhn-Tucker (KKT) Conditions
For any optimization problem where strong duality holds, any primal-dual optimal pair $(x^*, \lambda^*, \nu^*)$ must satisfy the **KKT conditions**:
1.  **Primal Feasibility:** $f_i(x^*) \le 0 \; \forall i$, and $h_j(x^*) = 0 \; \forall j$.
2.  **Dual Feasibility:** $\lambda_i^* \ge 0 \; \forall i$.
3.  **Complementary Slackness:** $\lambda_i^* f_i(x^*) = 0 \; \forall i$.
4.  **Stationarity:**
    $$\nabla_x \mathcal{L}(x^*, \lambda^*, \nu^*) = \nabla f_0(x^*) + \sum_{i=1}^m \lambda_i^* \nabla f_i(x^*) + \sum_{j=1}^r \nu_j^* \nabla h_j(x^*) = \mathbf{0}$$

---

## 3. Illustrative Derivation

### Dual Formulation of Soft-Margin SVM
We derive the dual optimization problem for the soft-margin Support Vector Machine classifier.

Primal problem:
$$\min_{w, b, \xi} \frac{1}{2} \|w\|_2^2 + C \sum_{i=1}^N \xi_i$$
$$\text{subject to} \quad 1 - \xi_i - y_i (w^T \phi(x_i) + b) \le 0 \quad \text{and} \quad -\xi_i \le 0 \quad (i=1, \dots, N)$$

*Proof:*
1.  **Formulate the Lagrangian:**
    Introduce Lagrange multipliers $\alpha_i \ge 0$ and $r_i \ge 0$:
    $$\mathcal{L}(w, b, \xi, \alpha, r) = \frac{1}{2} w^T w + C \sum_{i=1}^N \xi_i + \sum_{i=1}^N \alpha_i \left( 1 - \xi_i - y_i (w^T \phi(x_i) + b) \right) - \sum_{i=1}^N r_i \xi_i$$

2.  **Apply Stationarity (minimize over primal variables):**
    *   **With respect to $w$:**
        $$\nabla_w \mathcal{L} = w - \sum_{i=1}^N \alpha_i y_i \phi(x_i) = \mathbf{0} \implies w^* = \sum_{i=1}^N \alpha_i y_i \phi(x_i)$$
    *   **With respect to $b$:**
        $$\frac{\partial \mathcal{L}}{\partial b} = -\sum_{i=1}^N \alpha_i y_i = 0 \implies \sum_{i=1}^N \alpha_i y_i = 0$$
    *   **With respect to slack variables $\xi_i$:**
        $$\frac{\partial \mathcal{L}}{\partial \xi_i} = C - \alpha_i - r_i = 0 \implies \alpha_i + r_i = C$$
        Since $r_i \ge 0$, this implies $0 \le \alpha_i \le C$.

3.  **Substitute back to form the Dual Objective:**
    Substitute $w^*$ and the relations into the Lagrangian. The $b$ term vanishes because $\sum \alpha_i y_i = 0$. The slack terms cancel because $(C - \alpha_i - r_i)\xi_i = 0$:
    $$\mathcal{L} = \frac{1}{2} \left( \sum_{i=1}^N \alpha_i y_i \phi(x_i) \right)^T \left( \sum_{j=1}^N \alpha_j y_j \phi(x_j) \right) + \sum_{i=1}^N \alpha_i - \sum_{i=1}^N \alpha_i y_i \left( \sum_{j=1}^N \alpha_j y_j \phi(x_j) \right)^T \phi(x_i)$$
    $$\mathcal{L} = \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i=1}^N \sum_{j=1}^N \alpha_i \alpha_j y_i y_j K(x_i, x_j)$$
    where $K(x_i, x_j) = \phi(x_i)^T \phi(x_j)$ is the kernel function.

4.  **Formulate the final Dual problem:**
    $$\max_{\alpha} \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i=1}^N \sum_{j=1}^N \alpha_i \alpha_j y_i y_j K(x_i, x_j)$$
    $$\text{subject to} \quad 0 \le \alpha_i \le C \quad (i=1, \dots, N) \quad \text{and} \quad \sum_{i=1}^N \alpha_i y_i = 0 \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Convex Equality-Constrained Optimization
Minimize $f(x, y) = x^2 + y^2$ subject to $x + y = 10$.
1.  **Formulate the Lagrangian:**
    $$\mathcal{L}(x, y, \nu) = x^2 + y^2 + \nu(x + y - 10)$$
2.  **Calculate gradients (Stationarity):**
    $$\frac{\partial \mathcal{L}}{\partial x} = 2x + \nu = 0 \implies x = -\frac{\nu}{2}$$
    $$\frac{\partial \mathcal{L}}{\partial y} = 2y + \nu = 0 \implies y = -\frac{\nu}{2}$$
3.  **Enforce Primal Feasibility:**
    $$x + y = 10 \implies -\frac{\nu}{2} - \frac{\nu}{2} = 10 \implies \nu^* = -10$$
    Substituting back yields the unique global minimum:
    $$x^* = 5, \quad y^* = 5$$

### Example 2: Inequality-Constrained KKT Verification
Minimize $f(x) = x^2$ subject to $x \ge 2$ (which is $2 - x \le 0$).
1.  **Formulate the Lagrangian:**
    $$\mathcal{L}(x, \lambda) = x^2 + \lambda(2 - x)$$
2.  **Apply KKT Conditions:**
    *   **Stationarity:** $2x - \lambda = 0 \implies \lambda = 2x$
    *   **Complementary Slackness:** $\lambda(2 - x) = 0$
3.  **Solve the system:**
    *   If $\lambda = 0$, then $x = 0$. However, this violates primal feasibility ($x \ge 2$).
    *   Therefore, we must have $\lambda > 0$, which implies $2 - x = 0 \implies x^* = 2$.
    *   Substituting $x^* = 2$ into stationarity: $\lambda^* = 2(2) = 4$.
Since $\lambda^* = 4 \ge 0$, dual feasibility is satisfied. The optimal constrained solution is $x^* = 2$.

---

## 5. Applied ML Context

1.  **Support Vector Machines (SVM):** The dual representation allows classifying non-linear boundaries via kernels. Complementary slackness guarantees that only points lying on or violating margins (support vectors) have non-zero weights $\alpha_i^* > 0$.
2.  **LASSO Sparsity (L1 Regularization):** The L1 weight penalty is convex but non-differentiable at zero. Convex analysis and proximal operators are used to solve this, yielding sparse feature selections.
3.  **Logistic Regression Duality:** Minimizing binary cross-entropy loss is the direct dual problem of maximizing entropy under expectation constraints, ensuring both models converge to the same distribution.
4.  **Manifold Learning Semidefinite Programming:** Algorithms like Maximum Variance Unfolding (MVU) flatten high-dimensional manifolds while preserving local distances by solving semidefinite convex constraints.
5.  **Matrix Completion (Collaborative Filtering):** Reconstructing sparse ratings matrices is solved via convex relaxations that minimize the nuclear norm (sum of singular values) of the matrix.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating constrained convex optimization geometry:
*   Draw a 2D contour plot of a convex paraboloid bowl $f(x, y) = x^2 + y^2$ represented by concentric circles.
*   Draw a straight line representing the boundary constraint $x + y = 10$. Shade the disallowed region ($x+y < 10$ or similar depending on boundary).
*   Show that the unconstrained minimum lies at $(0, 0)$ (the center of the circles).
*   Show that the constrained minimum lies at $(5, 5)$, which is the tangent point where the circular contour line touches the straight constraint boundary.
*   Draw gradient vectors $\nabla f(x^*, y^*)$ and the constraint normal $\nabla h(x^*, y^*)$ at the tangent point. Show that they point in opposite directions along the same line, visually proving the stationarity KKT condition: $\nabla f + \nu \nabla h = \mathbf{0}$.
*   Add a caption explaining that the constrained minimum always occurs where the objective contour lines are perfectly parallel (tangent) to the active constraint boundaries, aligning their gradient vectors.
