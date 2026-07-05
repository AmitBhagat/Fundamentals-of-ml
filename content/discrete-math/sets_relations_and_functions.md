---
title: "Sets, Relations, and Functions"
description: "Cartesian products, equivalence relations, partitions, injectivity and surjectivity, and bijection inverse mappings."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Foundations"]
---

<h1 align="center"> Chapter 106: Sets, Relations, and Functions </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Cartesian Product:** The set of all ordered pairs $(a, b)$ formed by elements of two sets: $\mathcal{A} \times \mathcal{B} = \{(a, b) \mid a \in \mathcal{A} \land b \in \mathcal{B}\}$.
* **Equivalence Relation:** A binary relation that is reflexive, symmetric, and transitive, generalizing the concept of equality.

</div>

## 1. Conceptual Hook

Machine learning is often presented as a complex web of deep neural layers, but at its mathematical core, it is simply the study of mappings. We take a raw input (an image pixel grid, a text sequence, or credit history data) and transform it into a prediction or label.

The language we use to describe these mappings is built on **sets, relations, and functions**.

*   A **Set** is a distinct collection of items (such as the vocabulary of a language model or a group of categories).
*   A **Relation** describes the web of potential connections between different sets.
*   A **Function** is a strict, predictable relation: it guarantees that for every input, there is exactly one output.

Think of sorting laundry. The hampers are your sets. Every way you could match clothing to a washer setting is a relation. The washing machine cycle itself is a function: when you select "Delicates," the machine follows a deterministic rule to hit exactly $30^\circ\text{C}$ every time. If the same input led to different temperatures on different days, the mapping would be a relation, not a function, and your machine would be useless.

In machine learning, we strive to design and fit stable functions that map features to targets without ambiguity.

---

## 2. Formal Definition

### 1. Sets
A **set** is an unordered collection of distinct elements. We write $a \in \mathcal{S}$ to denote that element $a$ belongs to set $\mathcal{S}$.
*   **Cardinality ($|\mathcal{S}|$):** The number of elements in $\mathcal{S}$.
*   **Union ($\mathcal{A} \cup \mathcal{B}$):** $\{ x \mid x \in \mathcal{A} \lor x \in \mathcal{B} \}$.
*   **Intersection ($\mathcal{A} \cap \mathcal{B}$):** $\{ x \mid x \in \mathcal{A} \land x \in \mathcal{B} \}$.

### 2. Relations
A binary relation $\mathcal{R}$ from set $\mathcal{A}$ to set $\mathcal{B}$ is a subset of the Cartesian product $\mathcal{A} \times \mathcal{B}$:
$$\mathcal{R} \subseteq \mathcal{A} \times \mathcal{B}$$
We write $a \mathcal{R} b$ to denote $(a, b) \in \mathcal{R}$.

For a relation $\mathcal{R}$ on a single set $\mathcal{S}$ ($\mathcal{R} \subseteq \mathcal{S} \times \mathcal{S}$), we define the following properties:
*   **Reflexive:** $a \mathcal{R} a$ for all $a \in \mathcal{S}$.
*   **Symmetric:** $a \mathcal{R} b \implies b \mathcal{R} a$ for all $a, b \in \mathcal{S}$.
*   **Transitive:** $(a \mathcal{R} b \land b \mathcal{R} c) \implies a \mathcal{R} c$ for all $a, b, c \in \mathcal{S}$.
An **equivalence relation** is a relation that is reflexive, symmetric, and transitive.

### 3. Functions
A **function** $f: \mathcal{A} \to \mathcal{B}$ is a relation that associates each element $a \in \mathcal{A}$ with exactly one element $b \in \mathcal{B}$:
$$\forall a \in \mathcal{A}, \quad \exists! b \in \mathcal{B} \quad \text{such that } f(a) = b$$
*   **Domain:** The input set $\mathcal{A}$.
*   **Codomain:** The target set $\mathcal{B}$.
*   **Range (Image):** $\text{Im}(f) = \{ f(a) \mid a \in \mathcal{A} \} \subseteq \mathcal{B}$.

Functions can be classified as:
*   **Injective (One-to-One):** $f(x) = f(y) \implies x = y$.
*   **Surjective (Onto):** $\text{Im}(f) = \mathcal{B}$.
*   **Bijective:** Both injective and surjective. A bijection has a unique inverse function $f^{-1}: \mathcal{B} \to \mathcal{A}$.

---

## 3. Illustrative Derivation

### Proof: The Equivalence Class Partition Theorem
We prove that any equivalence relation $\mathcal{R}$ on a non-empty set $\mathcal{S}$ partitions $\mathcal{S}$ into mutually disjoint equivalence classes whose union is $\mathcal{S}$.

*Proof:*
For any $a \in \mathcal{S}$, define the equivalence class of $a$ as:
$$[a] = \{ x \in \mathcal{S} \mid x \mathcal{R} a \}$$

