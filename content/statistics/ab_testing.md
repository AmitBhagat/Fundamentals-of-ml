---
title: "A/B Testing"
description: "Statistical comparisons of product variants, binary conversion rates, pooled standard errors, and Z-score testing."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Discrete Probability Distributions", "Mean and Expectation", "Variance", "Hypothesis Testing", "The Z-Test"]
---

<h1 align="center"> Chapter 59: A/B Testing </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Bernoulli Trials:** Random trials that yield binary outcomes (success or failure, click or no-click).
* **Z-Test for Proportions:** Standardizing the difference between two sample rates under normal approximations.

</div>

## 1. Conceptual Hook

In product design and machine learning systems, we are constantly making optimization decisions: Does recommendation algorithm A yield higher revenue than algorithm B? Does a new page layout increase user click-through rates? Rather than relying on gut feelings, we put these choices to a vote by routing random, independent streams of users to different model variants. This process is called **A/B testing**.

A/B testing is the clinical application of hypothesis testing in engineering. We define a baseline model (the **Control**, or variant A) and a new candidate model (the **Treatment**, or variant B). By splitting incoming user traffic randomly between them, we calculate conversion rates and compute a test statistic. The math proves whether the observed difference in user behavior represents a real, causal effect of the design change, or if it is just a random fluke of traffic.

---

## 2. Formal Definition

Let $X_{A, 1}, X_{A, 2}, \dots, X_{A, n_A}$ be i.i.d. Bernoulli random variables representing outcomes for the Control group $A$, and let $X_{B, 1}, X_{B, 2}, \dots, X_{B, n_B}$ be i.i.d. outcomes for the Treatment group $B$:
$$X_A \sim \text{Bernoulli}(p_A) \quad \text{and} \quad X_B \sim \text{Bernoulli}(p_B)$$

### Hypotheses
We test the null hypothesis that the treatment does not increase conversion rates:
$$H_0: p_B - p_A \le 0$$
$$H_1: p_B - p_A > 0 \quad (\text{Right-Tailed Test})$$

### Sample Estimates and Pooled Proportion
The sample conversion rates are:
$$\hat{p}_A = \frac{1}{n_A} \sum_{i=1}^{n_A} X_{A,i} \quad \text{and} \quad \hat{p}_B = \frac{1}{n_B} \sum_{j=1}^{n_B} X_{B,j}$$

Under the null hypothesis $H_0$ that $p_A = p_B = p$, we estimate the common success rate $p$ using the **pooled sample proportion** $\hat{p}$:
$$\hat{p} = \frac{\sum_{i=1}^{n_A} X_{A,i} + \sum_{j=1}^{n_B} X_{B,j}}{n_A + n_B} = \frac{n_A \hat{p}_A + n_B \hat{p}_B}{n_A + n_B}$$

### The Standard Error and Test Statistic
The standard error ($SE$) of the difference between the two proportions is:
$$SE = \sqrt{\hat{p}(1 - \hat{p}) \left( \frac{1}{n_A} + \frac{1}{n_B} \right)}$$

The **Z-test statistic** represents the standardized signal-to-noise ratio:
$$Z = \frac{\hat{p}_B - \hat{p}_A}{SE} = \frac{\hat{p}_B - \hat{p}_A}{\sqrt{\hat{p}(1 - \hat{p}) \left( \frac{1}{n_A} + \frac{1}{n_B} \right)}}$$

Under $H_0$, as sample sizes $n_A, n_B \to \infty$, $Z$ asymptotically follows a standard normal distribution: $Z \sim \mathcal{N}(0, 1)$. We reject $H_0$ at significance level $\alpha$ if $Z \ge z_\alpha$.

---

## 3. Illustrative Derivation

### Derivation of the Pooled Proportion Standard Error
We derive the standard error formula for the difference of two independent sample proportions under the null hypothesis assumption: $\sigma_D = \sqrt{p(1-p)\left(\frac{1}{n_A} + \frac{1}{n_B}\right)}$.

*Proof:*
Recall the variance of a Bernoulli random variable is $p(1-p)$.
1.  **Formulate variance of sample proportions:**
    The sample proportion $\hat{p}_A = \frac{1}{n_A} \sum_{i=1}^{n_A} X_{i}$ is the sample mean. The variance of a sample mean is $\text{Var}(X)/n$:
    $$\text{Var}(\hat{p}_A) = \frac{p_A(1-p_A)}{n_A} \quad \text{and} \quad \text{Var}(\hat{p}_B) = \frac{p_B(1-p_B)}{n_B}$$

2.  **Apply independence to the difference of proportions:**
    Because the user groups are randomly partitioned, $\hat{p}_A$ and $\hat{p}_B$ are independent, yielding a covariance of zero.
    The variance of their difference is:
    $$\text{Var}(\hat{p}_B - \hat{p}_A) = \text{Var}(\hat{p}_B + (-1)\hat{p}_A) = \text{Var}(\hat{p}_B) + (-1)^2 \text{Var}(\hat{p}_A) = \text{Var}(\hat{p}_B) + \text{Var}(\hat{p}_A)$$
    Substitute the variance formulas:
    $$\text{Var}(\hat{p}_B - \hat{p}_A) = \frac{p_B(1-p_B)}{n_B} + \frac{p_A(1-p_A)}{n_A}$$

