---
title: "Regression Diagnostics"
description: "Model diagnostics, Gauss-Markov assumptions, residual analysis, homoscedasticity proofs, leverage hat matrices, and Cook's distance."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Linear Algebra: Matrices", "Linear Algebra: Matrix Multiplication", "Linear Algebra: Matrix Inverse", "Probability Distributions", "Ordinary Least Squares"]
---

<h1 align="center"> Chapter 70: Regression Diagnostics </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Gauss-Markov Theorem:** The mathematical guarantee that OLS is the Best Linear Unbiased Estimator (BLUE) under classic conditions.
* **Residuals ($e_i$):** The difference between the actual observed value and the model's prediction: $e_i = y_i - \hat{y}_i$.

</div>

## 1. Conceptual Hook

Building a linear regression model using Ordinary Least Squares is only half the battle. Once we obtain our coefficient weights, how can we be sure that our model is mathematically reliable? The Gauss-Markov theorem guarantees that OLS is the optimal estimator, but only if several strict mathematical assumptions about the model's errors (residuals) are satisfied.

**Regression diagnostics** is the clinical toolkit we use to inspect our model's health. We are checking if the relationship is truly linear, if the error variance is constant across all predictions (homoscedasticity), if the errors are independent, and if our inputs are redundant (multicollinearity). If our model fails these diagnostics, our coefficient weights become unstable and our confidence intervals collapse, turning our machine learning models into unreliable engineering liabilities.

---

## 2. Formal Definition

Consider the linear regression model:
$$\mathbf{y} = \mathbf{X}\mathbf{w} + \boldsymbol{\epsilon}$$
where $\mathbf{y} \in \mathbb{R}^n$ is the target vector, $\mathbf{X} \in \mathbb{R}^{n \times d}$ is the design matrix, and $\boldsymbol{\epsilon} \in \mathbb{R}^n$ represents the error vector.

### Classical Gauss-Markov Assumptions
For OLS to be BLUE, the residuals must satisfy:
1.  **Linearity in Parameters:** The expectation of the error vector conditioned on $\mathbf{X}$ is zero:
    $$\mathbb{E}[\boldsymbol{\epsilon} \mid \mathbf{X}] = \mathbf{0}$$
2.  **Homoscedasticity (Constant Variance):** The variance of the errors is constant:
    $$\text{Var}(\epsilon_i \mid \mathbf{X}) = \sigma^2 \quad \forall i$$
3.  **No Autocorrelation:** The covariance between distinct error terms is zero:
    $$\text{Cov}(\epsilon_i, \epsilon_j \mid \mathbf{X}) = 0 \quad \forall i \neq j$$
    Combining homoscedasticity and autocorrelation conditions in matrix form:
    $$\text{Var}(\boldsymbol{\epsilon} \mid \mathbf{X}) = \sigma^2 \mathbf{I}_n$$
4.  **No Multicollinearity:** The columns of $\mathbf{X}$ are linearly independent:
    $$\text{rank}(\mathbf{X}) = d \implies \det\left(\mathbf{X}^T\mathbf{X}\right) \neq 0$$

### Diagnostic Metrics
*   **Leverage ($h_{ii}$):** The diagonal elements of the projection (Hat) matrix $\mathbf{H}$:
    $$\mathbf{H} = \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T$$
    Leverage measures how far an observation's features are from the mean feature values.
*   **Cook's Distance ($D_i$):** Measures the influence of observation $i$ on the model's overall predictions:
    $$D_i = \frac{r_i^2}{d} \left( \frac{h_{ii}}{1 - h_{ii}} \right)$$
    where $r_i$ is the studentized residual and $d$ is the parameter dimension. Observations with $D_i > 1$ are flagged as high-influence outliers.
*   **Variance Inflation Factor (VIF):** Quantifies multicollinearity for feature $j$:
    $$VIF_j = \frac{1}{1 - R_j^2}$$
    where $R_j^2$ is the coefficient of determination when regressing feature $x_j$ against all other features. A $VIF_j > 10$ indicates severe multicollinearity.

---

## 3. Illustrative Derivation

### Derivation of the Hat Matrix and its Idempotency
We derive the projection matrix $\mathbf{H}$ (known as the Hat Matrix because it puts the "hat" on $\mathbf{y}$ to yield $\hat{\mathbf{y}}$) and prove that it is idempotent ($\mathbf{H}^2 = \mathbf{H}$).

