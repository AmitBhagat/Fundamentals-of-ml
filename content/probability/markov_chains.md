---
title: "Markov Chains"
description: "The Markov property, transition probability matrices, Chapman-Kolmogorov relations, stationary distributions, and MCMC algorithms."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Vectors", "Matrices", "Probability Distributions", "Conditional Probability"]
---

<h1 align="center"> Chapter 50: Markov Chains </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Conditional Probability:** Understanding the formulation $P(A|B)$.
* **Matrix Multiplication:** Comfort with row-by-column matrix multiplication.

</div>

## 1. Conceptual Hook

In machine learning, we frequently model sequential data—such as text sequences, weather fluctuations, or user behaviors. If our models had to remember the entire history of a sequence to predict the next step, their computational complexity would grow exponentially, exhausting memory resources. To simplify sequence modeling, we use **Markov Chains**.

Markov Chains operate under the **Markov Property**: the future state of a system depends only on its present state, not on the path it took to get there. It represents a "memoryless" system. For example, if you are cleaning an exhaust fan, the probability of the fan becoming clean in the next step depends entirely on how dirty it is *right now*, not on how many hours you spent scrubbing it in the past. This memoryless structure allows us to model complex, sequential systems using simple transition matrices, powering autocomplete text models, reinforcement learning (MDPs), and Google's PageRank algorithm.

---

## 2. Formal Definition

Let $\{X_t\}_{t \in \mathbb{N}_0}$ be a stochastic process taking values in a countable state space $\mathcal{S}$.

### The Markov Property
The process $\{X_t\}$ is a **Markov Chain** if for all time steps $t \ge 0$ and all possible states $i_0, i_1, \dots, i_t, j \in \mathcal{S}$:
$$P(X_{t+1} = j \mid X_t = i_t, X_{t-1} = i_{t-1}, \dots, X_0 = i_0) = P(X_{t+1} = j \mid X_t = i_t)$$

### Transition Probability Matrix
For a time-homogeneous Markov Chain, the probability of transitioning from state $i$ to state $j$ in a single step is constant over time:
$$P_{ij} = P(X_{t+1} = j \mid X_t = i)$$

These probabilities are organized into a square **Transition Probability Matrix** $\mathbf{P} = [P_{ij}]$, which is a stochastic matrix satisfying:
1.  **Non-negativity:** $P_{ij} \ge 0$ for all $i, j \in \mathcal{S}$.
2.  **Row Normalization:** The sum of probabilities in each row must equal exactly 1 (since the system must transition to some state in the next step):
    $$\sum_{j \in \mathcal{S}} P_{ij} = 1 \quad \forall i \in \mathcal{S}$$

### State Distribution
Let the probability distribution of the system at time $t$ be represented by the row vector $\boldsymbol{\pi}^{(t)} = [P(X_t = s_1), P(X_t = s_2), \dots]$. The distribution at the next step is:
$$\boldsymbol{\pi}^{(t+1)} = \boldsymbol{\pi}^{(t)} \mathbf{P}$$
By induction, the distribution after $n$ steps is:
$$\boldsymbol{\pi}^{(n)} = \boldsymbol{\pi}^{(0)} \mathbf{P}^n$$

### Stationary Distribution
A probability distribution vector $\boldsymbol{\pi}^*$ is a **stationary distribution** of the Markov Chain if it satisfies:
$$\boldsymbol{\pi}^* \mathbf{P} = \boldsymbol{\pi}^* \quad \text{where} \quad \sum_{i \in \mathcal{S}} \pi^*_i = 1$$
If a Markov Chain is irreducible and aperiodic, the state distribution will converge to this unique stationary distribution $\boldsymbol{\pi}^*$ in the limit $n \to \infty$, regardless of the initial state distribution $\boldsymbol{\pi}^{(0)}$.

---

## 3. Illustrative Derivation

### Derivation of the Chapman-Kolmogorov Equations (2-Step Case)
The Chapman-Kolmogorov equations describe the probability of transitioning from state $i$ to state $j$ in $n$ steps. We derive the 2-step transition probability $P_{ij}^{(2)}$ and show that it corresponds directly to matrix multiplication $\mathbf{P}^2$.

