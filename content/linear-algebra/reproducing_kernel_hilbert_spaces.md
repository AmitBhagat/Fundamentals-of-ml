---
title: "Reproducing Kernel Hilbert Spaces (RKHS)"
description: "Infinite-dimensional function spaces, the Riesz representation theorem, and the Representer Theorem."
complexity: "Advanced"
estimated_time: "45 min"
prerequisites: ["Vector Spaces", "Inner Products", "Eigenvalues and Eigenvectors"]
---

<h1 align="center"> Chapter 26: Reproducing Kernel Hilbert Spaces (RKHS) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Hilbert Spaces:** Inner product spaces that are complete (every Cauchy sequence converges).
* **Dual Spaces:** The space of bounded linear functionals mapping functions to scalars.
* **Positive Definiteness:** Generalizing positive semi-definite matrices to continuous kernels.

</div>

## Analogy

Think of a Reproducing Kernel Hilbert Space (RKHS) as an **infinite-dimensional sorting warehouse with a master blueprint**.

Imagine you are trying to classify complex, tangled shapes (like handwriting or protein sequences) that are impossible to separate on a flat table. To solve this, you decide to project these shapes into a high-dimensional space where they can be separated by a flat sheet of glass. 

Normally, working in an infinite-dimensional space would require infinite memory and computational power—an impossible warehouse to manage. 

The **kernel** is the "master blueprint." Instead of physically placing each item in the infinite warehouse and measuring their coordinates, the blueprint allows you to calculate the exact distance and relationship between any two items *as if* they were sitting in the warehouse, using only their original, flat-table coordinates. The **reproducing property** is the warehouse retrieval clerk: it guarantees that evaluating the value of a function at any specific point is as simple as taking a single inner product with the kernel.

## The Math Link

### 1. Evaluation Functionals and RKHS Definition
Let $\mathcal{H}$ be a Hilbert space of real-valued functions defined on a non-empty set $\mathcal{X}$. For any $x \in \mathcal{X}$, the **evaluation functional** $\delta_x: \mathcal{H} \to \mathbb{R}$ is the operator that evaluates a function $f \in \mathcal{H}$ at the point $x$:
$$\delta_x(f) = f(x)$$
A Hilbert space $\mathcal{H}$ is a **Reproducing Kernel Hilbert Space (RKHS)** if and only if the evaluation functional $\delta_x$ is bounded (continuous) for all $x \in \mathcal{X}$:
$$\exists M_x > 0 \quad \text{s.t.} \quad |\delta_x(f)| = |f(x)| \le M_x \|f\|_{\mathcal{H}} \quad \forall f \in \mathcal{H}$$

### 2. The Reproducing Kernel
By the **Riesz Representation Theorem**, since $\delta_x$ is a bounded linear functional on the Hilbert space $\mathcal{H}$, there exists a unique representative element in $\mathcal{H}$, which we denote as $K_x \in \mathcal{H}$, such that:
$$\delta_x(f) = \langle f, K_x \rangle_{\mathcal{H}} \quad \forall f \in \mathcal{H}$$
Defining the bivariate function $K: \mathcal{X} \times \mathcal{X} \to \mathbb{R}$ as $K(x, y) = K_x(y)$, we obtain the two defining properties of a reproducing kernel:
1. **Membership:** $K(\cdot, x) \in \mathcal{H}$ for all $x \in \mathcal{X}$.
2. **Reproducing Property:** For all $x \in \mathcal{X}$ and $f \in \mathcal{H}$:
   $$\langle f, K(\cdot, x) \rangle_{\mathcal{H}} = f(x)$$
In particular, for any $x, y \in \mathcal{X}$:
$$\langle K(\cdot, x), K(\cdot, y) \rangle_{\mathcal{H}} = K(x, y)$$

### 3. Mercer's Theorem
A symmetric function $K: \mathcal{X} \times \mathcal{X} \to \mathbb{R}$ is a reproducing kernel if and only if it is positive definite, meaning for any $n \in \mathbb{N}$, any points $x_1, \dots, x_n \in \mathcal{X}$, and any coefficients $c_1, \dots, c_n \in \mathbb{R}$:
$$\sum_{i=1}^n \sum_{j=1}^n c_i c_j K(x_i, x_j) \ge 0$$
**Mercer's Theorem** states that if $K$ is continuous and positive definite on a compact domain $\mathcal{X}$, it can be expanded as:
$$K(x, y) = \sum_{i=1}^\infty \lambda_i \phi_i(x) \phi_i(y)$$
where $\{\lambda_i\}_{i=1}^\infty$ are non-negative eigenvalues and $\{\phi_i\}_{i=1}^\infty$ are orthonormal eigenfunctions. This establishes the implicit feature map $\Phi(x) = (\sqrt{\lambda_1}\phi_1(x), \sqrt{\lambda_2}\phi_2(x), \dots)^T$ into the sequence space $\ell^2$, verifying the kernel trick:
$$\langle \Phi(x), \Phi(y) \rangle_{\ell^2} = K(x, y)$$

