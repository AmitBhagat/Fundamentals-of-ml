---
title: "Attention Mechanism Math"
description: "Scaled dot-product formulation, softmax gradient preservation proof, matrix shapes, and Transformer architectures."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Matrices", "Matrix Multiplication", "Dot Product"]
---

<h1 align="center"> Chapter 10: Attention Mechanism Math </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Matrix Multiplication:** Knowing how matrices represent compositions of linear maps.
* **Softmax Function:** The math that turns scores into a probability distribution.

</div>

## 1. Conceptual Hook

In modern artificial intelligence, the Transformer architecture—which powers Large Language Models like GPT-4 and Gemini—rules supreme. The core engine driving this success is the **attention mechanism**.

Attention is a dynamic, differentiable selection engine. Instead of processing words in isolation or using fixed convolutional filters, attention allows words in a sentence to dynamically decide which neighboring words they should focus on to extract context. A word updates its meaning by taking a weighted average of neighbor representations, where the weights are calculated on the fly using vector dot products. It acts as a "soft" lookup table where queries are matched against keys to retrieve values, ensuring that the model can learn and route information flexibly.

---

## 2. Formal Definition

Let $N$ be the number of query tokens and $M$ be the number of key/value tokens. The input matrices are:
*   **Queries ($Q \in \mathbb{R}^{N \times d_k}$):** The representations searching for context.
*   **Keys ($K \in \mathbb{R}^{M \times d_k}$):** The representations matching queries.
*   **Values ($V \in \mathbb{R}^{M \times d_v}$):** The actual content to be aggregated.

The **Scaled Dot-Product Attention** is defined as:
$$\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{QK^T}{\sqrt{d_k}} \right) V$$

where the softmax function is applied row-wise to the attention score matrix:
$$\left( \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) \right)_{ij} = \frac{\exp\left( \frac{Q_i K_j^T}{\sqrt{d_k}} \right)}{\sum_{l=1}^M \exp\left( \frac{Q_i K_l^T}{\sqrt{d_k}} \right)}$$

The final output is a matrix of size $\mathbb{R}^{N \times d_v}$ representing the context-weighted representations.

---

## 3. Illustrative Derivation

### Derivation of the Variance Scaling Factor $\frac{1}{\sqrt{d_k}}$
Why do we divide the queries and keys product by $\sqrt{d_k}$? We prove that this factor preserves the variance of the inputs, preventing softmax gradient saturation.

Let $q \in \mathbb{R}^{d_k}$ and $k \in \mathbb{R}^{d_k}$ be a query and key vector. Assume that the components $q_i$ and $k_j$ are independent random variables with a mean of 0 and a variance of 1:
$$\mathbb{E}[q_i] = \mathbb{E}[k_j] = 0, \quad \text{Var}(q_i) = \text{Var}(k_j) = 1 \quad \forall i, j$$
Let the raw attention dot product be $Z = q^T k = \sum_{i=1}^{d_k} q_i k_i$.

1.  **Calculate the Expected Value of $Z$:**
    $$\mathbb{E}[Z] = \mathbb{E}\left[ \sum_{i=1}^{d_k} q_i k_i \right] = \sum_{i=1}^{d_k} \mathbb{E}[q_i k_i]$$
    Since $q_i$ and $k_i$ are independent:
    $$\mathbb{E}[Z] = \sum_{i=1}^{d_k} \mathbb{E}[q_i] \mathbb{E}[k_i] = \sum_{i=1}^{d_k} (0)(0) = 0$$

2.  **Calculate the Variance of $Z$:**
    Since the terms $q_i k_i$ are independent for different indices $i$:
    $$\text{Var}(Z) = \text{Var}\left( \sum_{i=1}^{d_k} q_i k_i \right) = \sum_{i=1}^{d_k} \text{Var}(q_i k_i)$$
    Recall that for independent variables $X$ and $Y$ with $\mathbb{E}[X] = \mathbb{E}[Y] = 0$:
    $$\text{Var}(XY) = \mathbb{E}[X^2 Y^2] - (\mathbb{E}[XY])^2 = \mathbb{E}[X^2]\mathbb{E}[Y^2] - (\mathbb{E}[X]\mathbb{E}[Y])^2$$
    Since $\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 \implies \mathbb{E}[X^2] = 1$:
    $$\text{Var}(XY) = (1)(1) - (0)(0) = 1$$
    Substituting this back into the variance summation:
    $$\text{Var}(Z) = \sum_{i=1}^{d_k} 1 = d_k$$

3.  **Evaluate Softmax Impact:**
    As the dimensionality $d_k$ grows large, the variance of the dot product $Z$ grows linearly with $d_k$. This means the dot products can take very large values in magnitude, pushing the softmax function into regions of flat plateaus where the gradients vanish:
    $$\frac{\partial \text{softmax}(x)_i}{\partial x_j} \approx 0 \quad \text{for large } |x|$$
    This halts backpropagation training.