*Proof:*
By definition, the 2-step transition probability is:
$$P_{ij}^{(2)} = P(X_{t+2} = j \mid X_t = i)$$
Using the Law of Total Probability, we condition on all possible intermediate states $k$ at time $t+1$:
$$P(X_{t+2} = j \mid X_t = i) = \sum_{k \in \mathcal{S}} P(X_{t+2} = j, X_{t+1} = k \mid X_t = i)$$
Apply the definition of conditional probability:
$$P(X_{t+2} = j, X_{t+1} = k \mid X_t = i) = P(X_{t+2} = j \mid X_{t+1} = k, X_t = i) \cdot P(X_{t+1} = k \mid X_t = i)$$
By the Markov Property, the state at $t+2$ depends only on the state at $t+1$, making the conditioning on $X_t = i$ redundant:
$$P(X_{t+2} = j \mid X_{t+1} = k, X_t = i) = P(X_{t+2} = j \mid X_{t+1} = k) = P_{kj}$$
The second term is the 1-step transition probability from state $i$ to state $k$:
$$P(X_{t+1} = k \mid X_t = i) = P_{ik}$$
Substitute these terms back into the summation:
$$P_{ij}^{(2)} = \sum_{k \in \mathcal{S}} P_{ik} P_{kj}$$
Observe that this summation is exactly the definition of the $(i, j)$-th entry of the squared matrix $\mathbf{P}^2$:
$$\mathbf{P}^{(2)} = \mathbf{P}^2 \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Exhaust Fan Grease Transitions
An exhaust fan transitions between two states: $s_1: \text{Caked}$ and $s_2: \text{Sticky}$. The transition probability matrix is:
$$\mathbf{P} = \begin{pmatrix} 0.6 & 0.4 \\ 0.2 & 0.8 \end{pmatrix}$$
If the fan starts in the $\text{Caked}$ state ($\boldsymbol{\pi}^{(0)} = [1, 0]$), find the state distribution after two steps.
1.  **Calculate $\mathbf{P}^2$:**
    $$\mathbf{P}^2 = \begin{pmatrix} 0.6 & 0.4 \\ 0.2 & 0.8 \end{pmatrix} \begin{pmatrix} 0.6 & 0.4 \\ 0.2 & 0.8 \end{pmatrix} = \begin{pmatrix} (0.6)(0.6) + (0.4)(0.2) & (0.6)(0.4) + (0.4)(0.8) \\ (0.2)(0.6) + (0.8)(0.2) & (0.2)(0.4) + (0.8)(0.8) \end{pmatrix}$$
    $$\mathbf{P}^2 = \begin{pmatrix} 0.36 + 0.08 & 0.24 + 0.32 \\ 0.12 + 0.16 & 0.08 + 0.64 \end{pmatrix} = \begin{pmatrix} 0.44 & 0.56 \\ 0.28 & 0.72 \end{pmatrix}$$
2.  **Multiply by the initial state vector:**
    $$\boldsymbol{\pi}^{(2)} = \boldsymbol{\pi}^{(0)} \mathbf{P}^2 = [1, 0] \begin{pmatrix} 0.44 & 0.56 \\ 0.28 & 0.72 \end{pmatrix} = [0.44, 0.56]$$
After two steps, there is a $44\%$ probability the fan is still $\text{Caked}$, and a $56\%$ probability it is $\text{Sticky}$.

### Example 2: Stationary Distribution of Daily Maintenance
A system has two states: $s_1: \text{Dirty}$ and $s_2: \text{Sparkling}$. The transition matrix is:
$$\mathbf{P} = \begin{pmatrix} 0.7 & 0.3 \\ 0.1 & 0.9 \end{pmatrix}$$
Find the long-term stationary distribution $\boldsymbol{\pi}^* = [\pi_1, \pi_2]$.
1.  **Set up the stationary equation $\boldsymbol{\pi}^* \mathbf{P} = \boldsymbol{\pi}^*$:**
    $$[\pi_1, \pi_2] \begin{pmatrix} 0.7 & 0.3 \\ 0.1 & 0.9 \end{pmatrix} = [\pi_1, \pi_2]$$
2.  **Formulate the system of equations:**
    $$0.7\pi_1 + 0.1\pi_2 = \pi_1 \implies 0.1\pi_2 = 0.3\pi_1 \implies \pi_2 = 3\pi_1$$
3.  **Use the normalization constraint $\pi_1 + \pi_2 = 1$:**
    $$\pi_1 + 3\pi_1 = 1 \implies 4\pi_1 = 1 \implies \pi_1 = 0.25, \quad \pi_2 = 0.75$$
In the long run, the system will spend $75\%$ of its time in the $\text{Sparkling}$ state and $25\%$ of its time in the $\text{Dirty}$ state.

---

## 5. Applied ML Context

1.  **n-gram Language Models:** In early NLP, word sequences were modeled as homogeneous Markov Chains. A bigram model predicts the probability of the next word $w_{t+1}$ conditioned only on the current word $w_t$: $P(w_{t+1} \mid w_t)$.
2.  **Markov Decision Processes (MDPs) in RL:** MDPs extend Markov Chains by introducing actions $a$ and rewards $r$. The transition probability to the next state $s_{t+1}$ depends only on the current state $s_t$ and the action taken $a_t$: $P(s_{t+1} \mid s_t, a_t)$.
3.  **Google PageRank Algorithm:** PageRank models web surfing as a Markov Chain. Web pages are states, and hyperlinks are transition paths. The relevance ranking of a web page corresponds to its value in the chain's stationary distribution vector $\boldsymbol{\pi}^*$.
4.  **Hidden Markov Models (HMMs):** HMMs model sequences where states are hidden (e.g., parts of speech or phonemes) but generate observable emissions (e.g., words or acoustic signals). The sequence of hidden states is modeled as a Markov Chain.
5.  **MCMC Sampling (Metropolis-Hastings):** MCMC algorithms sample from complex probability distributions by constructing a Markov Chain whose stationary distribution is exactly the target distribution. The chain is run until it converges, and its states are recorded as samples.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating a state transition graph:
*   Draw a directed graph representing a two-state Markov Chain:
    *   Draw two circles representing state nodes: $S_1$ (Dirty) and $S_2$ (Sparkling).
*   Add transition arrows between nodes:
    1.  A self-loop arrow from $S_1$ to itself, labeled $0.7$.
    2.  A self-loop arrow from $S_2$ to itself, labeled $0.9$.
    3.  A directed arrow pointing from $S_1$ to $S_2$, labeled $0.3$.
    4.  A directed arrow pointing from $S_2$ to $S_1$, labeled $0.1$.
*   Add a caption explaining that this graph visually represents the transition matrix $\mathbf{P} = \begin{pmatrix} 0.7 & 0.3 \\ 0.1 & 0.9 \end{pmatrix}$, demonstrating how the next state is selected using only the current state's transition rules.
