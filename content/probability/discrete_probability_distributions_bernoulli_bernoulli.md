---
title: "Discrete Probability Distributions"
description: "Bernoulli, Binomial, and Poisson distributions, PMFs, summary statistics, and the Poisson limit proof."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Probability Distributions", "Random Variables"]
---

<h1 align="center"> Chapter 46: Discrete Probability Distributions </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Probability Mass Function (PMF):** Understanding discrete probability maps.
* **Combinatorics:** Familiarity with combinations and factorials.

</div>

## 1. Conceptual Hook

In machine learning, many of our tasks involve binary decisions and countable outcomes. A classifier predicts whether an image is a dog or not; we evaluate how many correct predictions our model makes over a batch of 100 test samples; or we track how many API requests hit our server per second to detect anomalies. To model these countable, discrete scenarios, we use **discrete probability distributions**.

The three pillars of discrete modeling are the **Bernoulli**, **Binomial**, and **Poisson** distributions. They exist on a scale of increasing complexity:
*   The **Bernoulli** distribution acts as the "single check," modeling a single binary outcome (success/failure).
*   The **Binomial** distribution acts as the "batch check," summing multiple independent Bernoulli trials to count total successes.
*   The **Poisson** distribution acts as the "flow check," counting the frequency of independent, rare events occurring over a continuous interval.
Grasping these three distributions allows us to construct loss functions (like cross-entropy), regularize networks (like dropout), and evaluate classification performance.

---

## 2. Formal Definition

### 1. Bernoulli Distribution
A discrete random variable $X$ follows a Bernoulli distribution, denoted $X \sim \text{Bernoulli}(p)$, if it has a binary outcome where success occurs with probability $p$ and failure with probability $1-p$.
*   **Support:** $x \in \{0, 1\}$
*   **PMF:**
    $$P(X = x) = p^x (1-p)^{1-x}$$
*   **Expectation & Variance:**
    $$\mathbb{E}[X] = p, \quad \text{Var}(X) = p(1-p)$$

### 2. Binomial Distribution
A discrete random variable $X$ follows a Binomial distribution, denoted $X \sim \text{Binomial}(n, p)$, if it represents the total number of successes in $n$ independent and identically distributed Bernoulli trials.
*   **Support:** $k \in \{0, 1, \dots, n\}$
*   **PMF:**
    $$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k} = \frac{n!}{k!(n-k)!} p^k (1-p)^{n-k}$$
*   **Expectation & Variance:**
    $$\mathbb{E}[X] = np, \quad \text{Var}(X) = np(1-p)$$

### 3. Poisson Distribution
A discrete random variable $X$ follows a Poisson distribution, denoted $X \sim \text{Poisson}(\lambda)$, if it models the number of events occurring in a fixed interval of time or space, where events occur independently at a constant average rate $\lambda$.
*   **Support:** $k \in \{0, 1, 2, \dots\}$
*   **PMF:**
    $$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
*   **Expectation & Variance:**
    $$\mathbb{E}[X] = \lambda, \quad \text{Var}(X) = \lambda$$

---

## 3. Illustrative Derivation

### Derivation of the Poisson Distribution as the Limit of the Binomial
We prove that as the number of trials $n$ in a Binomial distribution approaches infinity and the probability of success $p$ approaches zero, such that the expected value $\lambda = np$ remains constant, the Binomial PMF converges to the Poisson PMF.

*Proof:*
Let $X_n \sim \text{Binomial}(n, p)$. We substitute $p = \frac{\lambda}{n}$ into the Binomial PMF:
$$P(X_n = k) = \binom{n}{k} \left( \frac{\lambda}{n} \right)^k \left( 1 - \frac{\lambda}{n} \right)^{n-k}$$
Expand the binomial coefficient and rearrange the terms:
$$P(X_n = k) = \frac{n(n-1)(n-2)\dots(n-k+1)}{k!} \cdot \frac{\lambda^k}{n^k} \cdot \left(1 - \frac{\lambda}{n}\right)^n \cdot \left(1 - \frac{\lambda}{n}\right)^{-k}$$
Group the terms by powers of $n$:
$$P(X_n = k) = \frac{\lambda^k}{k!} \left[ \frac{n}{n} \cdot \frac{n-1}{n} \cdot \frac{n-2}{n} \dots \frac{n-k+1}{n} \right] \left(1 - \frac{\lambda}{n}\right)^n \left(1 - \frac{\lambda}{n}\right)^{-k}$$

