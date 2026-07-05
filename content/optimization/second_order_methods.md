---
title: "Second-Order Methods"
description: "Newton-Raphson optimization, Hessian matrices, Quasi-Newton approximations, quadratic convergence proofs, and L-BFGS algorithms."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Derivatives", "Calculus: Partial Derivatives", "Calculus: Hessian Matrix", "Linear Algebra: Matrices", "Linear Algebra: Matrix Inverse"]
---

<h1 align="center"> Chapter 93: Second-Order Methods </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Hessian Matrix ($\mathbf{H}$):** The symmetric matrix of second-order partial derivatives representing the local curvature of a multivariate function.
* **Taylor Series Expansion:** Approximating a differentiable function around a local point using a polynomial series of derivatives.

</div>

## 1. Conceptual Hook

In first-order optimization (like Gradient Descent), we treat the local loss landscape as a flat slide, using the gradient to guide our direction. While computationally cheap, this linear approximation ignores the local curvature of the surface. As a result, standard gradient descent is prone to overshooting in steep ravines and stalling on flat plains, requiring careful tuning of learning rates.

**Second-order optimization methods** (such as **Newton's Method** and **Quasi-Newton methods**) solve this by incorporating the curvature of the loss surface.

By calculating or approximating the Hessian matrix (second partial derivatives), these methods determine not only which direction is "down," but also how fast the slope is changing.

Think of this as standing in a dark valley. A first-order optimizer only feels the slope under its boots. A second-order optimizer uses the local curvature to fit a quadratic bowl to the valley. This allows it to jump directly to the bottom of the bowl in a single step, bypassing the slow, iterative steps of first-order descent.

---

## 2. Formal Definition

Let $f: \mathbb{R}^d \to \mathbb{R}$ be a twice continuously differentiable objective function. We seek to locate the local minimum $\mathbf{w}^* = \arg\min_{\mathbf{w}} f(\mathbf{w})$.

### 1. The Hessian Matrix
The Hessian matrix $\mathbf{H}(\mathbf{w}) \in \mathbb{R}^{d \times d}$ is defined as:
$$\mathbf{H}(\mathbf{w}) = \begin{bmatrix} 
\frac{\partial^2 f}{\partial w_1^2} & \frac{\partial^2 f}{\partial w_1 \partial w_2} & \dots & \frac{\partial^2 f}{\partial w_1 \partial w_d} \\
\frac{\partial^2 f}{\partial w_2 \partial w_1} & \frac{\partial^2 f}{\partial w_2^2} & \dots & \frac{\partial^2 f}{\partial w_2 \partial w_d} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^2 f}{\partial w_d \partial w_1} & \frac{\partial^2 f}{\partial w_d \partial w_2} & \dots & \frac{\partial^2 f}{\partial w_d^2}
\end{bmatrix}$$

### 2. Newton's Optimization Method
We approximate $f$ at the current point $\mathbf{w}^{(k)}$ using a second-order Taylor expansion:
$$f\left(\mathbf{w}^{(k)} + \Delta\mathbf{w}\right) \approx f\left(\mathbf{w}^{(k)}\right) + \nabla f\left(\mathbf{w}^{(k)}\right)^T \Delta\mathbf{w} + \frac{1}{2} \Delta\mathbf{w}^T \mathbf{H}\left(\mathbf{w}^{(k)}\right) \Delta\mathbf{w}$$

To minimize this quadratic approximation with respect to the step vector $\Delta\mathbf{w}$, we set the gradient of the right-hand side to zero:
$$\nabla_{\Delta\mathbf{w}} \left[ f\left(\mathbf{w}^{(k)}\right) + \nabla f\left(\mathbf{w}^{(k)}\right)^T \Delta\mathbf{w} + \frac{1}{2} \Delta\mathbf{w}^T \mathbf{H}\left(\mathbf{w}^{(k)}\right) \Delta\mathbf{w} \right] = \mathbf{0}$$
$$\nabla f\left(\mathbf{w}^{(k)}\right) + \mathbf{H}\left(\mathbf{w}^{(k)}\right) \Delta\mathbf{w} = \mathbf{0}$$

