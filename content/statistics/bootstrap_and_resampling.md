---
title: "Bootstrap and Resampling"
description: "Empirical distributions, resampling with replacement, standard error estimations, Out-of-Bag probability derivations, and bagging."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Mean and Expectation", "Variance", "Standard Deviation", "The Z-Test", "The T-Test"]
---

<h1 align="center"> Chapter 63: Bootstrap and Resampling </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Sampling with Replacement:** Drawing an item from a set and returning it before the next draw, keeping the probability of selection constant.
* **Empirical Distribution Function (ECDF):** The step-function CDF that assigns a probability of $1/n$ to each observed data point in a sample.

</div>

## 1. Conceptual Hook

In statistics and machine learning, we are often constrained by "small-data anxiety." We have one single dataset, and we are terrified that it does not represent the broader population. Gathering more data is often too expensive or impossible. How do we estimate the volatility of our model predictions or parameter estimates without collecting new observations? The mathematical solution is **bootstrapping**.

Bootstrapping operates under a simple, elegant philosophy: we treat our observed sample as the entire population. By repeatedly drawing new samples of equal size *with replacement* from this empirical distribution, we can simulate an infinite number of parallel datasets. This allows us to calculate confidence intervals, standard errors, and model stability bounds without ever needing to gather new real-world data.

---

## 2. Formal Definition

Let $\mathbf{X} = \{X_1, X_2, \dots, X_n\}$ be a sample of $n$ i.i.d. observations drawn from an unknown cumulative distribution function $F$.

### Empirical Distribution Function
The **empirical distribution function (ECDF)** $F_n$ is defined as:
$$F_n(x) = \frac{1}{n} \sum_{i=1}^{n} \mathbb{I}(X_i \le x)$$
where $\mathbb{I}(\cdot)$ is the indicator function. The ECDF assigns a probability of $1/n$ to each observed data point.

### Bootstrap Samples
A **bootstrap sample** $\mathbf{X}^* = \{X_1^*, X_2^*, \dots, X_n^*\}$ is an i.i.d. sample of size $n$ drawn directly from $F_n$. This is equivalent to sampling $n$ times with replacement from the set $\mathbf{X}$:
$$P(X_i^* = X_j \mid \mathbf{X}) = \frac{1}{n} \quad \forall i, j \in \{1, \dots, n\}$$

### Bootstrap Standard Error Estimator
Let $\hat{\theta} = t(F_n)$ be a plug-in estimator for a parameter $\theta = t(F)$. We generate $B$ independent bootstrap samples, computing the replication $\hat{\theta}^*_b$ for each sample $b \in \{1, \dots, B\}$. The **Bootstrap standard error** of $\hat{\theta}$ is estimated by:
$$\widehat{\text{se}}_B(\hat{\theta}) = \sqrt{\frac{1}{B-1} \sum_{b=1}^{B} \left( \hat{\theta}^*_b - \bar{\theta}^* \right)^2}$$
where $\bar{\theta}^*$ is the average of the bootstrap replications:
$$\bar{\theta}^* = \frac{1}{B} \sum_{b=1}^{B} \hat{\theta}^*_b$$

---

## 3. Illustrative Derivation

### Derivation of the Out-of-Bag (OOB) Asymptotic Probability
We derive the asymptotic probability that a specific observation $X_i$ is *not* selected in a bootstrap sample of size $n$ as $n \to \infty$. This derivation explains the source of the $36.8\%$ validation fraction in Random Forest models.

*Proof:*
Let $\mathbf{X}^* = \{X_1^*, \dots, X_n^*\}$ be a bootstrap sample drawn with replacement from $\mathbf{X} = \{X_1, \dots, X_n\}$.
1.  **Calculate selection probability on a single draw:**
    Since we sample uniformly with replacement, the probability of selecting a specific observation $X_i$ on a single draw $j$ is:
    $$P(\text{Select } X_i \text{ on draw } j) = \frac{1}{n}$$
    Therefore, the probability of *not* selecting $X_i$ on a single draw is:
    $$P(\text{Do not select } X_i \text{ on draw } j) = 1 - \frac{1}{n}$$

2.  **Calculate probability across $n$ independent draws:**
    Because the draws are independent, the probability that $X_i$ is not selected in any of the $n$ draws comprising the bootstrap sample is:
    $$P(\text{Observation } X_i \text{ is not in } \mathbf{X}^*) = \prod_{j=1}^{n} \left( 1 - \frac{1}{n} \right) = \left( 1 - \frac{1}{n} \right)^n$$

