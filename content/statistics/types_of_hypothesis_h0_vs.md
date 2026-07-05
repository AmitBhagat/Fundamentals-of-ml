---
title: "Types of Hypothesis"
description: "Statistical hypotheses, simple and composite formulations, null and alternative statements, Neyman-Pearson lemma, and likelihood ratios."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Mean and Expectation", "Variance", "Hypothesis Testing"]
---

<h1 align="center"> Chapter 74: Types of Hypothesis </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Hypothesis Testing Foundations:** Understanding the goal of comparing sample statistics against population claims.
* **Likelihood Functions:** Knowing how to express the joint density of observations as a function of parameters: $L(\theta \mid \mathbf{x})$.

</div>

## 1. Conceptual Hook

In machine learning, we don't just "guess" that a new model is better. We make a mathematical claim and systematically try to prove ourselves wrong. This comparative process requires establishing two competing statements: the **Null Hypothesis ($H_0$)** and the **Alternative Hypothesis ($H_1$)**.

Think of this as putting a new model on trial. The **Null Hypothesis** is the "innocent until proven guilty" stance. It represents the status quo—asserting that our new model is no different from the baseline, and any observed improvement is merely a random fluke. The **Alternative Hypothesis** is the challenger claim, asserting that the new model has a real, mathematically significant effect. By formally defining these hypotheses, we establish the exact mathematical rules required to reject the status quo and justify deploying a new algorithm.

---

## 2. Formal Definition

A **statistical hypothesis** is a statement about the probability distribution of a random variable, typically parameterized by $\theta \in \Theta$.

### Simple vs. Composite Hypotheses
*   **Simple Hypothesis:** A hypothesis that completely specifies the probability distribution of the data. For example, if $X \sim \mathcal{N}(\mu, 1)$, then:
    $$H: \mu = \mu_0$$
    is a simple hypothesis because it fixes the parameter to a single value, completely defining the density function.
*   **Composite Hypothesis:** A hypothesis that does not completely specify the distribution. For example:
    $$H: \mu > \mu_0 \quad \text{or} \quad H: \mu \neq \mu_0$$
    are composite hypotheses because the parameter can take any value within a range, leaving the exact density function unspecified.

### Null and Alternative Hypotheses
To perform a statistical test, we formulate two competing hypotheses about a parameter $\theta$:
1.  **Null Hypothesis ($H_0$):** The default statement of no effect or no difference, typically formulated as a simple hypothesis:
    $$H_0: \theta = \theta_0$$
2.  **Alternative Hypothesis ($H_1$ or $H_a$):** The statement that contradicts the null hypothesis, representing the presence of an effect. It is formulated in one of three ways:
    *   **Two-Tailed (Symmetric Composite):** Used when we search for deviations in either direction:
        $$H_1: \theta \neq \theta_0$$
    *   **Right-Tailed (One-Sided Composite):** Used when we look for a significant increase:
        $$H_1: \theta > \theta_0$$
    *   **Left-Tailed (One-Sided Composite):** Used when we look for a significant decrease:
        $$H_1: \theta < \theta_0$$

---

## 3. Illustrative Derivation

### Derivation of the Most Powerful Test (Neyman-Pearson Lemma)
We prove how the structural distinction between simple and composite hypotheses leads to the optimal decision rule. The **Neyman-Pearson Lemma** states that for testing a simple null $H_0: \theta = \theta_0$ against a simple alternative $H_1: \theta = \theta_1$, the test that maximizes the power (probability of rejecting $H_0$ when $H_1$ is true) for a given significance level $\alpha$ is the likelihood ratio test.

*Proof:*
Let $\mathbf{x} = \{x_1, \dots, x_n\}$ be the observed sample. The likelihood function under parameter $\theta$ is:
$$L(\theta \mid \mathbf{x}) = \prod_{i=1}^{n} f(x_i; \theta)$$

1.  **Define the Likelihood Ratio $\Lambda(\mathbf{x})$:**
    $$\Lambda(\mathbf{x}) = \frac{L(\theta_0 \mid \mathbf{x})}{L(\theta_1 \mid \mathbf{x})}$$
    This ratio measures the relative plausibility of the data under $H_0$ versus $H_1$.
2.  **Formulate the Rejection Region $R$:**
    The lemma asserts that the optimal critical region $R$ is defined by:
    $$R = \{ \mathbf{x} \in \mathbb{R}^n : \Lambda(\mathbf{x}) \le k \}$$
    where $k$ is a constant chosen to satisfy the significance level constraint:
    $$P(\mathbf{X} \in R \mid H_0) = \alpha$$
