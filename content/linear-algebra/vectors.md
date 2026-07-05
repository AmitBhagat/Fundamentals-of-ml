---
title: "Vectors"
description: "High-dimensional coordinate spaces, vector algebra, and the Cauchy-Schwarz inequality."
complexity: "Advanced"
estimated_time: "30 min"
prerequisites: ["Scalars", "Basic Geometry"]
---

<h1 align="center"> Chapter 28: Vectors </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Scalars:** Understanding elements of a field $\mathbb{F}$ (e.g., real numbers $\mathbb{R}$).
* **Cartesian Geometry:** Familiarity with coordinate axes and plotting points in a plane.

</div>

## 1. Conceptual Hook

In machine learning, data is rarely represented by a single number. An image is a collection of pixels, a document is a sequence of words, and a user profile is a list of preferences and historical interactions. To manipulate these rich entities, we group individual numbers together into a **vector**.

A vector is not just an arrow in space; in ML, a vector represents a **state** or a coordinate in a high-dimensional feature landscape. By treating features as coordinates, we can translate abstract concepts into geometry. We can measure the distance between two vectors to see how similar two users are, or compute the angle between word vectors (cosine similarity) to determine semantic relationships. Moving a vector through a network is equivalent to evolving the state of our data.

---

## 2. Formal Definition

An $n$-dimensional real **column vector** $v \in \mathbb{R}^n$ is an ordered list of $n$ real numbers, written as:
$$v = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix}$$
where $v_i \in \mathbb{R}$ is the $i$-th component of the vector. The transpose of $v$, denoted $v^T$, is a **row vector**:
$$v^T = \begin{bmatrix} v_1, & v_2, & \dots, & v_n \end{bmatrix}$$

For any two vectors $u, v \in \mathbb{R}^n$ and a scalar $c \in \mathbb{R}$, we define two fundamental operations:
1. **Vector Addition:**
   $$u + v = \begin{bmatrix} u_1 + v_1 \\ u_2 + v_2 \\ \vdots \\ u_n + v_n \end{bmatrix}$$
2. **Scalar Multiplication:**
   $$c \cdot v = \begin{bmatrix} c \cdot v_1 \\ c \cdot v_2 \\ \vdots \\ c \cdot v_n \end{bmatrix}$$

To measure the length or magnitude of a vector, we define the **$L_p$ norm** for $p \ge 1$:
$$\|v\|_p = \left( \sum_{i=1}^n |v_i|^p \right)^{1/p}$$
The most common norm in ML is the **Euclidean ($L_2$) norm**:
$$\|v\|_2 = \sqrt{\sum_{i=1}^n v_i^2}$$

---

## 3. Illustrative Derivation

### The Cauchy-Schwarz Inequality
A foundational result in vector spaces is the **Cauchy-Schwarz Inequality**, which bounds the dot product of two vectors by the product of their Euclidean norms:
$$|u^T v| \le \|u\|_2 \|v\|_2 \quad \forall u, v \in \mathbb{R}^n$$

*Proof:*
For any scalar $t \in \mathbb{R}$, the norm of the vector $u + t v$ must be non-negative:
$$\|u + t v\|_2^2 \ge 0$$
Using the relationship between the norm and the dot product ($\|x\|_2^2 = x^T x$):
$$(u + t v)^T (u + t v) \ge 0$$
Expanding the transpose and distributing terms:
$$u^T u + 2t u^T v + t^2 v^T v \ge 0$$
Substituting the norm symbols:
$$\|u\|_2^2 + 2t (u^T v) + t^2 \|v\|_2^2 \ge 0$$
This expression is a quadratic polynomial in $t$ of the form $a t^2 + b t + c \ge 0$, where:
$$a = \|v\|_2^2, \quad b = 2(u^T v), \quad c = \|u\|_2^2$$
For a quadratic polynomial to be non-negative for all real values of $t$, its discriminant ($b^2 - 4ac$) must be less than or equal to zero:
$$b^2 - 4ac \le 0$$
Substitute the values of $a, b,$ and $c$:
$$\left( 2(u^T v) \right)^2 - 4 \|v\|_2^2 \|u\|_2^2 \le 0$$
$$4 (u^T v)^2 \le 4 \|u\|_2^2 \|v\|_2^2$$
Divide both sides by $4$ and take the square root:
$$|u^T v| \le \|u\|_2 \|v\|_2$$
This completes the proof. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Vector Addition and the Triangle Inequality
Let $u = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$ and $v = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$.
1. **Vector Addition:**
   $$w = u + v = \begin{bmatrix} 3 + 1 \\ 4 + 2 \end{bmatrix} = \begin{bmatrix} 4 \\ 6 \end{bmatrix}$$
