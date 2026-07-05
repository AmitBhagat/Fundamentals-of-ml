---
title: "Constrained Optimization (Lagrange, KKT)"
description: "Optimization under boundary limits, Lagrange multipliers, Karush-Kuhn-Tucker conditions, and complementary slackness."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Derivatives", "Calculus: Partial Derivatives", "Calculus: Gradient", "Linear Algebra: Vectors"]
---

<h1 align="center"> Chapter 85: Constrained Optimization (Lagrange, KKT) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Gradient Vector ($\nabla f$):** The vector of partial derivatives pointing along the local direction of maximum ascent.
* **Feasible Region:** The set of all parameter coordinate configurations that satisfy all constraints.

</div>

## 1. Conceptual Hook

In machine learning, we rarely optimize in a vacuum. A model that achieves perfect training accuracy by blowing its weights up to infinity is useless. We must locate the best-performing parameter configurations subject to strict physical or regularization limits—such as bounding the norm of weight parameters (regularization), limiting model memory size (pruning), or enforcing strict margins between class boundaries (Support Vector Machines).

**Constrained optimization** is the mathematical framework that handles these boundaries.

If our parameters are constrained to lie along a specific line or surface, we use the **Method of Lagrange Multipliers** for equality constraints. When the parameters are restricted to a "fenced-in" region (such as a sphere or box), we use the **Karush-Kuhn-Tucker (KKT) conditions** for inequality constraints. These conditions define the math of balancing our desire to minimize loss with the reality of our constraints.

---

## 2. Formal Definition

Consider a general constrained optimization problem:
$$\min_{\mathbf{w} \in \mathbb{R}^d} f(\mathbf{w})$$
$$\text{subject to} \quad g_i(\mathbf{w}) = 0 \quad (i=1, \dots, m)$$
$$h_j(\mathbf{w}) \le 0 \quad (j=1, \dots, p)$$
where $f$ is the objective function, $g_i$ are the equality constraints, and $h_j$ are the inequality constraints.

### The Generalized Lagrangian
To solve this system, we define the **generalized Lagrangian** function $\mathcal{L}: \mathbb{R}^d \times \mathbb{R}^m \times \mathbb{R}^p \to \mathbb{R}$ as:
$$\mathcal{L}(\mathbf{w}, \boldsymbol{\lambda}, \boldsymbol{\mu}) = f(\mathbf{w}) + \sum_{i=1}^{m} \lambda_i g_i(\mathbf{w}) + \sum_{j=1}^{p} \mu_j h_j(\mathbf{w})$$
where:
*   **$\lambda_i \in \mathbb{R}$:** The Lagrange multipliers associated with the equality constraints.
*   **$\mu_j \ge 0$:** The KKT multipliers associated with the inequality constraints.

### The KKT Optimality Conditions
If $\mathbf{w}^*$ is a local minimum of the primal problem for which the constraint functions satisfy mild regularity conditions (constraint qualifications), there exist multiplier vectors $\boldsymbol{\lambda}^*$ and $\boldsymbol{\mu}^*$ such that the following four conditions hold:

1.  **Stationarity (Lagrangian gradient vanishes):**
    $$\nabla_{\mathbf{w}} \mathcal{L}(\mathbf{w}^*, \boldsymbol{\lambda}^*, \boldsymbol{\mu}^*) = \nabla f(\mathbf{w}^*) + \sum_{i=1}^{m} \lambda_i^* \nabla g_i(\mathbf{w}^*) + \sum_{j=1}^{p} \mu_j^* \nabla h_j(\mathbf{w}^*) = \mathbf{0}$$
2.  **Primal Feasibility (constraints satisfied):**
    $$g_i(\mathbf{w}^*) = 0 \quad \forall i \in \{1, \dots, m\} \quad \text{and} \quad h_j(\mathbf{w}^*) \le 0 \quad \forall j \in \{1, \dots, p\}$$
3.  **Dual Feasibility (multipliers non-negative):**
    $$\mu_j^* \ge 0 \quad \forall j \in \{1, \dots, p\}$$
4.  **Complementary Slackness (active/inactive constraint selector):**
    $$\mu_j^* h_j(\mathbf{w}^*) = 0 \quad \forall j \in \{1, \dots, p\}$$

---

## 3. Illustrative Derivation

### Geometric Derivation of KKT Complementary Slackness
We derive why the complementary slackness condition $\mu^* h(\mathbf{w}^*) = 0$ and the non-negativity of $\mu^*$ must hold at an optimal point.

*Proof:*
Consider a single inequality constraint $h(\mathbf{w}) \le 0$. The optimal solution $\mathbf{w}^*$ must lie in one of two cases:

*   **Case 1: The constraint is inactive at the optimum ($h(\mathbf{w}^*) < 0$).**
    If $h(\mathbf{w}^*) < 0$, the optimum lies strictly in the interior of the feasible region. Small perturbations around $\mathbf{w}^*$ do not violate the constraint. The local constrained minimum must behave exactly like an unconstrained local minimum, requiring the gradient of the objective to vanish:
    $$\nabla f(\mathbf{w}^*) = \mathbf{0}$$
    Substituting this into the stationarity condition $\nabla f(\mathbf{w}^*) + \mu^* \nabla h(\mathbf{w}^*) = \mathbf{0}$ forces:
    $$\mu^* = 0$$
    Since $h(\mathbf{w}^*) < 0$ and $\mu^* = 0$, their product is zero:
    $$\mu^* h(\mathbf{w}^*) = 0$$

