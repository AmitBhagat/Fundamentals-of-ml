---
title: "Automatic Differentiation"
description: "Computational graphs, forward and reverse mode differentiation, Wengert lists, adjoint accumulators, and backpropagation."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Chain Rule", "Calculus: Partial Derivatives"]
---

<h1 align="center"> Chapter 96: Automatic Differentiation </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Computational Graph:** A directed acyclic graph (DAG) representing mathematical operations, where nodes are variables and edges represent operations.
* **The Chain Rule:** The calculus rule for finding the derivative of composite functions: $\frac{\partial y}{\partial x} = \frac{\partial y}{\partial u} \frac{\partial u}{\partial x}$.

</div>

## 1. Conceptual Hook

Training a machine learning model requires finding how a change in any of its parameters affects the final loss—in other words, computing gradients. For deep neural networks with billions of weights, calculating these derivatives analytically by hand is impossible.

If we try to write symbolic equations (symbolic differentiation), we run into "expression swell," where formulas grow exponentially. If we try to approximate them numerically by checking how the loss shifts when we tweak each weight slightly (finite differences), we must run the model billions of times, which is computationally slow and vulnerable to rounding errors.

**Automatic Differentiation (AD)** solves this.

AD is a family of techniques that numerically evaluates the derivatives of functions defined by computer programs. By representing any calculation as a computational graph—a sequence of elementary arithmetic operations—and recursively applying the chain rule, AD computes derivatives to machine precision in a single pass. It is the engine under the hood of PyTorch and JAX that makes backpropagation possible.

---

## 2. Formal Definition

Let $f: \mathbb{R}^n \to \mathbb{R}^m$ be a differentiable function represented as a computational graph. The execution of $f$ is decomposed into a sequence of intermediate variables, called an **evaluation trace** (or Wengert list):

*   **Inputs:** $v_{i-n} = x_i$ for $i = 1, \dots, n$.
*   **Intermediate Operations:** $v_i = \phi_i\left( \text{Parents}(v_i) \right)$ for $i = 1, \dots, N$.
*   **Outputs:** $y_j = v_{N-m+j}$ for $j = 1, \dots, m$.

Where $\phi_i$ are elementary unary or binary operations (e.g. $\sin, \ln, + , \times$).

### 1. Forward Mode AD (Tangents)
Forward mode computes the derivative of all intermediate values with respect to a single independent variable $x_j$. We define the tangent accumulator $\dot{v}_i = \frac{\partial v_i}{\partial x_j}$, which is evaluated along with the forward pass:
$$\dot{v}_i = \sum_{k \in \text{Parents}(v_i)} \frac{\partial \phi_i}{\partial v_k} \dot{v}_k$$
with seed initialization $\dot{v}_{k-n} = 1$ if $k=j$, else $0$.

### 2. Reverse Mode AD (Adjoints)
Reverse mode computes the derivative of a single scalar output $y$ with respect to all intermediate values. We define the adjoint accumulator $\bar{v}_i = \frac{\partial y}{\partial v_i}$, which is evaluated by traversing the graph backward:
$$\bar{v}_j = \sum_{i \in \text{Children}(v_j)} \bar{v}_i \frac{\partial \phi_i}{\partial v_j}$$
with seed initialization $\bar{y} = 1$.

---

## 3. Illustrative Derivation

### Derivation of the Reverse Mode Adjoint Formula
We prove the recursive adjoint formula using the multivariate chain rule on a general directed acyclic computational graph.

*Proof:*
Let $y = v_N$ be the scalar output of our graph. For any intermediate variable $v_j$ in the graph, let $\text{Children}(v_j) = \{ v_i \mid v_j \text{ is an input to } v_i \}$ be the set of variables that directly depend on $v_j$.

1.  **Apply the multivariate chain rule:**
    The total change in the output $y$ caused by a change in $v_j$ is the sum of the partial changes propagated through all of its direct child nodes:
    $$\frac{\partial y}{\partial v_j} = \sum_{i \in \text{Children}(v_j)} \frac{\partial y}{\partial v_i} \frac{\partial v_i}{\partial v_j}$$

2.  **Substitute adjoint definitions:**
    By definition, we write the adjoint accumulators as $\bar{v}_j = \frac{\partial y}{\partial v_j}$ and $\bar{v}_i = \frac{\partial y}{\partial v_i}$:
    $$\bar{v}_j = \sum_{i \in \text{Children}(v_j)} \bar{v}_i \frac{\partial v_i}{\partial v_j}$$

3.  **Evaluate local partial derivatives:**
    Since each child node $v_i$ is computed via an elementary function $v_i = \phi_i(v_j, \dots)$, the term $\frac{\partial v_i}{\partial v_j} = \frac{\partial \phi_i}{\partial v_j}$ is the derivative of a simple elementary function, which is known analytically:
    $$\bar{v}_j = \sum_{i \in \text{Children}(v_j)} \bar{v}_i \frac{\partial \phi_i}{\partial v_j} \quad \blacksquare$$

