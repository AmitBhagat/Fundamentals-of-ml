---
title: "Confidence Intervals"
description: "Interval estimation, confidence levels, standard errors, critical values, pivotal quantities, and interval derivations."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Mean and Expectation", "Variance", "Standard Deviation", "Central Limit Theorem"]
---

<h1 align="center"> Chapter 65: Confidence Intervals </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Central Limit Theorem:** Understanding how sampling distributions of means converge to Normal distributions at scale.
* **Standard Error ($SE$):** Knowing how the standard deviation of a sample mean scales as $\sigma / \sqrt{n}$.

</div>

## 1. Conceptual Hook

In machine learning, reporting a single accuracy score (like "92%") or a single loss value can be highly misleading. How do we know if this score is a stable reflection of our model's performance, or just a lucky fluctuation on our specific test set? To quantify the reliability of our estimates, we use **confidence intervals**.

Instead of a single point estimate, a confidence interval defines a range of values within which the true, global population parameter (like the true generalization accuracy of our model) is likely to reside. It acts as a safety margin. By calculating this range, we can declare with a specified level of confidence (typically $95\%$ or $99\%$) how much our estimation is expected to fluctuate across different test sets, providing a rigorous metric for model comparison.

---

## 2. Formal Definition

Let $\mathbf{X} = \{X_1, X_2, \dots, X_n\}$ be an i.i.d. sample of size $n$ from a distribution parameterized by a fixed but unknown parameter $\theta \in \Theta$.

### Definition of a Confidence Interval
A **$(1-\alpha)$ Confidence Interval** for the parameter $\theta$ is an interval $[L(\mathbf{X}), U(\mathbf{X})]$ determined by two sample statistics $L(\mathbf{X})$ and $U(\mathbf{X})$ such that:
$$P\left( L(\mathbf{X}) \le \theta \le U(\mathbf{X}) \right) = 1 - \alpha \quad \forall \theta$$
where:
*   **$1-\alpha$ (Confidence Level):** The probability that the calculated interval will contain the true parameter $\theta$ across repeated sampling experiments.
*   **$L(\mathbf{X})$ and $U(\mathbf{X})$ (Lower and Upper Bounds):** Random variables whose values are calculated from the realized sample data.

### Frequentist Interpretation
In frequentist statistics, the population parameter $\theta$ is a **fixed constant**, not a random variable. The interval boundaries $L(\mathbf{X})$ and $U(\mathbf{X})$ are the random variables because they depend on the random sample $\mathbf{X}$. Therefore, the probability statement describes the probability that the *random interval covers the fixed parameter*, not that the parameter falls into a fixed interval.

---

## 3. Illustrative Derivation

### Derivation of the Confidence Interval for a Normal Mean (Known Variance)
We derive the formula for a $(1-\alpha)$ confidence interval for a population mean $\mu$, assuming the population variance $\sigma^2$ is known. We utilize the method of pivotal quantities.

*Proof:*
Let $\{X_1, X_2, \dots, X_n\}$ be i.i.d. random variables sampled from a normal distribution $\mathcal{N}(\mu, \sigma^2)$.
1.  **Formulate the pivotal quantity:**
    The sample mean $\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$ is distributed as:
    $$\bar{X} \sim \mathcal{N}\left( \mu, \frac{\sigma^2}{n} \right)$$
    We define the standard normal pivot variable $Z$:
    $$Z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1)$$

2.  **Establish probability bounds:**
    For a given significance level $\alpha$, we choose a critical value $z_{\alpha/2}$ from the standard normal distribution such that the probability of $Z$ falling between $-z_{\alpha/2}$ and $z_{\alpha/2}$ is exactly $1-\alpha$:
    $$P\left( -z_{\alpha/2} \le Z \le z_{\alpha/2} \right) = 1 - \alpha$$
    Substitute the definition of the pivot $Z$:
    $$P\left( -z_{\alpha/2} \le \frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \le z_{\alpha/2} \right) = 1 - \alpha$$

3.  **Isolate the parameter $\mu$:**
    Multiply all terms in the inequality by the standard error $SE = \frac{\sigma}{\sqrt{n}}$:
    $$P\left( -z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le \bar{X} - \mu \le z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right) = 1 - \alpha$$
    Subtract the sample mean $\bar{X}$ from all terms:
    $$P\left( -\bar{X} - z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le -\mu \le -\bar{X} + z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right) = 1 - \alpha$$
    Multiply the entire inequality by $-1$. This reverses the inequality directions:
    $$P\left( \bar{X} + z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \ge \mu \ge \bar{X} - z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right) = 1 - \alpha$$
    Rearrange the inequality into standard ascending order:
    $$P\left( \bar{X} - z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le \mu \le \bar{X} + z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right) = 1 - \alpha \quad \blacksquare$$

