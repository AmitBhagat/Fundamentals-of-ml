---
title: "Independence"
description: "Statistical independence, conditional independence, mutual vs. pairwise independence, and the Bernstein counter-example."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Random Variables", "Conditional Probability"]
---

<h1 align="center"> Chapter 47: Independence </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Joint Probability:** Knowing how to represent the likelihood of two events occurring together: $P(A \cap B)$.
* **Conditional Probability:** Understanding the notation $P(A|B)$ as the probability of $A$ given $B$.

</div>

## 1. Conceptual Hook

In machine learning, we build models to identify patterns and find correlations between variables. But to make these computations manageable, we also need to know when variables have *no* relationship at all. When two events are completely unlinked, we say they are **statistically independent**.

Two events are independent if the occurrence of one provides absolutely zero information about the likelihood of the other. For instance, if you roll a die, the probability of rolling a $6$ is $\frac{1}{6}$. If it is raining outside, the probability of rolling a $6$ is still exactly $\frac{1}{6}$. The rain provides zero predictive power for your die roll. Mathematically, independence allows us to simplify complex joint probability distributions into products of individual probabilities, dramatically reducing the number of parameters we need to estimate in models like Naive Bayes.

---

## 2. Formal Definition

### Independence of Events
Let $(\Omega, \mathcal{F}, P)$ be a probability space. Two events $A, B \in \mathcal{F}$ are **statistically independent** if and only if:
$$P(A \cap B) = P(A) \cdot P(B)$$

If $P(B) > 0$, this definition is equivalent to:
$$P(A|B) = P(A)$$
which states that the conditional probability of $A$ given $B$ is identical to the marginal (unconditioned) probability of $A$.

### Mutual vs. Pairwise Independence
A collection of events $\{A_1, A_2, \dots, A_n\}$ is **pairwise independent** if every pair of events is independent:
$$P(A_i \cap A_j) = P(A_i) \cdot P(A_j) \quad \forall i \neq j$$

The collection is **mutually independent** if for any finite subset of indices $I \subseteq \{1, 2, \dots, n\}$:
$$P\left( \bigcap_{i \in I} A_i \right) = \prod_{i \in I} P(A_i)$$
*Important Note:* Pairwise independence does *not* imply mutual independence.

### Independence of Random Variables
Two random variables $X$ and $Y$ are independent if their induced events are independent. Specifically, for all Borel sets $B_1, B_2 \in \mathcal{B}(\mathbb{R})$:
$$P(X \in B_1 \text{ and } Y \in B_2) = P(X \in B_1) \cdot P(Y \in B_2)$$
For continuous random variables with joint PDF $f_{X, Y}(x, y)$ and marginal PDFs $f_X(x), f_Y(y)$, this is equivalent to:
$$f_{X, Y}(x, y) = f_X(x) \cdot f_Y(y) \quad \forall (x, y) \in \mathbb{R}^2$$

---

## 3. Illustrative Derivation

### Proof that Pairwise Independence Does Not Imply Mutual Independence
We construct a classic probability space (originally due to Sergei Bernstein) consisting of four outcomes to prove that pairwise independence is a weaker condition than mutual independence.

Let the sample space have four equally likely outcomes:
$$\Omega = \{\omega_1, \omega_2, \omega_3, \omega_4\} \implies P(\omega_i) = \frac{1}{4} \quad \forall i$$

Define three events:
*   $A = \{\omega_1, \omega_2\} \implies P(A) = P(\omega_1) + P(\omega_2) = \frac{1}{4} + \frac{1}{4} = \frac{1}{2}$
*   $B = \{\omega_1, \omega_3\} \implies P(B) = \frac{1}{2}$
*   $C = \{\omega_1, \omega_4\} \implies P(C) = \frac{1}{2}$

1.  **Check Pairwise Independence:**
    We evaluate the intersections of all pairs:
    *   $A \cap B = \{\omega_1\} \implies P(A \cap B) = \frac{1}{4}$
        Since $P(A) \cdot P(B) = \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$, we have:
        $$P(A \cap B) = P(A) \cdot P(B)$$
    *   $B \cap C = \{\omega_1\} \implies P(B \cap C) = \frac{1}{4}$
        Since $P(B) \cdot P(C) = \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$, we have:
        $$P(B \cap C) = P(B) \cdot P(C)$$
    *   $A \cap C = \{\omega_1\} \implies P(A \cap C) = \frac{1}{4}$
        Since $P(A) \cdot P(C) = \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$, we have:
        $$P(A \cap C) = P(A) \cdot P(C)$$
    Every pair satisfies the product rule. Therefore, events $A$, $B$, and $C$ are **pairwise independent**.

