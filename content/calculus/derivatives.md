---
title: "Derivatives"
description: "Limit definition of derivatives, differentiability, derivative of activation functions, and gradient updates."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Real Number System", "Functional Notation"]
---

<h1 align="center"> Chapter 33: Derivatives </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Functions:** Understanding $y = f(x)$ as a mapping from inputs to outputs.
* **Limits:** Concept of analyzing a function's behavior as inputs approach a point.

</div>

## 1. Conceptual Hook

In machine learning, training a model is like navigating a thick fog down a mountain. You cannot see the bottom (the optimal parameters that minimize error), but you can feel the slope of the ground beneath your feet. To make progress, you take a step in the direction that slopes downward. The mathematical tool that measures this local slope is the **derivative**.

A derivative is the measurement of sensitivity. It tells us exactly how much a function's output changes in response to a tiny, microscopic change in its input. If the function is our model's loss (error) and the input is a neural network weight, the derivative tells us whether to increase or decrease that weight to reduce the error. The derivative is the fundamental compass of optimization, driving every update step in gradient descent.

---

## 2. Formal Definition

For a real-valued function $f: \mathbb{R} \to \mathbb{R}$, the **derivative** at a point $x$ in the interior of its domain is defined as the limit of the difference quotient, provided the limit exists:
$$f'(x) = \frac{df}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

If this limit exists at $x$, we say the function $f$ is **differentiable** at $x$. For $f$ to be differentiable on an open interval $(a, b)$, the limit must exist for all points in the interval.

### Differentiability vs. Continuity
If a function is differentiable at $x$, it is guaranteed to be continuous at $x$. However, the converse is not true. A function can be continuous but non-differentiable at a point. A classic example is the absolute value function $f(x) = |x|$, which is continuous everywhere but has a sharp "corner" at $x = 0$, where the left-hand limit ($-\lim_{h \to 0} \frac{-h}{h} = -1$) and right-hand limit ($1$) of the difference quotient do not match.

---

## 3. Illustrative Derivation

### Derivation of the Sigmoid Activation Derivative
In neural networks, we require the derivatives of activation functions to backpropagate errors. We derive the derivative of the **Sigmoid function**, $\sigma(x) = \frac{1}{1 + e^{-x}}$, demonstrating how it can be expressed elegantly in terms of itself.

*Proof:*
Using the quotient rule $\left( \frac{u}{v} \right)' = \frac{u'v - uv'}{v^2}$ (or the chain rule on $u(x)^{-1}$):
Let $u(x) = 1$ and $v(x) = 1 + e^{-x}$.
$$\sigma'(x) = \frac{d}{dx} \left( (1 + e^{-x})^{-1} \right)$$
Applying the chain rule:
$$\sigma'(x) = -1 \cdot (1 + e^{-x})^{-2} \cdot \frac{d}{dx}(1 + e^{-x})$$
Since $\frac{d}{dx}(1 + e^{-x}) = -e^{-x}$:
$$\sigma'(x) = -(1 + e^{-x})^{-2} \cdot (-e^{-x})$$
$$\sigma'(x) = \frac{e^{-x}}{(1 + e^{-x})^2}$$

Now, let us manipulate this fraction to express it in terms of $\sigma(x)$:
$$\sigma'(x) = \frac{1}{1 + e^{-x}} \cdot \frac{e^{-x}}{1 + e^{-x}}$$
Notice that $\frac{e^{-x}}{1 + e^{-x}} = \frac{(1 + e^{-x}) - 1}{1 + e^{-x}} = 1 - \frac{1}{1 + e^{-x}}$.
Substitute $\sigma(x) = \frac{1}{1 + e^{-x}}$ back into the expression:
$$\sigma'(x) = \sigma(x) \cdot (1 - \sigma(x)) \quad \blacksquare$$
This simple form makes the Sigmoid function highly computationally efficient in neural network backpropagation, as we do not need to compute expensive exponential functions twice.

---

## 4. Concrete Examples

### Example 1: Limit Definition Walkthrough
Find the derivative of $f(x) = x^2$ using the formal limit definition.
1.  **Set up the limit:**
    $$f'(x) = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}$$
2.  **Expand the numerator:**
    $$f'(x) = \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h}$$
    $$f'(x) = \lim_{h \to 0} \frac{2xh + h^2}{h}$$
3.  **Factor out and divide by $h$:**
    $$f'(x) = \lim_{h \to 0} (2x + h)$$
4.  **Evaluate the limit as $h \to 0$:**
    $$f'(x) = 2x$$

### Example 2: The ReLU Activation Function
The Rectified Linear Unit (ReLU) is defined as $f(x) = \max(0, x)$.
1.  **Differentiate for $x > 0$:**
    For positive inputs, $f(x) = x \implies f'(x) = 1$.
2.  **Differentiate for $x < 0$:**
    For negative inputs, $f(x) = 0 \implies f'(x) = 0$.
3.  **Analyze at $x = 0$:**
    The function has a sharp corner at the origin. The left-side slope is $0$ and the right-side slope is $1$. The derivative is undefined at $x=0$.
    In practice, deep learning libraries assign an arbitrary value (often $0$ or $0.5$) or use a **subgradient**, where the subdifferential interval at $x=0$ is $[0, 1]$.
    $$f'(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{if } x < 0 \\ [0, 1] & \text{if } x = 0 \end{cases}$$

---

## 5. Applied ML Context

1.  **Gradient Descent Optimization:** Model parameters $\theta$ are updated iteratively using the negative of the derivative of the cost function: $\theta_{new} = \theta_{old} - \eta f'(\theta_{old})$, where $\eta$ is the learning rate.
2.  **Backpropagation:** Neural networks calculate the sensitivity of the final loss to weights in early layers by multiplying local derivatives layer-by-layer using the chain rule.
3.  **Vanishing Gradients:** If an activation function's derivative is always small (for example, the Sigmoid derivative peaks at $0.25$), multiplying these derivatives over many layers causes the gradient to vanish, halting learning in deep architectures.
4.  **Regularization Derivatives:** L2 regularization adds a penalty $\frac{\lambda}{2} w^2$ to the loss. Its derivative with respect to weight is $\lambda w$, which is subtracted during update steps, performing **weight decay**.
5.  **Adversarial Attacks (FGSM):** Adversarial attacks (like Fast Gradient Sign Method) find malicious perturbations by taking the derivative of the loss function with respect to the input pixels, shifting the image in the direction that maximizes error.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the limit definition of the derivative:
*   Show a curve representing a function $y = f(x)$.
*   Plot a point $(x, f(x))$ and a neighboring point $(x+h, f(x+h))$ on the curve.
*   Draw a secant line passing through both points. Label the slope of this line as the difference quotient: $\frac{f(x+h) - f(x)}{h}$.
*   Draw a series of arrows showing the interval $h$ shrinking towards $0$. Show how the secant line rotates as the second point slides down the curve.
*   Show the final tangent line touching the curve at exactly $(x, f(x))$, and label its slope as the derivative $f'(x)$, visualizing the transition from average rate of change to instantaneous slope.
