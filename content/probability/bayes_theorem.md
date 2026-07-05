---
title: "Bayes Theorem"
description: "Prior beliefs, likelihood matching, posterior updates, partition normalization, and Bayesian ML applications."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Conditional Probability", "Law of Total Probability"]
---

<h1 align="center"> Chapter 41: Bayes Theorem </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Conditional Probability:** Knowing the formula $P(A|B) = \frac{P(A \cap B)}{P(B)}$.
* **Law of Total Probability:** Understanding how to decompose global probabilities into partitioned sums.

</div>

## 1. Conceptual Hook

In machine learning, we constantly make decisions under uncertainty. If we evaluate predictions using only new, raw data in isolation, we ignore historical context. For example, if a model detects a rare fraud signal, it might trigger false alarms because it overlooks how rare fraud actually is. The mathematical framework that integrates historical context with new evidence is **Bayes' Theorem**.

Bayes' Theorem is the ultimate engine for belief updating. It takes our baseline, historical assumption (the **prior**), multiplies it by the probability that our new data would occur under that assumption (the **likelihood**), and outputs an updated, context-aware probability (the **posterior**). It is the mathematical foundation of Bayesian machine learning, self-driving sensor fusion, and optimal hyperparameter optimization, allowing systems to systematically refine their knowledge as new observations arrive.

---

## 2. Formal Definition

Let $(\Omega, \mathcal{F}, P)$ be a probability space. Let $A$ and $B$ be two events in $\mathcal{F}$ such that the probability of $B$ is strictly positive ($P(B) > 0$). **Bayes' Theorem** states:
$$P(A|B) = \frac{P(B|A) P(A)}{P(B)}$$

where:
*   **$P(A|B)$ (Posterior Probability):** The updated probability of event $A$ occurring given that event $B$ has been observed.
*   **$P(B|A)$ (Likelihood):** The probability of observing event $B$ assuming that event $A$ is true.
*   **$P(A)$ (Prior Probability):** The baseline probability of event $A$ before observing the new evidence $B$.
*   **$P(B)$ (Evidence / Marginal Probability):** The total probability of observing event $B$ across all possible scenarios.

### Expanded Partition Form
If $\{A_1, A_2, \dots, A_n\}$ is a partition of the sample space $\Omega$, then by applying the Law of Total Probability to the denominator $P(B)$, Bayes' Theorem can be expressed in its expanded form:
$$P(A_i | B) = \frac{P(B | A_i) P(A_i)}{\sum_{j=1}^{n} P(B | A_j) P(A_j)}$$

---

## 3. Illustrative Derivation

### Derivation of Bayes' Theorem
We derive Bayes' Theorem directly from the definition of conditional probability.

*Proof:*
Let $A$ and $B$ be two events in the event space $\mathcal{F}$ with $P(A) > 0$ and $P(B) > 0$.
1.  Write the conditional probability of event $A$ given event $B$:
    $$P(A|B) = \frac{P(A \cap B)}{P(B)}$$
2.  Write the conditional probability of event $B$ given event $A$:
    $$P(B|A) = \frac{P(A \cap B)}{P(A)}$$
3.  Isolate the joint probability term $P(A \cap B)$ in both equations:
    From step 1:
    $$P(A \cap B) = P(A|B) P(B)$$
    From step 2:
    $$P(A \cap B) = P(B|A) P(A)$$
4.  Since both expressions describe the same joint event $A \cap B$, set them equal to each other:
    $$P(A|B) P(B) = P(B|A) P(A)$$
5.  Divide both sides by the non-zero marginal probability $P(B)$ to solve for the posterior probability $P(A|B)$:
    $$P(A|B) = \frac{P(B|A) P(A)}{P(B)} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Zipper Repair Diagnostics
