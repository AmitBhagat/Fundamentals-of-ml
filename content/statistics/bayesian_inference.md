---
title: "Bayesian Inference"
description: "Bayesian probability theory, parameter distributions, prior and likelihood updates, conjugate prior proofs, and Beta-Binomial conjugacy."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Discrete Probability Distributions", "Continuous Probability Distributions", "Conditional Probability", "Joint Distributions", "Bayes' Theorem"]
---

<h1 align="center"> Chapter 61: Bayesian Inference </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Bayes' Theorem:** The rule for calculating conditional probabilities: $P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}$.
* **Marginalization:** Summing or integrating out nuisance variables to isolate a single probability distribution.

</div>

## 1. Conceptual Hook

In classical frequentist statistics, probability is defined as the long-run limit of relative frequencies in infinitely repeated, identical trials. While mathematically convenient, this definition collapses when we deal with unique events or parameters that cannot be repeatedly sampled. How do we measure the probability that a specific model configuration will succeed, or estimate the uncertainty of a neural network's weights?

**Bayesian inference** offers a different perspective. It treats probability as a subjective *measure of belief* or certainty given incomplete information.

Instead of searching for a single, fixed "best" parameter, Bayesian inference treats parameters as random variables. It starts with an initial belief (the **prior**) and systematically updates this distribution as new evidence (the **likelihood**) arrives. This yields a complete probability distribution over all possible parameter values (the **posterior**), allowing machine learning models to reason about their own uncertainty.

---

## 2. Formal Definition

Let $\theta \in \Theta$ be a parameter vector modeled as a random variable with prior probability density function $p(\theta)$. Let $\mathbf{x} = \{x_1, x_2, \dots, x_n\}$ be a vector of observed data.

### Bayes' Theorem for Parameter Estimation
The posterior probability density $p(\theta \mid \mathbf{x})$ is defined as:
$$p(\theta \mid \mathbf{x}) = \frac{p(\mathbf{x} \mid \theta) p(\theta)}{p(\mathbf{x})}$$

where:
1.  **Prior $p(\theta)$:** Our initial belief about the parameter distribution before observing the data.
2.  **Likelihood $p(\mathbf{x} \mid \theta)$:** The probability density of observing the sample data $\mathbf{x}$ as a function of the parameter vector $\theta$.
3.  **Marginal Likelihood (Evidence) $p(\mathbf{x})$:** The total probability of observing the data across all possible parameter configurations, acting as a normalization constant:
    $$p(\mathbf{x}) = \int_{\Theta} p(\mathbf{x} \mid \theta) p(\theta) d\theta$$
    For discrete parameter spaces, the integral is replaced by a summation:
    $$p(\mathbf{x}) = \sum_{\theta_i \in \Theta} p(\mathbf{x} \mid \theta_i) p(\theta_i)$$
4.  **Posterior $p(\theta \mid \mathbf{x})$:** The updated probability distribution of our parameters after incorporating the observed data.

---

## 3. Illustrative Derivation

### Proof of Beta-Binomial Conjugacy
In Bayesian statistics, a prior is **conjugate** to the likelihood if the resulting posterior distribution belongs to the same algebraic family as the prior. We prove that the Beta distribution is the conjugate prior for a Binomial likelihood.

Let $X_1, X_2, \dots, X_n$ be i.i.d. Bernoulli trials with success probability $p \in [0, 1]$.
Let $k = \sum_{i=1}^n x_i$ be the total number of observed successes.
1.  **Formulate the Binomial Likelihood:**
    $$f(\mathbf{x} \mid p) = \left(\begin{array}{c}n\\k\end{array}\right) p^k (1-p)^{n-k} \propto p^k (1-p)^{n-k}$$

