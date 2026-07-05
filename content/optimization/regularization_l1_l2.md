---
title: "Regularization (L1, L2)"
description: "Overfitting controls, complexity penalties, Lasso and Ridge regressions, subgradients, weight decay, and sparsity proofs."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Derivatives", "Optimization: Gradient Descent", "Optimization: Stochastic Gradient Descent"]
---

<h1 align="center"> Chapter 92: Regularization (L1, L2) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Overfitting:** The phenomenon where a model fits the training set's random noise rather than the general population distribution.
* **Vector Norms:** Mathematical functions that measure the length or magnitude of a vector.

</div>

## 1. Conceptual Hook

When training machine learning models, there is a constant tug-of-war between fitting the training data and generalizing to new, unseen testing data. If a model has too much capacity, it will simply memorize the training set—including its random noise. When evaluated on test data, the model fails.

**Regularization** is the mathematical discipline that resolves this by imposing a cost on model complexity.

Instead of allowing parameters to grow arbitrarily large to fit every data point, we add a complexity penalty to our loss function. This forces the optimization algorithm to justify the presence of every parameter weight.

Think of this as cleaning out a refrigerator:
*   **$L_2$ regularization (Ridge)** acts as a gentle audit that shrinks all weights proportionally. It keeps the parameters small and well-behaved, ensuring no single feature dominates the model.
*   **$L_1$ regularization (Lasso)** acts as a strict filter that drives less useful weights to exactly zero. It actively discards noise features, leaving only the essential variables for general predictions.

---

## 2. Formal Definition

Let $L(\mathbf{w})$ represent the unregularized empirical loss of a model (e.g. Mean Squared Error) over a training dataset. We define the regularized objective function $J(\mathbf{w})$ as:
$$J(\mathbf{w}) = L(\mathbf{w}) + \lambda \Omega(\mathbf{w})$$
where:
*   **$\lambda \ge 0$ (Regularization Strength):** A hyperparameter that controls the trade-off between fitting the training data and keeping the weights small.
*   **$\Omega(\mathbf{w})$ (Complexity Penalty):** A function of the weight vector $\mathbf{w} \in \mathbb{R}^d$.

### 1. L2 Regularization (Ridge / Tikhonov Regularization)
The L2 penalty uses the squared Euclidean norm of the weight vector:
$$\Omega(\mathbf{w}) = \frac{1}{2} \|\mathbf{w}\|_2^2 = \frac{1}{2} \sum_{j=1}^{d} w_j^2$$
Under Gradient Descent with step size $\eta$, the L2 regularized update rule is:
$$\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \nabla L\left(\mathbf{w}^{(t)}\right) - \eta \lambda \mathbf{w}^{(t)} = (1 - \eta \lambda) \mathbf{w}^{(t)} - \eta \nabla L\left(\mathbf{w}^{(t)}\right)$$
This update is known as **Weight Decay** because it shrinks the weights by a factor of $(1 - \eta \lambda)$ before applying the gradient step.

