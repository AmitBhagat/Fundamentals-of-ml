---
title: "Hypothesis Testing"
description: "Statistical hypotheses, null and alternative formulations, test statistics, t-statistic derivations, and rejection boundaries."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Random Variables", "Mean and Expectation", "Variance", "Standard Deviation"]
---

<h1 align="center"> Chapter 66: Hypothesis Testing </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Student's t-Distribution:** A symmetric, bell-shaped distribution with heavier tails than the Normal distribution, defined by degrees of freedom.
* **Chi-Square Distribution ($\chi^2$):** The distribution of a sum of squares of independent standard normal random variables.

</div>

## 1. Conceptual Hook

When we develop a new machine learning model or tune a set of hyperparameters, how do we prove that the improvements we observe are real? If our validation accuracy increases by $1.5\%$, how can we be sure we didn't just get lucky with our random train-test split or initialization seed? The mathematical framework that prevents us from falling victim to random flukes is **hypothesis testing**.

Hypothesis testing operates like a court of law. It establishes a baseline assumption that our new model has zero impact and behaves no differently than the old model (the **null hypothesis**). We then gather empirical evidence (validation runs) and calculate a test statistic. We only reject the null hypothesis if the evidence is so extreme that the probability of it being a random coincidence (the **p-value**) drops below a strict significance threshold. This guarantees that our model improvements are statistically sound before we spend engineering resources deploying them.

---

## 2. Formal Definition

Let $\mathbf{X} = \{X_1, X_2, \dots, X_n\}$ be a sample of $n$ random observations drawn from a population parameterized by $\theta$.

### Competing Hypotheses
We define two mutually exclusive statements about the parameter $\theta$:
1.  **Null Hypothesis ($H_0$):** The status quo assumption that there is no effect or no difference:
    $$H_0: \theta = \theta_0$$
2.  **Alternative Hypothesis ($H_1$ or $H_a$):** The claim we hope to support:
    *   *Two-Tailed:* $H_1: \theta \neq \theta_0$
    *   *Right-Tailed:* $H_1: \theta > \theta_0$
    *   *Left-Tailed:* $H_1: \theta < \theta_0$

### Test Statistic, Rejection Region, and Significance Level
*   **Test Statistic $T(\mathbf{X})$:** A random variable computed from the sample data whose probability distribution under $H_0$ is completely known.
*   **Rejection Region (Critical Region) $R$:** The set of values for the test statistic $T(\mathbf{X})$ that lead to the rejection of $H_0$.
*   **Significance Level ($\alpha$):** The maximum allowable probability of committing a Type I error (rejecting $H_0$ when it is actually true):
    $$\alpha = P(\text{Reject } H_0 \mid H_0 \text{ is true}) = P(T(\mathbf{X}) \in R \mid H_0 \text{ is true})$$
    Common choices for $\alpha$ are $0.05$, $0.01$, or $0.001$.
*   **p-value:** The probability, under the assumption that $H_0$ is true, of obtaining a test statistic at least as extreme as the observed value $t_{obs}$:
    $$\text{p-value} = P(T(\mathbf{X}) \ge t_{obs} \mid H_0 \text{ is true}) \quad (\text{for a right-tailed test})$$
    We reject $H_0$ if $\text{p-value} \le \alpha$.

---

## 3. Illustrative Derivation

### Derivation of the Student's t-Statistic
When analyzing a population mean $\mu$, if the population variance $\sigma^2$ is unknown, we cannot use a standard Z-score. We derive the Student's t-statistic by combining a standard normal variable and an independent Chi-square variable.

Let $X_1, X_2, \dots, X_n$ be i.i.d. random variables sampled from a normal distribution $\mathcal{N}(\mu, \sigma^2)$.
1.  **Formulate the sample mean distribution:**
    The sample mean is $\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$. Under the properties of normal distributions, the sample mean is distributed as:
    $$\bar{X} \sim \mathcal{N}\left( \mu, \frac{\sigma^2}{n} \right)$$
    Standardizing the sample mean yields a standard normal random variable $Z$:
    $$Z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1)$$

2.  **Formulate the sample variance distribution:**
    The unbiased sample variance is $S^2 = \frac{1}{n-1} \sum_{i=1}^n (X_i - \bar{X})^2$. By Cochran's Theorem, the rescaled sample variance follows a Chi-square distribution with $n-1$ degrees of freedom:
    $$V = \frac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$$
    Furthermore, the sample mean $\bar{X}$ and sample variance $S^2$ are statistically independent.

