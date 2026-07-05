---
title: "Dot Product"
description: "Algebraic definition, law of cosines derivation, projections, and similarity measurements in machine learning."
complexity: "Advanced"
estimated_time: "35 min"
prerequisites: ["Scalars", "Vectors", "Vector Spaces"]
---

<h1 align="center"> Chapter 13: Dot Product </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Vectors:** Understanding components and coordinate systems.
* **Vector Norms:** Knowing how to calculate the $L_2$ Euclidean length of a vector.

</div>

## 1. Conceptual Hook

In machine learning, we often need to measure how closely aligned two objects are. For instance, how similar is a user's movie preference vector to a movie's genre vector? Or how much attention should a word vector in a sentence pay to another word vector? The fundamental mathematical operation that measures this alignment is the **dot product**.

The dot product is the ultimate similarity engine. It takes two equal-length vectors, multiplies their corresponding components, and adds them up to produce a single number. Geometrically, it projects one vector onto another and multiplies their lengths. If the vectors point in the same direction, their dot product is large and positive; if they are perpendicular, the product is zero (orthogonal); and if they point in opposite directions, the product is negative. It is the core mathematical building block of neural network layers, similarity search, and self-attention maps.

---

## 2. Formal Definition

Let $u, v \in \mathbb{R}^n$ be two vectors in an $n$-dimensional real vector space. The **dot product** (or standard inner product), denoted $u \cdot v$ or $u^T v$, is defined algebraically as:
$$u^T v = \sum_{i=1}^n u_i v_i = u_1 v_1 + u_2 v_2 + \dots + u_n v_n$$

Geometrically, for vectors in $\mathbb{R}^n$, the dot product is defined as:
$$u^T v = \|u\|_2 \|v\|_2 \cos(\theta)$$
where $\|\cdot\|_2$ is the Euclidean norm, and $\theta$ is the angle of separation between the two vectors ($0 \le \theta \le \pi$).

### Key Properties
For any vectors $u, v, w \in \mathbb{R}^n$ and scalar $c \in \mathbb{R}$:
1.  **Commutativity:** $u^T v = v^T u$
2.  **Distributivity:** $u^T (v + w) = u^T v + u^T w$
3.  **Homogeneity:** $(c \cdot u)^T v = c \cdot (u^T v)$
4.  **Positive-Definiteness:** $u^T u \ge 0$, and $u^T u = 0 \iff u = 0$. Note that $u^T u = \|u\|_2^2$.

---

## 3. Illustrative Derivation

### Deriving the Geometric Dot Product Formula
We derive the equivalence between the algebraic and geometric definitions of the dot product using the **Law of Cosines**.

Consider the triangle in $\mathbb{R}^n$ formed by vectors $u$, $v$, and their difference vector $u - v$. The lengths of the sides of this triangle are $\|u\|_2$, $\|v\|_2$, and $\|u - v\|_2$.
By the Law of Cosines:
$$\|u - v\|_2^2 = \|u\|_2^2 + \|v\|_2^2 - 2 \|u\|_2 \|v\|_2 \cos(\theta)$$

Let us expand the left-hand side $\|u - v\|_2^2$ using the algebraic properties of the inner product:
$$\|u - v\|_2^2 = (u - v)^T (u - v)$$
Using the distributive and commutative properties:
$$(u - v)^T (u - v) = u^T u - u^T v - v^T u + v^T v$$
$$(u - v)^T (u - v) = u^T u - 2 u^T v + v^T v$$
Substituting the norm definitions ($x^T x = \|x\|_2^2$):
$$\|u - v\|_2^2 = \|u\|_2^2 - 2 u^T v + \|v\|_2^2$$

Now, equate this expanded expression to our Law of Cosines equation:
$$\|u\|_2^2 - 2 u^T v + \|v\|_2^2 = \|u\|_2^2 + \|v\|_2^2 - 2 \|u\|_2 \|v\|_2 \cos(\theta)$$

