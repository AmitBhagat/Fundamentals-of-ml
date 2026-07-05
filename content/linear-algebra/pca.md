---
title: "Principal Component Analysis (PCA)"
description: "Covariance formulation, Lagrangian variance maximization, spectral projections, and dimension reduction."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Matrices", "Eigenvalues and Eigenvectors", "Positive Definite Matrices"]
---

<h1 align="center"> Chapter 22: PCA </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Covariance Matrix:** Understanding how features correlate and spread together.
* **Eigenvectors:** Knowing how to find characteristic scaling directions of a matrix.

</div>

## 1. Conceptual Hook

In machine learning, high-dimensional datasets are a double-edged sword. While more features can theoretically capture more detail, they also trigger the "curse of dimensionality," multiplying compute times, introducing correlation redundancies, and causing models to overfit on noise. How do we compress our features without losing the essential signals? We use **Principal Component Analysis (PCA)**.

PCA is an unsupervised coordinate transformation. Instead of selecting a subset of features, PCA rotates the coordinate axes of our data space to align with the directions of maximum spread, or **variance**. The first principal component captures the most significant pattern in the data; the second captures the next largest orthogonal pattern, and so on. By projecting our data onto the top principal components, we can discard the low-variance directions—which contain primarily random noise—and describe complex systems with a fraction of the original variables.

---

## 2. Formal Definition

Let $X \in \mathbb{R}^{n \times d}$ be a data matrix representing $n$ observations and $d$ features. We assume the data is centered such that each feature (column) has a mean of zero:
$$\sum_{i=1}^n X_{ij} = 0 \quad \forall j=1, \dots, d$$

The sample covariance matrix $\Sigma \in \mathbb{R}^{d \times d}$ is defined as:
$$\Sigma = \frac{1}{n-1} X^T X$$
$\Sigma$ is a symmetric, positive semi-definite matrix.

The objective of PCA is to find an orthogonal transformation matrix $W \in \mathbb{R}^{d \times k}$ (with $k \le d$) whose columns $\{w_1, w_2, \dots, w_k\}$ represent the **principal components**. For the first principal component $w_1 \in \mathbb{R}^d$, we seek the direction that maximizes the variance of the projected data points:
$$\max_{w_1} \text{Var}(Xw_1) = \max_{w_1} \frac{1}{n-1} (Xw_1)^T (Xw_1) = \max_{w_1} w_1^T \Sigma w_1$$
subject to the unit-norm constraint to prevent arbitrary scaling:
$$w_1^T w_1 = 1$$

Subsequent principal components $\{w_2, \dots, w_k\}$ maximize the projected variance under the same unit-norm constraint while remaining mutually orthogonal to all previous components:
$$w_j^T w_i = 0 \quad \forall i < j$$

---

## 3. Illustrative Derivation

### Lagrangian Formulation of PCA
We derive the optimal direction $w_1$ by setting up a constrained optimization problem using Lagrange multipliers.

The objective is:
$$\max_{w_1} w_1^T \Sigma w_1 \quad \text{subject to } w_1^T w_1 = 1$$
We formulate the Lagrangian function:
$$\mathcal{L}(w_1, \lambda) = w_1^T \Sigma w_1 - \lambda (w_1^T w_1 - 1)$$
where $\lambda \in \mathbb{R}$ is the Lagrange multiplier.

To find the critical points, we take the gradient of $\mathcal{L}$ with respect to the vector $w_1$:
$$\nabla_{w_1} \mathcal{L} = \nabla_{w_1} \left( w_1^T \Sigma w_1 \right) - \nabla_{w_1} \left( \lambda (w_1^T w_1 - 1) \right)$$
Using matrix calculus rules for symmetric $\Sigma$:
$$\nabla_{w_1} \mathcal{L} = 2 \Sigma w_1 - 2 \lambda w_1$$

Setting the gradient to zero:
$$2 \Sigma w_1 - 2 \lambda w_1 = 0$$
$$\Sigma w_1 = \lambda w_1$$
This is the classic **eigenvalue equation**. The weight vector $w_1$ must be an eigenvector of the covariance matrix $\Sigma$, and the Lagrange multiplier $\lambda$ is its corresponding eigenvalue.

