---
title: "Matrices"
description: "Matrix algebra, linear operators, column space, and linear transformations."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Scalars", "Vectors", "Vector Spaces"]
---

<h1 align="center"> Chapter 17: Matrices </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Vectors:** Understanding ordered lists of coordinates.
* **Linear Combinations:** Combining vectors via scaling and addition.

</div>

## 1. Conceptual Hook

In machine learning, we rarely process data points individually. A neural network layer processes batches of feature vectors, and an image is a large grid of pixel values. To handle these structures at scale, we use a **matrix**.

A matrix is more than just a rectangular spreadsheet of numbers. In linear algebra, a matrix represents a **linear operator**—a set of instructions that stretches, rotates, shears, or projects coordinate spaces. When we multiply a feature vector by a neural network's weight matrix, we are transforming the data into a new coordinate system where it is easier to classify. The matrix is the fundamental engine that performs these space-warping transformations.

---

## 2. Formal Definition

A **matrix** $A \in \mathbb{R}^{m \times n}$ is a rectangular array of real numbers arranged in $m$ rows and $n$ columns:
$$A = \begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{bmatrix}$$
where $a_{ij} \in \mathbb{R}$ represents the element in the $i$-th row and $j$-th column. The set of all $m \times n$ matrices over $\mathbb{R}$ forms a vector space denoted $M_{m,n}(\mathbb{R})$.

For any $A, B \in M_{m,n}(\mathbb{R})$ and scalar $c \in \mathbb{R}$, we define:
1. **Matrix Addition:** $(A + B)_{ij} = a_{ij} + b_{ij}$
2. **Scalar Multiplication:** $(c \cdot A)_{ij} = c \cdot a_{ij}$
3. **Transpose:** The transpose of $A \in \mathbb{R}^{m \times n}$, denoted $A^T \in \mathbb{R}^{n \times m}$, is defined by switching its rows and columns:
   $$(A^T)_{ij} = a_{ji}$$

---

## 3. Illustrative Derivation

### Matrix-Vector Multiplication as a Column Combination
We derive a fundamental concept in machine learning: a matrix-vector product $Ax$ is exactly a linear combination of the column vectors of $A$, weighted by the components of $x$.

Let $A \in \mathbb{R}^{m \times n}$ be represented by its column vectors:
$$A = \begin{bmatrix} a_1 & a_2 & \dots & a_n \end{bmatrix}$$
where each $a_j = [a_{1j}, a_{2j}, \dots, a_{mj}]^T \in \mathbb{R}^m$ is the $j$-th column vector.
Let $x = [x_1, x_2, \dots, x_n]^T \in \mathbb{R}^n$ be a vector. The matrix-vector product $y = Ax \in \mathbb{R}^m$ is defined by:
$$y_i = \sum_{j=1}^n a_{ij} x_j \quad \text{for } i=1, \dots, m$$

Expanding this term coordinate by coordinate:
$$y = \begin{bmatrix} \sum_{j=1}^n a_{1j} x_j \\ \sum_{j=1}^n a_{2j} x_j \\ \vdots \\ \sum_{j=1}^n a_{mj} x_j \end{bmatrix} = \begin{bmatrix} a_{11}x_1 + a_{12}x_2 + \dots + a_{1n}x_n \\ a_{21}x_1 + a_{22}x_2 + \dots + a_{2n}x_n \\ \vdots \\ a_{m1}x_1 + a_{m2}x_2 + \dots + a_{mn}x_n \end{bmatrix}$$