3.  **Prove Optimality (Maximized Power):**
    Let $C$ be any other critical region with the same significance level: $P(\mathbf{X} \in C \mid H_0) \le \alpha$. We want to show that the power of $R$ is greater than or equal to the power of $C$:
    $$P(\mathbf{X} \in R \mid H_1) \ge P(\mathbf{X} \in C \mid H_1)$$
    
    We write:
    $$\int_R L(\theta_1 \mid \mathbf{x}) d\mathbf{x} - \int_C L(\theta_1 \mid \mathbf{x}) d\mathbf{x} = \int_{R \setminus C} L(\theta_1 \mid \mathbf{x}) d\mathbf{x} - \int_{C \setminus R} L(\theta_1 \mid \mathbf{x}) d\mathbf{x}$$
    *   For any $\mathbf{x} \in R \setminus C$, since $\mathbf{x} \in R$, we have $L(\theta_0 \mid \mathbf{x}) \le k L(\theta_1 \mid \mathbf{x}) \implies L(\theta_1 \mid \mathbf{x}) \ge \frac{1}{k} L(\theta_0 \mid \mathbf{x})$.
    *   For any $\mathbf{x} \in C \setminus R$, since $\mathbf{x} \notin R$, we have $L(\theta_0 \mid \mathbf{x}) > k L(\theta_1 \mid \mathbf{x}) \implies L(\theta_1 \mid \mathbf{x}) < \frac{1}{k} L(\theta_0 \mid \mathbf{x})$.
    
    Substitute these inequalities:
    $$\int_{R \setminus C} L(\theta_1 \mid \mathbf{x}) d\mathbf{x} - \int_{C \setminus R} L(\theta_1 \mid \mathbf{x}) d\mathbf{x} \ge \frac{1}{k} \int_{R \setminus C} L(\theta_0 \mid \mathbf{x}) d\mathbf{x} - \frac{1}{k} \int_{C \setminus R} L(\theta_0 \mid \mathbf{x}) d\mathbf{x}$$
    Combine the integrals back:
    $$\ge \frac{1}{k} \left[ \int_R L(\theta_0 \mid \mathbf{x}) d\mathbf{x} - \int_C L(\theta_0 \mid \mathbf{x}) d\mathbf{x} \right] = \frac{1}{k} \left[ P(\mathbf{X} \in R \mid H_0) - P(\mathbf{X} \in C \mid H_0) \right]$$
    Since $P(\mathbf{X} \in R \mid H_0) = \alpha$ and $P(\mathbf{X} \in C \mid H_0) \le \alpha$, the bracketed term is non-negative:
    $$P(\mathbf{X} \in R \mid H_1) - P(\mathbf{X} \in C \mid H_1) \ge 0 \implies P(\mathbf{X} \in R \mid H_1) \ge P(\mathbf{X} \in C \mid H_1) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: One-Tailed Shagun Budget Check
A community average wedding gift is $\mu_0 = 100$. You suspect a specific group of friends spends less than this average. Formulate the hypotheses and test using a sample of $n=25$ gifts with mean $\bar{x} = 92$ and standard deviation $s = 15$ at significance level $\alpha = 0.05$.
1.  **Formulate the hypotheses:**
    $$H_0: \mu = 100 \quad \text{vs.} \quad H_1: \mu < 100 \quad (\text{Left-Tailed})$$
2.  **Calculate the t-statistic:**
    $$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}} = \frac{92 - 100}{15 / \sqrt{25}} = \frac{-8}{3} \approx -2.667$$
3.  **Determine the rejection boundary:**
    For a left-tailed test with degrees of freedom $df = 24$ and $\alpha = 0.05$, the critical value is $t_{crit} = -1.711$.
4.  **Evaluate:**
    Since $t \approx -2.667 < -1.711$, the statistic lies in the rejection region. We reject $H_0$ and conclude the group spends significantly less than the community average.

### Example 2: Two-Tailed Store Price Audit
A national online retailer claims the average price of a gift category is $\mu_0 = 50$. You suspect a local 24/7 store's pricing differs. Formulate the hypotheses and test using a sample of $n=16$ gifts with mean $\bar{x} = 58$ and standard deviation $s = 12$ at $\alpha = 0.05$.
1.  **Formulate the hypotheses:**
    $$H_0: \mu = 50 \quad \text{vs.} \quad H_1: \mu \neq 50 \quad (\text{Two-Tailed})$$
2.  **Calculate the t-statistic:**
    $$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}} = \frac{58 - 50}{12 / \sqrt{16}} = \frac{8}{3} \approx 2.667$$
3.  **Determine the rejection boundary:**
    For a two-tailed test with $df = 15$ and $\alpha = 0.05$, the critical values are $\pm t_{crit} = \pm 2.131$.
4.  **Evaluate:**
    Since $|t| \approx 2.667 > 2.131$, we reject $H_0$. The local store's average price is significantly different from the online baseline.

---

## 5. Applied ML Context

1.  **A/B Testing for Model Deployment:** When comparing a challenger model to a baseline model, the null hypothesis $H_0$ asserts that the difference in mean accuracy is zero ($\Delta\mu = 0$), while $H_1$ asserts that the challenger is superior ($\Delta\mu > 0$).
2.  **Feature Significance in Regression:** In linear models, for each feature weight $w_j$, we test $H_0: w_j = 0$ against $H_1: w_j \neq 0$. If we fail to reject $H_0$ for a feature, it is flagged as non-significant and pruned.
3.  **Covariate Shift Detection:** We monitor incoming feature data streams. The null hypothesis $H_0$ states that the distribution of incoming features matches the training distribution. If $H_0$ is rejected, it flags data drift.
4.  **Generative Adversarial Network Evaluation:** Evaluating whether the generated data distribution matches the real data distribution. The null hypothesis $H_0$ assumes the generated and real samples are drawn from the same distribution.
5.  **Hyperparameter Search Validation:** When tuning learning rates or batch sizes, we set $H_0$ as the statement that the change in hyperparameters yields no decrease in validation loss, rejecting it only when a significant loss reduction is observed.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here comparing one-tailed and two-tailed rejection boundaries:
*   Show two side-by-side Normal distribution plots:
    1.  **Plot A (One-Tailed Test):** Draw a normal curve. Shade only a single region in the right tail representing the significance level $\alpha$. Mark the boundary as $z_{crit}$. This visualizes a directional alternative hypothesis like $H_1: \theta > \theta_0$.
    2.  **Plot B (Two-Tailed Test):** Draw a normal curve. Shade two symmetric regions in both the left and right tails, each representing an area of $\alpha/2$ (together summing to $\alpha$). Mark the boundaries as $-z_{crit}$ and $+z_{crit}$. This visualizes a non-directional alternative hypothesis like $H_1: \theta \neq \theta_0$.
*   Add a caption explaining how the direction of the alternative hypothesis ($H_1$) determines whether we search for deviations in a single tail or split our rejection budget across both tails.