### 2. L1 Regularization (Lasso)
The L1 penalty uses the Manhattan norm of the weight vector, summing the absolute values of the coordinates:
$$\Omega(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_{j=1}^{d} |w_j|$$
Because the absolute value function $|w_j|$ has a sharp corner at zero, it is non-differentiable. We define the penalty's subgradient with respect to $w_j$ as:
$$\partial_{w_j} \Omega(\mathbf{w}) = \text{sgn}(w_j) = \begin{cases} \{1\} & \text{if } w_j > 0 \\ \{-1\} & \text{if } w_j < 0 \\ [-1, 1] & \text{if } w_j = 0 \end{cases}$$

---

## 3. Illustrative Derivation

### Proof: Why L1 Regularization Induces Sparsity while L2 Does Not
We prove the geometric necessity of sparsity in L1 optimization by formulating regularized objectives as constrained optimization problems.

*Proof:*
By the Lagrangian duality theorem, minimizing the regularized objective $J(\mathbf{w}) = L(\mathbf{w}) + \lambda \Omega(\mathbf{w})$ is mathematically equivalent to solving the constrained optimization problem:
$$\min_{\mathbf{w}} L(\mathbf{w}) \quad \text{subject to} \quad \Omega(\mathbf{w}) \le t$$
where $t > 0$ is a budget parameter inversely related to $\lambda$. Let us analyze the geometry of the feasible region in $d=2$ dimensions:

1.  **L2 Regularization geometry:**
    The constraint is $\|\mathbf{w}\|_2^2 \le t$, which corresponds to a circular feasible region bounded by the boundary curve $w_1^2 + w_2^2 = t$.
    The loss function contours $L(\mathbf{w})$ are represented as ellipsoids centered around the unregularized optimal solution $\mathbf{w}_{OLS}$.
    To locate the constrained optimum $\mathbf{w}^*$, we expand the ellipsoidal contours of the loss function outward until they touch the constraint boundary.
    Because the circular boundary is perfectly smooth, the tangent contact point between the circular constraint and the elliptical loss contours is highly unlikely to land exactly on one of the coordinate axes ($w_1 = 0$ or $w_2 = 0$).
    Therefore, both optimal weights $w_1^*$ and $w_2^*$ are shrunk toward zero but remain non-zero:
    $$\mathbf{w}^*_{L2} = (w_1^*, \quad w_2^*) \quad \text{where} \quad w_1^* \neq 0, \quad w_2^* \neq 0$$

2.  **L1 Regularization geometry:**
    The constraint is $\|\mathbf{w}\|_1 \le t$, which corresponds to a diamond-shaped feasible region bounded by the boundary curve $|w_1| + |w_2| = t$.
    This diamond has sharp corners (vertices) lying exactly on the coordinate axes: $(t, 0)$, $(0, t)$, $(-t, 0)$, and $(0, -t)$.
    As the ellipsoidal loss contours expand outward from $\mathbf{w}_{OLS}$ toward the origin, they are far more likely to contact one of these sharp corners of the diamond than a flat edge.
    This is because the corners project outward along the coordinate axes.
    When contact occurs at a vertex, the coordinate corresponding to the other axis is set to exactly zero:
    $$\mathbf{w}^*_{L1} = (t, \quad 0) \implies w_2^* = 0$$
In higher dimensions ($d \gg 2$), the L1 ball is a cross-polytope with many low-dimensional faces and vertices lying on coordinate subspaces. This geometry forces a large fraction of the optimal weights to be exactly zero, inducing sparsity. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: L2 Weight Decay Update Step
We perform one update step under L2 regularization. Let initial weight $w^{(0)} = 10.0$ and the loss gradient at this point be $\nabla L = 50.0$. We set the learning rate $\eta = 0.05$ and L2 penalty coefficient $\lambda = 0.2$.
1.  **Calculate the weight decay coefficient:**
    $$1 - \eta\lambda = 1 - 0.05 \cdot 0.2 = 1 - 0.01 = 0.99$$
2.  **Perform the update:**
    $$w^{(1)} = (1 - \eta\lambda)w^{(0)} - \eta \nabla L = 0.99 \cdot 10.0 - 0.05 \cdot 50.0 = 9.9 - 2.5 = 7.4$$
*Note:* Without regularization, the update would be $10.0 - 2.5 = 7.5$. The L2 penalty decays the weight by an additional $0.1$ units.

### Example 2: Elastic Net Cost Evaluation
We evaluate the Elastic Net cost function (which combines L1 and L2 penalties) for a weight vector $\mathbf{w} = [3.0, -4.0]^T$. Let the training loss $L(\mathbf{w}) = 12.0$, L1 coefficient $\lambda_1 = 2.0$, and L2 coefficient $\lambda_2 = 1.5$.
1.  **Compute norms:**
    $$\|\mathbf{w}\|_1 = |3.0| + |-4.0| = 7.0$$
    $$\frac{1}{2}\|\mathbf{w}\|_2^2 = \frac{1}{2} (3.0^2 + (-4.0)^2) = \frac{1}{2} (9.0 + 16.0) = 12.5$$
2.  **Evaluate total cost:**
    $$J(\mathbf{w}) = L(\mathbf{w}) + \lambda_1 \|\mathbf{w}\|_1 + \lambda_2 \left( \frac{1}{2}\|\mathbf{w}\|_2^2 \right) = 12.0 + 2.0 \cdot 7.0 + 1.5 \cdot 12.5 = 12.0 + 14.0 + 18.75 = 44.75$$

---

## 5. Applied ML Context

1.  **Lasso in Genomics:** When analyzing gene datasets where the number of features $d$ is far larger than the sample count $m$, L1 regularization is used to select the sparse subset of genes responsible for a disease.
2.  **Ridge in Multicollinear Regressions:** In econometrics, when features are highly correlated, the matrix $\mathbf{X}^T\mathbf{X}$ is nearly singular. L2 adds a diagonal scaling term $(\mathbf{X}^T\mathbf{X} + \lambda \mathbf{I})$, stabilizing matrix inversion.
3.  **Neural Network Weight Decay:** L2 regularization is standard in deep learning pipelines to prevent exploding weight values and stabilize backpropagation updates.
4.  **Elastic Net Credit Risk Models:** Combining L1 and L2 penalties allows models to handle groups of correlated financial variables (like income metrics) while maintaining sparsity.
5.  **Sparse Dictionary Coding:** In computer vision, L1 penalties are used to reconstruct complex images using a sparse combination of basis functions.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating L1 vs L2 geometry:
*   Draw 2D coordinate axes $w_1$ and $w_2$.
*   Draw two constraint shapes centered at $(0, 0)$:
    1.  **L2 Norm Ball:** A circle of radius $t$ representing the constraint $w_1^2 + w_2^2 \le t$.
    2.  **L1 Norm Ball:** A diamond of radius $t$ representing the constraint $|w_1| + |w_2| \le t$.
*   Draw concentric ellipses centered at $\mathbf{w}_{OLS}$ (representing constant loss contours).
*   Show one ellipse touching the L2 circle tangent boundary at a point off the axes (where both $w_1$ and $w_2$ are non-zero).
*   Show another ellipse touching the L1 diamond at a sharp corner vertex lying exactly on the $w_1$-axis (where $w_2 = 0$).
*   Add a caption explaining that because the L1 diamond has sharp corners on the axes, expanding loss contours are highly likely to make contact at a vertex where one or more weights are set to exactly zero, creating a sparse model.
