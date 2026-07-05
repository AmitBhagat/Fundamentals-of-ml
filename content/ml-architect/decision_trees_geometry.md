---
title: "Decision Trees Geometry"
description: "Recursive space partitioning, axis-aligned cuts, entropy and Gini impurity metrics, information gain, and high-cardinality bias."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Foundations", "Probability: Shannon Entropy", "Probability: Joint and Marginal Distributions"]
---

<h1 align="center"> Chapter 115: Decision Trees Geometry </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Shannon Entropy:** A measure of the average uncertainty or information content in a random variable distribution.
* **Recursive Partitioning:** The process of repeatedly splitting a dataset into smaller, more homogenous subsets.

</div>

## 1. Conceptual Hook

When classifying data, linear models draw straight continuous hyperplanes across the entire feature space. While this is highly effective for linear relationships, it fails when data is organized in non-linear, hierarchical clusters.

A **Decision Tree** takes a different geometric approach. Instead of fitting a continuous plane, it recursively cuts the feature space into orthogonal, axis-aligned boxes.

It acts as a sequential flow of binary choices, like a game of "Twenty Questions." The tree searches for cuts that maximize the purity of the resulting subsets, isolating clusters of similar labels into distinct bounding regions.

Think of this like slicing a cake. You make straight perpendicular cuts along the axes to separate the layers and decorations. While a greedy, step-by-step splitting approach makes decision trees simple to build, it also makes them prone to overfitting—they will chase tiny noise patterns until they have carved out a specific rule for every single data point.

---

## 2. Formal Definition

Let $\mathcal{D}_m = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N_m}$ be the training subset arriving at node $m$, where features $\mathbf{x}_i \in \mathbb{R}^d$ and class labels $y_i \in \{1, 2, \dots, c\}$.

The proportion of class $k$ samples at node $m$ is:
$$p_{mk} = \frac{1}{N_m} \sum_{\mathbf{x}_i \in \mathcal{D}_m} \mathbb{I}(y_i = k)$$
where $\mathbb{I}(\cdot)$ is the indicator function.

### Impurity Metrics
We measure the heterogeneity (or "impurity") of node $m$ using one of three metrics:

1.  **Shannon Entropy:**
    $$H(m) = -\sum_{k=1}^{c} p_{mk} \log_2(p_{mk})$$
    where we define $0 \log_2 0 = 0$.
2.  **Gini Impurity:**
    $$I_G(m) = 1 - \sum_{k=1}^{c} p_{mk}^2$$
3.  **Classification Error:**
    $$E(m) = 1 - \max_{k \in \{1, \dots, c\}} p_{mk}$$

### Splitting Criterion
A candidate split is parameterized by a feature index $j \in \{1, \dots, d\}$ and a threshold value $t \in \mathbb{R}$. This split partitions the dataset $\mathcal{D}_m$ into left and right child subsets:
$$\mathcal{D}_L(j, t) = \{\mathbf{x}_i \in \mathcal{D}_m \mid x_{ij} \le t\} \quad \text{and} \quad \mathcal{D}_R(j, t) = \{\mathbf{x}_i \in \mathcal{D}_m \mid x_{ij} > t\}$$

Let $N_L = |\mathcal{D}_L|$ and $N_R = |\mathcal{D}_R|$. The **Information Gain** (or impurity reduction) is:
$$IG(j, t) = I(m) - \left( \frac{N_L}{N_m} I(L) + \frac{N_R}{N_m} I(R) \right)$$
where $I(\cdot)$ represents one of our impurity metrics. The algorithm greedily selects the optimal split parameters:
$$(j^*, t^*) = \arg\max_{j, t} IG(j, t)$$

---

## 3. Illustrative Derivation

### Proof: Maximum Gini Impurity Value in $c$-Class Classification
We prove that Gini impurity is a concave function, and derive its maximum possible value for a $c$-class system, showing it occurs under a uniform distribution.

*Proof:*
We seek to maximize the Gini impurity function:
$$I_G(p_1, \dots, p_c) = 1 - \sum_{k=1}^{c} p_k^2$$
subject to the probability simplex constraint:
$$\sum_{k=1}^{c} p_k = 1$$

1.  **Formulate the Lagrangian function:**
    We introduce a Lagrange multiplier $\lambda$:
    $$\mathcal{L}(p_1, \dots, p_c, \lambda) = 1 - \sum_{k=1}^{c} p_k^2 - \lambda \left( \sum_{k=1}^{c} p_k - 1 \right)$$

2.  **Compute partial derivatives with respect to $p_k$:**
    For each class $k \in \{1, \dots, c\}$, set the gradient to zero:
    $$\frac{\partial \mathcal{L}}{\partial p_k} = -2p_k - \lambda = 0 \implies p_k = -\frac{\lambda}{2}$$
