---
title: "Conditional Probability"
description: "Updated sample spaces, conditional probability definitions, conditional independence, and the Law of Total Probability."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Random Variables", "Independence"]
---

<h1 align="center"> Chapter 43: Conditional Probability </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Event Spaces:** Understanding how events are defined as subsets of the sample space $\Omega$.
* **Intersection ($A \cap B$):** Representing outcomes where both events occur simultaneously.

</div>

## 1. Conceptual Hook

In machine learning, we almost never make predictions in a vacuum. We do not predict whether a user will click an ad without looking at their browsing history, nor do we diagnose a patient without analyzing their symptoms. When we receive new data, our understanding of the world changes. The mathematical framework that updates our probability models in light of new evidence is **conditional probability**.

Conditional probability is the act of zooming in on a restricted universe. It throws away the parts of the global sample space that are no longer possible under our new context, and recalculates the odds based entirely on this restricted reality. It represents the transition from "what is the baseline probability of an event?" to "what is the probability of this event *given* that we know this specific context is true?" Updating our models with this context is what transforms generic algorithms into intelligent, context-aware systems.

---

## 2. Formal Definition

Let $(\Omega, \mathcal{F}, P)$ be a probability space. Let $A, B \in \mathcal{F}$ be two events such that the probability of $B$ is strictly positive ($P(B) > 0$). The **conditional probability** of event $A$ given that event $B$ has occurred, denoted $P(A|B)$, is defined as:
$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

### The Multiplication Rule (Chain Rule of Probability)
From the definition of conditional probability, we can express the probability of the joint event $A \cap B$ as:
$$P(A \cap B) = P(A|B)P(B) = P(B|A)P(A)$$
Generalizing to a sequence of $n$ events $A_1, A_2, \dots, A_n$:
$$P\left( \bigcap_{i=1}^{n} A_i \right) = P(A_1) P(A_2 | A_1) P(A_3 | A_1 \cap A_2) \dots P(A_n | \bigcap_{i=1}^{n-1} A_i)$$

### Conditional Independence
Two events $A$ and $B$ are **conditionally independent** given a third event $C$ (where $P(C) > 0$) if the occurrence of $A$ and $B$ is independent when restricted to the space where $C$ is true:
$$P(A \cap B | C) = P(A|C) P(B|C)$$
This is equivalent to stating that if we already know $C$ has occurred, knowing $B$ provides no additional information about the likelihood of $A$: $P(A|B \cap C) = P(A|C)$.

---

## 3. Illustrative Derivation

### Derivation of the Law of Total Probability
In machine learning, we often cannot calculate the probability of a global event $A$ directly. Instead, we evaluate it in slices, conditioned on a set of mutually exclusive scenarios. We derive the **Law of Total Probability** from the axioms of probability measures.

Let $\{B_1, B_2, \dots, B_k\}$ be a finite partition of the sample space $\Omega$. By definition of a partition:
1.  The events are pairwise disjoint:
    $$B_i \cap B_j = \emptyset \quad \forall i \neq j$$
2.  The union of the partition covers the entire sample space:
    $$\bigcup_{i=1}^{k} B_i = \Omega$$
3.  Each partitioning event has a non-zero probability:
    $$P(B_i) > 0 \quad \forall i$$

We want to express the probability of any event $A \in \mathcal{F}$ as a weighted sum of conditional probabilities.

*Proof:*
Since the union of $\{B_i\}$ is the entire space $\Omega$, we can write:
$$A = A \cap \Omega = A \cap \left( \bigcup_{i=1}^k B_i \right)$$
Applying the distributive law of set theory:
$$A = \bigcup_{i=1}^{k} (A \cap B_i)$$

Since the events $B_i$ are pairwise disjoint, the intersection events $(A \cap B_i)$ must also be pairwise disjoint:
$$(A \cap B_i) \cap (A \cap B_j) = A \cap (B_i \cap B_j) = A \cap \emptyset = \emptyset \quad \forall i \neq j$$
By the countable additivity axiom of probability measures, the probability of the union of disjoint events is the sum of their individual probabilities:
$$P(A) = P\left( \bigcup_{i=1}^{k} (A \cap B_i) \right) = \sum_{i=1}^{k} P(A \cap B_i)$$