This proves that the adjoint accumulators can be computed recursively by traversing the computational graph in reverse order, starting from the output node where $\bar{v}_N = \frac{\partial y}{\partial v_N} = 1$.

---

## 4. Concrete Examples

### Example 1: Forward and Reverse AD
We compute the derivative $\frac{\partial y}{\partial x_1}$ for the function $y = \ln(x_1 x_2) + x_1^2$ evaluated at $x_1 = 2, x_2 = 5$.
1.  **Forward Pass (Evaluation Trace):**
    *   $v_{-1} = x_1 = 2$
    *   $v_0 = x_2 = 5$
    *   $v_1 = v_{-1} \cdot v_0 = 10$
    *   $v_2 = \ln(v_1) = \ln(10) \approx 2.302585$
    *   $v_3 = v_{-1}^2 = 4$
    *   $v_4 = v_2 + v_3 \approx 6.302585 \implies y \approx 6.302585$
2.  **Reverse Pass (Adjoint Accumulation):**
    *   Seed: $\bar{v}_4 = 1$
    *   $\bar{v}_3 = \bar{v}_4 \cdot \frac{\partial v_4}{\partial v_3} = 1 \cdot 1 = 1$
    *   $\bar{v}_2 = \bar{v}_4 \cdot \frac{\partial v_4}{\partial v_2} = 1 \cdot 1 = 1$
    *   $\bar{v}_1 = \bar{v}_2 \cdot \frac{\partial v_2}{\partial v_1} = 1 \cdot \frac{1}{v_1} = 0.1$
    *   $\bar{x}_1 = \bar{v}_{-1} = \bar{v}_1 \cdot \frac{\partial v_1}{\partial v_{-1}} + \bar{v}_3 \cdot \frac{\partial v_3}{\partial v_{-1}} = 0.1 \cdot v_0 + 1 \cdot 2v_{-1} = 0.1 \cdot 5 + 1 \cdot 4 = 4.5$
The derivative is $4.5$.

### Example 2: Sigmoid Activation Adjoint
We compute the adjoint with respect to the weight parameter $w$ for the sigmoid activation $y = \sigma(w x_1)$ where $\sigma(z) = \frac{1}{1 + e^{-z}}$, evaluated at $w = 0.5, x_1 = 2.0$.
1.  **Forward Pass:**
    *   $v_1 = w \cdot x_1 = 0.5 \cdot 2.0 = 1.0$
    *   $v_2 = \sigma(v_1) = \frac{1}{1 + e^{-1}} \approx 0.731059 \implies y \approx 0.731059$
2.  **Reverse Pass:**
    *   Seed: $\bar{v}_2 = 1$
    *   $\bar{v}_1 = \bar{v}_2 \cdot \frac{\partial \sigma(v_1)}{\partial v_1} = 1 \cdot \sigma(v_1)(1 - \sigma(v_1)) \approx 0.731059 \cdot 0.268941 \approx 0.196612$
    *   $\bar{w} = \bar{v}_1 \cdot \frac{\partial v_1}{\partial w} = \bar{v}_1 \cdot x_1 \approx 0.196612 \cdot 2.0 \approx 0.393224$
The parameter gradient is $\approx 0.393$.

---

## 5. Applied ML Context

1.  **Neural Network Backpropagation:** Reverse-mode AD is used to compute the gradient of the loss function $\mathcal{L}$ with respect to all network weights in a single backward pass, making gradient descent computationally feasible.
2.  **Physics-Informed Neural Networks (PINNs):** Forward or reverse AD is used to calculate higher-order partial derivatives of network outputs with respect to physical coordinate inputs $(x, y, z, t)$ to solve partial differential equations.
3.  **Validation-Based Hyperparameter Tuning:** Using AD to calculate the gradient of validation loss with respect to hyperparameter variables, automating learning rate decay tuning.
4.  **Quantitative Finance Risk Metrics:** Differentiating option pricing models with respect to market parameters to compute risk metrics (Greeks like Delta and Gamma) in real time.
5.  **Generative Adversarial Networks (GANs):** Propagating gradients from the discriminator output backward through generator parameters, enabling generative learning.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating computational graph flows:
*   Draw a Directed Acyclic Graph (DAG) for a composite function like $f(x_1, x_2) = \sin(x_1) + x_1 x_2$:
    *   Draw input nodes $x_1$ and $x_2$ on the left.
    *   Draw operation nodes $\sin$, $\times$, and $+$ in the center.
    *   Draw output node $y$ on the right.
*   Draw arrows showing two opposing flows:
    1.  **Forward Pass (Blue Arrows):** Moving left-to-right, computing intermediate numerical values.
    2.  **Backward Pass (Red Arrows):** Moving right-to-left, computing and accumulating adjoint vectors $\bar{v}_i$.
*   Add a caption explaining that the forward pass evaluates intermediate values, while the backward pass moves in reverse to accumulate derivatives with respect to all parameters simultaneously.
