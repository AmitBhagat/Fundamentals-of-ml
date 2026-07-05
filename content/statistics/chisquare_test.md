---
title: "The Chi-Square Test"
description: "Categorical hypothesis testing, Goodness-of-Fit, Tests of Independence, contingency tables, and expected frequency derivations."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Hypothesis Testing", "Types of Hypothesis", "Maximum Likelihood Estimation"]
---

<h1 align="center"> Chapter 64: The Chi-Square Test </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Categorical Data:** Nominal or ordinal discrete labels (e.g., product categories, user locations) rather than continuous values.
* **Degrees of Freedom ($df$):** The number of independent values that can vary in a statistical calculation.

</div>

## 1. Conceptual Hook

In machine learning, we often work with categorical variables—such as device types, user demographics, or class predictions. Unlike continuous features, we cannot describe categorical data using simple averages and variances. Instead, we analyze their frequency counts. How can we prove that the distribution of user clicks across different web page layouts matches our theoretical forecast? Or how do we determine if two categorical variables (like user subscription level and feature usage) are statistically independent or strongly related?

The mathematical framework designed to answer these questions is the **Chi-Square ($\chi^2$) test**. Instead of analyzing continuous means, it audits categorical frequency tables. The test compares the observed count in each category against the expected count under a null hypothesis. By calculating a normalized sum of these squared discrepancies, the Chi-Square test quantifies our "surprise." If this cumulative discrepancy exceeds a critical threshold, we reject the null hypothesis, proving that the observed frequency deviations represent a real underlying pattern rather than random sampling noise.

---

## 2. Formal Definition

Let $X$ be a categorical variable with $k$ mutually exclusive categories. We observe a sample of size $n$, yielding observed frequencies $\mathbf{O} = \{O_1, O_2, \dots, O_k\}$ such that $\sum_{i=1}^k O_i = n$.

### 1. Chi-Square Goodness-of-Fit Test
This test determines if a sample's distribution matches a hypothesized distribution $\mathbf{p} = \{p_1, p_2, \dots, p_k\}$, where $\sum_{i=1}^k p_i = 1$.
*   **Hypotheses:**
    *   $H_0$: The sample is drawn from the hypothesized multinomial distribution.
    *   $H_1$: The sample distribution deviates from the hypothesized distribution.
*   **Expected Frequencies:**
    $$E_i = n \cdot p_i \quad \forall i \in \{1, \dots, k\}$$
*   **Pearson's Chi-Square Test Statistic:**
    $$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$
    As $n \to \infty$, this statistic asymptotically follows a Chi-square distribution with $df = k - 1$ degrees of freedom.

### 2. Chi-Square Test of Independence
This test evaluates if two categorical variables, $A$ (with $r$ levels) and $B$ (with $c$ levels), are independent. The observed counts are arranged in an $r \times c$ contingency table with cells $O_{ij}$.
*   **Hypotheses:**
    *   $H_0$: Variable $A$ and Variable $B$ are independent.
    *   $H_1$: Variable $A$ and Variable $B$ are dependent.
*   **Expected Frequencies:** Under the independence assumption:
    $$E_{ij} = \frac{R_i \cdot C_j}{n}$$
    where $R_i = \sum_{j=1}^c O_{ij}$ is the row $i$ total, and $C_j = \sum_{i=1}^r O_{ij}$ is the column $j$ total.
*   **Test Statistic:**
    $$\chi^2 = \sum_{i=1}^{r} \sum_{j=1}^{c} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$
    Under $H_0$, this statistic asymptotically follows a Chi-square distribution with $df = (r - 1)(c - 1)$ degrees of freedom. We reject $H_0$ at significance level $\alpha$ if $\chi^2 \ge \chi^2_{\alpha, df}$.

---

## 3. Illustrative Derivation

### Derivation of the Expected Frequency Formula in Contingency Tables
We prove how the independence hypothesis $H_0$ algebraically leads to the cell expected value formula $E_{ij} = \frac{R_i \cdot C_j}{n}$.

*Proof:*
Let $n$ be the total sample size. Let $P(A_i)$ be the probability of an observation falling in row $i$, and $P(B_j)$ be the probability of falling in column $j$. Let $P(A_i \cap B_j)$ be the joint probability.
1.  **Formulate the independence assumption:**
    Under the null hypothesis $H_0$ of independence:
    $$P(A_i \cap B_j) = P(A_i) \cdot P(B_j)$$
    Therefore, the expected count $E_{ij}$ for cell $(i, j)$ is:
    $$E_{ij} = n \cdot P(A_i \cap B_j) = n \cdot P(A_i) \cdot P(B_j)$$

2.  **Estimate marginal probabilities from observed marginal counts:**
    Since the true population marginal probabilities are unknown, we calculate their maximum likelihood estimators (MLEs) from the contingency table's row and column totals:
    $$\hat{P}(A_i) = \frac{R_i}{n} \quad \text{and} \quad \hat{P}(B_j) = \frac{C_j}{n}$$
    where $R_i = \sum_{j=1}^c O_{ij}$ is the observed total for row $i$, and $C_j = \sum_{i=1}^r O_{ij}$ is the observed total for column $j$.

