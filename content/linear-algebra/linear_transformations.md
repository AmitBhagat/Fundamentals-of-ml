---
title: "Linear Transformations"
description: "Linear mappings, kernel and image subspaces, matrix representations, and the Rank-Nullity Theorem."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Vector Spaces", "Matrices"]
---

<h1 align="center"> Chapter 16: Linear Transformations </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Vector Spaces:** Understanding sets closed under addition and scaling.
* **Matrix Operations:** Familiarity with matrix-vector products.

</div>

## 1. Conceptual Hook

When we feed data through a neural network, we do not want the layers to merely scramble the input numbers. We want the layers to reshape the features systematically—rotating them to align with critical factors, stretching them to amplify features, or squashing them to discard noise. The mathematical framework that performs this space-warping is the **linear transformation**.

A linear transformation is a geometric mapping that moves vectors from one space to another without tearing the space. It keeps grid lines straight and parallel, and it keeps the origin fixed. In machine learning, a neural network layer is a sequence of these linear transformations (represented as weight matrix products) paired with non-linear activation functions. By analyzing these transformations, we can understand how models extract latent patterns and map raw inputs to predictions.

---

## 2. Formal Definition

Let $V$ and $W$ be vector spaces over the same field $\mathbb{F}$. A mapping $T: V \to W$ is a **linear transformation** (or linear map) if it satisfies the following two properties for all $u, v \in V$ and all scalars $c \in \mathbb{F}$:

1.  **Additivity:**
    $$T(u + v) = T(u) + T(v)$$
2.  **Homogeneity:**
    $$T(c \cdot v) = c \cdot T(v)$$

These two conditions can be compressed into a single preservation statement:
$$T(c_1 v_1 + c_2 v_2) = c_1 T(v_1) + c_2 T(v_2) \quad \forall v_1, v_2 \in V, \quad c_1, c_2 \in \mathbb{F}$$

### Fundamental Subspaces of a Linear Map
*   **The Kernel (Null Space), $\ker(T)$:** The set of all vectors in the input space $V$ that map to the zero vector in $W$:
    $$\ker(T) = \{v \in V \mid T(v) = 0_W\}$$
    The kernel is a subspace of $V$.
*   **The Image (Range), $\text{Im}(T)$:** The set of all vectors in the output space $W$ that are reached by applying $T$ to vectors in $V$:
    $$\text{Im}(T) = \{w \in W \mid \exists v \in V \text{ s.t. } T(v) = w\}$$
    The image is a subspace of $W$.

---

## 3. Illustrative Derivation

### The Rank-Nullity Theorem
One of the most important theorems in linear algebra connects the dimensions of the kernel and image of a linear transformation to the dimension of its domain.

**Theorem:** Let $T: V \to W$ be a linear transformation where $V$ is a finite-dimensional vector space. Then:
$$\dim(V) = \dim(\ker(T)) + \dim(\text{Im}(T))$$
In matrix terms, this states that the number of columns in a matrix equals the dimension of its null space plus its rank.

*Proof:*
Let $\dim(V) = n$, and let $\dim(\ker(T)) = k$.
1.  **Construct a basis for the kernel:**
    Since $\ker(T)$ is a subspace of $V$, we can choose a basis for it:
    $$\mathcal{B}_{ker} = \{u_1, u_2, \dots, u_k\}$$
2.  **Extend to a basis of the full space $V$:**
    By the Basis Extension Theorem, we can append $n-k$ vectors to $\mathcal{B}_{ker}$ to form a basis for $V$:
    $$\mathcal{B}_V = \{u_1, \dots, u_k, v_1, \dots, v_{n-k}\}$$
3.  **Show that the mapped vectors span $\text{Im}(T)$:**
    Any vector $x \in V$ can be written as a linear combination of the basis vectors:
    $$x = \sum_{i=1}^k c_i u_i + \sum_{j=1}^{n-k} d_j v_j$$
    Applying the linear map $T$:
    $$T(x) = T\left( \sum_{i=1}^k c_i u_i + \sum_{j=1}^{n-k} d_j v_j \right) = \sum_{i=1}^k c_i T(u_i) + \sum_{j=1}^{n-k} d_j T(v_j)$$
    Since $u_i \in \ker(T)$, we know $T(u_i) = 0$ for all $i$:
    $$T(x) = \sum_{j=1}^{n-k} d_j T(v_j)$$
    This shows that the set of vectors $\{T(v_1), \dots, T(v_{n-k})\}$ spans the image space $\text{Im}(T)$.
