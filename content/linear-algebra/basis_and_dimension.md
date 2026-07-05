---
title: "Basis and Dimension"
description: "Linear independence, spanning sets, unique representations, and coordinate transformations."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Linear Independence", "Vector Spaces"]
---

<h1 align="center"> Chapter 11: Basis and Dimension </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Linear Independence:** Knowing when a set of vectors contains no redundancies.
* **Vector Spaces & Span:** Understanding closure and how linear combinations cover space.

</div>

## 1. Conceptual Hook

In machine learning, we often work with massive datasets containing thousands of features (e.g., pixel intensities in images or word occurrences in text). However, much of this raw data is highly redundant. To analyze and process this information efficiently, we must find the **minimum set of independent features** needed to represent our data without losing any information. This set is a **basis**, and the size of this set is the **dimension** of our representation space.

Think of a basis as the "leanest possible shopping list" of unique ingredients needed to cook every recipe in a cookbook. If you have two different brands of the exact same salt, your list is redundant. In ML, a basis represents the primary coordinate axes of our data space (such as principal components in PCA or latent factors in recommendation systems), while the dimension tells us the intrinsic complexity and capacity of our models.

---

## 2. Formal Definition

Let $V$ be a vector space over a field $\mathbb{F}$. A set of vectors $\mathcal{B} = \{v_1, v_2, \dots, v_n\} \subset V$ is a **basis** of $V$ if it satisfies two conditions:
1. **Linear Independence:** The only linear combination of $\{v_i\}$ that equals the zero vector is the trivial one:
   $$\sum_{i=1}^n c_i v_i = 0 \implies c_1 = c_2 = \dots = c_n = 0$$
2. **Spanning Property:** Every vector in $V$ can be written as a linear combination of vectors in $\mathcal{B}$:
   $$\text{span}(\mathcal{B}) = V \iff \forall x \in V, \exists c_1, \dots, c_n \in \mathbb{F} \quad \text{s.t.} \quad x = \sum_{i=1}^n c_i v_i$$

The **dimension** of $V$, denoted $\dim(V)$, is the cardinality (number of elements) of its basis $\mathcal{B}$:
$$\dim(V) = |\mathcal{B}| = n$$

### Uniqueness of Representation Theorem
**Theorem:** If $\mathcal{B} = \{v_1, \dots, v_n\}$ is a basis of $V$, then every vector $x \in V$ can be expressed in the form $x = \sum_{i=1}^n c_i v_i$ in exactly one way.

*Proof:*
Suppose a vector $x$ has two different representations under the basis $\mathcal{B}$:
$$x = \sum_{i=1}^n a_i v_i \quad \text{and} \quad x = \sum_{i=1}^n b_i v_i$$
Subtracting these two equations:
$$x - x = \sum_{i=1}^n a_i v_i - \sum_{i=1}^n b_i v_i$$
$$0 = \sum_{i=1}^n (a_i - b_i) v_i$$
Since $\mathcal{B}$ is a basis, its vectors are linearly independent. By definition of linear independence, the coefficients of this linear combination must all be zero:
$$a_i - b_i = 0 \quad \forall i=1, \dots, n \implies a_i = b_i \quad \forall i=1, \dots, n$$
Thus, the coefficients are unique. $\blacksquare$

---

## 3. Illustrative Derivation

### Coordinate Transformations (Change of Basis)
In ML, we often transform data from a standard basis to a more informative one (e.g., projecting features onto principal components). Let us derive the change of basis transition matrix.

Let $\mathcal{B} = \{v_1, \dots, v_n\}$ and $\mathcal{C} = \{w_1, \dots, w_n\}$ be two bases of an $n$-dimensional space $V$. Any vector $x \in V$ can be represented in both bases:
$$x = \sum_{j=1}^n [x]_\mathcal{B}^j v_j \quad \text{and} \quad x = \sum_{i=1}^n [x]_\mathcal{C}^i w_i$$
where $[x]_\mathcal{B} \in \mathbb{F}^n$ and $[x]_\mathcal{C} \in \mathbb{F}^n$ are the coordinate vectors.

We can express each basis vector $v_j$ of the basis $\mathcal{B}$ as a linear combination of the basis vectors in $\mathcal{C}$:
$$v_j = \sum_{i=1}^n P_{ij} w_i$$
Substitute this representation of $v_j$ back into the equation for $x$:
$$x = \sum_{j=1}^n [x]_\mathcal{B}^j \left( \sum_{i=1}^n P_{ij} w_i \right) = \sum_{i=1}^n \left( \sum_{j=1}^n P_{ij} [x]_\mathcal{B}^j \right) w_i$$
By uniqueness of coordinate representations under basis $\mathcal{C}$:
$$[x]_\mathcal{C}^i = \sum_{j=1}^n P_{ij} [x]_\mathcal{B}^j \quad \forall i=1, \dots, n$$
In matrix form:
$$[x]_\mathcal{C} = P [x]_\mathcal{B}$$
where $P \in \mathbb{F}^{n \times n}$ is the transition matrix whose columns are the coordinates of the "old" basis vectors $\mathcal{B}$ written in terms of the "new" basis $\mathcal{C}$:
$$P = \Big[ \, [v_1]_\mathcal{C} \quad [v_2]_\mathcal{C} \quad \dots \quad [v_n]_\mathcal{C} \, \Big]$$
Since $\mathcal{B}$ and $\mathcal{C}$ are bases, the transition matrix $P$ is always invertible, and the reverse transformation is $[x]_\mathcal{B} = P^{-1} [x]_\mathcal{C}$.

