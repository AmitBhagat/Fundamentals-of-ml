---
title: "Vector Spaces"
description: "Abstract vector spaces, field axioms, subspaces, and closure properties in machine learning."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Scalars", "Vectors"]
---

<h1 align="center"> Chapter 27: Vector Spaces </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Fields:** Understanding algebraic sets (like $\mathbb{R}$) closed under standard arithmetic operations.
* **Sets and Closure:** Conceptual grasp of sets and operations that stay within those sets.

</div>

## 1. Conceptual Hook

In machine learning, we spend our lives designing and training models that handle high-dimensional representations of images, texts, and user profiles. To perform arithmetic on these representations—to combine features, adjust weights, or search for similar items—we need a structured mathematical environment that behaves consistently. This environment is a **vector space**.

A vector space is a mathematical sandbox. It defines a set of objects (vectors) and a set of rules (axioms) that ensure that no matter how much we add or scale our data, we never "break" the system or escape the boundaries of our space. If we combine two word vectors or scale up a neural network's activations, the results are guaranteed to remain valid coordinates within our representation space. It provides the rigid geometry that allows algorithms like PCA, GAN latent space interpolation, and SVMs to operate safely.

---

## 2. Formal Definition

A **vector space** $V$ over a field $\mathbb{F}$ (typically $\mathbb{R}$ or $\mathbb{C}$) is a set of elements called vectors, equipped with two operations:
1. **Vector Addition ($+$):** $V \times V \to V$ mapping $(u, v) \mapsto u + v$.
2. **Scalar Multiplication ($\cdot$):** $\mathbb{F} \times V \to V$ mapping $(c, v) \mapsto c \cdot v$.

For $V$ to be a vector space, it must satisfy the following eight axioms for all $u, v, w \in V$ and all $a, b \in \mathbb{F}$:

*   **Axioms for Vector Addition:**
    1.  **Associativity:** $u + (v + w) = (u + v) + w$.
    2.  **Commutativity:** $u + v = v + u$.
    3.  **Additive Identity:** There exists an element $0 \in V$ such that $v + 0 = v$ for all $v \in V$.
    4.  **Additive Inverse:** For every $v \in V$, there exists $-v \in V$ such that $v + (-v) = 0$.
*   **Axioms for Scalar Multiplication:**
    5.  **Compatibility:** $a(bv) = (ab)v$.
    6.  **Multiplicative Identity:** $1v = v$, where $1$ is the multiplicative identity in $\mathbb{F}$.
    7.  **Distributivity over Scalar Addition:** $(a + b)v = av + bv$.
    8.  **Distributivity over Vector Addition:** $a(u + v) = au + av$.

---

## 3. Illustrative Derivation

### Subspace Criteria and the Intersection Theorem
A subset $U \subseteq V$ is a **subspace** of $V$ if $U$ is itself a vector space over $\mathbb{F}$ under the inherited operations. To prove a subset is a subspace, we use the **Subspace Criterion**: $U$ is a subspace if and only if $U \neq \emptyset$ (or $0 \in U$) and $U$ is closed under vector addition and scalar multiplication:
$$\forall u_1, u_2 \in U, \forall c \in \mathbb{F} \implies u_1 + c u_2 \in U$$

**Theorem:** Let $U_1$ and $U_2$ be two subspaces of a vector space $V$. Prove that their intersection $U_1 \cap U_2$ is also a subspace of $V$.

*Proof:*
To prove $U_1 \cap U_2$ is a subspace, we must verify the three Subspace Criterion conditions:
1.  **Zero Vector Containment:**
    Since $U_1$ is a subspace of $V$, the zero vector $0 \in U_1$.
    Since $U_2$ is a subspace of $V$, the zero vector $0 \in U_2$.
    Thus, by definition of intersection:
    $$0 \in U_1 \cap U_2$$
2.  **Closure under Addition:**
    Let $x, y \in U_1 \cap U_2$. This implies:
    *   $x, y \in U_1 \implies x + y \in U_1$ (since $U_1$ is closed under addition).
    *   $x, y \in U_2 \implies x + y \in U_2$ (since $U_2$ is closed under addition).
    Since $x + y$ belongs to both $U_1$ and $U_2$:
    $$x + y \in U_1 \cap U_2$$