Now, let us evaluate the variance of the projected data along this optimal direction:
$$\text{Var}(Xw_1) = w_1^T \Sigma w_1$$
Substitute our eigenvalue identity $\Sigma w_1 = \lambda w_1$ into this expression:
$$\text{Var}(Xw_1) = w_1^T (\lambda w_1) = \lambda (w_1^T w_1)$$
Since $w_1$ is a unit vector ($w_1^T w_1 = 1$):
$$\text{Var}(Xw_1) = \lambda$$
This reveals that the variance of the projected data is exactly equal to the eigenvalue corresponding to the chosen eigenvector. Because our objective is to *maximize* the variance, we must choose the eigenvector $w_1$ associated with the largest eigenvalue $\lambda_1$:
$$\lambda_{max} = \lambda_1$$
The remaining principal components are the eigenvectors corresponding to the remaining eigenvalues sorted in descending order: $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_d$. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Centered 2D Dataset Projection
Let a centered dataset of 3 observations in $\mathbb{R}^2$ be:
$$X = \begin{pmatrix} 1 & 1 \\ 0 & 0 \\ -1 & -1 \end{pmatrix}$$
1.  **Compute the Covariance Matrix $\Sigma$:**
    $$\Sigma = \frac{1}{2} X^T X = \frac{1}{2} \begin{pmatrix} 1 & 0 & -1 \\ 1 & 0 & -1 \end{pmatrix} \begin{pmatrix} 1 & 1 \\ 0 & 0 \\ -1 & -1 \end{pmatrix} = \frac{1}{2} \begin{pmatrix} 2 & 2 \\ 2 & 2 \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$$
2.  **Find the Eigenvalues:**
    $$\det(\Sigma - \lambda I) = (1-\lambda)^2 - 1 = \lambda^2 - 2\lambda = \lambda(\lambda - 2) = 0 \implies \lambda_1 = 2, \quad \lambda_2 = 0$$
3.  **Find the Eigenvector for $\lambda_1 = 2$:**
    $$(\Sigma - 2I)w_1 = 0 \implies \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix} \begin{bmatrix} w_{11} \\ w_{12} \end{bmatrix} = 0 \implies w_{11} = w_{12}$$
    Normalizing the vector:
    $$w_1 = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix}$$
Since $\lambda_2 = 0$, $100\%$ of the variance is captured along the diagonal direction $w_1$. The waist and chest features move in perfect lockstep, meaning the tailor can compress this 2D dataset to 1D without losing any information.

### Example 2: Variance Coverage Calculation
Let a covariance matrix of a dataset be $\Sigma = \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$.
1.  **Compute Eigenvalues:**
    $$\det(\Sigma - \lambda I) = (3-\lambda)^2 - 1 = \lambda^2 - 6\lambda + 8 = 0 \implies (\lambda - 4)(\lambda - 2) = 0 \implies \lambda_1 = 4, \quad \lambda_2 = 2$$
2.  **Calculate Total Variance:**
    $$\text{Tr}(\Sigma) = 3 + 3 = 6$$
    $$\lambda_1 + \lambda_2 = 4 + 2 = 6$$
3.  **Find Proportion of Explained Variance:**
    $$\text{Explained Ratio (PC1)} = \frac{\lambda_1}{\lambda_1 + \lambda_2} = \frac{4}{6} \approx 66.67\%$$
Projecting the dataset onto the first principal component preserves $66.67\%$ of the total data spread, discarding the remaining $33.33\%$ as lower-priority variation.

---

## 5. Applied ML Context

1.  **Eigenfaces in Computer Vision:** Images of human faces consist of thousands of pixels (dimensions). PCA projects these pixel vectors onto the top eigenvectors of the facial covariance matrix (eigenfaces), reducing dimensions to enable efficient face recognition.
2.  **Removing Multicollinearity:** If features in a regression dataset are highly correlated, standard OLS will fail due to singular covariance. Projecting features onto principal components yields mutually orthogonal features, stabilizing the model.
3.  **Data Visualization:** In high-dimensional biological datasets (like gene expression tables containing 20,000 dimensions), PCA is used to project samples onto 2D or 3D spaces to visually inspect patient clusters.
4.  **Denoising Data:** By reconstructing datasets using only the top $k$ principal components (discarding components with small eigenvalues), PCA filters out high-frequency Gaussian noise.
5.  **LLM Latent Semantic Analysis (LSA):** Term-document matrices in natural language processing are compressed using SVD (the underlying algorithm for PCA) to map words and documents to a low-dimensional concept space.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating PCA rotation:
*   Show a 2D scatter plot of data points forming an elongated, tilted ellipse.
*   Draw two perpendicular vectors starting from the center of the ellipse:
    1.  A long green arrow ($w_1$, the first principal component) pointing along the major axis of the ellipse (the direction of maximum variance).
    2.  A short red arrow ($w_2$, the second principal component) pointing along the minor axis (orthogonal to $w_1$).
*   Draw a second graph showing the coordinate axes rotated so that the horizontal axis aligns with $w_1$ and the vertical axis aligns with $w_2$, demonstrating how PCA projects and aligns coordinates.
*   Add a visual projection line showing how collapsing points onto the $w_1$ axis simplifies the coordinates to 1D while preserving the maximum spread.
