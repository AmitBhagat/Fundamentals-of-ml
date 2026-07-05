---
title: "Partial Derivatives"
description: "Coordinate-wise rates of change, differentiability, Clairaut's theorem proof, and mixed partials."
complexity: "Advanced"
estimated_time: "45 min"
prerequisites: ["Scalars", "Vectors", "Derivatives"]
---

<h1 align="center"> Chapter 38: Partial Derivatives </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Single-Variable Derivatives:** Knowing how to compute instantaneous rates of change for $f(x)$.
* **Multivariable Functions:** Familiarity with functions of the form $f(x, y, z, \dots)$.

</div>

## 1. Conceptual Hook

In machine learning, we are rarely optimized by a single parameter. A neural network's loss function is determined by millions of weights and biases simultaneously. To minimize this loss, we cannot just tweak all parameters blindly. We need to isolate the influence of each individual weight. The mathematical tool that performs this isolation is the **partial derivative**.

A partial derivative allows us to freeze the rest of the world. It evaluates the sensitivity of a multivariable function to one specific variable while holding all other variables constant. It is the mathematical equivalent of looking at a complex model and asking: _"If I keep every other weight and bias in the network exactly the same, but I increase this single weight by a tiny fraction, how much does the final loss change?"_ By calculating these coordinate-wise sensitivities, we can decide how to update every parameter in our model.

---

## 2. Formal Definition

Let $f: U \to \mathbb{R}$ be a scalar-valued function defined on an open set $U \subseteq \mathbb{R}^n$. The **partial derivative** of $f$ with respect to the $i$-th coordinate variable $x_i$ at a point $a = (a_1, a_2, \dots, a_n) \in U$ is defined as the limit:
$$\frac{\partial f}{\partial x_i}(a) = \lim_{h \to 0} \frac{f(a_1, \dots, a_i + h, \dots, a_n) - f(a_1, \dots, a_n)}{h}$$
if the limit exists.

Other common notations for $\frac{\partial f}{\partial x_i}(a)$ include $\partial_{x_i} f(a)$, $f_{x_i}(a)$, and $D_i f(a)$.

### Multivariable Differentiability
The existence of all partial derivatives at a point $a$ is a *necessary* but *not sufficient* condition for a multivariable function to be differentiable at $a$. For a function to be differentiable in the multivariable sense, it must be locally approximable by a linear map (the total derivative). A sufficient condition for differentiability at $a$ is that all first-order partial derivatives exist in an open neighborhood around $a$ and are continuous at $a$.

---

## 3. Illustrative Derivation

### Proof of Clairaut's Theorem (Symmetry of Mixed Partials)
In machine learning optimization, we frequently calculate second-order derivatives (Hessian matrices). We prove that under continuity conditions, the order of differentiation does not matter: the mixed partial derivatives are symmetric.

**Theorem (Clairaut's/Schwarz's Theorem):** Let $f: U \to \mathbb{R}$ be defined on an open set $U \subseteq \mathbb{R}^2$. If the partial derivatives $\frac{\partial f}{\partial x}$, $\frac{\partial f}{\partial y}$, $\frac{\partial^2 f}{\partial x \partial y}$, and $\frac{\partial^2 f}{\partial y \partial x}$ exist and are continuous on $U$, then for any $(x, y) \in U$:
$$\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$$

*Proof:*
For fixed, sufficiently small increments $h, k \in \mathbb{R}$, define the double difference operator $\Delta(h, k)$ as:
$$\Delta(h, k) = f(x+h, y+k) - f(x+h, y) - f(x, y+k) + f(x, y)$$

1.  **First MVT Application (w.r.t $x$):**
    Define a single-variable auxiliary function $g(u) = f(u, y+k) - f(u, y)$. Then:
    $$\Delta(h, k) = g(x+h) - g(x)$$
    Since $f$ has continuous partial derivatives, $g$ is differentiable on $[x, x+h]$. By the Mean Value Theorem (MVT):
    $$\Delta(h, k) = h \cdot g'(c) = h \cdot \left[ \frac{\partial f}{\partial x}(c, y+k) - \frac{\partial f}{\partial x}(c, y) \right]$$
    for some $c \in (x, x+h)$.
    Applying the MVT a second time to the function $u(v) = \frac{\partial f}{\partial x}(c, v)$ on the interval $[y, y+k]$:
    $$\Delta(h, k) = h \cdot k \cdot \frac{\partial^2 f}{\partial y \partial x}(c, d)$$
    for some $d \in (y, y+k)$.

