---
title: "Singular Value Decomposition (SVD)"
description: "Decomposing general linear maps, spectral properties of A^T A, and the Eckart-Young-Mirsky theorem."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Vector Spaces", "Eigenvalues and Eigenvectors", "Inner Products"]
---

<h1 align="center"> Chapter 25: SVD </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Inner Product Spaces:** Understanding orthobases, adjoint operators, and projections.
* **Spectral Theorem:** Knowing that symmetric real matrices are orthogonally diagonalizable.
* **Matrix Properties:** Familiarity with positive semi-definite (PSD) matrices.

</div>

## Analogy

Think of Singular Value Decomposition (SVD) as the **ultimate multi-dimensional camera rig**. 

Suppose you have a complex 3D sculpture, and you want to capture its shape on a 2D canvas. If you place your camera randomly, the sculpture's features will squash, overlap, and get lost in perspective. 

SVD is the process of finding the absolute best angles to position your camera and lighting. It analyzes the sculpture (the matrix $A$) and identifies:
1. **$V$ (The Lighting Rig):** The natural coordinate directions of the sculpture's structure.
2. **$\Sigma$ (The Zoom Lenses):** How prominent or "stretched" the features are along each of those directions.
3. **$U$ (The Photo Frame):** How those features map onto the final photo canvas.

Instead of a random, distorted projection, SVD systematically aligns the camera with the sculpture's primary axes of variance, capturing the maximum structural detail in the first few shots, and allowing us to discard the rest as "shadows" or noise.

## The Math Link

### 1. The Singular Value Decomposition Theorem
Let $A \in \mathbb{R}^{m \times n}$ be a matrix of rank $r \le \min(m, n)$. There exist orthogonal matrices:
$$U = [u_1, \dots, u_m] \in \mathbb{R}^{m \times m} \quad \text{s.t.} \quad U^T U = I_m$$
$$V = [v_1, \dots, v_n] \in \mathbb{R}^{n \times n} \quad \text{s.t.} \quad V^T V = I_n$$
and a diagonal matrix $\Sigma \in \mathbb{R}^{m \times n}$ with diagonal entries $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$ and $\sigma_{i} = 0$ for $i > r$, such that:
$$A = U \Sigma V^T = \sum_{i=1}^r \sigma_i u_i v_i^T$$
The vectors $\{u_i\}$ are the **left-singular vectors**, $\{v_i\}$ are the **right-singular vectors**, and the scalars $\{\sigma_i\}$ are the **singular values**.

### 2. Connection to Spectral Theory
For any matrix $A \in \mathbb{R}^{m \times n}$:
* The matrix $A^T A \in \mathbb{R}^{n \times n}$ is symmetric and positive semi-definite. Its eigenvectors are the right-singular vectors $v_i$, and its non-zero eigenvalues are $\lambda_i = \sigma_i^2$.
* The matrix $A A^T \in \mathbb{R}^{m \times m}$ is symmetric and positive semi-definite. Its eigenvectors are the left-singular vectors $u_i$, and its non-zero eigenvalues are also $\lambda_i = \sigma_i^2$.

### 3. Low-Rank Approximation (Eckart-Young-Mirsky Theorem)
Let $A_k = \sum_{i=1}^k \sigma_i u_i v_i^T$ be the truncated SVD of $A$ at rank $k < r$. The **Eckart-Young-Mirsky Theorem** states that $A_k$ is the best rank-$k$ approximation of $A$ under both the spectral norm $\|\cdot\|_2$ and the Frobenius norm $\|\cdot\|_F$:
$$\min_{\text{rank}(B) \le k} \|A - B\|_F = \|A - A_k\|_F = \sqrt{\sum_{i=k+1}^r \sigma_i^2}$$
$$\min_{\text{rank}(B) \le k} \|A - B\|_2 = \|A - A_k\|_2 = \sigma_{k+1}$$

---

## Proof-Based Exercises

### Exercise 1: Eigenvalues of $A^T A$ and $A A^T$
**Theorem:** Prove that the non-zero eigenvalues of $A^T A$ and $A A^T$ are identical.

*Proof:*
Let $\lambda \neq 0$ be an eigenvalue of $A^T A$, and let $v$ be its corresponding eigenvector. By definition:
$$(A^T A)v = \lambda v \quad (v \neq 0)$$
Multiply both sides of the equation from the left by $A$:
$$A(A^T A)v = A(\lambda v)$$
Since matrix multiplication is associative and $\lambda$ is a scalar:
$$(A A^T)(Av) = \lambda (Av)$$
Let $u = Av$. Since $\lambda \neq 0$ and $v \neq 0$, we have:
$$(A^T A)v = \lambda v \implies v^T A^T A v = \lambda v^T v \implies \|Av\|_2^2 = \lambda \|v\|_2^2$$
Since $\lambda > 0$ (as $A^T A$ is positive semi-definite and $\lambda \neq 0$), it must be that $Av \neq 0$, so $u \neq 0$.
Thus:
$$(A A^T)u = \lambda u$$
This proves that $\lambda$ is also an eigenvalue of $A A^T$ with corresponding eigenvector $u = Av$. By symmetry, any non-zero eigenvalue of $A A^T$ is also an eigenvalue of $A^T A$. $\blacksquare$

### Exercise 2: Uniqueness of Right-Singular Vectors
Let $A = U \Sigma V^T$ be the SVD of $A$. Prove that if all non-zero singular values of $A$ are distinct ($\sigma_1 > \sigma_2 > \dots > \sigma_r > 0$), then the right-singular vectors $\{v_1, \dots, v_r\}$ are uniquely determined up to a sign change ($\pm 1$).