Solving for $\Delta\mathbf{w}$ yields the **Newton step**:
$$\Delta\mathbf{w} = -\mathbf{H}\left(\mathbf{w}^{(k)}\right)^{-1} \nabla f\left(\mathbf{w}^{(k)}\right)$$

The update rule is:
$$\mathbf{w}^{(k+1)} = \mathbf{w}^{(k)} - \mathbf{H}\left(\mathbf{w}^{(k)}\right)^{-1} \nabla f\left(\mathbf{w}^{(k)}\right)$$

### 3. Quasi-Newton Methods (BFGS / L-BFGS)
Computing and inverting the $d \times d$ Hessian matrix at each step is computationally expensive ($O(d^3)$ complexity). Quasi-Newton methods avoid this by maintaining a running approximation $\mathbf{B}^{(k)} \approx \mathbf{H}^{(k)}$ satisfying the **Secant Equation**:
$$\mathbf{B}^{(k+1)} \mathbf{s}^{(k)} = \mathbf{y}^{(k)}$$
where $\mathbf{s}^{(k)} = \mathbf{w}^{(k+1)} - \mathbf{w}^{(k)}$ and $\mathbf{y}^{(k)} = \nabla f\left(\mathbf{w}^{(k+1)}\right) - \nabla f\left(\mathbf{w}^{(k)}\right)$.

---

## 3. Illustrative Derivation

### Proof: Quadratic Convergence of Newton's Method
We prove that Newton's method converges quadratically to a stationary point of a twice continuously differentiable function. Let $g(w) = f'(w)$. We want to find a root $w^*$ such that $g(w^*) = 0$.

*Proof:*
The Newton update is:
$$w^{(k+1)} = w^{(k)} - \frac{g(w^{(k)})}{g'(w^{(k)})}$$
Define the parameter error at step $k$ as $e_k = w^{(k)} - w^* \implies w^{(k)} = w^* + e_k$.

1.  **Expand $g(w^*)$ around $w^{(k)}$ using Taylor's Theorem:**
    $$g(w^*) = g(w^{(k)} - e_k) = g(w^{(k)}) - e_k g'(w^{(k)}) + \frac{e_k^2}{2} g''(c_k)$$
    where $c_k$ is a point between $w^{(k)}$ and $w^*$.

2.  **Apply root condition:**
    Since $g(w^*) = 0$:
    $$0 = g(w^{(k)}) - e_k g'(w^{(k)}) + \frac{e_k^2}{2} g''(c_k)$$

3.  **Divide by $g'(w^{(k)})$ (assuming $g'(w^{(k)}) \neq 0$):**
    $$0 = \frac{g(w^{(k)})}{g'(w^{(k)})} - e_k + \frac{e_k^2}{2} \frac{g''(c_k)}{g'(w^{(k)})}$$
    Rearrange terms:
    $$e_k - \frac{g(w^{(k)})}{g'(w^{(k)})} = \frac{e_k^2}{2} \frac{g''(c_k)}{g'(w^{(k)})}$$