*   **Case 2: The constraint is active at the optimum ($h(\mathbf{w}^*) = 0$).**
    If $h(\mathbf{w}^*) = 0$, the optimum lies directly on the boundary of the feasible region. To minimize the objective function $f$, we want to move along the negative gradient direction $-\nabla f(\mathbf{w}^*)$. However, we cannot step outside the feasible region, which means we cannot step in the direction of increasing $h$ (which is $\nabla h(\mathbf{w}^*)$).
    At the optimal boundary point, the descent force $-\nabla f(\mathbf{w}^*)$ must point directly outward into the infeasible region. Mathematically, it must align with the outward normal vector of the boundary constraint, $\nabla h(\mathbf{w}^*)$.
    Thus, there must exist a positive scalar coefficient $\mu^* \ge 0$ such that:
    $$-\nabla f(\mathbf{w}^*) = \mu^* \nabla h(\mathbf{w}^*)$$
    Rearranging terms yields:
    $$\nabla f(\mathbf{w}^*) + \mu^* \nabla h(\mathbf{w}^*) = \mathbf{0} \quad \text{with} \quad \mu^* \ge 0$$
    Since the constraint is active ($h(\mathbf{w}^*) = 0$), their product is zero:
    $$\mu^* h(\mathbf{w}^*) = 0$$

Combining both cases, we conclude that $\mu^* h(\mathbf{w}^*) = 0$ must always hold. This completes the geometric proof. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Cylindrical Bottle Volume Maximization (Equality Constraint)
We maximize cylinder volume $V(r, h) = \pi r^2 h$ subject to surface area constraint $S(r, h) = 2\pi r^2 + 2\pi r h - 6\pi = 0$.
1.  **Formulate the Lagrangian (minimizing negative volume):**
    $$\mathcal{L}(r, h, \lambda) = -\pi r^2 h + \lambda(2\pi r^2 + 2\pi r h - 6\pi)$$
2.  **Apply Stationarity:**
    $$\frac{\partial \mathcal{L}}{\partial r} = -2\pi r h + \lambda(4\pi r + 2\pi h) = 0 \implies \lambda = \frac{2\pi r h}{4\pi r + 2\pi h} = \frac{r h}{2r + h}$$
    $$\frac{\partial \mathcal{L}}{\partial h} = -\pi r^2 + \lambda(2\pi r) = 0 \implies \lambda = \frac{\pi r^2}{2\pi r} = \frac{r}{2}$$
3.  **Solve for parameters:**
    Equate the expressions for $\lambda$:
    $$\frac{r h}{2r + h} = \frac{r}{2} \implies 2h = 2r + h \implies h = 2r$$
    Substitute $h = 2r$ into the constraint:
    $$2\pi r^2 + 2\pi r(2r) = 6\pi \implies 6\pi r^2 = 6\pi \implies r = 1, \quad h = 2$$

### Example 2: Weight Limit on Insulation Thickness (Inequality Constraint)
We minimize $f(x) = (x - 10)^2$ subject to $x^2 \le 16$ (which is $x^2 - 16 \le 0$).
1.  **Formulate the Lagrangian:**
    $$\mathcal{L}(x, \mu) = (x - 10)^2 + \mu(x^2 - 16)$$
2.  **Apply KKT Conditions:**
    *   **Stationarity:** $2(x - 10) + 2\mu x = 0 \implies x(1 + \mu) = 10 \implies x = \frac{10}{1 + \mu}$
    *   **Complementary Slackness:** $\mu(x^2 - 16) = 0$
3.  **Solve the system:**
    *   If $\mu = 0$, then $x = 10$. This violates primal feasibility since $10^2 = 100 \not\le 16$.
    *   Thus, we must have $\mu > 0 \implies x^2 - 16 = 0 \implies x^* = 4$ (excluding negative thickness).
    *   Substitute $x^* = 4$ into stationarity: $4(1 + \mu) = 10 \implies \mu^* = 1.5$.
Since $\mu^* = 1.5 \ge 0$, the KKT conditions are satisfied, yielding the optimal boundary thickness $x^* = 4$.

---

## 5. Applied ML Context

1.  **Support Vector Machines (SVM):** KKT conditions are used to derive maximum-margin hyperplanes. Complementary slackness guarantees that only support vectors lying directly on the margin boundary determine weight coefficients.
2.  **Regularization Bound Equivalences:** Lasso and Ridge regressions are constrained optimization problems that minimize training loss subject to norm limits on the weight vectors.
3.  **Memory-Constrained Network Pruning:** Compressing deep neural networks for deployment on edge devices by optimizing loss subject to bounds on parameter sparsity.
4.  **Wasserstein GAN Lipschitz Enforcement:** Restricting the discriminator function to be 1-Lipschitz by applying gradient penalties to stabilize adversarial training.
5.  **Hard Attention Image Selection:** Selecting localized pixel patches in computer vision models using sparsity constraints on spatial attention masks.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating KKT inequality geometry:
*   Draw a 2D contour map of an objective function $f(w_1, w_2)$ represented by concentric ellipses.
*   Draw a curved boundary line representing the inequality constraint $h(w_1, w_2) = 0$. Shade the interior region as the **Feasible Region**.
*   Show the unconstrained minimum lying in the infeasible region.
*   Mark the constrained optimal point $\mathbf{w}^*$ on the boundary line.
*   Draw the objective descent vector $-\nabla f(\mathbf{w}^*)$ pointing outward across the boundary.
*   Draw the constraint normal vector $\nabla h(\mathbf{w}^*)$ pointing outward from the feasible region.
*   Show that these two vectors point in opposite directions along the same line, visually explaining why their sum vanishes under a positive multiplier $\mu^*$: $\nabla f + \mu^* \nabla h = \mathbf{0}$.
*   Add a caption explaining that at the constrained boundary optimum, the objective's desire to descend is directly balanced by the constraint's pushback force, aligning their gradients.
