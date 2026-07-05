---
title: "Chain Rule"
description: "Composite functions, multivariable chain rule, limit definition proof, and backpropagation in deep networks."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Derivatives", "Partial Derivatives"]
---

<h1 align="center"> Chapter 31: Chain Rule </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Function Composition:** Familiarity with nested functions of the form $f(g(x))$.
* **Partial Derivatives:** Understanding rates of change along specific coordinate directions.

</div>

## 1. Conceptual Hook

In deep learning, we stack layers of neurons to form composite functions of extreme depth: $y = f_L(f_{L-1}(\dots(f_1(x))\dots))$. When a model makes a prediction, the input data flows forward through this sequence of nested functions. But when we want to train the network, how do we calculate the influence of a weight in the very first layer on the final error at the output? We cannot analyze them in isolation. We use the **chain rule**.

The chain rule is the mathematical gear system of calculus. It allows us to compute the derivative of a nested composite function by multiplying the rates of change (local derivatives) of its constituent parts. Just as a series of connected gears transfers rotational force from the first wheel to the last, the chain rule propagates sensitivity from the final loss function all the way back to the earliest weights in our network. It is the core algorithm that powers backpropagation.

---

## 2. Formal Definition

### Single-Variable Chain Rule
Let $g: \mathbb{R} \to \mathbb{R}$ be differentiable at $x$, and $f: \mathbb{R} \to \mathbb{R}$ be differentiable at $g(x)$. The composite function $h(x) = (f \circ g)(x) = f(g(x))$ is differentiable at $x$, and its derivative is:
$$h'(x) = f'(g(x)) \cdot g'(x)$$

In Leibniz notation, if $y = f(u)$ and $u = g(x)$, then:
$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

### Multivariable Chain Rule (General Form)
Let $g: \mathbb{R}^n \to \mathbb{R}^m$ be differentiable at $x$, and $f: \mathbb{R}^m \to \mathbb{R}^p$ be differentiable at $g(x)$. The derivative of the composite function $h = f \circ g: \mathbb{R}^n \to \mathbb{R}^p$ is given by the product of their Jacobian matrices:
$$D_x(f \circ g) = D_{g(x)}(f) \cdot D_x(g)$$
where $D(f) \in \mathbb{R}^{p \times m}$ and $D(g) \in \mathbb{R}^{m \times n}$ represent the Jacobian matrices of first-order partial derivatives.

---

## 3. Illustrative Derivation

### Rigorous Proof of the Single-Variable Chain Rule
A naive proof of the chain rule splits the difference quotient: $\frac{\Delta y}{\Delta x} = \frac{\Delta y}{\Delta u} \frac{\Delta u}{\Delta x}$, and takes the limit. However, this fails if $\Delta u = 0$ for values near $x$ (causing division by zero). We present a rigorous proof that avoids this pitfall using the linear approximation error formulation.

*Proof:*
Let $y = f(u)$ and $u = g(x)$. We assume $g$ is differentiable at $x_0$, and $f$ is differentiable at $u_0 = g(x_0)$.
Let $\Delta x$ be an increment in $x$, and let $\Delta u = g(x_0 + \Delta x) - g(x_0)$. By the differentiability of $g$ at $x_0$, $g$ is continuous at $x_0$, which implies:
$$\lim_{\Delta x \to 0} \Delta u = 0$$

