---
title: "Cumulative Distribution Functions (CDF)"
description: "Cumulative probabilities, probability integral transform, CDF properties, exponential distributions, and the KS test."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Integral Calculus", "Probability Distributions", "Random Variables", "Probability Density Functions (PDF)"]
---

<h1 align="center"> Chapter 45: Cumulative Distribution Functions (CDF) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Probability Density Functions (PDF):** Understanding how probability is distributed across continuous variables.
* **Continuous Integration:** Comfort with calculating antiderivatives and definite limits.

</div>

## 1. Conceptual Hook

In machine learning evaluation, we often need to make threshold-based decisions. For example, if a classification model outputs a probability score, at what threshold should we flag a transaction as fraud? To make this decision, we need to know: what is the total probability that our model's output falls below a certain score? We find this using the **Cumulative Distribution Function (CDF)**.

The CDF is the mathematical "progress bar" of probability. While the PDF shows us the local density of probability at any specific coordinate, the CDF tracks the accumulated likelihood from the absolute lowest possible outcome up to our chosen threshold. Because the CDF is cumulative, it starts at $0$ and climbs steadily toward $1.0$. It is the ultimate tool for outlier detection, quantile regression, and statistical hypothesis testing, allowing us to evaluate the cumulative risk of our model's parameters.

---

## 2. Formal Definition

Let $X$ be a real-valued random variable. The **Cumulative Distribution Function (CDF)** of $X$, denoted $F_X: \mathbb{R} \to [0, 1]$, is defined as:
$$F_X(x) = P(X \le x) \quad \forall x \in \mathbb{R}$$

### Fundamental Properties of a CDF
Every valid CDF must satisfy the following four mathematical properties:
1.  **Boundedness:** The function is bounded between 0 and 1:
    $$0 \le F_X(x) \le 1$$
2.  **Monotonicity:** The function is non-decreasing. If $x_1 \le x_2$, then:
    $$F_X(x_1) \le F_X(x_2)$$
3.  **Limits at Infinity:** As the threshold approaches infinity, the probability accumulates to 1. As it approaches negative infinity, the probability is 0:
    $$\lim_{x \to -\infty} F_X(x) = 0 \quad \text{and} \quad \lim_{x \to \infty} F_X(x) = 1$$
4.  **Right-Continuity:** The function is continuous from the right:
    $$\lim_{x \to x_0^+} F_X(x) = F_X(x_0)$$

### Calculating Probabilities over Intervals
For any two values $a < b$, the probability that the random variable $X$ falls within the interval $(a, b]$ is:
$$P(a < X \le b) = F_X(b) - F_X(a)$$

---

## 3. Illustrative Derivation

### Derivation of the Exponential Distribution CDF
We derive the Cumulative Distribution Function (CDF) of the **exponential distribution** directly from its PDF, and verify that it satisfies the properties of a valid CDF.

Let $X \sim \text{Exponential}(\lambda)$ where $\lambda > 0$ is the rate parameter. The PDF of $X$ is defined as:
$$f_X(t) = \begin{cases} \lambda e^{-\lambda t} & \text{if } t \ge 0 \\ 0 & \text{if } t < 0 \end{cases}$$

*Proof:*
By definition, the CDF is the integral of the PDF from $-\infty$ to the threshold $x$:
$$F_X(x) = \int_{-\infty}^{x} f_X(t) dt$$

1.  **Case 1: $x < 0$:**
    Since the PDF $f_X(t) = 0$ for all $t < 0$, the accumulated probability is zero:
    $$F_X(x) = \int_{-\infty}^{x} 0 \, dt = 0$$

2.  **Case 2: $x \ge 0$:**
    We split the integral at the boundary $0$:
    $$F_X(x) = \int_{-\infty}^{0} f_X(t) dt + \int_{0}^{x} f_X(t) dt$$
    $$F_X(x) = 0 + \int_{0}^{x} \lambda e^{-\lambda t} dt$$
    We evaluate the definite integral using the antiderivative of $e^{-\lambda t}$, which is $-\frac{1}{\lambda} e^{-\lambda t}$:
    $$F_X(x) = \lambda \left[ -\frac{1}{\lambda} e^{-\lambda t} \right]_0^x = \left[ -e^{-\lambda t} \right]_0^x$$
    Evaluate at the upper and lower limits:
    $$F_X(x) = -e^{-\lambda x} - (-e^{-\lambda \cdot 0}) = -e^{-\lambda x} + e^0 = 1 - e^{-\lambda x}$$