Now, we evaluate the limit of each component as $n \to \infty$ while holding $k$ constant:
1.  **Evaluate the bracketed fraction term:**
    The bracketed expression consists of a product of $k$ fractions. For any fixed index $i$:
    $$\lim_{n \to \infty} \frac{n - i}{n} = \lim_{n \to \infty} \left(1 - \frac{i}{n}\right) = 1$$
    Therefore, the entire bracketed product converges to 1:
    $$\lim_{n \to \infty} \left[ \left(1\right) \left(1 - \frac{1}{n}\right) \dots \left(1 - \frac{k-1}{n}\right) \right] = 1^k = 1$$
2.  **Evaluate the exponential term:**
    By definition of the natural exponential function:
    $$\lim_{n \to \infty} \left(1 - \frac{\lambda}{n}\right)^n = e^{-\lambda}$$
3.  **Evaluate the remainder term:**
    Since $k$ is constant, as $n \to \infty$, the term $\frac{\lambda}{n} \to 0$:
    $$\lim_{n \to \infty} \left(1 - \frac{\lambda}{n}\right)^{-k} = (1 - 0)^{-k} = 1$$

Multiplying these limits together:
$$\lim_{n \to \infty} P(X_n = k) = \frac{\lambda^k}{k!} \cdot (1) \cdot \left(e^{-\lambda}\right) \cdot (1) = \frac{\lambda^k e^{-\lambda}}{k!} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Bernoulli and Binomial Sweets Selection
You pick mangoes from a crate. The probability of picking a ripe mango is $p = 0.8$.
1.  **Bernoulli Trial:** For a single selection ($n=1$), find the probability of selecting an unripe mango ($x=0$).
    $$P(X = 0) = 0.8^0 (1-0.8)^{1-0} = 1 \cdot (0.2)^1 = 0.2$$
2.  **Binomial Batch:** You select $n=10$ mangoes at random. Find the probability that exactly $k=8$ are ripe.
    $$P(X = 8) = \binom{10}{8} (0.8)^8 (0.2)^2$$
    Evaluate the coefficient: $\binom{10}{8} = \frac{10 \cdot 9}{2 \cdot 1} = 45$.
    $$P(X = 8) = 45 \cdot (0.16777) \cdot (0.04) \approx 0.3020$$
There is approximately a $30.20\%$ chance of exactly 8 ripe mangoes.

### Example 2: Poisson Rare Buyers
A market stall sells a rare variety of fruit at an average rate of $\lambda = 3$ buyers per hour. Find the probability that exactly $k=5$ people buy this variety in the next hour.
1.  **Recall the Poisson PMF:**
    $$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
2.  **Substitute parameters:**
    $$P(X = 5) = \frac{3^5 e^{-3}}{5!} = \frac{243 \cdot e^{-3}}{120}$$
    Since $e^{-3} \approx 0.049787$:
    $$P(X = 5) = \frac{243 \cdot 0.049787}{120} \approx 0.1008$$
There is approximately a $10.08\%$ chance of exactly 5 buyers.

---

## 5. Applied ML Context

1.  **Binary Classification Targets:** Neural networks predicting binary classes (e.g. churn vs. retain) output a probability parameter $p$ via sigmoid. This models target labels as Bernoulli random variables.
2.  **Binary Cross-Entropy Loss:** BCE loss is derived directly from the Negative Log-Likelihood of the Bernoulli PMF: $\mathcal{L} = - \left( y \log(p) + (1-y)\log(1-p) \right)$.
3.  **Dropout Regularization:** During training, dropout sets hidden units to zero with probability $1-p$. Each node undergoes an independent Bernoulli trial, forcing the network to learn redundant pathways.
4.  **Poisson Anomaly Detection:** In monitoring server logs, we model the rate of error events (e.g. 500 status codes) per minute as a Poisson distribution. An unusually high count $k$ yielding $P(X \ge k) < \epsilon$ flags an outlier.
5.  **Accuracy Confidence Intervals:** Validation predictions are independent Bernoulli trials. The count of correct predictions follows a Binomial distribution, which is used to calculate confidence intervals for model accuracy.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the three discrete distributions side-by-side:
*   Show three subplots side-by-side:
    1.  **Bernoulli PMF ($p=0.8$):** Draw two simple vertical bars at $x = 0$ (height $0.2$) and $x = 1$ (height $0.8$). This represents a single binary check.
    2.  **Binomial PMF ($n=10, p=0.8$):** Draw a series of vertical bars from $x = 0$ to $x = 10$, forming a discrete bell-shaped curve that peaks at $x = 8$, representing the sum of discrete trials.
    3.  **Poisson PMF ($\lambda=3$):** Draw a right-skewed series of vertical bars starting at $x = 0, 1, 2, \dots$ and fading out to the right, representing rare event counts in a continuous flow.
*   Add a caption summarizing the progression: "Bernoulli (single event) $\to$ Binomial (sum of discrete trials) $\to$ Poisson (infinitely partitioned continuous flow)."
