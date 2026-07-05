---
title: "Variance"
description: "Sample variance, Bessel's correction, algebraic variance properties, derivations, and the bias-variance tradeoff."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Integral Calculus", "Probability Distributions", "Random Variables", "Mean and Expectation"]
---

<h1 align="center"> Chapter 57: Variance </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Expected Value:** Comfort with calculating the center of gravity $\mathbb{E}[X]$ of a distribution.
* **Linearity of Expectation:** Understanding that $\mathbb{E}[aX + b] = a\mathbb{E}[X] + b$.

</div>

## 1. Conceptual Hook

In machine learning, averages only tell half the story. Knowing that the average height of a class is 150 cm doesn't tell you if the room is filled with children of identical height, or a mix of toddlers and professional athletes. To understand the structure of our data, we must measure its spread. The mathematical tool that quantifies this spread is **variance**.

Variance measures how much our data points deviate from their mean. By squaring the differences between each data point and the average, variance guarantees that early and late deviations do not cancel each other out, while also penalizing larger deviations disproportionately. Controlling and balancing variance is the core objective behind regularization, dimensionality reduction (like PCA), and stabilizing training via weight initialization.

---

## 2. Formal Definition

For a random variable $X$ with expectation $\mathbb{E}[X] = \mu$, the **variance** of $X$, denoted $\text{Var}(X)$ or $\sigma^2$, is the expected value of the squared deviation from the mean:
$$\text{Var}(X) = \mathbb{E}\left[ (X - \mu)^2 \right] = \mathbb{E}\left[ (X - \mathbb{E}[X])^2 \right]$$

*   **Continuous Form:**
    $$\text{Var}(X) = \int_{-\infty}^{\infty} (x - \mu)^2 f(x) dx$$
*   **Discrete Form:**
    $$\text{Var}(X) = \sum_{x \in \mathcal{X}} (x - \mu)^2 p(x)$$

### Properties of Variance
For any random variables $X, Y$ and constants $a, b, c \in \mathbb{R}$:
1.  **Non-negativity:** $\text{Var}(X) \ge 0$.
2.  **Translation Invariance:** Adding a constant does not change the spread:
    $$\text{Var}(X + c) = \text{Var}(X)$$
3.  **Quadratic Scaling:** Scaling a variable scales the variance quadratically:
    $$\text{Var}(aX) = a^2 \text{Var}(X) \implies \text{Var}(aX + b) = a^2 \text{Var}(X)$$
4.  **Sum of Variables:**
    $$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$$
    If $X$ and $Y$ are independent, $\text{Cov}(X, Y) = 0 \implies \text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$.

### Sample Variance
For a dataset of $N$ observations $\{x_1, \dots, x_N\}$ with sample mean $\bar{x}$:
*   **Biased Sample Variance:**
    $$s_N^2 = \frac{1}{N} \sum_{i=1}^{N} (x_i - \bar{x})^2$$
*   **Unbiased Sample Variance (Bessel's Correction):**
    $$s^2 = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \bar{x})^2$$
    Bessel's correction replaces $N$ with $N-1$ to compensate for the fact that using the sample mean $\bar{x}$ instead of the true population mean $\mu$ systematically underestimates the variance.

---

## 3. Illustrative Derivation

### Derivation of the Computational Formula and Scaling Property
We prove two essential algebraic properties of variance using the linearity of expectation.

**Derivation 1: The Computational Formula.** $\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$.
*Proof:*
Let $\mathbb{E}[X] = \mu$. Since $\mu$ is a constant, its expectation is $\mathbb{E}[\mu] = \mu$.
$$\text{Var}(X) = \mathbb{E}\left[ (X - \mu)^2 \right]$$
Expand the quadratic expression inside the expectation:
$$(X - \mu)^2 = X^2 - 2\mu X + \mu^2$$
Apply the expectation operator to both sides. By the linearity of expectation:
$$\mathbb{E}\left[ (X - \mu)^2 \right] = \mathbb{E}[X^2 - 2\mu X + \mu^2] = \mathbb{E}[X^2] - \mathbb{E}[2\mu X] + \mathbb{E}[\mu^2]$$
Since $2\mu$ and $\mu^2$ are constants, pull them out of the expectation:
$$\text{Var}(X) = \mathbb{E}[X^2] - 2\mu \mathbb{E}[X] + \mu^2$$
Substitute $\mathbb{E}[X] = \mu$ back into the equation:
$$\text{Var}(X) = \mathbb{E}[X^2] - 2\mu(\mu) + \mu^2 = \mathbb{E}[X^2] - 2\mu^2 + \mu^2$$
$$\text{Var}(X) = \mathbb{E}[X^2] - \mu^2 = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 \quad \blacksquare$$

