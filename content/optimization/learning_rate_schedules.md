---
title: "Learning Rate Schedules"
description: "Optimization dynamics, step size decay, exponential and inverse time schedules, cosine annealing, and Robbins-Monro convergence proofs."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Derivatives", "Optimization: Gradient Descent", "Optimization: Stochastic Gradient Descent"]
---

<h1 align="center"> Chapter 88: Learning Rate Schedules </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Harmonic Series:** The infinite series $\sum_{n=1}^\infty \frac{1}{n}$, which diverges to infinity.
* **Convergence Bounds:** The mathematical limits within which a sequence is guaranteed to settle at a fixed point.

</div>

## 1. Conceptual Hook

In machine learning, the learning rate $\eta$ is the single most critical hyperparameter. It determines the size of the steps we take toward the minimum of the loss landscape. A learning rate that is too high causes the model to overshoot the valley and diverge; a learning rate that is too low stalls training on flat regions, taking forever to converge.

However, the optimal learning rate is not constant over time.

Ideally, we want a large learning rate early in training to rapidly explore the parameter landscape, escape local plateaus, and cross high-error zones. As we approach the minimum, we want a small learning rate to perform fine-grained parameter updates and settle quietly into the bottom of the basin without bouncing back and forth over the target.

**Learning rate schedules** are the mathematical controllers that dynamically decay the step size over the course of training to solve this convergence trade-off.

---

## 2. Formal Definition

Let $\mathbf{w}^{(t)} \in \mathbb{R}^d$ be the parameter vector at iteration step $t$. The gradient update rule is:
$$\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta_t \nabla J\left(\mathbf{w}^{(t)}\right)$$
where $\eta_t$ is the learning rate at step $t$. A schedule defines $\eta_t$ as a function of the iteration index $t$ or epoch number.

### Common Decay Schedules
1.  **Exponential Decay:**
    The learning rate decays exponentially at each step:
    $$\eta_t = \eta_0 e^{-kt} \quad \text{or} \quad \eta_t = \eta_0 \gamma^t$$
    where $\eta_0$ is the initial learning rate, $k > 0$ is the decay rate, and $\gamma \in (0, 1)$ is the decay factor.
2.  **Step Decay (Piecewise Constant):**
    The learning rate drops by a factor of $\gamma$ at pre-determined step intervals $s$:
    $$\eta_t = \eta_0 \gamma^{\lfloor t / s \rfloor}$$
3.  **Inverse Time Decay:**
    The learning rate decays inversely with time:
    $$\eta_t = \frac{\eta_0}{1 + kt}$$
4.  **Cosine Annealing (with optional Warmup):**
    The learning rate is decayed following a cosine curve:
    $$\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{T_{cur}}{T_{max}} \pi\right)\right)$$
    where $T_{cur}$ is the number of epochs since the last restart, and $T_{max}$ is the total number of epochs. In warmup schemes, $\eta$ starts at 0 and grows linearly to $\eta_{max}$ for the first few thousand steps before annealing begins.

---

## 3. Illustrative Derivation

### Proof: Convergence and Robbins-Monro Conditions under Decaying Schedules
We prove how the decay rate of a learning rate schedule affects convergence on a strictly convex 1D quadratic function $f(w) = \frac{1}{2} a w^2$ (with $a > 0$), and prove why the harmonic decay sequence satisfies the Robbins-Monro conditions for convergence under noise.

*Proof:*
The minimum of $f(w)$ lies at $w^* = 0$. The gradient is $f'(w) = a w$.
The update rule is:
$$w^{(t+1)} = w^{(t)} - \eta_t a w^{(t)} = (1 - a \eta_t) w^{(t)}$$
Unrolling this recurrence relation from step $0$ to $T$:
$$w^{(T)} = w^{(0)} \prod_{t=0}^{T-1} (1 - a \eta_t)$$

1.  **Constant Learning Rate Limit:**
    If $\eta_t = \eta$ is constant:
    $$w^{(T)} = w^{(0)} (1 - a \eta)^T$$
    For $w^{(T)}$ to converge to $0$ as $T \to \infty$, we must satisfy:
    $$|1 - a \eta| < 1 \implies 0 < \eta < \frac{2}{a}$$
    If $\eta \ge \frac{2}{a}$, the updates diverge. If $\eta$ is close to the boundary, the parameter oscillates back and forth. If noise is present, a constant learning rate will oscillate in a variance basin around the minimum.

