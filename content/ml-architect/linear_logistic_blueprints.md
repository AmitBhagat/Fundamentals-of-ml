---
title: "Linear & Logistic Blueprints"
description: "Skeptical hyperplanes, linear combinations, sigmoid squishing, binary cross-entropy, and gradient derivations of the classification boundary."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Foundations", "Calculus: Chain Rule", "Probability: Bernoulli Distribution"]
---

<h1 align="center"> Chapter 117: Linear & Logistic Blueprints </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Sigmoid Activation:** The non-linear mapping function $\sigma(z) = \frac{1}{1+e^{-z}}$ that maps the real line $\mathbb{R}$ to the open interval $(0, 1)$.
* **Binary Cross-Entropy Loss:** The information-theoretic metric that penalizes differences between binary targets and predicted probabilities.

</div>

## 1. Conceptual Hook

Linear and logistic regression are the twin bedrocks of supervised learning. While deep neural networks dominate headlines, these linear architectures are the primary workhorses of industry due to their execution speed, stability, and interpretability.

Linear regression is the mathematical ruler: it estimates a continuous value by fitting a flat hyperplane through your feature space.

Logistic regression is the mathematical gatekeeper: it makes binary decisions. It projects your features onto a line, but then wraps the result in a sigmoid "squishing" function, mapping arbitrary scores into probabilities between $0.0$ and $1.0$.

Think of this like classifying home sales. If you are predicting the exact price of a house, you are using a ruler (linear regression). If you are deciding whether a house is a "Luxury Mansion" based on a threshold boundary, you are using a gatekeeper (logistic regression).

Both models share the same skeletal structure: they form decisions by scaling and summing features.

---

## 2. Formal Definition