3.  **Closure under Scalar Multiplication:**
    Let $x \in U_1 \cap U_2$ and $c \in \mathbb{F}$. This implies:
    *   $x \in U_1 \implies c \cdot x \in U_1$ (since $U_1$ is closed under scalar multiplication).
    *   $x \in U_2 \implies c \cdot x \in U_2$ (since $U_2$ is closed under scalar multiplication).
    Since $c \cdot x$ belongs to both $U_1$ and $U_2$:
    $$c \cdot x \in U_1 \cap U_2$$
Since all three conditions are satisfied, the intersection $U_1 \cap U_2$ is a subspace of $V$. $\blacksquare$

> **Gotcha:** The union of two subspaces $U_1 \cup U_2$ is *not* generally a subspace. For example, if $U_1$ is the x-axis and $U_2$ is the y-axis in $\mathbb{R}^2$, both are subspaces. However, their union contains $[1, 0]^T$ and $[0, 1]^T$, but adding them yields $[1, 1]^T$, which lies outside the union. Subspaces must be flat and pass through the origin; unions introduce "kinks."

---

## 4. Concrete Examples

### Example 1: The Vector Space $\mathbb{R}^n$
The set of all ordered $n$-tuples of real numbers, $\mathbb{R}^n$, forms a vector space over the field $\mathbb{R}$ under coordinate-wise addition and scalar multiplication. Let $u, v \in \mathbb{R}^n$ and $c \in \mathbb{R}$.
1. **Addition:**
   $$u + v = [u_1 + v_1, \dots, u_n + v_n]^T \in \mathbb{R}^n$$
2. **Scaling:**
   $$c \cdot v = [c v_1, \dots, c v_n]^T \in \mathbb{R}^n$$
All 8 axioms follow directly from the properties of real numbers $\mathbb{R}$.

### Example 2: Non-Closure of Degree-$d$ Polynomials
Let $\mathcal{P}_d$ be the set of all real polynomials of degree *at most* $d$. This set forms a vector space. However, the set of polynomials of degree *exactly* $d$ does not.
*   Let $f(x) = x^2 + 2x$ and $g(x) = -x^2 + 5$ be two polynomials of degree exactly 2.
*   Adding them:
    $$f(x) + g(x) = (x^2 - x^2) + 2x + 5 = 2x + 5$$
*   The resulting polynomial has degree 1, which is not in the set. The set is not closed under addition, violating the fundamental definition of a vector space.

---

## 5. Applied ML Context

1.  **Latent Vector Space Interpation:** In generative models like VAEs or GANs, the latent space is a low-dimensional vector space. We can perform vector addition in this space to blend attributes (e.g., adding a "smiling" vector to a "neutral face" vector generates a smiling face).
2.  **Word Semantic Arithmetic:** Word embeddings (like Word2Vec) map words to a vector space where semantic relations are modeled as vectors. This allows linear combinations: $\text{vec("King")} - \text{vec("Man")} + \text{vec("Woman")} \approx \text{vec("Queen")}$.
3.  **PCA Subspaces:** Principal Component Analysis project high-dimensional data onto a low-dimensional subspace $U \subset \mathbb{R}^d$ that maximizes variance, reducing noise and dimensions.
4.  **Null Space of Linear Layers:** In neural networks, the null space of a weight matrix $W$ represents the subspace of inputs $x$ that are completely blocked (mapped to zero): $Wx = 0$. This determines what information the layer discards.
5.  **Graph Neural Networks (GNNs):** Feature vectors of nodes belong to local vector spaces. The message-passing step aggregates neighbor features using vector addition, staying within the node feature vector space.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating subspaces in 3D Euclidean space $\mathbb{R}^3$:
*   Show a 3D coordinate frame representing the full space $\mathbb{R}^3$.
*   Plot a 2D flat plane passing through the origin. Label this plane as "Subspace $U$ (closed under addition and scaling)."
*   Plot a second 2D flat plane that is shifted up, parallel to the first, but does *not* pass through the origin. Label this plane as "Not a Subspace (fails zero-vector and closure axioms)."
*   Draw two vectors inside the subspace $U$ showing their sum (parallelogram rule) also lying entirely within the plane, illustrating the concept of **closure**.