The resulting $(1-\alpha)$ confidence interval is:
$$CI = \left[ \bar{X} - z_{\alpha/2} \frac{\sigma}{\sqrt{n}}, \quad \bar{X} + z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right]$$

---

## 4. Concrete Examples

### Example 1: Airport Gate Transit Times (Known Variance)
You measure the walking time to a gate for $n=36$ travelers, finding a sample mean of $\bar{x} = 10$ minutes. The population standard deviation is known to be $\sigma = 1.2$ minutes. Find the $95\%$ confidence interval for the mean walking time ($\alpha = 0.05 \implies z_{0.025} = 1.96$).
1.  **Calculate the Standard Error:**
    $$SE = \frac{\sigma}{\sqrt{n}} = \frac{1.2}{\sqrt{36}} = \frac{1.2}{6} = 0.2 \text{ minutes}$$
2.  **Calculate the Margin of Error:**
    $$E = z_{0.025} \cdot SE = 1.96 \cdot 0.2 = 0.392 \text{ minutes}$$
3.  **Construct the interval:**
    $$CI = [10 - 0.392, \quad 10 + 0.392] = [9.608, \quad 10.392] \text{ minutes}$$
We are $95\%$ confident that the true average walking time lies between $9.61$ and $10.39$ minutes.

### Example 2: Carry-On Bag Width (Unknown Variance)
You measure carry-on bag widths for a sample of $n=25$ bags, finding a mean width of $\bar{x} = 45$ cm with sample standard deviation $s = 2.5$ cm. Find the $99\%$ confidence interval for the mean bag width.
1.  **Select the critical value:**
    Since the population variance is unknown and the sample size is small ($n < 30$), we use Student's t-distribution with $df = n-1 = 24$ degrees of freedom. At $99\%$ confidence ($\alpha = 0.01$), the critical value is $t_{0.005, 24} \approx 2.797$.
2.  **Calculate the Standard Error:**
    $$SE = \frac{s}{\sqrt{n}} = \frac{2.5}{\sqrt{25}} = 0.5 \text{ cm}$$
3.  **Calculate the Margin of Error:**
    $$E = t_{0.005, 24} \cdot SE = 2.797 \cdot 0.5 = 1.3985 \text{ cm}$$
4.  **Construct the interval:**
    $$CI = [45 - 1.3985, \quad 45 + 1.3985] = [43.6015, \quad 46.3985] \text{ cm}$$
We are $99\%$ confident that the true average bag width lies between $43.60$ and $46.40$ cm.

---

## 5. Applied ML Context

1.  **Generalization Performance Bounds:** Instead of reporting a single validation score, we construct confidence intervals over test set metrics (e.g. Accuracy or F1-Score) to describe the expected performance range on unseen future distributions.
2.  **A/B Testing Conversion Analysis:** In production deployments, we construct confidence intervals for user conversion rates or click-through rates (CTR) to determine if a new model's performance improvement is statistically significant.
3.  **Feature Coefficient Stability:** We use bootstrap resampling to construct confidence intervals for regression coefficients. If a feature's coefficient interval contains zero (e.g. $[-0.02, 0.05]$), the feature is flagged as unstable.
4.  **Bayesian Optimization Acquisition Functions:** In hyperparameter tuning, algorithms like Upper Confidence Bound (UCB) use confidence intervals to balance exploration (sampling coordinates with high standard error) and exploitation (sampling coordinates with high expected means): $\alpha_{UCB}(\mathbf{x}) = \mu(\mathbf{x}) + \kappa \sigma(\mathbf{x})$.
5.  **Active Learning Query Selection:** Active learning models prioritize unlabeled data points for manual labeling where the model's prediction confidence interval is widest, targeting regions of maximum uncertainty.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating confidence interval coverage:
*   Draw a solid vertical line down the center representing the true, fixed population parameter $\mu$.
*   Draw a vertical stack of 20 horizontal line segments (representing 20 calculated confidence intervals from 20 independent samples). Each line segment has a point in the center representing its sample mean $\bar{x}_i$.
*   Color code the line segments:
    *   Draw 19 segments in blue, showing that they overlap with and cross the central vertical line $\mu$.
    *   Draw 1 segment in red, showing it is shifted entirely to one side and fails to cross the vertical line $\mu$.
*   Add a caption explaining that the "95% confidence level" means that if we repeat the sampling process indefinitely, $95\%$ of our calculated intervals will successfully cover the true parameter $\mu$. This demonstrates that the confidence level describes the reliability of the estimation process, not the probability of the parameter moving.
