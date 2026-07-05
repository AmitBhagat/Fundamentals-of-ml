---
title: "Jacobian Matrix"
description: "Vector-valued functions, first-order multivariable approximations, Jacobian chain rule, and area scaling."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Matrices", "Partial Derivatives", "Chain Rule"]
---

<h1 align="center"> Chapter 37: Jacobian Matrix </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Partial Derivatives:** Knowing how to compute coordinate-wise rates of change.
* **Vector-Valued Functions:** Familiarity with functions that map vectors to vectors.

</div>

## 1. Conceptual Hook

When we deal with simple functions (like the loss of a linear regression model), we calculate a single derivative or a gradient vector. But what happens when our inputs and outputs are both high-dimensional vectors? For example, when backpropagating through a softmax layer, or mapping joint angles of a robotic arm to 3D spatial coordinates? In these multi-input, multi-output systems, we use the **Jacobian matrix**.

The Jacobian matrix is the ultimate first-order ledger. It aggregates every first-order partial derivative of a vector-valued function, mapping how every single input variable affects every single output variable. Geometrically, the Jacobian is the best linear approximation of a curved, non-linear coordinate mapping at a specific point. It captures how a local area stretches, shears, and rotates under the transformation, acting as the fundamental mathematical operator for chain-rule backpropagation through vector layers.

---

## 2. Formal Definition

Let $f: U \to \mathbb{R}^m$ be a differentiable function defined on an open set $U \subseteq \mathbb{R}^n$. The function can be represented as a vector of $m$ coordinate scalar functions:
$$f(x) = \begin{bmatrix} f_1(x_1, \dots, x_n) \\ f_2(x_1, \dots, x_n) \\ \vdots \\ f_m(x_1, \dots, x_n) \end{bmatrix}$$

The **Jacobian matrix** of $f$ at a point $a \in U$, denoted $J_f(a)$ or $Df(a)$, is the $m \times n$ matrix of first-order partial derivatives:
$$J_f(a) = \begin{pmatrix} \frac{\partial f_1}{\partial x_1}(a) & \frac{\partial f_1}{\partial x_2}(a) & \dots & \frac{\partial f_1}{\partial x_n}(a) \\ \frac{\partial f_2}{\partial x_1}(a) & \frac{\partial f_2}{\partial x_2}(a) & \dots & \frac{\partial f_2}{\partial x_n}(a) \\ \vdots & \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1}(a) & \frac{\partial f_m}{\partial x_2}(a) & \dots & \frac{\partial f_m}{\partial x_n}(a) \end{pmatrix}$$
where $(J_f(a))_{ij} = \frac{\partial f_i}{\partial x_j}(a)$.

### Linear Approximation Theorem
The Jacobian matrix represents the derivative of the vector-valued function $f$. It defines the linear map $h \mapsto J_f(a)h$ that best approximates the behavior of $f$ near $a$:
$$f(a + h) = f(a) + J_f(a)h + o(\|h\|) \quad \text{as } h \to 0$$
where $o(\|h\|)$ represents a remainder term that vanishes faster than the norm of $h$.

---

## 3. Illustrative Derivation

### Derivation of the Jacobian Chain Rule
In neural networks, we must chain derivatives through a sequence of vector-valued layers (e.g. going from input $x \in \mathbb{R}^n$ to hidden state $y \in \mathbb{R}^m$ and then output $z \in \mathbb{R}^p$). We prove that the Jacobian of the composition is the matrix product of the individual Jacobians.

Let $g: \mathbb{R}^n \to \mathbb{R}^m$ be differentiable at $x$, and let $f: \mathbb{R}^m \to \mathbb{R}^p$ be differentiable at $y = g(x)$. Define the composite function $h = f \circ g: \mathbb{R}^n \to \mathbb{R}^p$.
The $i$-th coordinate function of the composition is:
$$h_i(x) = f_i(g_1(x), g_2(x), \dots, g_m(x))$$

Using the multivariable chain rule, we compute the partial derivative of $h_i$ with respect to the input variable $x_j$:
$$\frac{\partial h_i}{\partial x_j}(x) = \sum_{k=1}^m \frac{\partial f_i}{\partial y_k}(g(x)) \cdot \frac{\partial g_k}{\partial x_j}(x)$$

Observe the structure of this summation:
*   $\frac{\partial f_i}{\partial y_k}(g(x))$ is the $(i, k)$-th entry of the Jacobian matrix $J_f(g(x)) \in \mathbb{R}^{p \times m}$.
*   $\frac{\partial g_k}{\partial x_j}(x)$ is the $(k, j)$-th entry of the Jacobian matrix $J_g(x) \in \mathbb{R}^{m \times n}$.