---

## Proof-Based Exercises

### Exercise 1: Proof of the Representer Theorem
**Theorem:** Let $\mathcal{X}$ be a set, $K$ a positive definite kernel, and $\mathcal{H}_K$ its corresponding RKHS. Given a training set $\{(x_i, y_i)\}_{i=1}^n \subset \mathcal{X} \times \mathbb{R}$, a strictly increasing regularization function $\Omega: [0, \infty) \to \mathbb{R}$, and an arbitrary loss function $L: \mathbb{R}^n \to \mathbb{R}$, any minimizer of the regularized empirical risk:
$$f^* = \arg\min_{f \in \mathcal{H}_K} L(f(x_1), \dots, f(x_n)) + \Omega(\|f\|_{\mathcal{H}_K}^2)$$
must admit a representation of the form:
$$f^*(x) = \sum_{i=1}^n \alpha_i K(x, x_i) \quad \text{for some } \alpha_1, \dots, \alpha_n \in \mathbb{R}$$

*Proof:*
This is a bit of a headache if you try using infinite expansions, but here is the trick: use the orthogonal decomposition of Hilbert spaces.
Let $\mathcal{U} = \text{span}\{K(\cdot, x_1), \dots, K(\cdot, x_n)\} \subset \mathcal{H}_K$ be the finite-dimensional subspace spanned by the kernel evaluations at the data points.
We can decompose any function $f \in \mathcal{H}_K$ into a component in $\mathcal{U}$ and a component orthogonal to it in $\mathcal{U}^\perp$:
$$f = f_{\parallel} + f_{\perp}$$
where $f_{\parallel} \in \mathcal{U}$ and $f_{\perp} \in \mathcal{U}^\perp$. By the definition of $\mathcal{U}$, we have:
$$\langle f_{\perp}, K(\cdot, x_i) \rangle_{\mathcal{H}_K} = 0 \quad \forall i=1, \dots, n$$
Evaluate $f$ at any training point $x_i$ using the reproducing property:
$$f(x_i) = \langle f, K(\cdot, x_i) \rangle_{\mathcal{H}_K} = \langle f_{\parallel} + f_{\perp}, K(\cdot, x_i) \rangle_{\mathcal{H}_K} = \langle f_{\parallel}, K(\cdot, x_i) \rangle_{\mathcal{H}_K} + \langle f_{\perp}, K(\cdot, x_i) \rangle_{\mathcal{H}_K}$$
Since $f_{\perp} \in \mathcal{U}^\perp$, the second term vanishes:
$$f(x_i) = \langle f_{\parallel}, K(\cdot, x_i) \rangle_{\mathcal{H}_K} = f_{\parallel}(x_i)$$
This proves that the predictions of $f$ and $f_{\parallel}$ are identical at all training points, meaning:
$$L(f(x_1), \dots, f(x_n)) = L(f_{\parallel}(x_1), \dots, f_{\parallel}(x_n))$$
Now examine the regularization term. By the Pythagorean theorem in Hilbert spaces, since $f_{\parallel} \perp f_{\perp}$:
$$\|f\|_{\mathcal{H}_K}^2 = \|f_{\parallel} + f_{\perp}\|_{\mathcal{H}_K}^2 = \|f_{\parallel}\|_{\mathcal{H}_K}^2 + \|f_{\perp}\|_{\mathcal{H}_K}^2 \ge \|f_{\parallel}\|_{\mathcal{H}_K}^2$$
Since $\Omega$ is strictly increasing:
$$\Omega(\|f\|_{\mathcal{H}_K}^2) \ge \Omega(\|f_{\parallel}\|_{\mathcal{H}_K}^2)$$
with equality holding if and only if $\|f_{\perp}\|_{\mathcal{H}_K}^2 = 0 \iff f_{\perp} = 0$.
Thus, the objective function value for $f_{\parallel}$ is always strictly less than or equal to that of $f$. Any minimizer $f^*$ must satisfy $f_{\perp} = 0$, meaning $f^* \in \mathcal{U}$.
Consequently, $f^*$ must lie in the span of $\{K(\cdot, x_1), \dots, K(\cdot, x_n)\}$:
$$f^*(x) = \sum_{i=1}^n \alpha_i K(x, x_i)$$
This completes the proof. $\blacksquare$

