---
title: "Matrix Rank"
description: "Row and column spaces, Gaussian elimination, rank inequality proofs, and low-rank representations."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Scalars", "Vectors", "Vector Spaces", "Linear Independence", "Matrices"]
---

<h1 align="center"> Chapter 20: Matrix Rank </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Linear Independence:** Knowing when a set of vectors contains no redundant paths.
* **Subspaces:** Understanding column and row spans.

</div>

## 1. Conceptual Hook

In machine learning, we routinely collect massive tables of data with hundreds of columns and millions of rows. But how many **independent facts** are actually contained within these tables? A dataset might have 100 features, but if several features are highly correlated (such as income, tax bracket, and house value), our data is mathematically crowded with redundant copies of the same underlying information.

The mathematical measure of a matrix's unique information is its **rank**. The rank tells us the number of truly independent dimensions spanned by the matrix's rows or columns. It separates genuine feature signals from redundant variables. By identifying and compressing low-rank structures, we can compress large language models (LoRA), build collaborative filtering recommendation engines, and filter out high-frequency noise from images.

---

## 2. Formal Definition

Let $A \in \mathbb{R}^{m \times n}$ be a matrix.
*   **Column Space ($\text{col}(A)$):** The subspace of $\mathbb{R}^m$ spanned by the column vectors of $A$. The dimension of this space is the **column rank** of $A$.
*   **Row Space ($\text{row}(A)$):** The subspace of $\mathbb{R}^n$ spanned by the row vectors of $A$. The dimension of this space is the **row rank** of $A$.

**Fundamental Theorem of Linear Algebra:** For any matrix $A \in \mathbb{R}^{m \times n}$, the row rank is exactly equal to the column rank. This common dimension is called the **rank** of the matrix, denoted $\text{rank}(A)$:
$$\text{rank}(A) = \dim(\text{col}(A)) = \dim(\text{row}(A))$$

### Core Algebraic Properties
1.  **Dimension Bound:** The rank of a matrix is bounded by its smallest dimension:
    $$\text{rank}(A) \le \min(m, n)$$
2.  **Full Rank:** A matrix is **full rank** if $\text{rank}(A) = \min(m, n)$. If $\text{rank}(A) < \min(m, n)$, it is **rank-deficient**.
3.  **Transpose Rank:** Transposing a matrix preserves its rank:
    $$\text{rank}(A^T) = \text{rank}(A)$$
4.  **Rank-Nullity Connection:** For $A \in \mathbb{R}^{m \times n}$:
    $$\text{rank}(A) + \dim(\ker(A)) = n$$
5.  **Gram Matrix Identity:** The rank of a matrix is identical to the rank of its Gram matrix:
    $$\text{rank}(A^T A) = \text{rank}(A A^T) = \text{rank}(A)$$

---

## 3. Illustrative Derivation

### Proof of the Rank Inequality of Matrix Products
**Theorem:** Let $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$ be two matrices. Prove that the rank of their product is bounded by the rank of each individual matrix:
$$\text{rank}(AB) \le \min(\text{rank}(A), \text{rank}(B))$$

*Proof:*
We prove this in two parts:
1.  **Part 1: Prove $\text{rank}(AB) \le \text{rank}(A)$:**
    Let $y$ be any vector in the column space of the product $AB$. By definition:
    $$y \in \text{col}(AB) \implies \exists x \in \mathbb{R}^p \quad \text{s.t.} \quad y = (AB)x$$
    Using the associative property of matrix-vector products:
    $$y = A(Bx)$$
    Let $z = Bx \in \mathbb{R}^n$. Thus, $y = Az$, which means $y$ is a linear combination of the columns of $A$. This implies that every vector in the column space of $AB$ must lie in the column space of $A$:
    $$\text{col}(AB) \subseteq \text{col}(A)$$
    Since the column space of $AB$ is a subspace of the column space of $A$, its dimension cannot exceed the dimension of $\text{col}(A)$:
    $$\dim(\text{col}(AB)) \le \dim(\text{col}(A)) \implies \text{rank}(AB) \le \text{rank}(A)$$

2.  **Part 2: Prove $\text{rank}(AB) \le \text{rank}(B)$:**
    Using the transpose identity ($\text{rank}(C) = \text{rank}(C^T)$):
    $$\text{rank}(AB) = \text{rank}((AB)^T) = \text{rank}(B^T A^T)$$
    Applying the result from Part 1 to the matrix product $B^T A^T$:
    $$\text{rank}(B^T A^T) \le \text{rank}(B^T)$$
    Since $\text{rank}(B^T) = \text{rank}(B)$, we obtain:
    $$\text{rank}(AB) \le \text{rank}(B)$$

