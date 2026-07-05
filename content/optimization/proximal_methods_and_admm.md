---
title: "Proximal Methods and ADMM"
description: "Non-smooth optimization, proximal operators, augmented Lagrangians, Soft-Thresholding derivations, and ADMM consensus algorithms."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Derivatives", "Optimization: Gradient Descent", "Optimization: Constrained Optimization (Lagrange, KKT)"]
---

<h1 align="center"> Chapter 91: Proximal Methods and ADMM </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Subgradient Calculus:** The generalization of derivatives to non-differentiable convex functions, defining a set of slopes at "kink" points.
* **Augmented Lagrangian:** A Lagrangian function modified with a quadratic penalty term of the equality constraints to improve convergence stability.

</div>

## 1. Conceptual Hook

In machine learning, we frequently encounter objective functions that are composite: they consist of a smooth, differentiable term (like a training loss function) and a non-smooth, non-differentiable term (like an $L_1$ regularization penalty or constraint indicator functions). Standard gradient descent fails here because derivatives do not exist at the "kinks" or boundary edges of these non-smooth terms.

**Proximal methods** solve this by introducing the **proximal operator**, which acts as a mathematical projection step.

Instead of taking a standard step that breaks on the kinks, we take a smooth gradient step and then use the proximal operator to "project" the parameters back into a stable, regularized state.

The **Alternating Direction Method of Multipliers (ADMM)** scales this up: it splits a complex, multi-objective problem into simpler sub-problems that are updated alternately, allowing us to solve massive, distributed optimization tasks with ease.

---

## 2. Formal Definition

### 1. The Proximal Operator
Let $h: \mathbb{R}^d \to \mathbb{R} \cup \{+\infty\}$ be a closed, proper, convex function. For a parameter $\rho > 0$, the proximal operator $\text{prox}_{\rho h}: \mathbb{R}^d \to \mathbb{R}^d$ is defined as:
$$\text{prox}_{\rho h}(\mathbf{v}) = \arg\min_{\mathbf{x} \in \mathbb{R}^d} \left( h(\mathbf{x}) + \frac{1}{2\rho} \|\mathbf{x} - \mathbf{v}\|_2^2 \right)$$

The proximal operator finds a point $\mathbf{x}$ that balances minimizing the non-smooth function $h(\mathbf{x})$ with staying close to the input vector $\mathbf{v}$.

### 2. Proximal Gradient Descent
To minimize an objective of the form $F(\mathbf{w}) = f(\mathbf{w}) + g(\mathbf{w})$, where $f$ is convex and differentiable, and $g$ is convex but non-differentiable, the update step is:
$$\mathbf{w}^{(t+1)} = \text{prox}_{\eta g}\left( \mathbf{w}^{(t)} - \eta \nabla f\left(\mathbf{w}^{(t)}\right) \right)$$
where $\eta > 0$ is the step size.

### 3. Alternating Direction Method of Multipliers (ADMM)
ADMM solves optimization problems with split variables under linear equality constraints:
$$\min_{\mathbf{x} \in \mathbb{R}^n, \mathbf{z} \in \mathbb{R}^m} f(\mathbf{x}) + g(\mathbf{z}) \quad \text{subject to} \quad \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{z} = \mathbf{c}$$

We construct the **Augmented Lagrangian** with penalty parameter $\rho > 0$:
$$\mathcal{L}_{\rho}(\mathbf{x}, \mathbf{z}, \mathbf{y}) = f(\mathbf{x}) + g(\mathbf{z}) + \mathbf{y}^T\left(\mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{z} - \mathbf{c}\right) + \frac{\rho}{2}\|\mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{z} - \mathbf{c}\|_2^2$$
where $\mathbf{y} \in \mathbb{R}^k$ is the Lagrange multiplier vector.

The ADMM algorithm alternates updates of the primal and dual variables:
1.  **Primal $\mathbf{x}$ Minimization:**
    $$\mathbf{x}^{(k+1)} = \arg\min_{\mathbf{x}} \mathcal{L}_{\rho}\left(\mathbf{x}, \mathbf{z}^{(k)}, \mathbf{y}^{(k)}\right)$$
2.  **Primal $\mathbf{z}$ Minimization:**
    $$\mathbf{z}^{(k+1)} = \arg\min_{\mathbf{z}} \mathcal{L}_{\rho}\left(\mathbf{x}^{(k+1)}, \mathbf{z}, \mathbf{y}^{(k)}\right)$$
3.  **Dual $\mathbf{y}$ Update:**
    $$\mathbf{y}^{(k+1)} = \mathbf{y}^{(k)} + \rho\left(\mathbf{A}\mathbf{x}^{(k+1)} + \mathbf{B}\mathbf{z}^{(k+1)} - \mathbf{c}\right)$$

---

## 3. Illustrative Derivation

### Derivation of the Soft-Thresholding Operator
We derive the closed-form analytical proximal operator for the $L_1$ norm function $h(x) = \lambda |x|$ in 1D.