3.  **Evaluate the limit as $n \to \infty$:**
    We evaluate the asymptotic behavior of this probability for large datasets:
    $$p_{\infty} = \lim_{n \to \infty} \left( 1 - \frac{1}{n} \right)^n$$
    Recall the calculus definition of the exponential constant $e$:
    $$\text{For any } x \in \mathbb{R}, \quad \lim_{n \to \infty} \left( 1 + \frac{x}{n} \right)^n = e^x$$
    Setting $x = -1$ yields:
    $$p_{\infty} = e^{-1} = \frac{1}{e} \approx 0.367879 \quad (36.79\%)$$

Consequently, for large datasets, the probability that a specific data point is *not* included in a bootstrap sample is approximately $36.8\%$. This implies that a bootstrap sample contains roughly $1 - e^{-1} \approx 63.2\%$ of the unique observations from the original dataset. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Customer Efficiency Resampling (Single Resample)
An front-desk clerk efficiency score sample is $\mathbf{X} = \{2, 8, 5\}$ ($n=3$). We draw a bootstrap sample $\mathbf{X}^*$ by selecting the 2nd, 2nd, and 1st elements of $\mathbf{X}$ with replacement.
1.  **Identify the bootstrap sample:**
    $$\mathbf{X}^* = \{x_2, \quad x_2, \quad x_1\} = \{8, \quad 8, \quad 2\}$$
2.  **Calculate the bootstrap mean:**
    $$\hat{\theta}^* = \frac{8 + 8 + 2}{3} = 6.0$$
*Note:* The mean of our original sample was $5.0$. By replaying the trials and emphasizing the second interaction, our bootstrap replication is $6.0$.

### Example 2: View Quality Variance Estimation
A view quality rating sample is $\mathbf{X} = \{7, 9, 7, 10\}$ ($n=4$). We draw a bootstrap sample $\mathbf{X}^* = \{10, 7, 7, 7\}$. Calculate the mean and variance of this bootstrap sample.
1.  **Calculate the bootstrap mean:**
    $$\bar{x}^* = \frac{10 + 7 + 7 + 7}{4} = 7.75$$
2.  **Calculate the bootstrap variance:**
    $$\text{Var}(\mathbf{X}^*) = \frac{\sum (x_i^* - \bar{x}^*)^2}{n} = \frac{(10 - 7.75)^2 + 3(7 - 7.75)^2}{4}$$
    $$\text{Var}(\mathbf{X}^*) = \frac{2.25^2 + 3(-0.75)^2}{4} = \frac{5.0625 + 3(0.5625)}{4} = \frac{6.75}{4} = 1.6875$$

---

## 5. Applied ML Context

1.  **Random Forest (Bagging):** Bootstrap Aggregation (Bagging) trains multiple decision trees on independent bootstrap samples. This averages out the high variance of individual trees to produce a stable ensemble model.
2.  **Out-of-Bag (OOB) Error Estimation:** Since each bootstrap sample leaves out roughly $36.8\%$ of the dataset, these unselected observations serve as a built-in validation set to estimate model generalization performance without needing explicit cross-validation folds.
3.  **Coefficient Confidence Intervals:** In regression models, bootstrapping is used to estimate confidence intervals for parameter weights, which is especially useful when errors are non-normal.
4.  **Non-Parametric Hypothesis Testing:** Resampling is used to test the statistical significance of a metric (like the difference in mean accuracy between two models) without making parametric assumptions about the underlying distribution.
5.  **Feature Importance Stability Audits:** By running feature selection algorithms over multiple bootstrap samples, engineers check which features are consistently selected, pruning those that were selected due to noise in a specific data split.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the bootstrapping process:
*   Draw a central box representing the "Original Dataset $\mathbf{X}$" containing $n$ distinct shapes.
*   Draw multiple diverging arrows pointing to $B$ boxes labeled "Bootstrap Sample $\mathbf{X}^*_1 \dots \mathbf{X}^*_B$."
*   Inside each bootstrap box, show $n$ shapes sampled with replacement (some shapes duplicated, some missing). Label the missing shapes in each box as "Out-of-Bag (OOB) data ($36.8\%$)."
*   Draw arrows from each bootstrap sample box to a calculator node, yielding estimators $\hat{\theta}^*_1 \dots \hat{\theta}^*_B$.
*   Show these estimators merging into a final histogram representing the bootstrap distribution of the estimator, showing how we estimate standard error.