2. **Verify the Triangle Inequality ($\|u+v\|_2 \le \|u\|_2 + \|v\|_2$):**
   $$\|u\|_2 = \sqrt{3^2 + 4^2} = 5$$
   $$\|v\|_2 = \sqrt{1^2 + 2^2} = \sqrt{5} \approx 2.236$$
   $$\|u+v\|_2 = \sqrt{4^2 + 6^2} = \sqrt{52} \approx 7.211$$
   Since $7.211 \le 5 + 2.236 = 7.236$, the triangle inequality holds.

### Example 2: Cosine Similarity between Embeddings
Let two vectors representing words in a semantic space be $u = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ (representing "king") and $v = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$ (representing "queen").
1. **Compute Dot Product:**
   $$u^T v = 1 \cdot 1 + 0 \cdot 1 = 1$$
2. **Compute Norms:**
   $$\|u\|_2 = \sqrt{1^2 + 0^2} = 1$$
   $$\|v\|_2 = \sqrt{1^2 + 1^2} = \sqrt{2} \approx 1.414$$
3. **Compute Cosine Similarity:**
   $$\cos(\theta) = \frac{u^T v}{\|u\|_2 \|v\|_2} = \frac{1}{1 \cdot \sqrt{2}} = \frac{1}{\sqrt{2}} \approx 0.707$$
   This indicates a $45^\circ$ angle of separation between the two concept vectors.

---

## 5. Applied ML Context

1. **Word Embeddings:** In natural language processing, words are represented as dense vectors in spaces like $\mathbb{R}^{300}$ or $\mathbb{R}^{768}$. The similarity between words is measured via the cosine similarity of their embedding vectors.
2. **Feature Representation:** In tabular data, each sample is represented as a feature vector $x^{(i)} \in \mathbb{R}^d$, where each dimension is a numerical measurement (e.g., age, income, blood pressure) used as input for predictions.
3. **Loss Landscape Gradients:** The gradient of a neural network's loss function with respect to its parameters, $\nabla_\theta L$, is a vector pointing in the direction of the steepest ascent on the loss surface. Optimizers scale and invert this vector to update the weights.
4. **Weight Vectors:** In linear classifiers (e.g., SVMs, perceptrons), the boundary between classes is a hyperplane defined by a normal weight vector $w$. The decision boundary is the set of points where $w^T x + b = 0$.
5. **Image Flattening:** A grayscale image of size $28 \times 28$ is represented as a matrix, but is often flattened into a single vector $x \in \mathbb{R}^{784}$ to serve as the input layer of a multi-layer perceptron.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating vector addition and subtraction in a 2D Cartesian plane:
*   Show vector $u = [3, 4]^T$ and $v = [1, 2]^T$ drawn as arrows from the origin.
*   Draw a parallelogram with $u$ and $v$ as adjacent sides. Plot the diagonal arrow representing $u+v = [4, 6]^T$ using the **Parallelogram Law**.
*   Draw a directed line segment from the tip of $v$ to the tip of $u$ to visualize the vector difference $u - v = [2, 2]^T$, illustrating how vector subtraction defines the displacement vector between two states.