Combining the inequalities from Part 1 and Part 2:
$$\text{rank}(AB) \le \text{rank}(A) \quad \text{and} \quad \text{rank}(AB) \le \text{rank}(B) \implies \text{rank}(AB) \le \min(\text{rank}(A), \text{rank}(B))$$
This completes the proof. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Finding Rank via Row Echelon Form
Determine the rank of the matrix:
$$A = \begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 3 & 5 & 7 \end{pmatrix}$$
Apply Gaussian elimination (elementary row operations):
1.  Subtract twice row 1 from row 2 ($R_2 \leftarrow R_2 - 2R_1$):
    $$\begin{pmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 3 & 5 & 7 \end{pmatrix}$$
2.  Subtract three times row 1 from row 3 ($R_3 \leftarrow R_3 - 3R_1$):
    $$\begin{pmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{pmatrix}$$
3.  Swap row 2 and row 3 ($R_2 \leftrightarrow R_3$) to obtain row echelon form:
    $$\begin{pmatrix} 1 & 2 & 3 \\ 0 & -1 & -2 \\ 0 & 0 & 0 \end{pmatrix}$$
The number of non-zero rows is $2$. Thus, $\text{rank}(A) = 2$. Row 2 of the original matrix was redundant (exactly double row 1).

### Example 2: Rank of an Outer Product (Rank-1 Matrix)
Let $u = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$ and $v = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$. Compute the rank of their outer product matrix $A = uv^T$.
1.  **Calculate the product matrix:**
    $$A = uv^T = \begin{bmatrix} 1 \\ 2 \end{bmatrix} \begin{bmatrix} 3, & 4 \end{bmatrix} = \begin{pmatrix} 3 & 4 \\ 6 & 8 \end{pmatrix}$$
2.  **Evaluate columns:**
    The columns are $a_1 = \begin{bmatrix} 3 \\ 6 \end{bmatrix}$ and $a_2 = \begin{bmatrix} 4 \\ 8 \end{bmatrix}$. Notice that $a_2 = \frac{4}{3} a_1$. Since the columns are collinear, the dimension of the column space is 1. Thus, $\text{rank}(A) = 1$. The outer product of any two non-zero vectors always yields a rank-1 matrix.

---

## 5. Applied ML Context

1.  **Collaborative Filtering (Recommender Systems):** In user-item recommendation algorithms, we represent user ratings in a matrix $R$. We assume $R$ is approximately low-rank, allowing us to factorize it into user and item latent matrices: $R \approx U V^T$, where $U$ and $V$ have a small rank $k$, discovering hidden attributes (e.g. movie genres).
2.  **Low-Rank Adaptation (LoRA):** Instead of fine-tuning the full weight matrix of an LLM ($W \in \mathbb{R}^{d \times k}$), LoRA parameterizes the update matrix $\Delta W$ as the product of two low-rank matrices: $\Delta W = B \cdot A$, where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with $r \ll \min(d, k)$, saving significant GPU training memory.
3.  **Numerical/Effective Rank:** In real-world data, noise prevents matrices from being mathematically rank-deficient. We estimate the **effective rank** by computing the SVD and counting only the singular values that exceed a threshold: $\sigma_i > \epsilon$.
4.  **Multicollinearity Diagnostics:** In OLS linear regression, if the features are linearly dependent, the design matrix $X$ is rank-deficient. The Gram matrix $X^T X$ will not have full rank, making it singular and preventing parameter weight inversion.
5.  **Image Compression:** A high-resolution image is represented as a matrix. Because adjacent pixels are highly correlated, the matrix can be approximated by a low-rank representation using SVD, preserving core features while discarding negligible singular components.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here showing how matrix rank determines output dimensionality:
*   Show a 3D coordinate space containing a sphere representing the input data.
*   Draw three different mapping outcomes under a $3 \times 3$ matrix $A$:
    1.  **Full Rank ($\text{rank}(A) = 3$):** The sphere transforms into a stretched 3D ellipsoid. No dimensions are collapsed.
    2.  **Rank Deficient ($\text{rank}(A) = 2$):** The 3D sphere is compressed entirely flat onto a 2D plane passing through the origin. The dimension orthogonal to the plane is lost.
    3.  **Rank Deficient ($\text{rank}(A) = 1$):** The 3D sphere collapses into a single 1D line passing through the origin, squeezing all 3D coordinates into a single linear span.
*   Annotate each case with its rank value to emphasize that rank is the dimension of the destination subspace.
