---
title: "Backpropagation Math"
description: "Reverse-mode automatic differentiation, the four fundamental equations of backpropagation, error signals, and layer updates."
complexity: "Advanced"
estimated_time: "45 min"
prerequisites: ["Matrices", "Partial Derivatives", "Chain Rule", "Jacobian Matrix"]
---

<h1 align="center"> Chapter 30: Backpropagation Math </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **The Chain Rule:** Knowing how to propagate derivatives through nested functions.
* **Matrix Calculus:** Comfort with matrix-vector products and outer products.

</div>

## 1. Conceptual Hook

When we train a deep neural network, we adjust millions of weights to minimize a loss function. If we calculated the gradient of the loss with respect to each individual weight from scratch, we would need to run the entire network calculations over and over for every single weight. For modern networks, this would take years. The algorithm that allows us to calculate all these gradients in a single step is **backpropagation**.

Backpropagation is a highly efficient implementation of the chain rule. Instead of computing gradients independently, it uses **dynamic programming**. It runs a forward pass to calculate the activations of every neuron, and then runs a backward pass that caches and propagates error signals from the output layer to the input. By recycling these intermediate values, backpropagation reduces the computational complexity of gradient calculation from a disastrous quadratic scale to a linear scale, making deep learning practically viable.

---

## 2. Formal Definition

Consider an $L$-layer feedforward neural network. The feedforward equations for layer $l$ (where $l = 1, 2, \dots, L$) are:
$$z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$$
$$a^{(l)} = \sigma(z^{(l)})$$
where:
*   $W^{(l)} \in \mathbb{R}^{n_l \times n_{l-1}}$ is the weight matrix for layer $l$.
*   $b^{(l)} \in \mathbb{R}^{n_l}$ is the bias vector for layer $l$.
*   $a^{(l-1)} \in \mathbb{R}^{n_{l-1}}$ is the activation vector from the previous layer ($a^{(0)} = x$, the input vector).
*   $z^{(l)} \in \mathbb{R}^{n_l}$ is the pre-activation logit vector of layer $l$.
*   $\sigma$ is the activation function (applied element-wise).

Let $C$ be the scalar cost function (e.g. Mean Squared Error or Cross-Entropy) evaluating the network's output $a^{(L)}$ against target label $y$.

We define the **error signal** vector for layer $l$ as the partial derivative of the cost with respect to the pre-activation logits:
$$\delta^{(l)} = \frac{\partial C}{\partial z^{(l)}} \in \mathbb{R}^{n_l}$$

### The Four Fundamental Equations of Backpropagation
1.  **Error at the output layer $L$:**
    $$\delta^{(L)} = \nabla_{a^{(L)}} C \odot \sigma'(z^{(L)})$$
2.  **Error at a hidden layer $l$ (w.r.t the next layer $l+1$):**
    $$\delta^{(l)} = \left( (W^{(l+1)})^T \delta^{(l+1)} \right) \odot \sigma'(z^{(l)})$$
3.  **Gradient of the cost w.r.t the bias $b^{(l)}$:**
    $$\frac{\partial C}{\partial b^{(l)}} = \delta^{(l)}$$
4.  **Gradient of the cost w.r.t the weight $W^{(l)}$:**
    $$\frac{\partial C}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T$$
where $\odot$ represents the Hadamard (element-wise) product.

---

## 3. Illustrative Derivation

### Derivation of the Four Backpropagation Equations
We derive the fundamental equations of backpropagation using index notation and the multivariable chain rule.

*Proof of Equation 1 (Output Error $\delta^{(L)}$):*
By definition, the $i$-th component of the error vector $\delta^{(L)}$ is:
$$\delta_i^{(L)} = \frac{\partial C}{\partial z_i^{(L)}}$$
Since the cost $C$ depends directly on the activations $a^{(L)}$, and each $a_k^{(L)}$ depends on $z_k^{(L)}$:
$$\delta_i^{(L)} = \sum_k \frac{\partial C}{\partial a_k^{(L)}} \frac{\partial a_k^{(L)}}{\partial z_i^{(L)}}$$
Because $a_k^{(L)} = \sigma(z_k^{(L)})$, the derivative $\frac{\partial a_k^{(L)}}{\partial z_i^{(L)}}$ is non-zero only when $k = i$. Thus, the summation collapses to:
$$\delta_i^{(L)} = \frac{\partial C}{\partial a_i^{(L)}} \sigma'(z_i^{(L)})$$
Vectorizing this coordinate-wise equation yields:
$$\delta^{(L)} = \nabla_{a^{(L)}} C \odot \sigma'(z^{(L)}) \quad \blacksquare$$