Define the linear approximation error function $E(k)$ for $f$ around $u_0$ as:
$$E(k) = \begin{cases} \frac{f(u_0 + k) - f(u_0)}{k} - f'(u_0) & \text{if } k \neq 0 \\ 0 & \text{if } k = 0 \end{cases}$$
Since $f$ is differentiable at $u_0$, the limit of the difference quotient is exactly $f'(u_0)$, meaning:
$$\lim_{k \to 0} E(k) = 0$$
By construction, $E(k)$ is continuous at $k=0$. Multiplying the error definition by $k$, we obtain an equation valid for all values of $k$ (including $k=0$):
$$f(u_0 + k) - f(u_0) = \left[ f'(u_0) + E(k) \right] k$$

Now, substitute $k = \Delta u$:
$$f(g(x_0 + \Delta x)) - f(g(x_0)) = \left[ f'(g(x_0)) + E(\Delta u) \right] \Delta u$$
Divide both sides by the non-zero increment $\Delta x$:
$$\frac{f(g(x_0 + \Delta x)) - f(g(x_0))}{\Delta x} = \left[ f'(g(x_0)) + E(\Delta u) \right] \frac{\Delta u}{\Delta x}$$

Take the limit as $\Delta x \to 0$ of both sides. Using the limit product rule:
$$(f \circ g)'(x_0) = \lim_{\Delta x \to 0} \left[ f'(g(x_0)) + E(\Delta u) \right] \cdot \lim_{\Delta x \to 0} \frac{g(x_0 + \Delta x) - g(x_0)}{\Delta x}$$
Since $E(k)$ is continuous at $0$, and $\lim_{\Delta x \to 0} \Delta u = 0$:
$$\lim_{\Delta x \to 0} E(\Delta u) = E(0) = 0$$
Evaluating the second limit yields the derivative $g'(x_0)$:
$$(f \circ g)'(x_0) = \left[ f'(g(x_0)) + 0 \right] \cdot g'(x_0) = f'(g(x_0)) \cdot g'(x_0) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Nested Single-Variable Derivative
Differentiate $h(x) = \sin(x^2)$ using the chain rule.
1.  **Identify the nested functions:**
    $$y = f(u) = \sin(u) \quad \text{where} \quad u = g(x) = x^2$$
2.  **Calculate the individual derivatives:**
    $$\frac{dy}{du} = \cos(u) = \cos(x^2)$$
    $$\frac{du}{dx} = 2x$$
3.  **Multiply the derivatives:**
    $$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = \cos(x^2) \cdot 2x = 2x\cos(x^2)$$

### Example 2: Multivariable Chain Rule
Let $z = f(x, y) = x^2 + 3xy$, where $x(t) = \sin(t)$ and $y(t) = e^t$. Find the derivative $\frac{dz}{dt}$ at $t = 0$.
1.  **Compute the partial derivatives of $z$:**
    $$\frac{\partial z}{\partial x} = 2x + 3y, \quad \frac{\partial z}{\partial y} = 3x$$
2.  **Compute the derivatives w.r.t $t$:**
    $$\frac{dx}{dt} = \cos(t), \quad \frac{dy}{dt} = e^t$$
3.  **Evaluate variables at $t = 0$:**
    $$x(0) = \sin(0) = 0, \quad y(0) = e^0 = 1$$
    $$\frac{\partial z}{\partial x} = 2(0) + 3(1) = 3, \quad \frac{\partial z}{\partial y} = 3(0) = 0$$
    $$\frac{dx}{dt} = \cos(0) = 1, \quad \frac{dy}{dt} = e^0 = 1$$
4.  **Apply the multivariable chain rule:**
    $$\frac{dz}{dt} = \frac{\partial z}{\partial x} \frac{dx}{dt} + \frac{\partial z}{\partial y} \frac{dy}{dt} = (3)(1) + (0)(1) = 3$$

---

## 5. Applied ML Context

1.  **Backpropagation:** Neural networks update weights using gradient descent. The gradient of the loss with respect to early weights is computed by chaining the partial derivatives backwards layer-by-layer: $\frac{\partial \mathcal{L}}{\partial w^{(1)}} = \frac{\partial \mathcal{L}}{\partial a^{(L)}} \frac{\partial a^{(L)}}{\partial a^{(L-1)}} \dots \frac{\partial a^{(2)}}{\partial w^{(1)}}$.
2.  **Backpropagation Through Time (BPTT):** In Recurrent Neural Networks (RNNs), the model is unrolled over time steps. The chain rule calculates how an error at step $T$ propagates through recurrent state transitions to affect weights at step $t=1$.
3.  **Residual Networks (ResNets):** ResNets add shortcut links to layers: $y = x + f(x)$. Chaining derivatives through this link yields $\frac{\partial y}{\partial x} = 1 + f'(x)$. The addition of the "$1$" term prevents gradients from vanishing during backpropagation.
4.  **Reinforcement Learning (Policy Gradients):** In policy gradient optimization, the reward depends on actions, which depend on network policy outputs. The chain rule calculates the gradient of the expected reward with respect to policy parameters.
5.  **Differentiable Rendering:** In 3D computer vision, the pixel loss is propagated backward through the rendering equations using the chain rule to optimize 3D shape and texture parameters directly from 2D photos.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the flow of derivatives in a computational graph:
*   Show an input variable $x$ pointing to an intermediate node $u = g(x)$ with an arrow labeled $\frac{du}{dx}$ (local derivative).
*   Show the intermediate node $u$ pointing to the output node $y = f(u)$ with an arrow labeled $\frac{dy}{du}$.
*   Draw a path under these nodes showing the **forward pass** (values flowing left to right) and a second path showing the **backward pass** (gradients flowing right to left).
*   Illustrate how the total derivative $\frac{dy}{dx}$ is computed by multiplying the labels along the path: $\frac{dy}{du} \cdot \frac{du}{dx}$, visualizing the chain rule as a sequential multiplier of sensitivities.