3.  **Define Student's t-distribution:**
    A Student's t-distributed random variable $T$ is defined as the ratio of a standard normal variable $Z$ to the square root of an independent Chi-square variable $V$ divided by its degrees of freedom $r$:
    $$T = \frac{Z}{\sqrt{V / r}}$$
    Substitute $Z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}}$, $V = \frac{(n-1)S^2}{\sigma^2}$, and $r = n-1$:
    $$T = \frac{\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}}{\sqrt{\frac{(n-1)S^2}{\sigma^2} \Big/ (n-1)}} = \frac{\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}}{\sqrt{\frac{S^2}{\sigma^2}}} = \frac{\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}}{\frac{S}{\sigma}}$$
    The population standard deviation $\sigma$ cancels out of the equation:
    $$T = \frac{\bar{X} - \mu}{S / \sqrt{n}}$$
    Therefore, the test statistic $T$ follows a Student's t-distribution with $n-1$ degrees of freedom: $T \sim t(n-1)$. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Engine Idle Stability (Two-Tailed T-Test)
A seller claims a motorcycle engine idles at a mean rate of $\mu_0 = 1000$ RPM. You record the idle rate for $n=10$ seconds, finding a sample mean of $\bar{x} = 1200$ RPM and sample standard deviation $s = 200$. Test the hypothesis $H_0: \mu = 1000$ against $H_1: \mu \neq 1000$ at significance level $\alpha = 0.05$.
1.  **Calculate the t-statistic:**
    $$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}} = \frac{1200 - 1000}{200 / \sqrt{10}} = \frac{200}{63.2456} \approx 3.162$$
2.  **Determine the rejection boundary:**
    For a two-tailed t-test with degrees of freedom $df = n-1 = 9$ and $\alpha = 0.05$, the critical value from the t-distribution table is $t_{crit} = 2.262$.
3.  **Evaluate:**
    Since $|t| \approx 3.162 > 2.262$, the test statistic falls in the rejection region. We reject $H_0$ and conclude that the engine's idle rate differs significantly from the claimed 1000 RPM.

### Example 2: Motorcycle Acceleration claims (One-Tailed T-Test)
A manufacturer claims a bike takes at most $4.0$ seconds to reach $60$ mph. You perform $n=5$ test runs, measuring an average time of $\bar{x} = 4.5$ seconds with standard deviation $s = 0.4$. Test $H_0: \mu \le 4.0$ against $H_1: \mu > 4.0$ at significance level $\alpha = 0.05$.
1.  **Calculate the t-statistic:**
    $$t = \frac{4.5 - 4.0}{0.4 / \sqrt{5}} = \frac{0.5}{0.1789} \approx 2.795$$
2.  **Determine the rejection boundary:**
    For a right-tailed t-test with $df = 4$ and $\alpha = 0.05$, the critical value is $t_{crit} = 2.132$.
3.  **Evaluate:**
    Since $t \approx 2.795 > 2.132$, we reject $H_0$. The evidence supports the claim that the average acceleration time is significantly longer than 4 seconds.

---

## 5. Applied ML Context

1.  **A/B Testing Model Upgrades:** When comparing a baseline model against a challenger model, we compute the mean accuracy difference over multiple folds and perform a t-test to ensure the performance lift is statistically significant.
2.  **Feature Significance in Linear Regression:** In OLS regression models, we perform hypothesis tests on each weight parameter: $H_0: w_j = 0$ against $H_1: w_j \neq 0$. Features with high p-values ($p > 0.05$) are pruned during feature selection.
3.  **Covariate Shift Detection:** We monitor input distributions in production. If the mean value of incoming features shifts significantly over time (using tests like the Kolmogorov-Smirnov test), we flag the change to trigger model retraining.
4.  **Neural Network Activation Verification:** During weight initialization audits, we perform t-tests on hidden layer activations to verify that their distributions are centered at a mean of zero, preventing vanishing or exploding gradients.
5.  **Statistical Anomaly Detection:** In fraud detection, we model normal transaction patterns as the null hypothesis. Any incoming transaction that yields a test statistic in the extreme tails (e.g. $p < 0.001$) is flagged as anomalous.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the distribution of a test statistic under the null hypothesis:
*   Draw a symmetric bell curve representing the probability density of the test statistic (e.g. standard normal or t-distribution) under the assumption that $H_0$ is true.
*   Mark the center of the curve as $\mu_0$.
*   For a two-tailed test, shade both the extreme left and right tails of the curve. Label these shaded regions as the "Rejection Regions (Critical Regions)" and mark the boundary thresholds as $-t_{crit}$ and $+t_{crit}$.
*   Draw a clear vertical line indicating the position of the observed test statistic $t_{obs}$.
*   If $t_{obs}$ falls within the shaded tail, show an arrow pointing to the conclusion: "Reject $H_0$ (Reject status quo)." If it falls in the unshaded center, point to "Fail to reject $H_0$," visually showing how the p-value corresponds to the remaining tail area.