*Proof of Equation 2 (Hidden Layer Error $\delta^{(l)}$):*
We apply the chain rule to relate $\delta^{(l)}$ to the error of the subsequent layer $\delta^{(l+1)}$:
$$\delta_j^{(l)} = \frac{\partial C}{\partial z_j^{(l)}} = \sum_k \frac{\partial C}{\partial z_k^{(l+1)}} \frac{\partial z_k^{(l+1)}}{\partial z_j^{(l)}} = \sum_k \delta_k^{(l+1)} \frac{\partial z_k^{(l+1)}}{\partial z_j^{(l)}}$$
Using the relation $z_k^{(l+1)} = \sum_r W_{kr}^{(l+1)} a_r^{(l)} + b_k^{(l+1)}$, we take the derivative w.r.t $z_j^{(l)}$:
$$\frac{\partial z_k^{(l+1)}}{\partial z_j^{(l)}} = \sum_r W_{kr}^{(l+1)} \frac{\partial a_r^{(l)}}{\partial z_j^{(l)}}$$
Since $a_r^{(l)} = \sigma(z_r^{(l)})$, $\frac{\partial a_r^{(l)}}{\partial z_j^{(l)}}$ is non-zero only when $r = j$:
$$\frac{\partial z_k^{(l+1)}}{\partial z_j^{(l)}} = W_{kj}^{(l+1)} \sigma'(z_j^{(l)})$$
Substitute this back into the coordinate summation:
$$\delta_j^{(l)} = \sum_k \delta_k^{(l+1)} W_{kj}^{(l+1)} \sigma'(z_j^{(l)}) = \left( \sum_k W_{kj}^{(l+1)} \delta_k^{(l+1)} \right) \sigma'(z_j^{(l)})$$
Notice that $\sum_k W_{kj}^{(l+1)} \delta_k^{(l+1)}$ is the $j$-th component of the matrix-vector product $(W^{(l+1)})^T \delta^{(l+1)}$. Vectorizing this expression yields:
$$\delta^{(l)} = \left( (W^{(l+1)})^T \delta^{(l+1)} \right) \odot \sigma'(z^{(l)}) \quad \blacksquare$$

*Proof of Equations 3 and 4 (Parameter Gradients):*
Using the chain rule to find the derivative of the cost with respect to individual weights and biases at layer $l$:
$$\frac{\partial C}{\partial W_{ij}^{(l)}} = \frac{\partial C}{\partial z_i^{(l)}} \frac{\partial z_i^{(l)}}{\partial W_{ij}^{(l)}}$$
Since $z_i^{(l)} = \sum_r W_{ir}^{(l)} a_r^{(l-1)} + b_i^{(l)}$, we have $\frac{\partial z_i^{(l)}}{\partial W_{ij}^{(l)}} = a_j^{(l-1)}$. Substituting this:
$$\frac{\partial C}{\partial W_{ij}^{(l)}} = \delta_i^{(l)} a_j^{(l-1)}$$
This coordinate product is the definition of the outer product of $\delta^{(l)}$ and $a^{(l-1)}$, yielding:
$$\frac{\partial C}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T \quad \blacksquare$$
For the bias gradient:
$$\frac{\partial C}{\partial b_i^{(l)}} = \frac{\partial C}{\partial z_i^{(l)}} \frac{\partial z_i^{(l)}}{\partial b_i^{(l)}}$$
Since $\frac{\partial z_i^{(l)}}{\partial b_i^{(l)}} = 1$:
$$\frac{\partial C}{\partial b_i^{(l)}} = \delta_i^{(l)} \implies \frac{\partial C}{\partial b^{(l)}} = \delta^{(l)} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Single-Neuron Network
Let a simple network be defined by: $z = wx + b \implies a = \sigma(z)$, with MSE loss $C = \frac{1}{2}(a - y)^2$.
Inputs: $x = 2$, target $y = 1$, current parameters: $w = 0.5, b = 0$.
Learning rate: $\eta = 0.1$. Activation: Sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$.
1.  **Forward Pass:**
    *   $z = (0.5)(2) + 0 = 1.0$
    *   $a = \sigma(1.0) = \frac{1}{1 + e^{-1}} \approx 0.731$
    *   $C = \frac{1}{2}(0.731 - 1)^2 \approx 0.036$