1.  **Prove the union of all equivalence classes is $\mathcal{S}$:**
    Since $\mathcal{R}$ is reflexive, we have $a \mathcal{R} a$ for all $a \in \mathcal{S}$. Thus, $a \in [a]$.
    Since every element $a$ belongs to its own equivalence class, the union of all classes covers the entire set:
    $$\bigcup_{a \in \mathcal{S}} [a] = \mathcal{S}$$

2.  **Prove disjointness of equivalence classes:**
    Let $a, b \in \mathcal{S}$ be elements whose equivalence classes share a common element $c$:
    $$c \in [a] \cap [b]$$
    By definition, this implies:
    $$c \mathcal{R} a \quad \text{and} \quad c \mathcal{R} b$$
    By symmetry of $\mathcal{R}$:
    $$a \mathcal{R} c \quad \text{and} \quad c \mathcal{R} b$$
    By transitivity of $\mathcal{R}$:
    $$a \mathcal{R} c \land c \mathcal{R} b \implies a \mathcal{R} b$$
    Now, let $x$ be any element in $[a]$, meaning $x \mathcal{R} a$. Since we proved $a \mathcal{R} b$, transitivity yields:
    $$x \mathcal{R} a \land a \mathcal{R} b \implies x \mathcal{R} b \implies x \in [b]$$
    This shows $[a] \subseteq [b]$. By symmetric reasoning (swapping $a$ and $b$), we have $[b] \subseteq [a]$.
    Therefore, if two classes share any element, they are identical:
    $$[a] = [b]$$
Thus, the equivalence classes are mutually disjoint, partitioning $\mathcal{S}$ into distinct blocks. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Function vs. General Relation
Let input set $\mathcal{A} = \{\text{Silk}, \text{Wool}, \text{Lace}\}$ and codomain temperature set $\mathcal{B} = \{20, 30, 40\}$.
*   **Relation $\mathcal{R}$ (Not a function):**
    $$\mathcal{R} = \{ (\text{Silk}, 30), (\text{Silk}, 40), (\text{Wool}, 30), (\text{Lace}, 20) \}$$
    This is not a function because the input "Silk" maps to both $30$ and $40$, violating uniqueness.
*   **Function $f$ (Injective but not Surjective):**
    $$f = \{ (\text{Silk}, 30), (\text{Wool}, 30), (\text{Lace}, 20) \}$$
    Each element of $\mathcal{A}$ has a unique output. However, the range is $\text{Im}(f) = \{20, 30\} \neq \mathcal{B}$ (since $40$ is not mapped), meaning the function is not surjective.

### Example 2: Verifying a Bijection and its Inverse
We evaluate the function $f: \mathbb{R} \to \mathbb{R}$ defined by $f(x) = 10x + 5$.
1.  **Verify Injectivity:**
    $$f(x_1) = f(x_2) \implies 10x_1 + 5 = 10x_2 + 5 \implies 10x_1 = 10x_2 \implies x_1 = x_2 \quad (\text{Injective})$$
2.  **Verify Surjectivity:**
    Let $y \in \mathbb{R}$ be an element in the codomain. We solve for input $x$:
    $$y = 10x + 5 \implies x = \frac{y - 5}{10}$$
    Since $\frac{y-5}{10} \in \mathbb{R}$ exists for all $y \in \mathbb{R}$, $f$ is surjective.
3.  **Formulate the inverse function:**
    Since $f$ is a bijection, its unique inverse is:
    $$f^{-1}(y) = \frac{y - 5}{10}$$

---

## 5. Applied ML Context

1.  **Neural Network Classification Heads:** The final classification layer acts as a function mapping high-dimensional activation vectors in $\mathbb{R}^d$ to a discrete set of class label indices $\{1, \dots, K\}$.
2.  **Database Joins in Feature Stores:** SQL tables utilize relations (UserID to PurchaseHistory) that leverage set unions, intersections, and Cartesian products.
3.  **One-Hot Category Encoding:** Category sets $\mathcal{S}$ are mapped to orthonormal basis vectors in $\mathbb{R}^{|\mathcal{S}|}$, ensuring distinct categories are represented orthogonally.
4.  **Support Vector Machine Margins:** SVMs find a separating hyperplane that splits two sets of points in a vector space by maximizing the margin between them.
5.  **Recommender Bipartite Relations:** Collaborative filtering models user-item interactions as a relation on a bipartite graph. The goal is to estimate the strength of the relation $(u, i)$ for unobserved user-item pairs.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating sets and mapping relations:
*   Draw three oval mapping diagrams side-by-side:
    1.  **General Relation (Non-function):** Show Domain $\mathcal{A}$ mapping to Codomain $\mathcal{B}$. Draw arrows showing one input element pointing to two different outputs.
    2.  **Surjective but Non-Injective Function:** Show two inputs mapping to the same output, with all outputs covered.
    3.  **Bijective Function:** Show a one-to-one mapping between all elements, with reverse arrows showing $f^{-1}$.
*   Add a caption explaining that functions are restricted relations where each input maps to exactly one output, and bijective functions permit perfect reconstruction via an inverse mapping.
