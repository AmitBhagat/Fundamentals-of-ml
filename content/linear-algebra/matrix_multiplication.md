---
title: "Matrix Multiplication"
description: "Inner products, outer products, composition of linear maps, and different perspectives of matrix multiplication."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Matrices"]
---

<h1 align="center"> Chapter 19: Matrix Multiplication </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Dot Products:** Understanding how to compute the inner product of two vectors.
* **Matrix Transpose:** Knowing that transposing swaps rows and columns.

</div>

## 1. Conceptual Hook

In machine learning, we often write a single line of code—like `y = x @ W` in Python or `y = tf.matmul(x, W)`—that triggers billions of individual numerical calculations. This operation is **matrix multiplication**, the computational workhorse of deep learning.

Matrix multiplication is more than just nested loops that multiply and add numbers. In ML, we think of it as the **composition of linear maps** or the **simultaneous projection of batches of data**. When a model processes a batch of inputs, matrix multiplication applies the learned rules (stored in the weight matrix) to all inputs in parallel. It is the language of collective transformation, allowing us to project inputs to hidden representations, compute attention maps, and compress high-dimensional states.

---

## 2. Formal Definition

Let $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$ be two matrices. The matrix product $C = AB \in \mathbb{R}^{m \times p}$ is a matrix whose elements $c_{ij}$ are defined by:
$$c_{ij} = \sum_{k=1}^n a_{ik} b_{kj} \quad \text{for } i=1, \dots, m, \quad j=1, \dots, p$$
The product is defined if and only if the inner dimensions match: the number of columns in $A$ ($n$) must equal the number of rows in $B$ ($n$).

### Algebraic Properties
*   **Associativity:** $A(BC) = (AB)C$ for any matrices with compatible dimensions.
*   **Distributivity:** $A(B + C) = AB + AC$ and $(A + B)C = AC + BC$.
*   **Non-commutativity:** In general, $AB \neq BA$, even if both products are defined and have the same shape.

> **Gotcha:** Because matrix multiplication is non-commutative, the order of operations in your code is critical. For example, in a linear layer, if you represent inputs as row vectors $x \in \mathbb{R}^{1 \times d}$ and weights as $W \in \mathbb{R}^{d \times d_{out}}$, the forward pass is $y = xW$. If you represent inputs as column vectors, the forward pass is $y = Wx$. Swapping these will result in dimension mismatch errors.

---

## 3. Illustrative Derivation

### The Four Perspectives of Matrix Multiplication
While the standard definition focuses on row-column inner products, there are four mathematically equivalent ways to interpret the product $C = AB$:

1.  **Row-Column (Inner Product) View:** Each element $c_{ij}$ is the dot product of the $i$-th row of $A$ (denoted $a_{i, \cdot}$) and the $j$-th column of $B$ (denoted $b_{\cdot, j}$):
    $$c_{ij} = a_{i, \cdot} b_{\cdot, j}$$
2.  **Column Combination View:** The $j$-th column of $C$ is a linear combination of the columns of $A$, weighted by the entries of the $j$-th column of $B$:
    $$c_{\cdot, j} = A b_{\cdot, j} = \sum_{k=1}^n b_{kj} a_{\cdot, k}$$
3.  **Row Combination View:** The $i$-th row of $C$ is a linear combination of the rows of $B$, weighted by the entries of the $i$-th row of $A$:
    $$c_{i, \cdot} = a_{i, \cdot} B = \sum_{k=1}^n a_{ik} b_{k, \cdot}$$
4.  **Outer Product (Sum of Rank-1 Matrices) View:** $C$ is the sum of the outer products of the columns of $A$ and the rows of $B$:
    $$C = \sum_{k=1}^n a_{\cdot, k} b_{k, \cdot}$$

**Theorem:** Prove that the Outer Product View is equivalent to the standard coordinate-wise definition of matrix multiplication.

*Proof:*
Let $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$. The $k$-th column of $A$ is $a_{\cdot, k} \in \mathbb{R}^m$, and the $k$-th row of $B$ is $b_{k, \cdot} \in \mathbb{R}^{1 \times p}$.
The outer product of $a_{\cdot, k}$ and $b_{k, \cdot}$ is an $m \times p$ matrix $M^{(k)} = a_{\cdot, k} b_{k, \cdot}$ whose $(i, j)$-th entry is:
$$M^{(k)}_{ij} = (a_{\cdot, k})_i \cdot (b_{k, \cdot})_j = a_{ik} b_{kj}$$