2.  **Backward Pass:**
    *   $\nabla_a C = \frac{\partial C}{\partial a} = (a - y) = (0.731 - 1) = -0.269$
    *   $\sigma'(z) = a(1-a) = (0.731)(1 - 0.731) \approx 0.196$
    *   Output error $\delta = \nabla_a C \cdot \sigma'(z) = (-0.269)(0.196) \approx -0.0527$
3.  **Compute Gradients:**
    *   $\frac{\partial C}{\partial w} = \delta \cdot x = (-0.0527)(2) = -0.1054$
    *   $\frac{\partial C}{\partial b} = \delta = -0.0527$
4.  **Perform Weight Update:**
    *   $w_{new} = w - \eta \frac{\partial C}{\partial w} = 0.5 - (0.1)(-0.1054) = 0.51054$
    *   $b_{new} = b - \eta \frac{\partial C}{\partial b} = 0 - (0.1)(-0.0527) = 0.00527$

### Example 2: Simple 3-Layer MLP Chain
Let an input $a^{(0)} = 1$ pass through $w^{(1)} = 2 \implies a^{(1)} \implies w^{(2)} = 0.5 \implies a^{(2)}$.
Assume linear activations $\sigma(z) = z \implies \sigma'(z) = 1$ for simplicity. Let $b^{(1)} = b^{(2)} = 0$.
The cost function is $C = \frac{1}{2}(a^{(2)} - y)^2$ with target $y = 3$.
1.  **Forward Pass:**
    *   $z^{(1)} = w^{(1)} a^{(0)} = 2(1) = 2 \implies a^{(1)} = 2$
    *   $z^{(2)} = w^{(2)} a^{(1)} = (0.5)(2) = 1 \implies a^{(2)} = 1$
    *   $C = \frac{1}{2}(1 - 3)^2 = 2$
2.  **Backward Pass:**
    *   $\delta^{(2)} = (a^{(2)} - y) \cdot 1 = (1 - 3) = -2$
    *   $\delta^{(1)} = \left( (w^{(2)})^T \delta^{(2)} \right) \cdot 1 = (0.5)(-2) = -1$
3.  **Compute Gradients:**
    *   $\frac{\partial C}{\partial w^{(2)}} = \delta^{(2)} a^{(1)} = (-2)(2) = -4$
    *   $\frac{\partial C}{\partial w^{(1)}} = \delta^{(1)} a^{(0)} = (-1)(1) = -1$

---

## 5. Applied ML Context

1.  **Autograd Systems (PyTorch / TensorFlow):** Modern deep learning frameworks build dynamic computation graphs during the forward pass. Calling `.backward()` executes reverse-mode automatic differentiation, computing the backpropagation equations automatically.
2.  **Vanishing Gradients:** If we use Sigmoid activations, their derivative $\sigma'(z)$ peaks at $0.25$. Multiplying these values recursively across many hidden layers causes the error signal $\delta^{(l)}$ to vanish as it reaches early layers, halting training.
3.  **Mini-Batch Gradient Aggregation:** During standard training, we run backpropagation over a batch of $B$ samples. The final weight gradient is the average of the individual sample gradients: $\frac{\partial C}{\partial W^{(l)}} = \frac{1}{B} \sum_{b=1}^B \delta_b^{(l)} (a_b^{(l-1)})^T$.
4.  **Backpropagation Through Time (BPTT):** In recurrent neural networks (RNNs), the model is unrolled across time steps. BPTT applies standard backpropagation backward through the temporal dependencies to compute gradients for shared weights.
5.  **Integrated Gradients for Model Interpretability:** To understand feature attribution, we integrate the gradients of a model's prediction with respect to input pixels ($\frac{\partial y}{\partial x}$), which are computed by running backpropagation all the way back to the input layer.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the dual-pass information flow of backpropagation:
*   Show a sequence of layers: Input Layer $a^{(0)}$, Hidden Layer $a^{(1)}$, and Output Layer $a^{(2)}$ culminating in a Loss $C$.
*   Draw blue arrows pointing from left to right to illustrate the **Forward Pass**. Label them with equations showing activations propagating forward: $z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)} \to a^{(l)} = \sigma(z^{(l)})$.
*   Draw red arrows pointing from right to left to illustrate the **Backward Pass**. Show the output error signal $\delta^{(2)}$ flowing backward.
*   Show how $\delta^{(2)}$ is transformed by $(W^{(2)})^T$ and scaled by $\sigma'(z^{(1)})$ to compute $\delta^{(1)}$, visualizing how the error signal propagates recursively.
*   Draw vertical branches at each layer showing the local gradient computation: $\frac{\partial C}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T$, highlighting that gradients are computed locally by combining incoming activations and backward-flowing error signals.