3.  **Incorporate the Null Hypothesis assumption:**
    Under $H_0$, the true success rates are equal ($p_A = p_B = p$):
    $$\text{Var}(\hat{p}_B - \hat{p}_A) = \frac{p(1-p)}{n_B} + \frac{p(1-p)}{n_A} = p(1-p) \left( \frac{1}{n_A} + \frac{1}{n_B} \right)$$
    Since $p$ is unknown, we estimate it using the pooled sample proportion $\hat{p}$, which yields the standard error:
    $$SE = \sqrt{\hat{p}(1-\hat{p}) \left( \frac{1}{n_A} + \frac{1}{n_B} \right)} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Shoe Rack Organization System
Devotees exiting a temple must locate their shoes. Under the old pile method (Control A), 300 out of $n_A = 1000$ find their shoes quickly. Under a new rack method (Treatment B), 380 out of $n_B = 1000$ find their shoes quickly. Test if the rack method is superior at $\alpha = 0.05$.
1.  **Calculate sample proportions:**
    $$\hat{p}_A = \frac{300}{1000} = 0.30 \quad \text{and} \quad \hat{p}_B = \frac{380}{1000} = 0.38$$
2.  **Calculate pooled proportion:**
    $$\hat{p} = \frac{300 + 380}{1000 + 1000} = \frac{680}{2000} = 0.34$$
3.  **Compute the Standard Error:**
    $$SE = \sqrt{0.34(1 - 0.34) \left( \frac{1}{1000} + \frac{1}{1000} \right)} = \sqrt{0.34 \cdot 0.66 \cdot 0.002} = \sqrt{0.0004488} \approx 0.02118$$
4.  **Compute the Z-statistic:**
    $$Z = \frac{\hat{p}_B - \hat{p}_A}{SE} = \frac{0.38 - 0.30}{0.02118} \approx 3.777$$
For a right-tailed test at $\alpha = 0.05$, the critical value is $z_{0.05} = 1.645$. Since $Z \approx 3.777 > 1.645$, we reject $H_0$. The rack system significantly improves shoe retrieval speed.

### Example 2: Sweet Distribution Exit Satisfaction
We offer a small sweet at the exit to see if it increases customer satisfaction. In Group A (Control, no sweet), 100 out of $n_A = 200$ report high satisfaction. In Group B (Treatment, sweet), 110 out of $n_B = 200$ report high satisfaction. Test if the sweet increases satisfaction at $\alpha = 0.05$.
1.  **Calculate sample proportions:**
    $$\hat{p}_A = \frac{100}{200} = 0.50 \quad \text{and} \quad \hat{p}_B = \frac{110}{200} = 0.55$$
2.  **Calculate pooled proportion:**
    $$\hat{p} = \frac{100 + 110}{200 + 200} = \frac{210}{400} = 0.525$$
3.  **Compute the Standard Error:**
    $$SE = \sqrt{0.525(1-0.525) \left( \frac{2}{200} \right)} = \sqrt{0.525 \cdot 0.475 \cdot 0.01} = \sqrt{0.00249375} \approx 0.04994$$
4.  **Compute the Z-statistic:**
    $$Z = \frac{0.55 - 0.50}{0.04994} \approx 1.001$$
Since $Z \approx 1.001 < 1.645$, we fail to reject $H_0$. The difference is not statistically significant.

---

## 5. Applied ML Context

1.  **Hyperparameter Optimization Evaluation:** Comparing validation accuracies when training neural networks with Adam vs. SGD to verify if the accuracy difference is statistically significant.
2.  **Recommender System click optimization:** Routing different collaborative filtering recommendation models to different user segments to determine which model maximizes Click-Through Rates (CTR).
3.  **Model Canary Releases:** Deploying a new LLM version to a small, randomized subset of traffic and using Z-tests to monitor if there is a significant change in error rates or latency.
4.  **Feature Embeddings Validation:** Running tests on two regression models (with and without a new set of embeddings) to evaluate if the embeddings yield a significant drop in Mean Squared Error.
5.  **Multi-Armed Bandit Exploration:** Using A/B test statistics within reinforcement learning algorithms (like Thompson Sampling) to update policy selection probabilities.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the A/B testing workflow:
*   Show a splitting node dividing incoming users randomly:
    *   **Group A (Control):** Routed to baseline model version A, yielding conversion rate $\hat{p}_A$.
    *   **Group B (Treatment):** Routed to candidate model version B, yielding conversion rate $\hat{p}_B$.
*   Show both outputs feeding into a calculator node that computes the difference $\hat{p}_B - \hat{p}_A$.
*   Draw a normal distribution curve centered at $0$, representing the distribution of the difference under $H_0$.
*   Draw a vertical dashed line representing the critical value threshold $z_{crit}$. Shade the area to the right of this threshold as the rejection region.
*   Draw a marker showing where the observed difference lands, visually demonstrating if the treatment conversion lift is far enough from zero to reject the null hypothesis.
