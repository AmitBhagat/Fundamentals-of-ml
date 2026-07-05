---
title: "Type I and Type II Errors"
description: "Statistical decisions, Type I vs. Type II errors, confusion matrices, statistical power, and decision threshold proofs."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Conditional Probability", "Hypothesis Testing", "Types of Hypothesis"]
---

<h1 align="center"> Chapter 73: Type I and Type II Errors </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Null Hypothesis ($H_0$):** The status quo assumption that there is no effect.
* **Alternative Hypothesis ($H_1$):** The active claim of a significant effect.

</div>

## 1. Conceptual Hook

In machine learning, no model is perfect. When we make decisions based on statistical thresholds—whether classifying a transaction as fraudulent or predicting whether a lithium-ion battery is fully charged—we are always choosing between two specific types of failure: **false alarms** and **missed detections**.

In statistics, these mistakes are categorized as **Type I** and **Type II** errors:
*   A **Type I error** is a False Positive (false alarm). It occurs when we reject the null hypothesis, claiming a significant discovery, when in reality no effect exists.
*   A **Type II error** is a False Negative (missed detection). It occurs when we fail to reject the null hypothesis, failing to notice a real effect.
Balancing these errors is a fundamental zero-sum game of ML system design. Lowering the rate of false alarms systematically increases the rate of missed detections, forcing engineers to decide which type of error their business logic can tolerate.

---

## 2. Formal Definition

Let $H_0$ be the null hypothesis and $H_1$ be the alternative hypothesis. Let $R$ be the rejection region for our test statistic $T(\mathbf{X})$.

### Type I Error ($\alpha$)
A Type I error occurs when the null hypothesis is rejected when it is actually true. The probability of committing a Type I error is the significance level $\alpha$:
$$\alpha = P(\text{Reject } H_0 \mid H_0 \text{ is true}) = P(T(\mathbf{X}) \in R \mid H_0 \text{ is true})$$

### Type II Error ($\beta$)
A Type II error occurs when the null hypothesis is not rejected when the alternative hypothesis is actually true. The probability of committing a Type II error is denoted $\beta$:
$$\beta = P(\text{Fail to Reject } H_0 \mid H_1 \text{ is true}) = P(T(\mathbf{X}) \notin R \mid H_1 \text{ is true})$$

### Statistical Power ($1 - \beta$)
The statistical power of a test is the probability of correctly rejecting the null hypothesis when the alternative is true (True Positive rate):
$$\text{Power} = 1 - \beta = P(\text{Reject } H_0 \mid H_1 \text{ is true}) = P(T(\mathbf{X}) \in R \mid H_1 \text{ is true})$$

### Decision Confusion Matrix
These outcomes are organized into a $2 \times 2$ matrix mapping decision states against ground truth:

| True State | Fail to Reject $H_0$ (Predict Negative) | Reject $H_0$ (Predict Positive) |
| :--- | :---: | :---: |
| **$H_0$ is True** (Actual Negative) | Correct Decision ($1 - \alpha$) | **Type I Error ($\alpha$, False Positive)** |
| **$H_1$ is True** (Actual Positive) | **Type II Error ($\beta$, False Negative)** | Correct Decision ($1 - \beta$, Power, True Positive) |

---

## 3. Illustrative Derivation

### Proof of the Threshold Trade-Off (The Zero-Sum Game of Errors)
We prove that for a fixed sample size $n$, any adjustment to the decision threshold that decreases the probability of a Type I error ($\alpha$) must systematically increase the probability of a Type II error ($\beta$).

*Proof:*
Let $X$ be our test statistic. We evaluate two simple hypotheses:
*   Under $H_0$: $X \sim \mathcal{N}(\mu_0, \sigma^2)$
*   Under $H_1$: $X \sim \mathcal{N}(\mu_1, \sigma^2)$ where $\mu_1 > \mu_0$.

We define a decision rule where we reject $H_0$ if the observed statistic exceeds a threshold $x_c$:
$$R = \{x \in \mathbb{R} : x > x_c\}$$

1.  **Express $\alpha$ as a function of the threshold $x_c$:**
    $$\alpha(x_c) = P(X > x_c \mid H_0) = P\left( \frac{X - \mu_0}{\sigma} > \frac{x_c - \mu_0}{\sigma} \right) = 1 - \Phi\left( \frac{x_c - \mu_0}{\sigma} \right)$$
    where $\Phi(z)$ is the standard normal Cumulative Distribution Function.

2.  **Express $\beta$ as a function of the threshold $x_c$:**
    $$\beta(x_c) = P(X \le x_c \mid H_1) = P\left( \frac{X - \mu_1}{\sigma} \le \frac{x_c - \mu_1}{\sigma} \right) = \Phi\left( \frac{x_c - \mu_1}{\sigma} \right)$$

