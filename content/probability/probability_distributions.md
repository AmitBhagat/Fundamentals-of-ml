---
title: "Probability Distributions"
description: "Probability spaces, Kolmogorov axioms, discrete and continuous random variables, PMFs, PDFs, and Bernoulli derivations."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Integral Calculus"]
---

<h1 align="center"> Chapter 54: Probability Distributions </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Sample Space ($\mathcal{S}$ or $\Omega$):** The set of all possible outcomes of a random process.
* **Continuous Integration:** Knowing how to evaluate areas under curves.

</div>

## 1. Conceptual Hook

In machine learning, data is rarely deterministic. Sensor measurements are corrupted by noise, image labels are subject to human ambiguity, and future predictions are fundamentally uncertain. If we treat these variables as fixed numbers, our models will fail when encountering slight variations. To model uncertainty, we use **probability distributions**.

A probability distribution is a mathematical function that describes the likelihood of different possible outcomes for a random variable. It defines the "shape" of randomness, showing where the probability is concentrated and where it is scarce. You can think of a probability distribution as a **budget of certainty**: you have exactly $1.0$ (or $100\%$) of likelihood to spend, and the distribution defines exactly how you allocate this budget across all possible states. Knowing this shape allows models to calculate confidence intervals and make risk-averse decisions.

---

## 2. Formal Definition

### Probability Space
Formally, we define probability using a **probability space**, which is a measure space $(\Omega, \mathcal{F}, P)$ consisting of:
1.  **Sample Space ($\Omega$):** The set of all possible outcomes.
2.  **Event Space ($\mathcal{F}$):** A $\sigma$-algebra of subsets of $\Omega$ representing the collection of all valid events.
3.  **Probability Measure ($P$):** A function $P: \mathcal{F} \to [0, 1]$ satisfying the **Kolmogorov Axioms**:
    *   **Non-negativity:** $P(A) \ge 0$ for all $A \in \mathcal{F}$.
    *   **Normalization:** $P(\Omega) = 1$.
    *   **Countable Additivity:** For any countable sequence of pairwise disjoint events $A_1, A_2, \dots \in \mathcal{F}$:
        $$P\left( \bigcup_{i=1}^{\infty} A_i \right) = \sum_{i=1}^{\infty} P(A_i)$$

### Random Variables and Distributions
A **random variable** $X$ is a measurable function $X: \Omega \to \mathbb{R}$ that maps outcomes from the sample space to real numbers. The **probability distribution** of $X$ is the probability measure $P_X$ induced on $\mathbb{R}$:
$$P_X(B) = P(X^{-1}(B)) = P(\{\omega \in \Omega : X(\omega) \in B\})$$
where $B$ is a Borel subset of $\mathbb{R}$.

*   **Discrete Distributions:** The random variable $X$ takes on values in a countable set. Its distribution is defined by a **Probability Mass Function (PMF)** $p(x) = P(X = x)$ satisfying:
    $$p(x) \ge 0 \quad \forall x \quad \text{and} \quad \sum_{x} p(x) = 1$$
*   **Continuous Distributions:** The random variable $X$ takes on values in an uncountable set. Its distribution is defined by a **Probability Density Function (PDF)** $f(x)$ satisfying:
    $$f(x) \ge 0 \quad \forall x, \quad \int_{-\infty}^{\infty} f(x) dx = 1, \quad \text{and} \quad P(a \le X \le b) = \int_{a}^{b} f(x) dx$$

---

## 3. Illustrative Derivation

### Derivation of Bernoulli Expectation and Variance
The **Bernoulli distribution** models a single trial with binary outcomes: success ($1$) with probability $p$, and failure ($0$) with probability $1-p$. We derive its mean (expectation) and variance directly from its PMF.

Let $X \sim \text{Bernoulli}(p)$ with PMF:
$$P(X = x) = \begin{cases} p & \text{if } x = 1 \\ 1 - p & \text{if } x = 0 \end{cases}$$
which can be written compactly as $P(X = x) = p^x (1-p)^{1-x}$ for $x \in \{0, 1\}$.