4.  **Restore Variance to Unit Scale:**
    We scale the dot product by the factor $\frac{1}{\sqrt{d_k}}$:
    $$\text{Var}\left( \frac{Z}{\sqrt{d_k}} \right) = \frac{1}{d_k} \text{Var}(Z) = \frac{d_k}{d_k} = 1 \quad \blacksquare$$
Dividing by $\sqrt{d_k}$ stabilizes the distribution of attention logits, ensuring gradients flow stably during backpropagation.

---

## 4. Concrete Examples

### Example 1: Softmax Scaling Contrast
Suppose $d_k = 100$ (so $\sqrt{d_k} = 10$). A query has raw dot products with two keys: $Z = [50, 20]$.
*   **Without Scaling:**
    $$\text{softmax}([50, 20])_1 = \frac{\exp(50)}{\exp(50) + \exp(20)} \approx 1.0$$
    $$\text{softmax}([50, 20])_2 = \frac{\exp(20)}{\exp(50) + \exp(20)} \approx 0.0$$
    The model allocates 100% attention to the first token. The gradient for the second token is completely zeroed out.
*   **With Scaling ($\frac{Z}{\sqrt{d_k}} = [5, 2]$):**
    $$\text{softmax}([5, 2])_1 = \frac{\exp(5)}{\exp(5) + \exp(2)} \approx \frac{148.4}{148.4 + 7.4} \approx 0.952$$
    $$\text{softmax}([5, 2])_2 = \frac{\exp(2)}{\exp(5) + \exp(2)} \approx \frac{7.4}{155.8} \approx 0.048$$
    The smaller score maintains a non-zero probability ($4.8\%$), allowing gradients to flow back to both key representations.

### Example 2: Simple Attention Forward Pass
Let $d_k = 2, d_v = 2, N=2, M=2$.
$$Q = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad K = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad V = \begin{pmatrix} 10 & 20 \\ 30 & 40 \end{pmatrix}$$
1.  **Compute $QK^T$:**
    $$QK^T = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$$
2.  **Scale by $\sqrt{d_k} = \sqrt{2} \approx 1.414$:**
    $$\frac{QK^T}{\sqrt{2}} = \begin{pmatrix} 0.707 & 0 \\ 0 & 0.707 \end{pmatrix}$$
3.  **Apply Row-Wise Softmax:**
    *   Row 1: $\exp(0.707) \approx 2.028$, $\exp(0) = 1$. Sum $= 3.028$.
        $$\text{Weights}_{1} = \left[ \frac{2.028}{3.028}, \frac{1}{3.028} \right] \approx [0.67, 0.33]$$
    *   Row 2: Similarly:
        $$\text{Weights}_{2} = [0.33, 0.67]$$
    $$A = \begin{pmatrix} 0.67 & 0.33 \\ 0.33 & 0.67 \end{pmatrix}$$
4.  **Compute Output $A V$:**
    $$\text{Output} = \begin{pmatrix} 0.67 & 0.33 \\ 0.33 & 0.67 \end{pmatrix} \begin{pmatrix} 10 & 20 \\ 30 & 40 \end{pmatrix} = \begin{pmatrix} 0.67(10) + 0.33(30) & 0.67(20) + 0.33(40) \\ 0.33(10) + 0.67(30) & 0.33(20) + 0.67(40) \end{pmatrix} = \begin{pmatrix} 16.6 & 26.6 \\ 23.4 & 33.4 \end{pmatrix}$$

---

## 5. Applied ML Context

1.  **Multi-Head Attention (MHA):** Instead of calculating attention once, transformers project queries, keys, and values $h$ times into lower-dimensional subspaces, calculating attention in parallel. This allows the model to attend to multiple attributes simultaneously (e.g. grammar vs. coreference).
2.  **Cross-Attention in Translation:** In encoder-decoder translation networks, the decoder generates queries that attend to key-value pairs generated by the encoder, translating words in context.
3.  **Vision Transformers (ViTs):** In CV, images are divided into patches, flattened, and projected into embedding vectors. Self-attention dynamically connects remote patches of the image to analyze global structures.
4.  **Graph Attention Networks (GATs):** Nodes update their feature vectors by computing attention scores over neighboring nodes, weighting node aggregation based on topological importance.
5.  **Multi-Modal Embeddings (CLIP):** Text and image representations are aligned by calculating the dot product attention score between text token embeddings and image patch embeddings.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the forward data flow of scaled dot-product attention:
*   Show Query ($Q$) and Key ($K^T$) matrices multiplying to generate a square $N \times N$ matrix. Label this matrix "Raw Attention Scores."
*   Draw a step showing element-wise division of this matrix by the scalar $\sqrt{d_k}$.
*   Draw a step showing a row-wise Softmax operation converting the scaled scores to "Attention Weights (summing to 1 per row)."
*   Show this weight matrix multiplying the Value ($V$) matrix to yield the final "Context-Weighted output."