Using the multiplication rule, we substitute $P(A \cap B_i) = P(A | B_i) P(B_i)$ into the summation:
$$P(A) = \sum_{i=1}^{k} P(A | B_i) P(B_i) \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Broken Bus Handles
A bus has 20 handles ($N=20$). There are 5 broken handles ($B=5$), and 8 handles are within your reach ($R=8$). Among the 8 handles within reach, 2 are broken ($B \cap R = 2$). You grab a handle at random within your reach. What is the probability that it is broken?
1.  **Formulate the conditional probability:**
    $$P(B|R) = \frac{P(B \cap R)}{P(R)}$$
2.  **Substitute probabilities:**
    $$P(B \cap R) = \frac{2}{20}, \quad P(R) = \frac{8}{20}$$
    $$P(B|R) = \frac{2/20}{8/20} = \frac{2}{8} = 0.25$$
The conditional probability is $25\%$.

### Example 2: Medical Diagnostic Testing
A rare disease affects $1\%$ of the population: $P(D) = 0.01$. A diagnostic test has a sensitivity of $99\%$ (probability of testing positive given you have the disease: $P(T^+ | D) = 0.99$) and a false positive rate of $5\%$ (probability of testing positive given you do not have the disease: $P(T^+ | D^c) = 0.05$). Find the probability that a person who tests positive actually has the disease.
1.  **Find the total probability of testing positive $P(T^+)$ using the Law of Total Probability:**
    $$P(T^+) = P(T^+ | D)P(D) + P(T^+ | D^c)P(D^c)$$
    Since $P(D) = 0.01$, then $P(D^c) = 1 - 0.01 = 0.99$:
    $$P(T^+) = (0.99)(0.01) + (0.05)(0.99) = 0.0099 + 0.0495 = 0.0594$$
2.  **Calculate the conditional probability $P(D | T^+)$:**
    $$P(D | T^+) = \frac{P(D \cap T^+)}{P(T^+)} = \frac{P(T^+ | D)P(D)}{P(T^+)}$$
    $$P(D | T^+) = \frac{(0.99)(0.01)}{0.0594} = \frac{0.0099}{0.0594} \approx 0.1667$$
Despite the $99\%$ test sensitivity, if you test positive, there is only a $16.67\%$ probability you have the disease, due to its low baseline prevalence.

---

## 5. Applied ML Context

1.  **Naive Bayes Classification:** Naive Bayes calculates the posterior probability of class label $C$ given features $x$ using $P(C|x) \propto P(C) \prod_i P(x_i | C)$, assuming that features $x_i$ are conditionally independent given the class.
2.  **Autoregressive Large Language Models (LLMs):** LLMs generate text by predicting the next token $w_t$ based on the conditional probability distribution over the preceding context tokens: $P(w_t | w_1, w_2, \dots, w_{t-1})$.
3.  **Hidden Markov Models (HMMs):** HMMs rely on the Markov property, which assumes that the probability of the current hidden state $S_t$ is conditionally independent of all past states given the immediate prior state: $P(S_t | S_{t-1}, \dots, S_1) = P(S_t | S_{t-1})$.
4.  **Precision Evaluation Metric:** In binary classification, Precision measures the reliability of the model's positive alarms, which is the conditional probability: $P(\text{Actual Positive} \mid \text{Predicted Positive})$.
5.  **Active Learning Query Strategies:** Active learning systems select unlabeled instances to query for human labeling by computing the model's output entropy conditional on the observed feature inputs: $H(Y|X=x)$.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating conditional probability as a restricted universe:
*   Draw a large rectangle representing the sample space $\Omega$.
*   Inside the rectangle, draw two overlapping circles: circle $A$ (left) and circle $B$ (right). Shade the overlapping intersection area $A \cap B$.
*   Draw a second, adjacent diagram representing the restricted universe where $B$ has occurred:
    *   Crop or black out everything outside circle $B$. Circle $B$ now acts as the new bounding rectangle (the new sample space).
    *   Highlight that the conditional probability $P(A|B)$ is represented visually as the ratio of the shaded intersection area $A \cap B$ to the total area of the new bounding circle $B$.
*   Use this visualization to emphasize how conditioning collapses the outer space $\Omega$, scaling the overlap relative to the subset $B$.