*Proof:*
1.  **Derive the projection matrix:**
    The vector of predicted values $\hat{\mathbf{y}}$ is:
    $$\hat{\mathbf{y}} = \mathbf{X}\hat{\mathbf{w}}$$
    Substitute the closed-form OLS estimator $\hat{\mathbf{w}} = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T\mathbf{y}$:
    $$\hat{\mathbf{y}} = \mathbf{X}\left( \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T\mathbf{y} \right)$$
    Grouping the matrix multiplication:
    $$\hat{\mathbf{y}} = \left[ \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T \right] \mathbf{y}$$
    We define the Hat Matrix $\mathbf{H}$ as the operator inside the brackets:
    $$\mathbf{H} = \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T$$
    This matrix maps the observed targets to the predicted values:
    $$\hat{\mathbf{y}} = \mathbf{H}\mathbf{y}$$

2.  **Prove Idempotency ($\mathbf{H}^2 = \mathbf{H}$):**
    An idempotent matrix represents a projection operator. Projecting a vector onto a subspace a second time does not change the result. We verify this algebraically:
    $$\mathbf{H}^2 = \mathbf{H} \cdot \mathbf{H} = \left[ \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T \right] \cdot \left[ \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T \right]$$
    Regroup the matrix products:
    $$\mathbf{H}^2 = \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1} \left[ \mathbf{X}^T \mathbf{X} \right] \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T$$
    Since $\left(\mathbf{X}^T\mathbf{X}\right)^{-1} \left[ \mathbf{X}^T \mathbf{X} \right]$ is the identity matrix $\mathbf{I}$:
    $$\mathbf{H}^2 = \mathbf{X} \left[ \mathbf{I} \right] \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T = \mathbf{X}\left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T$$
    $$\mathbf{H}^2 = \mathbf{H} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Cook's Distance Outlier Detection
A model has $p=2$ parameters. For an observation $i$, the standardized residual is $e_i = 3.0$ and the leverage is $h_{ii} = 0.8$. Calculate Cook's Distance to determine if this observation is a high-influence outlier.
1.  **Apply Cook's Distance formula:**
    $$D_i = \frac{e_i^2}{p} \left( \frac{h_{ii}}{1 - h_{ii}} \right) = \frac{3^2}{2} \left( \frac{0.8}{1 - 0.8} \right)$$
    $$D_i = 4.5 \left( \frac{0.8}{0.2} \right) = 4.5 \cdot 4.0 = 18.0$$
2.  **Evaluate:**
    Since $D_i = 18.0 \gg 1.0$, this data point has a massive influence on the model. It represents a significant outlier that tilts the entire regression line and should be inspected.

### Example 2: Multicollinearity Audit (VIF)
You fit a model with features $x_1$ (Shoe Length) and $x_2$ (Sole Length). Regressing $x_1$ against $x_2$ yields a coefficient of determination $R_1^2 = 0.95$. Calculate the Variance Inflation Factor.
1.  **Apply the VIF formula:**
    $$VIF_1 = \frac{1}{1 - R_1^2} = \frac{1}{1 - 0.95} = \frac{1}{0.05} = 20.0$$
2.  **Evaluate:**
    Since $VIF_1 = 20.0 > 10.0$, there is severe multicollinearity. The features are redundant. One of them should be removed to ensure stable coefficient estimations.

---

## 5. Applied ML Context

1.  **Feature Selection in Genomics:** VIF is used to identify and prune highly correlated gene expression features before fitting high-dimensional regression models.
2.  **Financial Time-Series Analysis:** The Durbin-Watson statistic is computed over regression residuals to detect autocorrelation, ensuring that temporal correlation does not bias model parameters.
3.  **Real Estate Asset Valuation:** Breusch-Pagan tests are applied to residuals to identify heteroscedasticity, which occurs because price variance increases as the absolute house value increases.
4.  **Autonomous Perception Calibration:** In self-driving systems, Cook's distance is used to flag faulty sensor calibration records (outliers) that would skew the alignment model.
5.  **Clinical Dosage Modeling:** Quantile-Quantile (Q-Q) plots are used to verify that the prediction residuals follow a normal distribution, validating the safety boundaries of predicted drug dosages.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the four classic diagnostic plots:
*   Show a $2 \times 2$ grid of plots:
    1.  **Residuals vs. Fitted Plot:** Draw a horizontal line at 0. Show a random, uniform cloud of points representing homoscedasticity. Contrast it with a "funnel shape" representing heteroscedasticity.
    2.  **Normal Q-Q Plot:** Draw a diagonal line. Show points lining up straight along this line, illustrating normally distributed errors.
    3.  **Scale-Location Plot:** Draw a horizontal trend line of square-rooted standardized residuals, indicating stable variance.
    4.  **Residuals vs. Leverage Plot:** Draw a plot with dashed contour boundaries representing Cook's distance levels. Show a single point positioned far to the right labeled "High Influence Outlier" that crosses the $1.0$ contour boundary.
*   Add a caption explaining that these four plots provide a complete health check for linear models, confirming that error variance is constant, errors are normal, and no single outlier is distorting the model's coefficients.
