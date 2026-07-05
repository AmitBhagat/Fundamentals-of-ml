---
title: "Ordinary Least Squares"
description: "Linear regression, Residual Sum of Squares, Normal Equations, matrix calculus derivations, and multicollinearity."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Linear Algebra: Matrices", "Linear Algebra: Matrix Multiplication", "Linear Algebra: Matrix Inverse", "Calculus: Partial Derivatives", "Calculus: Gradient"]
---

<h1 align="center"> Chapter 69: Ordinary Least Squares </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Matrix Calculus:** Familiarity with taking gradients of vector quadratic forms: $\nabla_{\mathbf{w}} (\mathbf{w}^T\mathbf{A}\mathbf{w}) = 2\mathbf{A}\mathbf{w}$.
* **Matrix Invertibility:** Knowing that a matrix has an inverse if and only if it is of full rank.

</div>

## 1. Conceptual Hook

When we want to predict a continuous target variable—such as predicting house prices or estimating server CPU demand—the most fundamental model we turn to is Linear Regression. But how do we mathematically define the "best" straight line through a messy cloud of data points? The mathematical engine that solves this is **Ordinary Least Squares (OLS)**.

OLS operates like a tension system. It measures the vertical distance (residual) between each observed data point and our model's predicted line. To prevent positive and negative errors from canceling each other out, OLS squares these distances. This squaring behavior heavily penalizes large misses, ensuring the line stays close to all points. By minimizing the sum of these squared areas, OLS derives the famous "normal equations," providing a direct closed-form solution that calculates optimal parameters instantly without needing gradient descent.

---

## 2. Formal Definition

Let $\mathbf{y} \in \mathbb{R}^n$ be a vector of observed targets, and let $\mathbf{X} \in \mathbb{R}^{n \times d}$ be the design matrix of features (with sample size $n$ and feature dimension $d$, where $n \ge d$).

### The Linear Model
The linear relationship is formulated as:
$$\mathbf{y} = \mathbf{X}\mathbf{w} + \boldsymbol{\epsilon}$$
where:
*   **$\mathbf{w} \in \mathbb{R}^d$:** The vector of parameter coefficients we want to estimate.
*   **$\boldsymbol{\epsilon} \in \mathbb{R}^n$:** The vector of unobserved random error terms (residuals) representing the discrepancy between reality and predictions.

### The OLS Criterion
The OLS estimator $\hat{\mathbf{w}}$ is defined as the parameter vector that minimizes the **Residual Sum of Squares (RSS)**:
$$RSS(\mathbf{w}) = \sum_{i=1}^{n} (y_i - \mathbf{x}_i^T\mathbf{w})^2 = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2$$

In matrix notation, this quadratic objective is written as:
$$RSS(\mathbf{w}) = (\mathbf{y} - \mathbf{X}\mathbf{w})^T(\mathbf{y} - \mathbf{X}\mathbf{w})$$

Assuming the design matrix $\mathbf{X}$ has full column rank (meaning the features are linearly independent), the unique closed-form solution that minimizes this objective is given by the **Normal Equations**:
$$\hat{\mathbf{w}} = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T\mathbf{y}$$

---

## 3. Illustrative Derivation

### Derivation of the OLS Closed-Form Solution
We derive the estimator $\hat{\mathbf{w}} = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T\mathbf{y}$ by minimizing the matrix quadratic form of $RSS(\mathbf{w})$ using matrix calculus.