Grouping by the scalars $x_j$:
$$y = x_1 \begin{bmatrix} a_{11} \\ a_{21} \\ \vdots \\ a_{m1} \end{bmatrix} + x_2 \begin{bmatrix} a_{12} \\ a_{22} \\ \vdots \\ a_{m2} \end{bmatrix} + \dots + x_n \begin{bmatrix} a_{1n} \\ a_{2n} \\ \vdots \\ a_{mn} \end{bmatrix}$$
$$y = \sum_{j=1}^n x_j a_j$$
This shows that $Ax$ is a linear combination of the columns of $A$. The output vector $Ax$ must lie in the subspace spanned by the columns of $A$ (known as the **column space** or **image** of $A$, denoted $\text{Im}(A)$). $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Product as a Column Combination
Let $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $x = \begin{bmatrix} 2 \\ -1 \end{bmatrix}$.
1. **Compute $Ax$ directly:**
   $$Ax = \begin{bmatrix} 1(2) + 2(-1) \\ 3(2) + 4(-1) \end{bmatrix} = \begin{bmatrix} 0 \\ 2 \end{bmatrix}$$
2. **Recompute as a column combination:**
   $$Ax = 2 \begin{bmatrix} 1 \\ 3 \end{bmatrix} - 1 \begin{bmatrix} 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 2(1) - 2 \\ 2(3) - 4 \end{bmatrix} = \begin{bmatrix} 0 \\ 2 \end{bmatrix}$$
Both methods yield the same output, verifying the column combination perspective.

### Example 2: Transposing a Matrix-Vector Product
Verify the identity $(Ax)^T = x^T A^T$ using the parameters from Example 1.
1. **Compute $(Ax)^T$:**
   $$(Ax)^T = \begin{bmatrix} 0 \\ 2 \end{bmatrix}^T = \begin{bmatrix} 0, & 2 \end{bmatrix}$$
2. **Compute $x^T A^T$:**
   $$x^T = \begin{bmatrix} 2, & -1 \end{bmatrix}, \quad A^T = \begin{pmatrix} 1 & 3 \\ 2 & 4 \end{pmatrix}$$
   $$x^T A^T = \begin{bmatrix} 2(1) - 1(2), & 2(3) - 1(4) \end{bmatrix} = \begin{bmatrix} 0, & 2 \end{bmatrix}$$
The identity holds. In ML, transposing products is a frequent step when converting batch vector operations between row-vector formats and column-vector formats.

---

## 5. Applied ML Context

1.  **Image Representation:** A grayscale image is represented as a matrix $I \in \mathbb{R}^{H \times W}$, where each element $I_{ij}$ is the pixel intensity. Color images are represented as 3D matrices (tensors) of size $H \times W \times 3$ representing RGB channels.
2.  **Neural Network Weights:** The feedforward step in a neural network layer is formulated as $y = g(Wx + b)$, where $W \in \mathbb{R}^{d_{out} \times d_{in}}$ is the weight matrix containing the connection strengths between layers.
3.  **Covariance Matrices:** For a zero-mean design matrix $X \in \mathbb{R}^{n \times d}$, the empirical covariance matrix is $\Sigma = \frac{1}{n} X^T X \in \mathbb{R}^{d \times d}$. The entries $\Sigma_{ij}$ represent the covariance between feature $i$ and feature $j$.
4.  **Attention Map Calculation:** In Transformer blocks, the query and key token representations are grouped into matrices $Q$ and $K$. The product $QK^T$ generates the raw attention alignment score matrix.
5.  **Markov State Transitions:** In stochastic systems, transition probabilities are represented as a transition matrix $P$, where $P_{ij} = P(X_{t+1} = j \mid X_t = i)$. The state probability distribution at step $t$ is updated via $p_{t+1} = P^T p_t$.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the geometric action of a matrix $A = [a_1 \quad a_2]$ as a space-warping linear operator in $\mathbb{R}^2$:
*   Show a standard 2D grid with unit basis vectors $e_1 = [1, 0]^T$ and $e_2 = [0, 1]^T$ forming a unit square.
*   Next to it, show the transformed grid under the action of the matrix $A = \begin{pmatrix} 2 & 1 \\ 0 & 1.5 \end{pmatrix}$. 
*   Illustrate how the unit square transforms into a sheared parallelogram, where the basis vectors $e_1$ and $e_2$ are mapped directly to the column vectors $a_1 = [2, 0]^T$ and $a_2 = [1, 1.5]^T$, visualizing how the columns of a matrix define the destination of the standard coordinate axes.