Subtract $\|u\|_2^2 + \|v\|_2^2$ from both sides of the equation:
$$-2 u^T v = -2 \|u\|_2 \|v\|_2 \cos(\theta)$$

Divide both sides by $-2$:
$$u^T v = \|u\|_2 \|v\|_2 \cos(\theta)$$
This completes the proof, establishing the link between algebraic components and spatial angles. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Basic Dot Product Calculation
Let $u = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$ and $v = \begin{bmatrix} 4 \\ -1 \\ 2 \end{bmatrix}$ in $\mathbb{R}^3$.
1. **Apply the algebraic definition:**
   $$u^T v = (1)(4) + (2)(-1) + (3)(2)$$
   $$u^T v = 4 - 2 + 6 = 8$$
The positive result indicates that the vectors generally point in a similar direction (the angle between them is acute).

### Example 2: Determining Angle of Separation
Find the angle $\theta$ between $u = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ and $v = \begin{bmatrix} 1 \\ \sqrt{3} \end{bmatrix}$.
1. **Compute the dot product:**
   $$u^T v = (1)(1) + (0)(\sqrt{3}) = 1$$
2. **Compute the Euclidean norms:**
   $$\|u\|_2 = \sqrt{1^2 + 0^2} = 1$$
   $$\|v\|_2 = \sqrt{1^2 + (\sqrt{3})^2} = \sqrt{1 + 3} = 2$$
3. **Solve for $\cos(\theta)$:**
   $$\cos(\theta) = \frac{u^T v}{\|u\|_2 \|v\|_2} = \frac{1}{1 \cdot 2} = 0.5$$
4. **Find $\theta$:**
   $$\theta = \arccos(0.5) = 60^\circ \quad \left(\text{or } \frac{\pi}{3} \text{ radians}\right)$$
This geometric analysis calculates the exact angular separation of the two vectors.

---

## 5. Applied ML Context

1.  **Neural Network Activation:** In a fully connected neuron, the output before activation is calculated as the dot product of the input feature vector $x$ and the parameter weight vector $w$, plus a bias: $y = w^T x + b$. The dot product measures how closely the input matches the neuron's learned weights.
2.  **Cosine Similarity in NLP:** In vector search and natural language processing, semantic similarity between text embeddings is measured by the cosine of the angle between them: $\text{Sim}(u, v) = \frac{u^T v}{\|u\|_2 \|v\|_2}$.
3.  **Attention Maps in Transformers:** Scaled dot-product attention computes the relationship between token representations by taking the dot product of Query and Key vectors, scaled by the feature dimension: $\text{Score}(Q_i, K_j) = \frac{Q_i^T K_j}{\sqrt{d_k}}$.
4.  **Support Vector Machines (SVM):** The decision boundary of a linear SVM is a hyperplane defined by the set of feature points where the dot product with the normal weight vector equals the bias: $w^T x + b = 0$.
5.  **Kernel Trick:** Dual formulations of ML models (like kernel SVMs or Kernel PCA) compute predictions using inner products in high-dimensional feature spaces, calculated implicitly via a kernel function: $K(u, v) = \phi(u)^T \phi(v)$.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the dot product as a projection:
*   Show two vectors $u$ and $v$ drawn from the origin with an angle $\theta$ between them.
*   Draw a dashed perpendicular line from the tip of $u$ down to the span of $v$. Label the distance from the origin to the foot of this perpendicular as the **projection length** of $u$ onto $v$: $\|u\|_2 \cos(\theta)$.
*   Illustrate that the dot product is the product of this projection length and the length of $v$ ($\|v\|_2$).
*   Draw three side-by-side scenarios:
    1.  **Acute Angle ($\theta < 90^\circ$):** Projection points in the direction of $v$, resulting in a positive dot product.
    2.  **Right Angle ($\theta = 90^\circ$):** Projection length is zero, resulting in a zero dot product (orthogonality).
    3.  **Obtuse Angle ($\theta > 90^\circ$):** Projection points in the opposite direction of $v$, resulting in a negative dot product.