The summation $\sum_{k=1}^m (J_f)_{ik} (J_g)_{kj}$ is exactly the definition of the $(i, j)$-th entry of the matrix product $J_f(g(x)) \cdot J_g(x)$. Thus, the entire coordinate-wise system of derivatives can be represented as the matrix multiplication:
$$J_{f \circ g}(x) = J_f(g(x)) \cdot J_g(x) \quad \blacksquare$$
This justifies why backpropagation through vector layers is formulated as multiplying Jacobian matrices.

---

## 4. Concrete Examples

### Example 1: 2D-to-2D Nonlinear Jacobian
Compute the Jacobian of the vector-valued function $f(x, y) = \begin{bmatrix} x^2 + y \\ 3x + \sin(y) \end{bmatrix}$ at the point $(1, 0)$.
1.  **Formulate the partial derivative entries:**
    *   Row 1: $\frac{\partial f_1}{\partial x} = 2x, \quad \frac{\partial f_1}{\partial y} = 1$
    *   Row 2: $\frac{\partial f_2}{\partial x} = 3, \quad \frac{\partial f_2}{\partial y} = \cos(y)$
2.  **Construct the Jacobian matrix:**
    $$J_f(x, y) = \begin{pmatrix} 2x & 1 \\ 3 & \cos(y) \end{pmatrix}$$
3.  **Evaluate at $(1, 0)$:**
    $$J_f(1, 0) = \begin{pmatrix} 2(1) & 1 \\ 3 & \cos(0) \end{pmatrix} = \begin{pmatrix} 2 & 1 \\ 3 & 1 \end{pmatrix}$$

### Example 2: Polar Coordinate Transformation
Let $f(r, \theta) = \begin{bmatrix} r \cos\theta \\ r \sin\theta \end{bmatrix}$ map polar coordinates to Cartesian coordinates.
1.  **Construct the Jacobian:**
    $$J_f(r, \theta) = \begin{pmatrix} \frac{\partial(r\cos\theta)}{\partial r} & \frac{\partial(r\cos\theta)}{\partial \theta} \\ \frac{\partial(r\sin\theta)}{\partial r} & \frac{\partial(r\sin\theta)}{\partial \theta} \end{pmatrix} = \begin{pmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{pmatrix}$$
2.  **Compute the Jacobian determinant:**
    $$\det\left(J_f(r, \theta)\right) = (\cos\theta)(r\cos\theta) - (-r\sin\theta)(\sin\theta)$$
    $$\det\left(J_f(r, \theta)\right) = r\cos^2\theta + r\sin^2\theta = r(\cos^2\theta + \sin^2\theta) = r$$
This determinant $r$ is the local area scaling factor, explaining why the differential area element changes from $dx dy$ to $r dr d\theta$ during polar integration.

---

## 5. Applied ML Context

1.  **Backpropagation through Vector Layers:** In layers with coupled outputs (like Softmax or Layer Normalization), backpropagation cannot be done element-wise. We must multiply the incoming gradient vector by the layer's Jacobian matrix: $g_{in} = J_{layer}^T g_{out}$.
2.  **Normalizing Flows:** In generative modeling, we map a simple density to a complex one: $y = g(x)$. To compute the log-likelihood of $y$, the model must calculate the log-determinant of the Jacobian: $\log p(y) = \log p(x) - \log |\det J_g(x)|$.
3.  **Jacobian Regularization in GANs:** To stabilize GAN training and avoid mode collapse, a penalty is placed on the Frobenius norm of the generator's Jacobian: $\mathcal{R} = \|J_G(z)\|_F^2$. This prevents the generator from being overly sensitive to small changes in input noise.
4.  **RNN Gradient Diagnostics:** In recurrent networks, the hidden state update is $h_{t} = \tanh(W_{hh} h_{t-1} + W_{xh} x_t)$. The Jacobian of this transition, $J_t = \frac{\partial h_t}{\partial h_{t-1}}$, is analyzed to detect exploding ($|\lambda_{max}| > 1$) or vanishing ($|\lambda_{max}| < 1$) gradients.
5.  **Robot Policy Gradients:** In reinforcement learning for robot control, the policy outputs joint velocities. The kinematic Jacobian of the robot maps these joint velocities to the physical 3D velocities of the end-effector.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the local coordinate warping of a Jacobian:
*   Show a 2D input coordinate grid $(x_1, x_2)$ with a highlighted tiny square.
*   Draw a curved arrow representing the non-linear vector-valued mapping $f$.
*   Show the output coordinate grid $(y_1, y_2)$ where the grid lines are now curved and distorted. Show how the tiny input square has been warped into a tilted, stretched parallelogram.
*   Draw a zoomed-in detail of this parallelogram, showing that its sides are defined by the column vectors of the Jacobian: $J_{\cdot, 1} = \frac{\partial f}{\partial x_1}$ and $J_{\cdot, 2} = \frac{\partial f}{\partial x_2}$. This visualizes the Jacobian as the local linear transformation that maps the standard basis vectors to the local tangent space of the output.
