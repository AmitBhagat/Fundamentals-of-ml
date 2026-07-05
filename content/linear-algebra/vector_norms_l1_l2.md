---
title: "Vector Norms (L1, L2)"
description: "Mathematical axioms of norms, L1 Manhattan and L2 Euclidean geometry, and regularization properties."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Scalars", "Vectors"]
---

<h1 align="center"> Chapter 26: Vector Norms (L1, L2) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Vectors:** Understanding coordinate representations of points in space.
* **Calculus basics:** Familiarity with derivatives and gradients.

</div>

## 1. Conceptual Hook

In machine learning, we are constantly trying to balance two opposing forces: making our models fit the training data, and keeping them simple enough to generalize to new, unseen data. To control the complexity of a model, we need a mathematical ruler that can measure the "size" or "magnitude" of the model's weight parameters. This ruler is a **vector norm**.

A vector norm collapses a multi-dimensional vector into a single real number representing its magnitude. Depending on which ruler we choose, we get vastly different learning behaviors. The **$L_1$ norm** (sum of absolute values) acts like a strict editor, forcing less important weights to become exactly zero, thereby selecting only the most vital features. The **$L_2$ norm** (Euclidean distance) acts like a stabilizer, shrinking all weights smoothly and preventing any single feature from dominating the network.

---

## 2. Formal Definition

Let $V$ be a vector space over a field $\mathbb{F}$ (where $\mathbb{F} \in \{\mathbb{R}, \mathbb{C}\}$). A **norm** on $V$ is a function $\|\cdot\|: V \to \mathbb{R}$ that satisfies the following three axioms for all $u, v \in V$ and all scalars $c \in \mathbb{F}$:

1.  **Non-negativity and Definiteness:**
    $$\|v\| \ge 0 \quad \forall v \in V, \quad \text{and} \quad \|v\| = 0 \iff v = 0$$
2.  **Absolute Homogeneity:**
    $$\|c \cdot v\| = |c| \cdot \|v\|$$
3.  **Triangle Inequality:**
    $$\|u + v\| \le \|u\| + \|v\|$$

For a coordinate vector $x = [x_1, \dots, x_n]^T \in \mathbb{R}^n$, the family of **$L_p$ norms** for $p \ge 1$ is defined as:
$$\|x\|_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p}$$

*   **The $L_1$ Norm (Manhattan or Taxicab Norm):** Obtained by setting $p=1$:
    $$\|x\|_1 = \sum_{i=1}^n |x_i|$$
*   **The $L_2$ Norm (Euclidean Norm):** Obtained by setting $p=2$:
    $$\|x\|_2 = \sqrt{\sum_{i=1}^n x_i^2}$$

---

## 3. Illustrative Derivation

### Sparsity of $L_1$ vs. Smoothness of $L_2$
Why does the $L_1$ norm produce sparse solutions (weights exactly zero) while the $L_2$ norm does not? We can understand this by looking at their gradients.

Let $w \in \mathbb{R}^n$ be the weight vector of a model.
1.  **Gradient of the squared $L_2$ norm:**
    Let $f_2(w) = \frac{1}{2} \|w\|_2^2 = \frac{1}{2} \sum_{i=1}^n w_i^2$. This function is differentiable everywhere:
    $$\frac{\partial f_2}{\partial w_i} = w_i \implies \nabla_w \left( \frac{1}{2} \|w\|_2^2 \right) = w$$
    As the weight $w_i$ gets closer to zero, the gradient $w_i$ also approaches zero. The update step under gradient descent becomes infinitesimally small:
    $$w_i^{(t+1)} = w_i^{(t)} - \eta w_i^{(t)} = (1 - \eta) w_i^{(t)}$$
    This shrinks the weights exponentially toward zero but never forces them to be exactly zero.

2.  **Gradient of the $L_1$ norm:**
    Let $f_1(w) = \|w\|_1 = \sum_{i=1}^n |w_i|$. This function is non-differentiable at $w_i = 0$. For $w_i \neq 0$:
    $$\frac{\partial f_1}{\partial w_i} = \text{sign}(w_i) = \begin{cases} 1 & \text{if } w_i > 0 \\ -1 & \text{if } w_i < 0 \end{cases}$$
    At $w_i = 0$, we must use the **subgradient**, which is the interval $[-1, 1]$.
    Under gradient descent, the update step for $w_i \neq 0$ is:
    $$w_i^{(t+1)} = w_i^{(t)} - \eta \cdot \text{sign}(w_i^{(t)})$$
    Notice that the step size is constant ($\eta$) and does not shrink as $w_i$ approaches zero. This constant force pushes the weight directly to zero. Once a weight hits zero, the subgradient allows it to remain exactly zero if the loss gradient is not strong enough to pull it away. This explains why $L_1$ regularization performs feature selection.