Summing these rank-1 matrices over all $k=1, \dots, n$:
$$\left( \sum_{k=1}^n a_{\cdot, k} b_{k, \cdot} \right)_{ij} = \sum_{k=1}^n M^{(k)}_{ij} = \sum_{k=1}^n a_{ik} b_{kj}$$
This expression is exactly the standard definition of the entry $c_{ij}$ in the matrix product $C = AB$. Thus:
$$AB = \sum_{k=1}^n a_{\cdot, k} b_{k, \cdot}$$
This completes the proof. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Standard Inner Product View
Multiply $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ by $B = \begin{pmatrix} 2 & 0 \\ 1 & 3 \end{pmatrix}$.
1. **Compute each element $c_{ij}$:**
   * $c_{11} = \text{row}_1(A) \cdot \text{col}_1(B) = (1)(2) + (2)(1) = 4$
   * $c_{12} = \text{row}_1(A) \cdot \text{col}_2(B) = (1)(0) + (2)(3) = 6$
   * $c_{21} = \text{row}_2(A) \cdot \text{col}_1(B) = (3)(2) + (4)(1) = 10$
   * $c_{22} = \text{row}_2(A) \cdot \text{col}_2(B) = (3)(0) + (4)(3) = 12$
2. **Form the product matrix $C$:**
   $$C = \begin{pmatrix} 4 & 6 \\ 10 & 12 \end{pmatrix}$$

### Example 2: Outer Product Reconstruction
Using the same matrices, reconstruct $C$ using the outer product view:
$$C = a_{\cdot, 1} b_{1, \cdot} + a_{\cdot, 2} b_{2, \cdot}$$
1. **Identify columns of $A$ and rows of $B$:**
   $$a_{\cdot, 1} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}, \quad b_{1, \cdot} = \begin{bmatrix} 2, & 0 \end{bmatrix}$$
   $$a_{\cdot, 2} = \begin{bmatrix} 2 \\ 4 \end{bmatrix}, \quad b_{2, \cdot} = \begin{bmatrix} 1, & 3 \end{bmatrix}$$
2. **Compute outer products:**
   $$a_{\cdot, 1} b_{1, \cdot} = \begin{bmatrix} 1 \\ 3 \end{bmatrix} \begin{bmatrix} 2, & 0 \end{bmatrix} = \begin{pmatrix} 2 & 0 \\ 6 & 0 \end{pmatrix}$$
   $$a_{\cdot, 2} b_{2, \cdot} = \begin{bmatrix} 2 \\ 4 \end{bmatrix} \begin{bmatrix} 1, & 3 \end{bmatrix} = \begin{pmatrix} 2 & 6 \\ 4 & 12 \end{pmatrix}$$
3. **Sum the matrices:**
   $$C = \begin{pmatrix} 2 & 0 \\ 6 & 0 \end{pmatrix} + \begin{pmatrix} 2 & 6 \\ 4 & 12 \end{pmatrix} = \begin{pmatrix} 4 & 6 \\ 10 & 12 \end{pmatrix}$$
This matches the result from Example 1, demonstrating the outer product perspective.

---

## 5. Applied ML Context

1.  **Fully Connected Layers:** In a feedforward layer, a batch of $m$ inputs $X \in \mathbb{R}^{m \times d_{in}}$ is multiplied by the transposed weight matrix $W^T \in \mathbb{R}^{d_{in} \times d_{out}}$: $Y = XW^T + b$. This computes the activations for all batch elements simultaneously.
2.  **Efficient Convolution (im2col):** While convolutions are mathematically distinct, modern deep learning frameworks unroll the input image and kernel tensors into large matrices (using the `im2col` operation). The convolution is then computed as a single General Matrix Multiply (GEMM) operation, utilizing highly optimized GPU hardware (e.g., NVIDIA Tensor Cores).
3.  **Transformer Self-Attention:** The self-attention block computes token similarities using a matrix product of queries ($Q \in \mathbb{R}^{n \times d_k}$) and keys ($K \in \mathbb{R}^{n \times d_k}$): $\text{Score} = QK^T$. The output features are computed by multiplying the attention weights by the value matrix: $\text{Output} = \text{Score} \cdot V$.
4.  **Low-Rank Adaptation (LoRA):** In parameter-efficient fine-tuning of Large Language Models, instead of updating a full weight matrix $W_0 \in \mathbb{R}^{d \times k}$, we freeze $W_0$ and decompose the update $\Delta W$ into the product of two low-rank matrices: $\Delta W = B \cdot A$ where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with rank $r \ll \min(d, k)$. This drastically reduces the number of trainable parameters.
5.  **Graph Neural Networks (GNNs):** Node feature aggregation is computed using the adjacency matrix $A$ and node feature matrix $X$: $X_{new} = A X W$. This propagates information from neighboring nodes in a single parallel step.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the two primary perspectives of matrix multiplication $C = AB$:
*   **The Inner Product View:** Show matrix $A$ on the left and matrix $B$ on top. Highlight the $i$-th row of $A$ sweeping across the $j$-th column of $B$, with arrows converging to the entry $c_{ij}$ in the output matrix $C$.
*   **The Outer Product View:** Show the column vectors of $A$ ($a_{\cdot, k}$) and row vectors of $B$ ($b_{k, \cdot}$) multiplying to form a sequence of full-sized $m \times p$ grids (rank-1 matrices). Show that adding these grids together layer-by-layer yields the final output matrix $C$.