---

## 4. Concrete Examples

### Example 1: Coordinate Conversion
Let the standard basis of $\mathbb{R}^2$ be $\mathcal{E} = \{e_1, e_2\} = \{\begin{bmatrix} 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \end{bmatrix}\}$, and let a new basis be $\mathcal{B} = \{b_1, b_2\} = \{\begin{bmatrix} 2 \\ 1 \end{bmatrix}, \begin{bmatrix} 1 \\ 2 \end{bmatrix}\}$.
Find the coordinate vector $[x]_\mathcal{B}$ for the standard vector $x = \begin{bmatrix} 5 \\ 4 \end{bmatrix}$.

1. **Set up the system $x = c_1 b_1 + c_2 b_2$:**
   $$\begin{bmatrix} 5 \\ 4 \end{bmatrix} = c_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + c_2 \begin{bmatrix} 1 \\ 2 \end{bmatrix} \implies \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix} \begin{bmatrix} c_1 \\ c_2 \end{bmatrix} = \begin{bmatrix} 5 \\ 4 \end{bmatrix}$$
2. **Solve using matrix inversion:**
   The transition matrix from $\mathcal{B}$ to $\mathcal{E}$ is $P = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$. Its determinant is $2(2) - 1(1) = 3$.
   $$P^{-1} = \frac{1}{3} \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$$
   $$[x]_\mathcal{B} = P^{-1} x = \frac{1}{3} \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix} \begin{bmatrix} 5 \\ 4 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 10 - 4 \\ -5 + 8 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$$
   This shows that the vector $x = 5e_1 + 4e_2$ is represented as $2b_1 + 1b_2$ under the basis $\mathcal{B}$.

### Example 2: Spanning Set Check
Verify whether the set $\mathcal{A} = \{a_1, a_2\} = \{\begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}\}$ forms a basis for $\mathbb{R}^3$.
1. **Compare Dimension to Cardinality:**
   The dimension of the vector space $\mathbb{R}^3$ is $\dim(\mathbb{R}^3) = 3$.
   The number of vectors in $\mathcal{A}$ is $|\mathcal{A}| = 2$.
2. **Apply Dimension Theorem:**
   Any spanning set of $\mathbb{R}^3$ must contain at least $\dim(\mathbb{R}^3) = 3$ vectors. Since $|\mathcal{A}| < 3$, the set cannot span $\mathbb{R}^3$. Specifically, any vector with a non-zero first coordinate and zero second coordinate (e.g., $x = [1, 0, 0]^T$) cannot be written as a linear combination of $a_1$ and $a_2$. Thus, $\mathcal{A}$ is not a basis for $\mathbb{R}^3$.

---

## 5. Applied ML Context

1.  **Principal Component Analysis (PCA):** PCA finds an orthogonal basis of the feature space aligned with the directions of maximum variance. Projecting data onto the first $k$ eigenvectors of the covariance matrix reduces the dimension of the space from $d$ to $k$, filtering out noise.
2.  **Autoencoder Latent Dimension:** The bottleneck layer in an autoencoder acts as a compressed, non-linear coordinate space. The dimension of this bottleneck dictates the compression ratio and capacity of the network to reconstruct complex inputs.
3.  **Matrix Rank in Recommendation Systems:** In collaborative filtering, the user-item rating matrix is assumed to have a low rank $k$. This rank $k$ is the dimension of the latent factor space (e.g., movie genres or user preferences) that governs user ratings.
4.  **Multicollinearity Diagnostics:** If features in a dataset are not linearly independent (e.g., if one feature is a linear combination of others), the covariance matrix will not have full rank. This makes it impossible to compute its inverse, causing regression algorithms to fail.
5.  **Kernel Methods in SVMs:** Standard support vector machines fail when data is not linearly separable. By using the kernel trick, we implicitly map the data into a higher-dimensional space with a larger basis, allowing the model to construct a linear separating boundary.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here visualizing basis spans and dimension:
*   Show a 3D coordinate system ($x, y, z$).
*   Plot a 2D tilted plane passing through the origin. Label this plane as "Subspace $W$, $\dim(W) = 2$."
*   Plot two linearly independent vectors $b_1$ and $b_2$ lying on this plane. Show that any point on the plane can be reached via a linear combination of $b_1$ and $b_2$, proving they form a basis for $W$.
*   Plot a third vector $b_3$ that sticks out of the plane into the 3D space. Illustrate that to span the full 3D space $\mathbb{R}^3$, we must expand our basis to $\{b_1, b_2, b_3\}$, increasing the dimension of our coordinate representation to 3.