A tailor knows from historical records that $70\%$ of snagged zippers just need wax ($A_{wax}$), while $30\%$ are actually bent ($A_{bent}$).
*   If a zipper only needs wax, the likelihood of a hard snag ($B$) is $P(B|A_{wax}) = 0.20$.
*   If a zipper is bent, the likelihood of a hard snag ($B$) is $P(B|A_{bent}) = 0.90$.
The tailor encounters a zipper that has hard snagged. What is the posterior probability that it only needs wax?
1.  **Formulate the expanded Bayes' Theorem:**
    $$P(A_{wax}|B) = \frac{P(B|A_{wax})P(A_{wax})}{P(B|A_{wax})P(A_{wax}) + P(B|A_{bent})P(A_{bent})}$$
2.  **Substitute values:**
    $$P(A_{wax}|B) = \frac{(0.20)(0.70)}{(0.20)(0.70) + (0.90)(0.30)} = \frac{0.14}{0.14 + 0.27} = \frac{0.14}{0.41} \approx 0.3415$$
Although the prior probability of needing only wax was high ($70\%$), the severe snag drops the posterior probability to $34.15\%$.

### Example 2: Alignment Test Gauge
A test gauge checks alignment on a luxury coat. The prior probability of a coat being misaligned is $P(A) = 0.05$. The gauge is $95\%$ accurate (sensitivity $P(B|A) = 0.95$) and has a $2\%$ false positive rate ($P(B|A^c) = 0.02$). The gauge reports a misalignment. Find the posterior probability of misalignment.
1.  **Formulate the expanded Bayes' Theorem:**
    $$P(A|B) = \frac{P(B|A)P(A)}{P(B|A)P(A) + P(B|A^c)P(A^c)}$$
2.  **Substitute values (since $P(A^c) = 1 - 0.05 = 0.95$):**
    $$P(A|B) = \frac{(0.95)(0.05)}{(0.95)(0.05) + (0.02)(0.95)} = \frac{0.0475}{0.0475 + 0.0190} = \frac{0.0475}{0.0665} \approx 0.7143$$
Despite the $95\%$ accuracy, because misalignment is rare, a positive reading yields only a $71.43\%$ posterior probability of actual misalignment.

---

## 5. Applied ML Context

1.  **Naive Bayes Classifier:** Used in spam filtering. The model calculates the posterior probability of an email being spam given the words present: $P(\text{Spam} \mid \text{words}) \propto P(\text{Spam}) \prod_i P(\text{word}_i \mid \text{Spam})$, assuming word frequencies are conditionally independent.
2.  **Bayesian Neural Networks (BNNs):** Instead of calculating single-point weights, BNNs estimate weight distributions conditional on the observed training data $D$ using Bayes' Theorem: $P(W|D) = \frac{P(D|W)P(W)}{P(D)}$, enabling uncertainty quantification.
3.  **Latent Dirichlet Allocation (Topic Modeling):** LDA uses Bayesian inference (via Gibbs sampling or variational Bayes) to estimate the posterior distribution of hidden topics under documents.
4.  **Bayesian Optimization:** In hyperparameter tuning, Bayesian optimization fits a Gaussian Process prior over the hyperparameter loss space, and updates the posterior with each experiment to choose the next optimal hyperparameter combination.
5.  **Sensor Fusion (Kalman Filtering):** Autonomous vehicles track their position by combining a transition motion model (prior prediction) with new, noisy sensor readings (likelihood updates) via recursive Bayesian estimation.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the flow of a Bayesian update:
*   Draw a flowchart showing three sequential stages:
    1.  **Prior Belief $P(Hypothesis)$:** Represented as a broad, flat probability distribution, indicating high initial uncertainty.
    2.  **Likelihood Filter $P(Data \mid Hypothesis)$:** Represented as a narrow funnel that filters out hypotheses that do not align with the new data.
    3.  **Posterior Belief $P(Hypothesis \mid Data)$:** Represented as a tall, narrow peak centered at the updated parameters, indicating increased confidence.
*   Draw an equation arrow showing:
    $$\text{Posterior} \propto \text{Prior} \times \text{Likelihood}$$
*   Use this diagram to visually demonstrate how Bayes' Theorem acts as an information filter, focusing a broad prior distribution into a sharp posterior distribution using empirical evidence.