---

## 4. Concrete Examples

### Example 1: $L_1$ and $L_2$ Magnitude Comparison
Let two weight vectors be $w_1 = \begin{bmatrix} 3 \\ 0 \\ 4 \end{bmatrix}$ (sparse, one feature active) and $w_2 = \begin{bmatrix} 2.5 \\ 2.5 \\ 2 \end{bmatrix}$ (dense, distributed weights).
1.  **Compute $L_1$ Norms:**
    $$\|w_1\|_1 = |3| + |0| + |4| = 7$$
    $$\|w_2\|_1 = |2.5| + |2.5| + |2| = 7$$
    Under $L_1$, both models have the same absolute parameter magnitude.
2.  **Compute $L_2$ Norms:**
    $$\|w_1\|_2 = \sqrt{3^2 + 0^2 + 4^2} = \sqrt{25} = 5$$
    $$\|w_2\|_2 = \sqrt{2.5^2 + 2.5^2 + 2^2} = \sqrt{6.25 + 6.25 + 4} = \sqrt{16.5} \approx 4.06$$
    The $L_2$ norm of $w_1$ is higher than $w_2$. Because $L_2$ squares the coordinates, it heavily penalizes large individual weight values ($3$ and $4$), showing that sparse configurations with larger values carry a higher $L_2$ penalty than distributed configurations.

### Example 2: Triangle Inequality Numerical Check
Let $u = \begin{bmatrix} 1 \\ -2 \end{bmatrix}$ and $v = \begin{bmatrix} 3 \\ 1 \end{bmatrix}$. Verify $\|u+v\|_1 \le \|u\|_1 + \|v\|_1$.
1.  **Compute $u+v$:**
    $$u+v = \begin{bmatrix} 1+3 \\ -2+1 \end{bmatrix} = \begin{bmatrix} 4 \\ -1 \end{bmatrix}$$
2.  **Calculate Norms:**
    $$\|u\|_1 = |1| + |-2| = 3$$
    $$\|v\|_1 = |3| + |1| = 4$$
    $$\|u+v\|_1 = |4| + |-1| = 5$$
    Since $5 \le 3 + 4 = 7$, the triangle inequality holds.

---

## 5. Applied ML Context

1.  **LASSO Regularization ($L_1$ Regularization):** Adding the $L_1$ norm of the weights to the loss function ($\mathcal{L}_{lasso} = \mathcal{L}_{data} + \lambda \|w\|_1$) performs automatic feature selection by forcing the weights of non-essential features to become exactly zero.
2.  **Ridge Regularization ($L_2$ Regularization):** Adding the squared $L_2$ norm of the weights ($\mathcal{L}_{ridge} = \mathcal{L}_{data} + \lambda \|w\|_2^2$) prevents overfitting by shrinking the parameter weights towards zero, distributing the importance across features.
3.  **Mean Absolute Error (MAE) Loss:** A loss function defined by the $L_1$ norm of the prediction error vector ($e = y - \hat{y}$): $\text{MAE} = \frac{1}{n} \|e\|_1$. MAE is robust to outliers because it does not square the error terms.
4.  **Mean Squared Error (MSE) Loss:** A loss function defined by the squared $L_2$ norm of the prediction error vector: $\text{MSE} = \frac{1}{n} \|e\|_2^2$. MSE heavily penalizes large errors and is differentiable everywhere, making it highly compatible with standard gradient descent.
5.  **Cosine Similarity:** The cosine of the angle between two vectors $u$ and $v$ is computed by dividing their dot product by the product of their $L_2$ norms: $\text{Sim}(u, v) = \frac{u^T v}{\|u\|_2 \|v\|_2}$. This normalizes the vectors to unit length, evaluating correlation independent of scale.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the unit spheres (contours of equal norm value) for the $L_1$ and $L_2$ norms in $\mathbb{R}^2$:
*   Show a 2D Cartesian coordinate plane ($w_1, w_2$).
*   Plot the **$L_1$ Unit Ball** ($|w_1| + |w_2| = 1$), which forms a sharp **diamond** shape with corners sitting directly on the axes.
*   Plot the **$L_2$ Unit Ball** ($w_1^2 + w_2^2 = 1$), which forms a smooth **circle**.
*   Draw concentric ellipses representing the contours of a loss function $\mathcal{L}(w)$ centered around an optimal point away from the origin. 
*   Illustrate how the loss function contour first touches the $L_1$ diamond at a corner (where $w_1 = 0$ or $w_2 = 0$), demonstrating why $L_1$ induces sparsity. Contrast this with the $L_2$ circle, where the loss contour touches at a smooth, non-axial point.