2.  **Decaying Schedule convergence (Robbins-Monro):**
    Under stochastic gradients, to guarantee convergence to the exact minimum rather than a variance basin, the schedule must satisfy the Robbins-Monro conditions:
    $$\sum_{t=0}^{\infty} \eta_t = \infty \quad \text{and} \quad \sum_{t=0}^{\infty} \eta_t^2 < \infty$$
    Let us evaluate these conditions for the harmonic decay schedule $\eta_t = \frac{c}{t+1}$ for a constant $c > 0$.
    *   **First Condition (Divergence of sum):**
        $$\sum_{t=0}^{\infty} \frac{c}{t+1} = c \sum_{n=1}^{\infty} \frac{1}{n} = \infty$$
        Because the harmonic series diverges to infinity, the model has enough capacity to travel any distance to reach the minimum, regardless of how far away the initialization was.
    *   **Second Condition (Convergence of squared sum):**
        $$\sum_{t=0}^{\infty} \left( \frac{c}{t+1} \right)^2 = c^2 \sum_{n=1}^{\infty} \frac{1}{n^2} = c^2 \frac{\pi^2}{6} < \infty$$
        Because the sum of squared terms converges (the Basel problem), the step sizes shrink fast enough to cancel out the variance of random gradient noise at the minimum, ensuring stable convergence. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Step Decay Schedule
We compute the learning rate at epoch $t = 3$. Let initial learning rate $\eta_0 = 0.5$, decay factor $\gamma = 0.5$, and step size interval $s = 2$ epochs.
1.  **Formulate the equation:**
    $$\eta_3 = \eta_0 \gamma^{\lfloor 3 / 2 \rfloor}$$
2.  **Calculate the floor division and evaluate:**
    $$\lfloor 3 / 2 \rfloor = 1 \implies \eta_3 = 0.5 \cdot (0.5)^1 = 0.25$$

### Example 2: Inverse Time Decay Schedule
We compute the learning rate at iteration step $t = 4$. Let initial learning rate $\eta_0 = 1.0$ and decay rate $k = 1.0$.
1.  **Formulate the equation:**
    $$\eta_4 = \frac{\eta_0}{1 + k \cdot t}$$
2.  **Substitute and calculate:**
    $$\eta_4 = \frac{1.0}{1 + 1.0 \cdot 4} = \frac{1.0}{5.0} = 0.2$$

---

## 5. Applied ML Context

1.  **Transformer Language Model Pre-training:** Large language models (e.g. GPT architectures) utilize Cosine Annealing with a linear warmup phase. The warmup phase prevents early gradients from destabilizing self-attention weights.
2.  **Image Classification Convolutional Networks:** Models like ResNets trained on ImageNet employ step decay schedules, reducing the learning rate by a factor of $10$ at epochs $30$, $60$, and $90$ to refine feature weights.
3.  **Transfer Learning Fine-Tuning:** Decaying schedules are used when adapting pre-trained models to new datasets, keeping early features stable while allowing downstream layers to adapt.
4.  **Online Streaming Systems:** Decaying schedules like inverse time decay are used in real-time prediction pipelines to prevent a single noisy data point from causing massive updates to a mature model.
5.  **Reinforcement Learning Policies:** Schedules are used to scale down policy updates alongside exploration rates ($\epsilon$-greedy), ensuring the agent stabilizes on an optimal policy.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating learning rate decay curves:
*   Draw a 2D plot with Learning Rate ($\eta$) on the vertical axis and Training Progress (epochs) on the horizontal axis.
*   Draw three distinct scheduled curves:
    1.  **Step Decay (staircase line):** Shows the learning rate dropping in flat blocks.
    2.  **Exponential Decay (smooth curve):** Shows the learning rate falling rapidly early and flattening out close to zero.
    3.  **Cosine Annealing with Warmup (arched curve):** Shows the learning rate rising linearly to a peak (warmup) and then rolling down like a cosine wave.
*   Add a callout box explaining that early high learning rates allow large steps to escape local plateaus, while late small learning rates prevent overshooting.