3.  **Calculate the expected cell counts:**
    Substitute the estimators back into the expectation formula:
    $$E_{ij} = n \cdot \hat{P}(A_i) \cdot \hat{P}(B_j) = n \cdot \left( \frac{R_i}{n} \right) \cdot \left( \frac{C_j}{n} \right)$$
    Simplifying by canceling $n$:
    $$E_{ij} = \frac{R_i \cdot C_j}{n} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Quote Distribution Audit (Goodness-of-Fit)
Neighbors sample premium quotes across three insurance providers ($k=3$). Based on baseline market data, we expect quotes to be distributed evenly ($p_i = 1/3$). Out of $n=300$ quotes, we observe Provider A (120), Provider B (90), and Provider C (90). Test $H_0$ at $\alpha = 0.05$.
1.  **Calculate expected frequencies:**
    $$E_A = 300 \cdot \frac{1}{3} = 100, \quad E_B = 100, \quad E_C = 100$$
2.  **Compute the $\chi^2$ statistic:**
    $$\chi^2 = \sum_{i=1}^3 \frac{(O_i - E_i)^2}{E_i} = \frac{(120-100)^2}{100} + \frac{(90-100)^2}{100} + \frac{(90-100)^2}{100} = \frac{400}{100} + \frac{100}{100} + \frac{100}{100} = 4 + 1 + 1 = 6.0$$
3.  **Evaluate:**
    For $df = k-1 = 2$ and $\alpha = 0.05$, the critical value from the Chi-square table is $\chi^2_{crit} = 5.991$. Since $\chi^2 = 6.0 > 5.991$, we reject $H_0$. The market distribution deviates significantly from an even share.

### Example 2: Vehicle Value vs. Claims (Test of Independence)
We track $n=200$ policies to determine if Insured Declared Value (IDV) (High vs. Low) is independent of whether a claim was filed:

| Category | Claim filed | No Claim filed | Row Total |
| :--- | :---: | :---: | :---: |
| **High IDV** | 40 | 60 | $R_1 = 100$ |
| **Low IDV** | 20 | 80 | $R_2 = 100$ |
| **Column Total** | $C_1 = 60$ | $C_2 = 140$ | $n = 200$ |

Test if IDV and Claim status are independent at $\alpha = 0.05$.
1.  **Calculate expected frequencies:**
    *   $E_{11} = \frac{R_1 \cdot C_1}{n} = \frac{100 \cdot 60}{200} = 30$, $\quad E_{12} = \frac{100 \cdot 140}{200} = 70$
    *   $E_{21} = \frac{100 \cdot 60}{200} = 30$, $\quad E_{22} = \frac{100 \cdot 140}{200} = 70$
2.  **Compute the $\chi^2$ statistic:**
    $$\chi^2 = \frac{(40-30)^2}{30} + \frac{(60-70)^2}{70} + \frac{(20-30)^2}{30} + \frac{(80-70)^2}{70} = \frac{100}{30} + \frac{100}{70} + \frac{100}{30} + \frac{100}{70} \approx 3.333 + 1.429 + 3.333 + 1.429 = 9.524$$
3.  **Evaluate:**
    For $df = (r-1)(c-1) = (2-1)(2-1) = 1$ and $\alpha = 0.05$, the critical value is $\chi^2_{crit} = 3.841$. Since $\chi^2 \approx 9.524 > 3.841$, we reject $H_0$. Vehicle value and claim occurrence are dependent.

---

## 5. Applied ML Context

1.  **Categorical Feature Selection:** In classification pipelines, we calculate the $\chi^2$ statistic between each categorical feature and the target label. Features that exhibit statistical independence ($p > 0.05$) are pruned to reduce dimension.
2.  **Feature Discretization Binning:** When converting continuous variables into discrete categories, we use a Chi-Square merger algorithm (like ChiMerge) to ensure that adjacent bins maintain a strong statistical relationship with the target variable.
3.  **Classifier Probability Calibration Checks:** We divide our test set into confidence bins (e.g. $[0.0, 0.1], [0.1, 0.2], \dots$). We run a Goodness-of-Fit test comparing observed class frequencies to predicted model probabilities to verify calibration.
4.  **Production Data Drift Alerts:** MLOps pipelines monitor categorical feature inputs. If the observed frequencies of categories in production drift from the training baseline, a Chi-Square test triggers a covariate shift retraining alert.
5.  **Text Token Relevance in NLP:** In bag-of-words text classifiers, a Chi-Square test is used to measure the association between the presence of specific word tokens and the target classes, selecting the most informative vocabulary terms.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here showing the Chi-Square distribution curves:
*   Draw probability density curves for the Chi-Square distribution for different degrees of freedom (e.g. $df = 1, 2, 4, 8$).
*   Highlight how the curve is highly right-skewed when $df$ is low (especially for $df=1, 2$) and becomes more symmetric and bell-shaped as $df$ increases, illustrating the Central Limit Theorem.
*   On the curve for $df=2$, mark the critical value boundary of $\chi^2_{crit} = 5.991$ with a vertical dashed line.
*   Shade the right tail area corresponding to the rejection region ($\alpha = 0.05$).
*   Draw a clear marker indicating our calculated test statistic $\chi^2 = 6.0$, showing it landing just inside the rejection tail, visually explaining how the test evaluates the significance of observed deviations.