4.  **Show that $\{T(v_1), \dots, T(v_{n-k})\}$ is linearly independent:**
    Consider the equation:
    $$\sum_{j=1}^{n-k} a_j T(v_j) = 0$$
    Using the linearity of $T$:
    $$T\left( \sum_{j=1}^{n-k} a_j v_j \right) = 0$$
    This implies that the vector $\sum_{j=1}^{n-k} a_j v_j$ lies in the kernel $\ker(T)$. Therefore, it must be expressible as a linear combination of the kernel basis vectors $\{u_i\}$:
    $$\sum_{j=1}^{n-k} a_j v_j = \sum_{i=1}^k b_i u_i \implies \sum_{j=1}^{n-k} a_j v_j - \sum_{i=1}^k b_i u_i = 0$$
    Since the set $\mathcal{B}_V = \{u_1, \dots, u_k, v_1, \dots, v_{n-k}\}$ is a basis for $V$, its vectors are linearly independent. Thus, all coefficients must be zero:
    $$a_1 = \dots = a_{n-k} = 0 \quad \text{and} \quad b_1 = \dots = b_k = 0$$
    Since $a_j = 0$ for all $j$, the set $\{T(v_1), \dots, T(v_{n-k})\}$ is linearly independent.
5.  **Conclude dimensions:**
    The set $\{T(v_1), \dots, T(v_{n-k})\}$ spans $\text{Im}(T)$ and is independent, meaning it forms a basis of $\text{Im}(T)$. Thus:
    $$\dim(\text{Im}(T)) = n - k = \dim(V) - \dim(\ker(T))$$
    Rearranging terms:
    $$\dim(V) = \dim(\ker(T)) + \dim(\text{Im}(T))$$
This completes the proof. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Projection Mapping
Define the mapping $T: \mathbb{R}^3 \to \mathbb{R}^3$ by $T(x, y, z) = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$.
1.  **Verify linearity:**
    Let $u = [x_1, y_1, z_1]^T$ and $v = [x_2, y_2, z_2]^T$.
    $$T(u+v) = T\left( \begin{bmatrix} x_1 + x_2 \\ y_1 + y_2 \\ z_1 + z_2 \end{bmatrix} \right) = \begin{bmatrix} x_1 + x_2 \\ y_1 + y_2 \\ 0 \end{bmatrix} = \begin{bmatrix} x_1 \\ y_1 \\ 0 \end{bmatrix} + \begin{bmatrix} x_2 \\ y_2 \\ 0 \end{bmatrix} = T(u) + T(v)$$
    Homogeneity follows similarly, proving $T$ is linear.
2.  **Determine Kernel and Image:**
    *   $\ker(T) = \{ [0, 0, z]^T \mid z \in \mathbb{R} \}$, which is the z-axis ($\dim(\ker(T)) = 1$).
    *   $\text{Im}(T) = \{ [x, y, 0]^T \mid x, y \in \mathbb{R} \}$, which is the xy-plane ($\dim(\text{Im}(T)) = 2$).
3.  **Check Rank-Nullity:**
    $$\dim(V) = 3 = \dim(\ker(T)) + \dim(\text{Im}(T)) = 1 + 2 = 3$$

### Example 2: 2D Spatial Rotation
Let $T_\theta: \mathbb{R}^2 \to \mathbb{R}^2$ be the counterclockwise rotation by angle $\theta$. The matrix representation is:
$$R_\theta = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$
Let $\theta = \frac{\pi}{2}$ (rotation by $90^\circ$):
$$R_{\pi/2} = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$$
Applying this transformation to vector $v = \begin{bmatrix} 3 \\ 1 \end{bmatrix}$:
$$T(v) = R_{\pi/2} v = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} (0)(3) + (-1)(1) \\ (1)(3) + (0)(1) \end{bmatrix} = \begin{bmatrix} -1 \\ 3 \end{bmatrix}$$
The vector $[3, 1]^T$ is rotated to $[-1, 3]^T$, preserving its length ($\|v\|_2 = \sqrt{10}$) while changing its direction, illustrating a rotation transformation.

---

## 5. Applied ML Context

1.  **Fully Connected Layers:** A feedforward neural network layer projects input activations $x \in \mathbb{R}^{d_{in}}$ to a new feature space via $y = Wx + b$. The matrix product $Wx$ is the linear transformation component.
2.  **Self-Attention Projections:** In Transformers, input token embeddings $X$ are projected using three linear transformations $W_Q, W_K, W_V$ to create query, key, and value matrices ($Q = XW_Q, K = XW_K, V = XW_V$).
3.  **Kernel (Null Space) Information Loss:** The null space of a neural network's weight matrix $W$ contains all input signals that map to zero. Identifying the kernel reveals exactly what features the network discards.
4.  **PCA (Principal Component Analysis):** PCA calculates a linear transformation matrix that rotates the input data coordinates so that the axes align with the directions of maximum variance.
5.  **Data Augmentation (Vision):** Affine transformations (rotation, scaling, translation, shearing) are applied to training images to create synthetic variations, helping models generalize better.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the visual properties of linear transformations:
*   Show a standard 2D Cartesian grid with a unit circle.
*   Draw a transformed grid after applying the shearing transformation matrix $A = \begin{pmatrix} 1 & 1.5 \\ 0 & 1 \end{pmatrix}$.
*   Highlight that:
    1.  The grid origin $(0, 0)$ remains perfectly fixed.
    2.  All straight lines in the original grid remain straight.
    3.  All parallel lines in the original grid remain parallel.
    4.  The unit circle transforms into an elongated ellipse.
*   Add a warning label illustrating a non-linear transformation (like a warped grid with curved lines or shifted origin) to visually contrast linear vs. non-linear mappings.