*Proof:*
This is a bit of a headache if you don't use spectral theory, but here is the trick:
We know that $v_i$ are eigenvectors of the symmetric matrix $A^T A$ corresponding to eigenvalues $\lambda_i = \sigma_i^2$. 
Since the singular values $\sigma_i$ are distinct, their squares $\lambda_i = \sigma_i^2$ are also distinct. 
For a symmetric matrix, the eigenspace corresponding to any simple (non-repeated) eigenvalue $\lambda_i$ has dimension exactly $1$.
Thus, any eigenvector $w$ corresponding to $\lambda_i$ must lie in the 1-dimensional subspace spanned by $v_i$:
$$w = c v_i \quad \text{for some } c \in \mathbb{R}$$
Since right-singular vectors must be normalized to unit length:
$$\|w\|_2 = 1 \implies |c| \|v_i\|_2 = 1 \implies |c| = 1 \implies c = \pm 1$$
Thus, $w = \pm v_i$. The right-singular vectors are uniquely determined up to their sign. $\blacksquare$

---

## Let's Run the Numbers

### Example: SVD of a $2 \times 1$ Matrix

Let $A = \begin{pmatrix} 3 \\ 4 \end{pmatrix}$. Note that $m = 2, n = 1$.

1. **Form $A^T A$:**
   $$A^T A = \begin{pmatrix} 3 & 4 \end{pmatrix} \begin{pmatrix} 3 \\ 4 \end{pmatrix} = [25] \in \mathbb{R}^{1 \times 1}$$

2. **Compute Eigenvalues and Eigenvectors of $A^T A$:**
   The single eigenvalue is $\lambda_1 = 25$.
   The singular value is $\sigma_1 = \sqrt{25} = 5$.
   The eigenvector $v_1$ of $A^T A$ must satisfy $v_1^T v_1 = 1$, which gives $V = [1]$.
   Thus, $\Sigma = \begin{pmatrix} 5 \\ 0 \end{pmatrix} \in \mathbb{R}^{2 \times 1}$.

3. **Compute Left-Singular Vectors ($U$):**
   $$u_1 = \frac{1}{\sigma_1} A v_1 = \frac{1}{5} \begin{pmatrix} 3 \\ 4 \end{pmatrix} [1] = \begin{pmatrix} 0.6 \\ 0.8 \end{pmatrix}$$
   We need an orthonormal basis for $\mathbb{R}^2$, so we must find a vector $u_2$ that is orthogonal to $u_1$:
   $$u_2^T u_1 = 0 \implies u_2 = \begin{pmatrix} -0.8 \\ 0.6 \end{pmatrix}$$
   Thus, $U = \begin{pmatrix} 0.6 & -0.8 \\ 0.8 & 0.6 \end{pmatrix} \in \mathbb{R}^{2 \times 2}$.

4. **Verify Reconstruction:**
   $$U \Sigma V^T = \begin{pmatrix} 0.6 & -0.8 \\ 0.8 & 0.6 \end{pmatrix} \begin{pmatrix} 5 \\ 0 \end{pmatrix} [1] = \begin{pmatrix} 0.6 \times 5 \\ 0.8 \times 5 \end{pmatrix} = \begin{pmatrix} 3 \\ 4 \end{pmatrix} = A$$
   The reconstruction is exact. SVD has decomposed the $2 \times 1$ transformation into a scaling of $5$ mapping from the 1D input space $V$ into the primary output direction $u_1$ of the 2D space.

---

## ML Applications

1. **Low-Rank Matrix Completion (Recommender Systems):**
   In collaborative filtering, we have a partially observed user-item rating matrix $R \in \mathbb{R}^{m \times n}$. We assume $R$ can be approximated by a low-rank matrix $X = U_k \Sigma_k V_k^T$ where $k \ll \min(m, n)$. Algorithms like Alternating Least Squares (ALS) solve this low-rank matrix completion problem, predicting unobserved ratings by learning latent user features ($U_k$) and item features ($V_k$).
2. **Latent Semantic Analysis (LSA):**
   In NLP, a document collection is represented as a term-document matrix $X \in \mathbb{R}^{m \times n}$ where $X_{ij}$ is the frequency of term $i$ in document $j$. By computing the truncated SVD $X \approx U_k \Sigma_k V_k^T$, we map terms and documents into a low-dimensional "latent semantic space." Words that appear in similar contexts are mapped to nearby vectors, allowing the discovery of latent synonyms and topics.
3. **Principal Component Analysis (PCA):**
   PCA is traditionally implemented via SVD. For a design matrix $X \in \mathbb{R}^{n \times d}$ centered to have zero column mean, SVD yields $X = U \Sigma V^T$. The columns of $V$ are the principal directions, and the project representation is $XV = U\Sigma$. Implementing PCA via SVD is numerically more stable than diagonalizing the covariance matrix $X^T X$ directly.
4. **Image Compression and Denoising:**
   An image represented as a matrix $A \in \mathbb{R}^{m \times n}$ is compressed by storing only $U_k, \Sigma_k, V_k^T$ for $k \ll \min(m, n)$. This reduces storage from $O(mn)$ to $O(k(m+n))$. Similarly, denoising is performed by truncating singular values below a threshold, effectively discarding the low-energy, high-frequency components that represent random noise.

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** When implementing SVD in code, different libraries (e.g., NumPy's `np.linalg.svd` vs. SciPy's `scipy.sparse.linalg.svds`) return the matrices in different formats. For example, NumPy returns $V^T$ directly as the third argument, whereas some packages return $V$. Always check the shape and verify the orthogonality condition $U^T U = I$ before performing projection operations.

</div>