*Proof:*
1.  **Expand the RSS objective function $S(\mathbf{w})$:**
    $$S(\mathbf{w}) = (\mathbf{y} - \mathbf{X}\mathbf{w})^T(\mathbf{y} - \mathbf{X}\mathbf{w}) = \left(\mathbf{y}^T - \mathbf{w}^T\mathbf{X}^T\right)(\mathbf{y} - \mathbf{X}\mathbf{w})$$
    $$S(\mathbf{w}) = \mathbf{y}^T\mathbf{y} - \mathbf{y}^T\mathbf{X}\mathbf{w} - \mathbf{w}^T\mathbf{X}^T\mathbf{y} + \mathbf{w}^T\mathbf{X}^T\mathbf{X}\mathbf{w}$$
    
    Since the term $\mathbf{y}^T\mathbf{X}\mathbf{w}$ is a scalar ($1 \times 1$ matrix), it is equal to its own transpose:
    $$\mathbf{y}^T\mathbf{X}\mathbf{w} = \left(\mathbf{y}^T\mathbf{X}\mathbf{w}\right)^T = \mathbf{w}^T\mathbf{X}^T\mathbf{y}$$
    Substitute this identity to simplify the objective:
    $$S(\mathbf{w}) = \mathbf{y}^T\mathbf{y} - 2\mathbf{w}^T\mathbf{X}^T\mathbf{y} + \mathbf{w}^T\mathbf{X}^T\mathbf{X}\mathbf{w}$$

2.  **Take the gradient with respect to the vector $\mathbf{w}$:**
    We apply the standard rules of matrix differentiation:
    *   $\nabla_{\mathbf{w}} (\mathbf{a}^T\mathbf{w}) = \mathbf{a}$
    *   $\nabla_{\mathbf{w}} (\mathbf{w}^T\mathbf{A}\mathbf{w}) = 2\mathbf{A}\mathbf{w}$ (for symmetric matrix $\mathbf{A}$)
    
    Applying these rules:
    $$\nabla_{\mathbf{w}} S(\mathbf{w}) = \mathbf{0} - 2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\mathbf{w}$$

3.  **Set the gradient to $\mathbf{0}$ to find the critical point:**
    $$-2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\mathbf{w} = \mathbf{0} \implies \mathbf{X}^T\mathbf{X}\mathbf{w} = \mathbf{X}^T\mathbf{y}$$
    Assuming $\mathbf{X}^T\mathbf{X}$ is invertible, we multiply both sides by $\left(\mathbf{X}^T\mathbf{X}\right)^{-1}$ from the left:
    $$\hat{\mathbf{w}} = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T\mathbf{y} \quad \blacksquare$$

4.  **Verify the Second-Order Condition (Minimization):**
    We compute the Hessian matrix of second-order derivatives:
    $$\mathbf{H} = \nabla_{\mathbf{w}}^2 S(\mathbf{w}) = 2\mathbf{X}^T\mathbf{X}$$
    Because $\mathbf{X}$ has full column rank, for any non-zero vector $\mathbf{u} \neq \mathbf{0}$, we have:
    $$\mathbf{u}^T\left(2\mathbf{X}^T\mathbf{X}\right)\mathbf{u} = 2\|\mathbf{X}\mathbf{u}\|_2^2 > 0$$
    The Hessian is positive definite ($\mathbf{H} \succ 0$), confirming that the critical point is a global minimum.

---

## 4. Concrete Examples

### Example 1: Football Turnout Projection (Single Feature, No Intercept)
You want to predict game turnout ($y$) based on the number of invites sent ($x$). You have data from two weeks:
*   **Week 1:** Invited 12, 10 showed up.
*   **Week 2:** Invited 14, 11 showed up.
Fit the model $y = w \cdot x$.
1.  **Formulate matrices:**
    $$\mathbf{X} = \begin{bmatrix} 12 \\ 14 \end{bmatrix}, \quad \mathbf{y} = \begin{bmatrix} 10 \\ 11 \end{bmatrix}$$
2.  **Calculate Normal Equations components:**
    $$\mathbf{X}^T\mathbf{X} = [12 \quad 14] \begin{bmatrix} 12 \\ 14 \end{bmatrix} = 144 + 196 = 340$$
    $$\mathbf{X}^T\mathbf{y} = [12 \quad 14] \begin{bmatrix} 10 \\ 11 \end{bmatrix} = 120 + 154 = 274$$