2.  **Formulate the Beta Prior:**
    Let $p$ follow a Beta distribution, $p \sim \text{Beta}(\alpha, \beta)$ with hyperparameters $\alpha, \beta > 0$:
    $$g(p; \alpha, \beta) = \frac{1}{\text{B}(\alpha, \beta)} p^{\alpha-1} (1-p)^{\beta-1} \propto p^{\alpha-1} (1-p)^{\beta-1}$$
    where $\text{B}(\alpha, \beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$ is the Beta function normalization constant.

3.  **Apply Bayes' Theorem to calculate the posterior:**
    $$f(p \mid \mathbf{x}) \propto f(\mathbf{x} \mid p) \cdot g(p; \alpha, \beta)$$
    Substitute the proportional terms of the likelihood and prior:
    $$f(p \mid \mathbf{x}) \propto \left[ p^k (1-p)^{n-k} \right] \cdot \left[ p^{\alpha-1} (1-p)^{\beta-1} \right]$$
    Combine exponents:
    $$f(p \mid \mathbf{x}) \propto p^{(\alpha + k) - 1} (1-p)^{(\beta + n - k) - 1}$$

4.  **Identify the normalized posterior distribution:**
    The functional form $p^{a-1} (1-p)^{b-1}$ is the core kernel of a Beta distribution with parameters $a = \alpha + k$ and $b = \beta + n - k$. Thus:
    $$f(p \mid \mathbf{x}) = \frac{1}{\text{B}(\alpha+k, \beta+n-k)} p^{(\alpha+k)-1} (1-p)^{(\beta+n-k)-1}$$
    This proves that:
    $$p \mid \mathbf{x} \sim \text{Beta}(\alpha + k, \quad \beta + n - k) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Hidden Indie Gem Discovery (Discrete Bayes)
You have a prior probability $P(\theta) = 0.20$ that the "Indie" category contains a hidden gem. You search and find $3$ award winners ($D$). The probability of finding them given a good category is $P(D \mid \theta) = 0.70$, and in a bad category is $P(D \mid \neg\theta) = 0.10$. Update your belief.
1.  **Calculate the Marginal Likelihood (Evidence):**
    $$P(D) = P(D \mid \theta)P(\theta) + P(D \mid \neg\theta)P(\neg\theta)$$
    $$P(D) = (0.70 \cdot 0.20) + (0.10 \cdot 0.80) = 0.14 + 0.08 = 0.22$$
2.  **Calculate the Posterior Probability:**
    $$P(\theta \mid D) = \frac{P(D \mid \theta)P(\theta)}{P(D)} = \frac{0.70 \cdot 0.20}{0.22} = \frac{0.14}{0.22} \approx 0.6364$$
Your confidence that the category contains a gem has updated from $20\%$ to $63.64\%$.

### Example 2: Stream Quality Impact on Movie Enjoyment
You consider watching a classic movie with a prior probability of enjoyment $P(\theta) = 0.95$. You encounter a low-quality stream warning ($D$). The probability of a bad stream occurring given a good movie is $P(D \mid \theta) = 0.10$, and given a mediocre movie is $P(D \mid \neg\theta) = 0.90$. Update your belief.
1.  **Calculate the Marginal Likelihood (Evidence):**
    $$P(D) = (0.10 \cdot 0.95) + (0.90 \cdot 0.05) = 0.095 + 0.045 = 0.140$$
2.  **Calculate the Posterior Probability:**
    $$P(\theta \mid D) = \frac{P(D \mid \theta)P(\theta)}{P(D)} = \frac{0.10 \cdot 0.95}{0.140} = \frac{0.095}{0.140} \approx 0.6786$$
Your confidence in having a good experience drops to $67.86\%$.

---

## 5. Applied ML Context

1.  **Naïve Bayes Email Classification:** Spam filters classify emails based on conditional likelihoods. The prior is the general spam frequency; the likelihood is the joint probability of seeing specific words (like "off", "deal") given a spam target.
2.  **Bayesian Neural Networks (BNNs):** BNNs place prior distributions over model weights rather than learning point estimates. Training computes a posterior distribution over weights, allowing the model to output predictive uncertainty.
3.  **Gaussian Process Regression:** A non-parametric Bayesian method that fits distributions over functions, yielding a mean prediction along with a variance (uncertainty) parameter for every input coordinate.
4.  **Bayesian Optimization Hyperparameter Search:** Surrogate models (often Gaussian Processes) construct posterior distributions over validation performance to guide hyperparameter selection (e.g. learning rate, regularization weight).
5.  **Latent Dirichlet Allocation (LDA):** A generative text model that uses Bayesian inference to discover latent topics in a text corpus, representing documents as mixtures of latent distributions over vocabularies.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the Bayesian update process:
*   Draw three probability density curves along a parameter axis $\theta$:
    1.  **Prior Distribution (dotted line):** A wide, flat curve representing high initial uncertainty about the parameter.
    2.  **Likelihood Function (dashed line):** A curve peaking around the observed sample statistics.
    3.  **Posterior Distribution (solid line):** A narrow, tall curve representing the updated parameters.
*   Show that the posterior curve peak is positioned between the prior and the likelihood peaks, but is narrower than both, illustrating how incorporating evidence increases precision.
*   Add a caption explaining that Bayesian inference acts as a mathematical filter, combining prior beliefs with empirical evidence to sharpen our parameter estimates and quantify uncertainty.