---

## Let's Run the Numbers

### Example: Kernel Ridge Regression (KRR)

Suppose we have a 1D training set $\{(x_1, y_1), (x_2, y_2)\} = \{(1, 2), (2, 3)\}$ and we use a linear kernel $K(x, z) = xz$. We want to find the optimal function $f^*(x)$ that minimizes:
$$\sum_{i=1}^2 (f(x_i) - y_i)^2 + \lambda \|f\|_{\mathcal{H}_K}^2 \quad \text{with } \lambda = 1$$

1. **Apply the Representer Theorem:**
   The optimal function is $f^*(x) = \alpha_1 K(x, x_1) + \alpha_2 K(x, x_2) = \alpha_1 (x) + \alpha_2 (2x) = (\alpha_1 + 2\alpha_2)x$.

2. **Formulate the Kernel Matrix $K$:**
   $$K = \begin{pmatrix} K(x_1, x_1) & K(x_1, x_2) \\ K(x_2, x_1) & K(x_2, x_2) \end{pmatrix} = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$$

3. **Solve for $\alpha$:**
   The KRR objective in matrix form is $(K\alpha - y)^2 + \lambda \alpha^T K \alpha$. Differentiating and setting to zero yields the system:
   $$(K + \lambda I)\alpha = y$$
   $$\begin{pmatrix} 1+1 & 2 \\ 2 & 4+1 \end{pmatrix} \begin{pmatrix} \alpha_1 \\ \alpha_2 \end{pmatrix} = \begin{pmatrix} 2 \\ 3 \end{pmatrix} \implies \begin{pmatrix} 2 & 2 \\ 2 & 5 \end{pmatrix} \begin{pmatrix} \alpha_1 \\ \alpha_2 \end{pmatrix} = \begin{pmatrix} 2 \\ 3 \end{pmatrix}$$
   Solving this linear system:
   $$\alpha_2 = \frac{1}{3}, \quad \alpha_1 = \frac{2}{3}$$
   The optimal function is:
   $$f^*(x) = \left(\frac{2}{3} + 2\left(\frac{1}{3}\right)\right)x = \frac{4}{3}x$$

---

## ML Applications

1. **Kernel Support Vector Machines (SVM):**
   SVMs classify non-linearly separable data by implicitly mapping them to an infinite-dimensional RKHS. By using kernels like the Radial Basis Function (RBF) kernel $K(x, y) = \exp(-\gamma \|x-y\|^2)$, SVMs construct a linear hyperplane classifier in the RKHS, which maps back to a non-linear decision boundary in the input space $\mathcal{X}$.
2. **Gaussian Processes (GP):**
   GPs define a prior distribution over functions, where the covariance between any two function evaluations is determined by a positive definite kernel. Solving a GP regression problem is mathematically equivalent to Kernel Ridge Regression, with the RKHS norm acting as the log-prior in a Bayesian formulation.
3. **Maximum Mean Discrepancy (MMD):**
   MMD is a kernel-based statistical test used to determine whether two probability distributions $P$ and $Q$ are different. It measures the distance between the mean embeddings of $P$ and $Q$ in the RKHS:
   $$\text{MMD}^2(P, Q) = \|\mathbb{E}_{X \sim P}[\Phi(X)] - \mathbb{E}_{Y \sim Q}[\Phi(Y)]\|_{\mathcal{H}_K}^2$$
   MMD is widely used to train Generative Adversarial Networks (MMD-GANs) and to evaluate domain adaptation.
4. **Kernel PCA:**
   Standard PCA only identifies linear principal components. Kernel PCA projects data into an RKHS first, then performs PCA on the mapped features. This allows the extraction of non-linear principal components, revealing complex topological manifolds in the data.

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Gotcha:** While RBF kernels are incredibly powerful, they assume the data is dense and smooth. If your input space is high-dimensional and sparse (e.g., text document vectors), the RBF kernel can suffer from the **curse of dimensionality**, where the distance between any two points approaches a constant, causing the kernel matrix to degenerate into the identity matrix $I$.

</div>