2.  **Check Mutual Independence:**
    We evaluate the intersection of all three events:
    $$A \cap B \cap C = \{\omega_1\} \implies P(A \cap B \cap C) = \frac{1}{4}$$
    However, the product of all three individual probabilities is:
    $$P(A) \cdot P(B) \cdot P(C) = \frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{8}$$
    Comparing the two values:
    $$P(A \cap B \cap C) \neq P(A) \cdot P(B) \cdot P(C) \quad \left( \frac{1}{4} \neq \frac{1}{8} \right)$$
The events are pairwise independent, but **not mutually independent**. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Independent ATM Failures
Two bank brand ATMs operate on independent networks. The probability of Bank X running out of cash is $P(X) = 0.20$. The probability of Bank Y running out of cash is $P(Y) = 0.15$. Find the probability that both ATMs are depleted.
1.  **Apply the independence product rule:**
    $$P(X \cap Y) = P(X) \cdot P(Y)$$
2.  **Substitute values:**
    $$P(X \cap Y) = 0.20 \cdot 0.15 = 0.03$$
There is only a $3\%$ chance that both ATMs are out of cash.

### Example 2: Continuous Independent PDFs
Let $X$ and $Y$ be independent continuous random variables representing server processing times, with marginal PDFs $f_X(x) = e^{-x}$ (for $x \ge 0$) and $f_Y(y) = 2e^{-2y}$ (for $y \ge 0$). Find their joint PDF $f_{X, Y}(x, y)$.
1.  **Apply the random variable independence property:**
    $$f_{X,Y}(x, y) = f_X(x) \cdot f_Y(y)$$
2.  **Multiply the functions:**
    $$f_{X,Y}(x, y) = \left(e^{-x}\right) \left(2e^{-2y}\right) = 2e^{-(x+2y)}$$
    for $x, y \ge 0$.

---

## 5. Applied ML Context

1.  **Naive Bayes Classification:** This classifier assumes that features $x_i$ are independent given the class label $C$: $P(x_1, \dots, x_d | C) = \prod_{i=1}^d P(x_i | C)$. This assumption dramatically simplifies parameter estimation by eliminating feature interaction terms.
2.  **Independent Component Analysis (ICA):** ICA separates a multivariate signal into additive subcomponents by maximizing the statistical independence of the source signals, used in applications like separating voices in audio mixes.
3.  **Dropout Regularization:** During neural network training, dropout turns off individual neurons with probability $1-p$. Each neuron's survival is modeled as an independent Bernoulli trial, preventing co-adaptation of features.
4.  **Feature Selection via Mutual Information:** We calculate the mutual information between features $X$ and targets $Y$. If $X$ and $Y$ are independent, their mutual information is zero, meaning $X$ has no predictive power and can be pruned.
5.  **DQN Experience Replay:** Standard reinforcement learning updates are unstable because successive state transitions are highly correlated. Experience replay buffers store and sample transitions randomly to break this correlation, satisfying the independent and identically distributed (i.i.d.) assumption.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the geometric interpretation of independence:
*   Draw a large square representing the sample space $\Omega$ with area 1.
*   Draw two overlapping circles representing events $A$ and $B$.
*   Highlight the intersection area $A \cap B$. Annotate that for independent events, the area of this overlap must satisfy the equation: $\text{Area}(A \cap B) = \text{Area}(A) \cdot \text{Area}(B)$.
*   Draw a second, zoomed-in view focusing only on the circle of event $B$. Show that the ratio of the overlap area to the area of $B$ (representing the conditional probability $P(A|B) = \frac{P(A \cap B)}{P(B)}$) is visually identical to the ratio of the area of $A$ to the entire square $\Omega$ (representing the marginal probability $P(A)$). This visualizes how the occurrence of $B$ does not alter the relative likelihood of $A$.