This shows that at the critical point, the probability values for all classes must be equal to a constant.

3.  **Apply the constraint to solve for the constant value:**
    $$\sum_{k=1}^{c} p_k = 1 \implies c \left( -\frac{\lambda}{2} \right) = 1 \implies p_k = \frac{1}{c} \quad \forall k \in \{1, \dots, c\}$$

4.  **Confirm the critical point is a global maximum:**
    We construct the Hessian matrix $\mathbf{J}^2(I_G)$ with respect to $\mathbf{p}$:
    $$\frac{\partial^2 I_G}{\partial p_i \partial p_j} = \begin{cases} -2 & \text{if } i = j \\ 0 & \text{if } i \neq j \end{cases}$$
The Hessian matrix is diagonal with negative entries, making it negative definite ($\mathbf{H} \prec 0$). This guarantees that the uniform distribution point $p_k = \frac{1}{c}$ is a global maximum.

5.  **Evaluate the maximum Gini impurity:**
    $$I_{G, max} = 1 - \sum_{k=1}^{c} \left( \frac{1}{c} \right)^2 = 1 - c \left( \frac{1}{c^2} \right) = 1 - \frac{1}{c} = \frac{c - 1}{c} \quad \blacksquare$$

This proves that for a binary classification task ($c=2$), the maximum Gini impurity is exactly $0.5$, representing complete uncertainty.

---

## 4. Concrete Examples

### Example 1: Purity Metrics for Binary Datasets
Consider a node containing $10$ samples, with $7$ positive samples and $3$ negative samples.
1.  **Calculate Gini Impurity:**
    $$p_+ = 0.7 \quad \text{and} \quad p_- = 0.3$$
    $$I_G = 1 - \left( 0.7^2 + 0.3^2 \right) = 1 - (0.49 + 0.09) = 1 - 0.58 = 0.42$$
2.  **Calculate Shannon Entropy:**
    $$H = - \left( 0.7 \log_2 0.7 + 0.3 \log_2 0.3 \right)$$
    Since $\log_2 0.7 \approx -0.5146$ and $\log_2 0.3 \approx -1.7370$:
    $$H \approx - \left[ 0.7(-0.5146) + 0.3(-1.7370) \right] = -(-0.3602 - 0.5211) = 0.8813 \text{ bits}$$

### Example 2: Calculating Information Gain of a Split
We evaluate a candidate split that partitions the parent node ($N=10$, $I_G=0.42$) into:
*   **Left Child:** $N_L = 4$ samples, all positive ($I_G(L) = 0$).
*   **Right Child:** $N_R = 6$ samples, $3$ positive and $3$ negative ($I_G(R) = 0.5$).
1.  **Calculate weighted child impurity:**
    $$I_{children} = \frac{4}{10} \cdot I_G(L) + \frac{6}{10} \cdot I_G(R) = 0.4 \cdot 0 + 0.6 \cdot 0.5 = 0.3$$
2.  **Calculate Information Gain:**
    $$IG = I_{parent} - I_{children} = 0.42 - 0.3 = 0.12$$
If another candidate split yields an Information Gain of $0.2$, the tree will select that split instead.

---

## 5. Applied ML Context

1.  **Tabular Classification Baseline (CART):** Classification and Regression Trees (CART) are used to construct simple, interpretable baseline rules for tabular databases.
2.  **Random Forest Ensembles:** Constructing bags of uncorrelated trees using bootstrap aggregation, reducing the high variance of individual deep trees.
3.  **Gradient Boosted Decision Trees:** Algorithms like XGBoost, LightGBM, and CatBoost build sequential ensembles of shallow trees to fit residual errors.
4.  **Medical Symptom Triage:** Building decision trees of symptoms (e.g. fever, blood pressure thresholds) to classify emergency room patient priority.
5.  **Game AI NPC Behavior:** Simple decision trees are compiled to define non-player character actions based on state indicators (health, player proximity).

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating decision boundary partitioning:
*   Draw a 2D plane side-by-side with its corresponding binary tree structure:
    1.  **2D Partitioning Plot:** Show data points scattered on a plane. Draw a vertical line at $x_1 = t_1$ that cuts the plane. Draw a horizontal line at $x_2 = t_2$ cutting only the right half. Label the partitioned regions as leaves ($L_1, L_2, L_3$).
    2.  **Tree Diagram:** Draw the root node labeled "$x_1 \le t_1$". Show one branch leading to leaf $L_1$ and the other to decision node "$x_2 \le t_2$". Show this node branching to leaves $L_2$ and $L_3$.
*   Add a caption explaining that decision trees recursively partition high-dimensional feature spaces using axis-aligned cuts, creating rectangular, non-continuous decision boundaries.