3.  **Evaluate the derivatives with respect to the threshold $x_c$:**
    By the Leibniz integral rule, the derivative of $\Phi(g(x))$ is $\phi(g(x)) \cdot g'(x)$, where $\phi(z)$ is the normal Probability Density Function (which is strictly positive for all $z \in \mathbb{R}$):
    $$\frac{d\alpha}{dx_c} = -\frac{1}{\sigma} \phi\left( \frac{x_c - \mu_0}{\sigma} \right) < 0$$
    This negative derivative proves that increasing the threshold $x_c$ strictly decreases the Type I error rate $\alpha$.
    
    $$\frac{d\beta}{dx_c} = \frac{1}{\sigma} \phi\left( \frac{x_c - \mu_1}{\sigma} \right) > 0$$
    This positive derivative proves that increasing the threshold $x_c$ strictly increases the Type II error rate $\beta$.
    
Since $\frac{d\alpha}{dx_c} < 0$ and $\frac{d\beta}{dx_c} > 0$ for all real-valued thresholds $x_c$, any adjustment to the threshold that lowers one error rate must increase the other. The only way to simultaneously reduce both $\alpha$ and $\beta$ is to increase the sample size $n$, which narrows the variance $\sigma^2 = \frac{\sigma_0^2}{n}$ of the distributions. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Public Charging Dock Tracker
An app predicts whether charging docks are active ($\hat{Y}=1$, representing rejecting the null hypothesis that the dock is broken). In 250 predictions, the results are:
*   Ground Truth: 185 docks are active ($H_1$), 65 docks are broken ($H_0$).
*   The app flags 200 docks as active ($\text{Reject } H_0$). Of these, 180 were active ($TP$), but 20 were broken ($FP$).
*   Of the 50 docks flagged as broken ($\text{Fail to Reject } H_0$), 45 were broken ($TN$), but 5 were active ($FN$).
Calculate the Type I and Type II error rates.
1.  **Compute the Type I error rate ($\alpha$):**
    $$\alpha = \frac{FP}{FP + TN} = \frac{20}{20 + 45} = \frac{20}{65} \approx 0.3077 \quad (30.77\%)$$
2.  **Compute the Type II error rate ($\beta$):**
    $$\beta = \frac{FN}{FN + TP} = \frac{5}{5 + 180} = \frac{5}{185} \approx 0.0270 \quad (2.70\%)$$

### Example 2: Security Intrusion Alarm
A security classifier monitors server access. In $1000$ simulation runs:
*   Ground Truth: 100 actual intrusions ($H_1$), 900 safe events ($H_0$).
*   The system flags 150 events as intrusions ($\text{Reject } H_0$). Of these, 90 were actual intrusions ($TP$) and 60 were false alarms ($FP$).
*   Of the remaining 850 unflagged events ($\text{Fail to Reject } H_0$), 10 were actual intrusions ($FN$) and 840 were safe events ($TN$).
Calculate the Type I and Type II error rates, and the statistical power.
1.  **Compute the Type I error rate ($\alpha$):**
    $$\alpha = \frac{FP}{FP + TN} = \frac{60}{60 + 840} = \frac{60}{900} \approx 0.0667 \quad (6.67\%)$$
2.  **Compute the Type II error rate ($\beta$):**
    $$\beta = \frac{FN}{FN + TP} = \frac{10}{10 + 90} = \frac{10}{100} = 0.10 \quad (10.0\%)$$
3.  **Compute the Statistical Power ($1 - \beta$):**
    $$\text{Power} = 1 - 0.10 = 0.90 \quad (90.0\%)$$

---

## 5. Applied ML Context

1.  **Medical Diagnostic Classification:** In detecting aggressive diseases from scans, Type II errors (False Negatives) are life-threatening, while Type I errors (False Positives) result in temporary anxiety. Model thresholds are calibrated to prioritize high Recall ($1-\beta$) to minimize missed detections.
2.  **Spam Filtering:** In email systems, a Type I error (False Positive) means an important business email is sent to the spam folder. Spam classifiers prioritize high Precision to ensure $\alpha$ is kept near zero.
3.  **Credit Card Fraud Detection:** Banks monitor transactions. A Type I error results in a declined card at a register (annoying to the user), while a Type II error results in direct financial loss. The threshold is tuned based on cost-benefit metrics.
4.  **Autonomous Vehicle Collision Avoidance:** A vehicle must decide if a road shadow is an obstacle. A False Positive (Type I) causes phantom braking, which risks rear-end collisions from behind, while a False Negative (Type II) results in a forward collision.
5.  **Biometric Authentication Access:** In facial recognition security systems, the False Acceptance Rate (FAR), which represents the Type I error rate ($\alpha$), must be kept near zero to prevent unauthorized users from gaining access.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating overlapping distributions and error regions:
*   Draw two overlapping Normal curves along a single horizontal axis:
    1.  **Left Curve:** The distribution of the test statistic under the null hypothesis $H_0$.
    2.  **Right Curve:** The distribution of the test statistic under the alternative hypothesis $H_1$.
*   Draw a bold vertical line slicing through the overlap, representing the decision threshold $x_c$.
*   Shade the area under the left curve ($H_0$) that lies to the right of $x_c$. Label this shaded region as the **Type I Error ($\alpha$, False Positive)** region.
*   Shade the area under the right curve ($H_1$) that lies to the left of $x_c$. Label this shaded region as the **Type II Error ($\beta$, False Negative)** region.
*   Use this visualization to show that moving the threshold line $x_c$ left or right dynamically trades off the two shaded areas, visually demonstrating the zero-sum nature of decision errors.