1.  **Derivation of Expectation $\mathbb{E}[X]$:**
    The expectation of a discrete random variable is $\mathbb{E}[X] = \sum x \cdot P(X = x)$:
    $$\mathbb{E}[X] = 0 \cdot P(X = 0) + 1 \cdot P(X = 1)$$
    $$\mathbb{E}[X] = 0 \cdot (1-p) + 1 \cdot p = p$$
    Thus, the expected value of a Bernoulli random variable is its success probability $p$.

2.  **Derivation of Variance $\text{Var}(X)$:**
    The variance is defined as $\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$.
    First, we calculate the second moment $\mathbb{E}[X^2] = \sum x^2 \cdot P(X = x)$:
    $$\mathbb{E}[X^2] = 0^2 \cdot P(X = 0) + 1^2 \cdot P(X = 1)$$
    $$\mathbb{E}[X^2] = 0 \cdot (1-p) + 1 \cdot p = p$$
    Now, substitute $\mathbb{E}[X^2] = p$ and $\mathbb{E}[X] = p$ into the variance formula:
    $$\text{Var}(X) = p - p^2 = p(1-p) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Binomial Distribution (Discrete)
The Binomial distribution models the number of successes $k$ in $n$ independent Bernoulli trials. Let $X \sim \text{Binomial}(n=3, p=0.7)$. Find the probability of obtaining exactly $k = 2$ successes.
1.  **Recall the PMF:**
    $$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$
2.  **Substitute the parameters:**
    $$P(X = 2) = \binom{3}{2} (0.7)^2 (1-0.7)^{3-2}$$
    $$P(X = 2) = \frac{3!}{2!(3-2)!} \cdot (0.49) \cdot (0.3)^1 = 3 \cdot 0.49 \cdot 0.3 = 0.441$$
There is a $44.1\%$ chance of exactly 2 successes.

### Example 2: Poisson Distribution (Discrete)
The Poisson distribution models the number of events occurring within a fixed interval of time. Let $Y \sim \text{Poisson}(\lambda=2)$ represent the average number of server crashes per day. Find the probability of $0$ crashes in a day.
1.  **Recall the PMF:**
    $$P(Y = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
2.  **Substitute $k=0$ and $\lambda=2$:**
    $$P(Y = 0) = \frac{2^0 e^{-2}}{0!} = \frac{1 \cdot e^{-2}}{1} = e^{-2} \approx 0.1353$$
There is approximately a $13.53\%$ chance of a day without server crashes.

---

## 5. Applied ML Context

1.  **Gaussian Naive Bayes Classifiers:** To classify continuous features, this algorithm assumes that values associated with each class follow a Normal (Gaussian) distribution, calculating class-conditional likelihoods.
2.  **Latent Prior in VAEs:** Variational Autoencoders enforce a continuous structure on the latent space by minimizing the KL divergence between the encoder's output distribution and a standard normal prior distribution: $\mathcal{N}(\mathbf{0}, \mathbf{I})$.
3.  **Cross-Entropy Loss:** In classification, the model outputs a categorical probability distribution over classes via softmax. Cross-entropy measures the divergence between this predicted distribution and the target one-hot distribution.
4.  **Maximum Likelihood Estimation (MLE):** Standard supervised learning fits parameters $\theta$ by maximizing the likelihood of observing the training data: $\theta_{MLE} = \arg\max_\theta \sum_i \log P(y_i | x_i; \theta)$ under an assumed distribution (e.g. Gaussian for MSE regression).
5.  **Generative Diffusion Models:** These models systematically add noise to images following a forward Gaussian transition distribution, and train a neural network to estimate the reverse distribution to generate images from random noise.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating discrete vs. continuous probability distributions:
*   Show two side-by-side plots:
    1.  **Discrete Distribution (PMF):** Draw a bar chart (for example, a Binomial distribution). Show discrete vertical lines at $x = 0, 1, 2, 3$. Label the vertical axis as "Probability $P(X=x)$." Emphasize that the sum of the heights of all bars is exactly $1.0$.
    2.  **Continuous Distribution (PDF):** Draw a smooth, continuous bell curve. Label the vertical axis as "Probability Density $f(x)$." Draw vertical lines at bounds $a$ and $b$, and shade the region under the curve between them. Label the shaded area as the probability $P(a \le X \le b) = \int_a^b f(x) dx$. Emphasize that the total area under the entire curve is exactly $1.0$.
*   Use this comparison to reinforce the "budget of certainty" concept, showing how discrete packets differ from continuous spreads.