4.  **Relate to the next step's error:**
    Observe that the left-hand side is:
    $$e_k - \frac{g(w^{(k)})}{g'(w^{(k)})} = (w^{(k)} - w^*) - (w^{(k)} - w^{(k+1)}) = w^{(k+1)} - w^* = e_{k+1}$$
    Substitute this back:
    $$e_{k+1} = \frac{e_k^2}{2} \frac{g''(c_k)}{g'(w^{(k)})}$$

5.  **Establish convergence bound:**
    Assuming $g'(w^*) \neq 0$ and $g$ is twice continuously differentiable, there exists a constant $M > 0$ in a local neighborhood of $w^*$ such that:
    $$\left| \frac{g''(c_k)}{2 g'(w^{(k)})} \right| \le M$$
    Taking the absolute value yields:
    $$|e_{k+1}| \le M |e_k|^2 \quad \blacksquare$$
This proves that the error at step $k+1$ is bounded by the squared error of step $k$, confirming quadratic convergence.

---

## 4. Concrete Examples

### Example 1: 1D Function Minimization
We minimize the function $f(w) = w^4$ starting from $w^{(0)} = 2.0$.
1.  **Calculate derivatives:**
    $$f'(w) = 4w^3 \quad \text{and} \quad f''(w) = 12w^2$$
2.  **Evaluate at $w^{(0)} = 2.0$:**
    $$f'(2) = 4 \cdot 8 = 32 \quad \text{and} \quad f''(2) = 12 \cdot 4 = 48$$
3.  **Compute the Newton step:**
    $$\Delta w = -\frac{f'(2)}{f''(2)} = -\frac{32}{48} = -0.667$$
    $$w^{(1)} = 2.0 - 0.667 = 1.333$$

### Example 2: 2D Quadratic Minimization in a Single Step
Minimize the quadratic function $f(w_1, w_2) = w_1^2 + 10 w_2^2$ starting from $\mathbf{w}^{(0)} = [10, 10]^T$.
1.  **Calculate the Gradient and Hessian:**
    $$\nabla f = \begin{bmatrix} 2w_1 \\ 20w_2 \end{bmatrix} \implies \nabla f(\mathbf{w}^{(0)}) = \begin{bmatrix} 20 \\ 200 \end{bmatrix}$$
    $$\mathbf{H} = \begin{bmatrix} 2 & 0 \\ 0 & 20 \end{bmatrix} \implies \mathbf{H}^{-1} = \begin{bmatrix} 0.5 & 0 \\ 0 & 0.05 \end{bmatrix}$$
2.  **Compute the Newton update:**
    $$\Delta \mathbf{w} = -\mathbf{H}^{-1} \nabla f(\mathbf{w}^{(0)}) = -\begin{bmatrix} 0.5 & 0 \\ 0 & 0.05 \end{bmatrix} \begin{bmatrix} 20 \\ 200 \end{bmatrix} = \begin{bmatrix} -10 \\ -10 \end{bmatrix}$$
    $$\mathbf{w}^{(1)} = \mathbf{w}^{(0)} + \Delta \mathbf{w} = \begin{bmatrix} 10 \\ 10 \end{bmatrix} + \begin{bmatrix} -10 \\ -10 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
Because the function is quadratic, Newton's method reaches the global minimum in exactly one step.

---

## 5. Applied ML Context

1.  **Logistic Regression Training:** Newton's method (known as Iteratively Reweighted Least Squares or IRLS) is used to optimize logistic regression models because the loss function is strictly convex.
2.  **Quasi-Newton Training (L-BFGS):** Used to train Conditional Random Fields (CRFs) and linear models, approximating the inverse Hessian to save memory.
3.  **Natural Gradient Descent:** Used in reinforcement learning algorithms (like TRPO) to ensure policy updates do not change the output probability distribution too drastically, using the Fisher Information Matrix as a proxy for the Hessian.
4.  **Deep Learning Curvature Scaling:** Optimizers like AdaHessian utilize randomized approximations of the Hessian diagonal to adaptively scale learning rates for transformer models.
5.  **Recurrent Neural Networks (RNNs):** Hessian-Free optimization is used to navigate the highly non-convex, pathological curvatures of RNN loss landscapes where standard first-order methods stall.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating first-order vs. second-order approximations:
*   Draw a convex curve representing a function $f(w)$.
*   Mark a point $w^{(k)}$ on the curve.
*   Draw a straight tangent line at $w^{(k)}$ representing the first-order linear approximation. Show that it diverges from the function curve quickly.
*   Draw a parabolic curve that is tangent to $w^{(k)}$ and matches the local curvature of $f(w)$. Show that it tracks the function curve closely.
*   Draw an arrow showing the Newton step jumping directly to the vertex of the approximating parabola, illustrating why second-order updates are highly accurate.
*   Add a caption explaining that first-order methods approximate the surface as a flat plane, while second-order methods fit a quadratic bowl, allowing them to calculate the distance to the minimum.