2.  **Second MVT Application (w.r.t $y$):**
    Alternatively, define a single-variable auxiliary function $w(v) = f(x+h, v) - f(x, v)$. Then:
    $$\Delta(h, k) = w(y+k) - w(y)$$
    By the MVT:
    $$\Delta(h, k) = k \cdot w'(d') = k \cdot \left[ \frac{\partial f}{\partial y}(x+h, d') - \frac{\partial f}{\partial y}(x, d') \right]$$
    for some $d' \in (y, y+k)$.
    Applying the MVT a second time to the function $p(u) = \frac{\partial f}{\partial y}(u, d')$ on the interval $[x, x+h]$:
    $$\Delta(h, k) = k \cdot h \cdot \frac{\partial^2 f}{\partial x \partial y}(c', d')$$
    for some $c' \in (x, x+h)$.

3.  **Equate and limit:**
    Since both derivations yield $\Delta(h, k)$, we set them equal (for $h, k \neq 0$):
    $$h \cdot k \cdot \frac{\partial^2 f}{\partial y \partial x}(c, d) = h \cdot k \cdot \frac{\partial^2 f}{\partial x \partial y}(c', d')$$
    Divide both sides by $h \cdot k$:
    $$\frac{\partial^2 f}{\partial y \partial x}(c, d) = \frac{\partial^2 f}{\partial x \partial y}(c', d')$$
    Take the limit as $(h, k) \to (0, 0)$. Since $c, c' \to x$ and $d, d' \to y$, and because the second-order mixed partial derivatives are assumed to be continuous on $U$:
    $$\lim_{(h,k) \to (0,0)} \frac{\partial^2 f}{\partial y \partial x}(c, d) = \frac{\partial^2 f}{\partial y \partial x}(x, y)$$
    $$\lim_{(h,k) \to (0,0)} \frac{\partial^2 f}{\partial x \partial y}(c', d') = \frac{\partial^2 f}{\partial x \partial y}(x, y)$$
    Thus, we obtain:
    $$\frac{\partial^2 f}{\partial y \partial x}(x, y) = \frac{\partial^2 f}{\partial x \partial y}(x, y) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: First-Order Partial Derivatives
Compute $\frac{\partial f}{\partial x}$ and $\frac{\partial f}{\partial y}$ for $f(x, y) = x^2 y + \sin(xy)$.
1.  **Differentiate with respect to $x$ (treat $y$ as a constant):**
    $$\frac{\partial f}{\partial x} = \frac{\partial}{\partial x}(x^2 y) + \frac{\partial}{\partial x}(\sin(xy))$$
    $$\frac{\partial f}{\partial x} = 2xy + \cos(xy) \cdot \frac{\partial}{\partial x}(xy) = 2xy + y\cos(xy)$$
2.  **Differentiate with respect to $y$ (treat $x$ as a constant):**
    $$\frac{\partial f}{\partial y} = \frac{\partial}{\partial y}(x^2 y) + \frac{\partial}{\partial y}(\sin(xy))$$
    $$\frac{\partial f}{\partial y} = x^2 + \cos(xy) \cdot \frac{\partial}{\partial y}(xy) = x^2 + x\cos(xy)$$

### Example 2: Verifying Clairaut's Theorem
Verify that the mixed partials of $f(x, y) = e^{x y^2}$ are symmetric.
1.  **Compute first-order partials:**
    $$\frac{\partial f}{\partial x} = y^2 e^{x y^2}$$
    $$\frac{\partial f}{\partial y} = 2xy e^{x y^2}$$
2.  **Compute mixed partial $\frac{\partial^2 f}{\partial y \partial x}$ (differentiate $\frac{\partial f}{\partial x}$ w.r.t $y$):**
    Use the product rule:
    $$\frac{\partial^2 f}{\partial y \partial x} = \frac{\partial}{\partial y}(y^2) \cdot e^{x y^2} + y^2 \cdot \frac{\partial}{\partial y}(e^{x y^2})$$
    $$\frac{\partial^2 f}{\partial y \partial x} = 2y e^{x y^2} + y^2 (2xy e^{x y^2}) = 2y e^{x y^2} + 2xy^3 e^{x y^2} = (2y + 2xy^3)e^{x y^2}$$
3.  **Compute mixed partial $\frac{\partial^2 f}{\partial x \partial y}$ (differentiate $\frac{\partial f}{\partial y}$ w.r.t $x$):**
    Use the product rule:
    $$\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial}{\partial x}(2xy) \cdot e^{x y^2} + 2xy \cdot \frac{\partial}{\partial x}(e^{x y^2})$$
    $$\frac{\partial^2 f}{\partial x \partial y} = 2y e^{x y^2} + 2xy (y^2 e^{x y^2}) = (2y + 2xy^3)e^{x y^2}$$
The mixed partials are identical, verifying Clairaut's Theorem.

---

## 5. Applied ML Context

1.  **Backpropagation:** The gradient of the loss function is computed by calculating the partial derivative of the loss with respect to each individual weight parameter: $\frac{\partial \mathcal{L}}{\partial w_{ij}}$.
2.  **Jacobian Matrices:** In multi-task learning or generative adversarial networks, we construct Jacobian matrices containing the first-order partial derivatives of multiple outputs with respect to multiple inputs.
3.  **Hessian Matrices:** Second-order optimization methods (like Newton's method) compute the Hessian matrix of second partial derivatives ($\frac{\partial^2 f}{\partial x_i \partial x_j}$) to measure curvature.
4.  **Sensitivity Analysis:** In interpretability models (like Integrated Gradients), the feature importance of an input feature $x_i$ is evaluated by computing the partial derivative of the prediction with respect to that feature: $\frac{\partial \hat{y}}{\partial x_i}$.
5.  **Softmax Logit Updates:** The derivative of the softmax output with respect to a logit input requires computing partial derivatives, which are used to formulate cross-entropy classification updates.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the geometric interpretation of partial derivatives on a 3D surface:
*   Show a 3D surface $z = f(x, y)$ (for example, a curved mountain peak).
*   Plot a point $P(x_0, y_0, z_0)$ on the surface.
*   Draw a vertical plane slicing through the surface along the line $y = y_0$ (parallel to the x-axis).
*   Show the 2D curve formed by the intersection of this plane and the surface. Draw a tangent line to this curve at $P$.
*   Label the slope of this tangent line as the partial derivative with respect to $x$: $\frac{\partial f}{\partial x}(x_0, y_0)$.
*   Draw a second vertical plane slicing through $P$ along the line $x = x_0$ (parallel to the y-axis). Draw the tangent line to the resulting intersection curve, and label its slope as the partial derivative with respect to $y$: $\frac{\partial f}{\partial y}(x_0, y_0)$, illustrating how partial derivatives represent slopes in axis-aligned directions.