*Proof:*
We solve:
$$\text{prox}_{\rho h}(v) = \arg\min_{x \in \mathbb{R}} \left( \lambda |x| + \frac{1}{2\rho} (x - v)^2 \right)$$
Let $F(x) = \lambda |x| + \frac{1}{2\rho}(x - v)^2$. Since $F(x)$ is convex but non-differentiable at $x = 0$, we find its minimum using subgradient optimality:
$$0 \in \partial F(x^*)$$
$$0 \in \lambda \partial |x^*| + \frac{1}{\rho}(x^* - v)$$
where the subdifferential of the absolute value function is:
$$\partial |x| = \begin{cases} \{1\} & \text{if } x > 0 \\ \{-1\} & \text{if } x < 0 \\ [-1, 1] & \text{if } x = 0 \end{cases}$$

We solve for $x^*$ in three cases:
1.  **Case 1: $x^* > 0$**
    $$\lambda + \frac{1}{\rho}(x^* - v) = 0 \implies x^* = v - \lambda\rho$$
    For this solution to satisfy $x^* > 0$, we must have:
    $$v - \lambda\rho > 0 \implies v > \lambda\rho$$

2.  **Case 2: $x^* < 0$**
    $$-\lambda + \frac{1}{\rho}(x^* - v) = 0 \implies x^* = v + \lambda\rho$$
    For this solution to satisfy $x^* < 0$, we must have:
    $$v + \lambda\rho < 0 \implies v < -\lambda\rho$$

3.  **Case 3: $x^* = 0$**
    Substitute $x^* = 0$ into the subgradient inclusion:
    $$0 \in \lambda [-1, 1] - \frac{v}{\rho} \implies \frac{v}{\rho} \in [-\lambda, \lambda] \implies |v| \le \lambda\rho$$

Combining the three cases yields the **Soft-Thresholding Operator** $\mathcal{S}_{\lambda\rho}(v)$:
$$\text{prox}_{\rho h}(v) = \mathcal{S}_{\lambda\rho}(v) = \begin{cases} v - \lambda\rho & \text{if } v > \lambda\rho \\ 0 & \text{if } |v| \le \lambda\rho \\ v + \lambda\rho & \text{if } v < -\lambda\rho \end{cases} = \text{sgn}(v) \max(0, \quad |v| - \lambda\rho) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Indicator Function Projection
Let the constraint set be $\mathcal{C} = \{140\}$ (face shape constraint). The penalty function is the indicator function $h(x) = \mathcal{I}_{\mathcal{C}}(x)$ ($0$ if $x = 140$, $\infty$ otherwise). Find $\text{prox}_{h}(150)$ for $\rho = 1$.
1.  **Formulate the minimization:**
    $$\text{prox}_{h}(150) = \arg\min_{x \in \mathbb{R}} \left( \mathcal{I}_{\mathcal{C}}(x) + \frac{1}{2} (x - 150)^2 \right)$$
2.  **Determine the minimum:**
    Since $\mathcal{I}_{\mathcal{C}}(x)$ is infinite for any $x \neq 140$, the only feasible coordinate is $x = 140$, giving:
    $$\text{prox}_{h}(150) = 140$$
The proximal operator acts as a direct projection mapping.

### Example 2: L1 Norm Soft-Thresholding
We apply soft-thresholding to an input vector coordinate $v = 10.0$ under regularization penalty parameter $\lambda = 2.0$ and $\rho = 1.0$.
1.  **Evaluate threshold boundary:**
    $$\text{Threshold} = \lambda\rho = 2.0 \cdot 1.0 = 2.0$$
2.  **Calculate update:**
    $$x^* = \text{sgn}(10.0) \max(0, \quad |10.0| - 2.0) = 1.0 \cdot 8.0 = 8.0$$
The input is shrunk toward zero by $2.0$ units.

---

## 5. Applied ML Context

1.  **Lasso Regression (L1 Regularization):** Proximal Gradient Descent (ISTA) uses the soft-thresholding operator to optimize losses with non-differentiable $L_1$ norms.
2.  **Total Variation (TV) Image Denoising:** ADMM solves the ROF denoising model by separating the $L_2$ data fidelity term from the non-smooth $L_1$ derivative-based smoothing constraints.
3.  **Consensus Distributed Training:** ADMM splits training across multiple nodes. Each node optimizes local weights (local primal updates), and a central server updates dual variables to force agreement.
4.  **Matrix Completion Recommenders:** Solving low-rank matrix recovery by splitting the objective into observed rating matching and nuclear norm singular value thresholding.
5.  **Decentralized SVM Optimization:** ADMM trains Support Vector Machines across decentralized databases where aggregating data in one location is restricted.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating proximal mapping and ADMM updates:
*   Draw a block flow diagram:
    *   **Smooth Gradient Step:** Shows parameters updated along a smooth trajectory $f(\mathbf{w})$.
    *   **Proximal Operator Box:** Shows the tentative parameters projected back onto constraint sets or shrunk toward zero via soft-thresholding.
*   For ADMM:
    *   Draw two parallel loops representing alternating updates for $\mathbf{x}$ and $\mathbf{z}$.
    *   Show both loops feeding into a central consensus node updated by the dual variable $\mathbf{y}$, illustrating how the variables negotiate to satisfy the constraints.
*   Add a caption explaining that proximal methods decouple optimization into a smooth gradient phase and a non-smooth correction phase, allowing models to handle non-differentiable boundaries.