**Derivation 2: The Scaling Property.** $\text{Var}(aX + b) = a^2 \text{Var}(X)$.
*Proof:*
Let $Y = aX + b$. By the linearity of expectation, $\mathbb{E}[Y] = a\mathbb{E}[X] + b$.
$$\text{Var}(Y) = \mathbb{E}\left[ (Y - \mathbb{E}[Y])^2 \right] = \mathbb{E}\left[ ((aX + b) - (a\mathbb{E}[X] + b))^2 \right]$$
Simplify the terms inside the square:
$$(aX + b) - (a\mathbb{E}[X] + b) = aX - a\mathbb{E}[X] = a(X - \mathbb{E}[X])$$
Square this term:
$$(a(X - \mathbb{E}[X]))^2 = a^2 (X - \mathbb{E}[X])^2$$
Substitute back into the expectation:
$$\text{Var}(aX + b) = \mathbb{E}\left[ a^2 (X - \mathbb{E}[X])^2 \right]$$
Pull the constant factor $a^2$ out of the expectation:
$$\text{Var}(aX + b) = a^2 \mathbb{E}\left[ (X - \mathbb{E}[X])^2 \right] = a^2 \text{Var}(X) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Courier Packaging Times (Discrete)
You measure packaging times for four returns: $\{3, 5, 7, 9\}$ minutes. Find the sample variance.
1.  **Find the sample mean $\bar{x}$:**
    $$\bar{x} = \frac{3 + 5 + 7 + 9}{4} = \frac{24}{4} = 6 \text{ minutes}$$
2.  **Calculate the biased sample variance $s_N^2$:**
    $$s_N^2 = \frac{(3-6)^2 + (5-6)^2 + (7-6)^2 + (9-6)^2}{4}$$
    $$s_N^2 = \frac{(-3)^2 + (-1)^2 + (1)^2 + (3)^2}{4} = \frac{9 + 1 + 1 + 9}{4} = \frac{20}{4} = 5 \text{ min}^2$$
3.  **Calculate the unbiased sample variance $s^2$ using Bessel's Correction:**
    $$s^2 = \frac{20}{4-1} = \frac{20}{3} \approx 6.67 \text{ min}^2$$

### Example 2: Continuous Exponential Variance
Let $X \sim \text{Exponential}(\lambda)$ represent bolt loosening times with PDF $f(x) = \lambda e^{-\lambda x}$ for $x \ge 0$, and mean $\mathbb{E}[X] = 1/\lambda$. Find the variance.
1.  **Calculate $\mathbb{E}[X^2]$ using LOTUS:**
    $$\mathbb{E}[X^2] = \int_{0}^{\infty} x^2 \cdot \lambda e^{-\lambda x} dx$$
    Integrate by parts: let $u = x^2 \implies du = 2x dx$, and $dv = \lambda e^{-\lambda x} dx \implies v = -e^{-\lambda x}$.
    $$\mathbb{E}[X^2] = \left[ -x^2 e^{-\lambda x} \right]_0^{\infty} - \int_{0}^{\infty} 2x \left(-e^{-\lambda x}\right) dx = 0 + 2 \int_{0}^{\infty} x e^{-\lambda x} dx$$
    $$\mathbb{E}[X^2] = \frac{2}{\lambda} \int_{0}^{\infty} x \cdot \lambda e^{-\lambda x} dx = \frac{2}{\lambda} \mathbb{E}[X] = \frac{2}{\lambda} \left(\frac{1}{\lambda}\right) = \frac{2}{\lambda^2}$$
2.  **Compute variance using the computational formula:**
    $$\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{2}{\lambda^2} - \left(\frac{1}{\lambda}\right)^2 = \frac{2}{\lambda^2} - \frac{1}{\lambda^2} = \frac{1}{\lambda^2}$$
For rate $\lambda = 0.5$, variance is $\frac{1}{0.5^2} = 4 \text{ min}^2$.

---

## 5. Applied ML Context

1.  **Bias-Variance Tradeoff:** In model evaluation, prediction error is decomposed into $\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$. High variance indicates overfitting—the model is highly sensitive to noise in the training set.
2.  **Principal Component Analysis (PCA):** PCA finds orthogonal axes that maximize the variance of the projected data points. Preserving variance ensures we retain the maximum possible information in lower dimensions.
3.  **Zero-Variance Feature Selection:** In preprocessing, features with zero or near-zero variance are dropped. If a feature is constant across all samples, it has no predictive power.
4.  **Xavier/He Weight Initialization:** Weight initialization schemes set weight variances to prevent signal attenuation or explosion. Xavier sets $\text{Var}(W) = \frac{2}{n_{in} + n_{out}}$, ensuring stable activation variance across layers.
5.  **Batch Normalization:** Batch Norm normalizes layer inputs by subtracting the batch mean and dividing by the standard deviation (square root of variance): $\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating low vs. high variance distributions:
*   Show two bell curves on the same axis:
    1.  **Low Variance Curve:** Tall and narrow, centered at $\mu$, indicating that data points are tightly packed near the mean.
    2.  **High Variance Curve:** Short and broad, centered at the same $\mu$, indicating that data points are widely dispersed.
*   Draw horizontal double-headed arrows under both curves representing the width of their spread.
*   To illustrate the squaring effect, draw a separate bar chart of deviations from the mean:
    *   Show a deviation of $1$ unit as a small square box of area $1 \times 1 = 1$.
    *   Show a deviation of $3$ units (an outlier) as a large square box of area $3 \times 3 = 9$.
*   Use this to visually demonstrate how squaring outliers disproportionately penalizes wide deviations, making variance highly sensitive to extreme noise.