### 1. Linear Regression (Continuous Estimation)
Given a dataset $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^n$ where $\mathbf{x}_i \in \mathbb{R}^d$ and $y_i \in \mathbb{R}$, the linear regression hypothesis is:
$$h_{\mathbf{w}, b}(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b$$
where $\mathbf{w} \in \mathbb{R}^d$ is the weight vector and $b \in \mathbb{R}$ is the bias.

The objective is to locate the parameters that minimize the Mean Squared Error (MSE) cost function:
$$J(\mathbf{w}, b) = \frac{1}{2n} \sum_{i=1}^{n} \left( h_{\mathbf{w}, b}(\mathbf{x}_i) - y_i \right)^2$$

### 2. Logistic Regression (Probabilistic Classification)
For classification where targets are binary ($y_i \in \{0, 1\}$), the hypothesis wraps the linear predictor in the sigmoid function:
$$h_{\mathbf{w}, b}(\mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
The output $a_i = h_{\mathbf{w}, b}(\mathbf{x}_i)$ represents the conditional probability $P(y_i = 1 \mid \mathbf{x}_i)$.

The objective is to minimize the Binary Cross-Entropy (Log-Loss) cost function:
$$J(\mathbf{w}, b) = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \ln a_i + (1 - y_i) \ln(1 - a_i) \right]$$

---

## 3. Illustrative Derivation

### Derivation of the Logistic Regression Loss Gradient
We prove that the gradient of the Binary Cross-Entropy loss with respect to the weight parameters $\mathbf{w}$ simplifies to a simple error-scaled feature sum, mirroring the linear regression update rule.

*Proof:*
Let $a_i = \sigma(z_i)$ where $z_i = \mathbf{w}^T \mathbf{x}_i + b$.
1.  **Calculate the derivative of the Sigmoid function:**
    $$\sigma'(z) = \frac{d}{dz} (1+e^{-z})^{-1} = -(1+e^{-z})^{-2}(-e^{-z}) = \frac{e^{-z}}{(1+e^{-z})^2} = \left(\frac{1}{1+e^{-z}}\right)\left(\frac{e^{-z}}{1+e^{-z}}\right) = \sigma(z)(1-\sigma(z))$$
    Therefore:
    $$\frac{\partial a_i}{\partial z_i} = a_i(1 - a_i)$$

2.  **Define the individual loss term $\mathcal{L}_i$:**
    $$\mathcal{L}_i = - \left[ y_i \ln a_i + (1 - y_i) \ln(1 - a_i) \right]$$
    By the chain rule, the derivative with respect to weight parameter $w_j$ is:
    $$\frac{\partial \mathcal{L}_i}{\partial w_j} = \frac{\partial \mathcal{L}_i}{\partial a_i} \frac{\partial a_i}{\partial z_i} \frac{\partial z_i}{\partial w_j}$$

3.  **Evaluate each partial derivative term:**
    *   **Term 1:** $\frac{\partial \mathcal{L}_i}{\partial a_i} = - \left[ \frac{y_i}{a_i} - \frac{1 - y_i}{1 - a_i} \right] = -\frac{y_i(1 - a_i) - a_i(1 - y_i)}{a_i(1 - a_i)} = \frac{a_i - y_i}{a_i(1 - a_i)}$
    *   **Term 2:** $\frac{\partial a_i}{\partial z_i} = a_i(1 - a_i)$
    *   **Term 3:** $\frac{\partial z_i}{\partial w_j} = x_{ij}$ (where $x_{ij}$ is the $j$-th feature of sample $i$).

4.  **Combine the terms:**
    $$\frac{\partial \mathcal{L}_i}{\partial w_j} = \left( \frac{a_i - y_i}{a_i(1 - a_i)} \right) \cdot \left( a_i(1 - a_i) \right) \cdot x_{ij} = (a_i - y_i) x_{ij}$$
    Expressed in vector notation:
    $$\nabla_{\mathbf{w}} \mathcal{L}_i = (a_i - y_i) \mathbf{x}_i$$

5.  **Average over the entire dataset:**
    $$\nabla_{\mathbf{w}} J(\mathbf{w}, b) = \frac{1}{n} \sum_{i=1}^{n} (a_i - y_i) \mathbf{x}_i \quad \blacksquare$$

This shows that the gradient update direction is simply the prediction error $(a_i - y_i)$ scaled by the feature vector $\mathbf{x}_i$.

---

## 4. Concrete Examples

### Example 1: Linear House Appraiser
We predict a house price using features $x_1$ (square footage) and $x_2$ (age).
*   **Weights:** $w_1 = 200$, $w_2 = -500$, bias $b = 50000$.
*   **Input:** $\mathbf{x} = [2000 \text{ sqft}, 10 \text{ years}]^T$.
$$\hat{y} = 200(2000) - 500(10) + 50000 = 400000 - 5000 + 50000 = 445000 \text{ dollars}$$

### Example 2: Logistic Fraud Gatekeeper
We evaluate a credit transaction where the linear score is calculated as $z = \mathbf{w}^T\mathbf{x} + b = -2$.
1.  **Compute the probability of fraud ($y=1$):**
    $$\hat{y} = \sigma(-2) = \frac{1}{1 + e^2} \approx \frac{1}{1 + 7.389} \approx 0.119 \quad (11.9\% \text{ probability})$$
2.  **Calculate the Cross-Entropy loss if the true label is $y=0$ (safe transaction):**
    $$\mathcal{L} = - \left[ 0 \cdot \ln(0.119) + (1 - 0) \cdot \ln(1 - 0.119) \right] = -\ln(0.881) \approx 0.127$$
3.  **Calculate the Cross-Entropy loss if the true label is $y=1$ (fraud transaction):**
    $$\mathcal{L} = - \left[ 1 \cdot \ln(0.119) + 0 \cdot \ln(0.881) \right] = -\ln(0.119) \approx 2.128$$
Note how the loss is significantly higher ($\approx 17\times$) when the model is confident but wrong.

---

## 5. Applied ML Context

1.  **Consumer Credit Approval:** Using Logistic Regression to compute the probability of loan default based on credit history and debt-to-income features.
2.  **Quantitative Stock Pricing:** Using Linear Regression models as simple baseline predictors to forecast equity values based on trailing metrics.
3.  **Ad CTR (Click-Through Rate):** Ad placement networks use logistic estimators to predict the probability that a user clicks a given display banner.
4.  **Medical Diagnosis Probability:** Estimating the likelihood of cardiac disease based on clinical indicators (blood pressure, age, cholesterol levels).
5.  **Spam Filter Baselines:** Initial screening filters use logistic regression classifiers to evaluate incoming email features.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here comparing Linear and Logistic predictions:
*   Draw two 2D plots side-by-side:
    1.  **Linear Regression Plot:** Show data points scattered around a straight diagonal regression line representing $y = \mathbf{w}^T\mathbf{x} + b$. Annotate that the output extends to $\pm \infty$.
    2.  **Logistic Regression Plot:** Show points clustered at $y=0$ and $y=1$. Draw an S-shaped sigmoid curve $\sigma(\mathbf{w}^T\mathbf{x} + b)$ running between them.
*   On the Logistic plot, highlight the **Decision Boundary** at the point where the sigmoid curve crosses $0.5$ ($z = 0$).
*   Add a caption explaining that linear regression outputs continuous values along a straight line, whereas logistic regression squishes the output into a probability curve between $0.0$ and $1.0$.