3.  **Synthesize the CDF:**
    $$F_X(x) = \begin{cases} 1 - e^{-\lambda x} & \text{if } x \ge 0 \\ 0 & \text{if } x < 0 \end{cases}$$

4.  **Verify properties:**
    *   $\lim_{x \to -\infty} F_X(x) = 0$ (verified by Case 1).
    *   $\lim_{x \to \infty} F_X(x) = \lim_{x \to \infty} (1 - e^{-\lambda x}) = 1 - 0 = 1$ (since $\lambda > 0$).
    *   Taking the derivative for $x > 0$ yields: $\frac{d}{dx}(1 - e^{-\lambda x}) = \lambda e^{-\lambda x} = f_X(x)$, confirming the Fundamental Theorem of Calculus. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Discrete Die Roll CDF
Let $X$ represent the outcome of a single roll of a biased six-sided die, with PMF $P(X=x) = \frac{x}{21}$ for $x \in \{1, 2, 3, 4, 5, 6\}$. Find the probability of rolling a value less than or equal to $3$.
1.  **Formulate the sum:**
    $$F_X(3) = P(X \le 3) = \sum_{x_i \le 3} P(X = x_i)$$
2.  **Evaluate:**
    $$F_X(3) = P(X=1) + P(X=2) + P(X=3)$$
    $$F_X(3) = \frac{1}{21} + \frac{2}{21} + \frac{3}{21} = \frac{6}{21} \approx 0.2857$$
There is approximately a $28.57\%$ chance of rolling a $3$ or lower.

### Example 2: Continuous Uniform CDF
Let $X \sim U(2, 10)$ represent the distance your hand travels during a Ludo game, with PDF $f_X(x) = \frac{1}{8}$ for $2 \le x \le 10$. Find the probability that the distance is less than or equal to $5$ inches.
1.  **Formulate the integral:**
    $$F_X(5) = P(X \le 5) = \int_{2}^{5} \frac{1}{8} dt$$
2.  **Evaluate:**
    $$F_X(5) = \left[ \frac{t}{8} \right]_2^5 = \frac{5}{8} - \frac{2}{8} = \frac{3}{8} = 0.375$$
There is a $37.5\%$ probability of the distance being within 5 inches.

---

## 5. Applied ML Context

1.  **Kolmogorov-Smirnov (KS) Test:** The KS test measures the maximum absolute vertical distance between two CDF curves (e.g. comparing model predictions $F_{model}(x)$ to the actual test distribution $F_{true}(x)$) to verify if they originate from the same distribution.
2.  **Quantile Regression:** In forecasting, instead of predicting the mean, models predict specific quantiles (like the 90th percentile). This requires inverting the CDF (the Percent-Point Function): $Q(q) = F_X^{-1}(q)$.
3.  **Classification Threshold Selection:** We analyze the empirical CDF of predicted scores to choose decision thresholds that optimize precision and recall metrics.
4.  **Image Histogram Equalization:** In computer vision pre-processing, the empirical CDF of pixel intensities is used as a mapping function to flatten the image histogram, maximizing local contrast.
5.  **Copulas for Dependency Modeling:** Copulas use the Probability Integral Transform, which maps any continuous random variable to a uniform distribution via its own CDF: $U = F_X(X)$. This allows us to model multivariate feature dependencies independently of their marginal distributions.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the relationship between PDF and CDF:
*   Show two vertically stacked plots:
    1.  **Top Plot (PDF):** Draw a bell curve. Mark a coordinate $x_0$ on the horizontal axis. Shade the entire area under the curve from $-\infty$ to $x_0$.
    2.  **Bottom Plot (CDF):** Draw an S-curve that starts at $0$ on the left and rises continuously to asymptote at $1.0$ on the right. Mark the same coordinate $x_0$ on the horizontal axis.
*   Draw a vertical dashed arrow starting from the shaded area of the PDF plot and pointing directly to the height of the S-curve at $x_0$. Label the vertical coordinate on the CDF as $F_X(x_0) = P(X \le x_0)$.
*   Use this diagram to visually show that the vertical height of the CDF at any point $x$ is equal to the accumulated area under the PDF curve up to that point.