3.  **Compute the coefficient:**
    $$\hat{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y} = \frac{274}{340} \approx 0.8059$$
Our model predicts a yield of $80.59\%$ turnout per invite.

### Example 2: Turnout Prediction with Intercept
We fit a model with a bias term: $y = w_0 + w_1 x$. Our data points are $(x_1=10, y_1=7)$ and $(x_2=15, y_2=12)$.
1.  **Formulate matrices:**
    $$\mathbf{X} = \begin{bmatrix} 1 & 10 \\ 1 & 15 \end{bmatrix}, \quad \mathbf{y} = \begin{bmatrix} 7 \\ 12 \end{bmatrix}$$
2.  **Calculate Normal Equations components:**
    $$\mathbf{X}^T\mathbf{X} = \begin{bmatrix} 1 & 1 \\ 10 & 15 \end{bmatrix} \begin{bmatrix} 1 & 10 \\ 1 & 15 \end{bmatrix} = \begin{bmatrix} 2 & 25 \\ 25 & 325 \end{bmatrix}$$
    $$\mathbf{X}^T\mathbf{y} = \begin{bmatrix} 1 & 1 \\ 10 & 15 \end{bmatrix} \begin{bmatrix} 7 \\ 12 \end{bmatrix} = \begin{bmatrix} 19 \\ 250 \end{bmatrix}$$
3.  **Invert $\mathbf{X}^T\mathbf{X}$:**
    $$\det(\mathbf{X}^T\mathbf{X}) = 2(325) - 25^2 = 650 - 625 = 25$$
    $$\left(\mathbf{X}^T\mathbf{X}\right)^{-1} = \frac{1}{25} \begin{bmatrix} 325 & -25 \\ -25 & 2 \end{bmatrix} = \begin{bmatrix} 13 & -1 \\ -1 & 0.08 \end{bmatrix}$$
4.  **Compute parameter weights:**
    $$\hat{\mathbf{w}} = \begin{bmatrix} 13 & -1 \\ -1 & 0.08 \end{bmatrix} \begin{bmatrix} 19 \\ 250 \end{bmatrix} = \begin{bmatrix} 13(19) - 250 \\ -19 + 0.08(250) \end{bmatrix} = \begin{bmatrix} -3 \\ 1 \end{bmatrix}$$
Our fitted regression model is $y = -3 + 1x$. The slope is $1$, and the intercept is $-3$.

---

## 5. Applied ML Context

1.  **Baseline Linear Regression Modeling:** OLS forms the training engine for standard linear regression models, providing a non-iterative benchmark for complex neural architectures.
2.  **Marketing Media Attribution:** OLS regression is used to determine advertising channel impact by regressing revenue against daily spending metrics across TV, social, and search channels.
3.  **Real Estate Asset Valuation:** Training pricing models on property sizes, bedroom counts, and neighborhood indicators to predict market listing prices.
4.  **Cloud VM Resource Allocation:** Forecasting system memory and CPU usage parameters based on time-of-day indicators to scale virtual server capacities.
5.  **Polynomial Curve Fitting:** Extending design matrices to higher powers ($\mathbf{X} = [\mathbf{1}, \mathbf{x}, \mathbf{x}^2]$) and solving via OLS to fit non-linear curves to data points.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here visualizing OLS error squares:
*   Draw a 2D scatter plot showing a sequence of data points.
*   Draw a diagonal line cutting through the points representing the fitted regression line.
*   For each data point, draw a vertical dashed line connecting it to the regression line, representing the residuals ($e_i = y_i - \hat{y}_i$).
*   Draw a square box adjacent to each dashed residual line, where the area of the box represents the squared residual $e_i^2$.
*   Add a caption explaining that the goal of Ordinary Least Squares is to find the slope and intercept that minimizes the sum of the areas of all these square boxes, visually illustrating why the method is called "Least Squares."
