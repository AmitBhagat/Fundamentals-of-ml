---
title: "Adaptive Methods (Adam, RMSProp)"
description: "Adaptive optimizers, parameter-specific learning rates, moving averages of squared gradients, bias correction derivations, and NLP/CV applications."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Partial Derivatives", "Calculus: Gradient", "Optimization: Gradient Descent", "Optimization: Stochastic Gradient Descent", "Optimization: Momentum and Nesterov Acceleration"]
---

<h1 align="center"> Chapter 84: Adaptive Methods (Adam, RMSProp) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Exponentially Weighted Moving Average (EWMA):** A recursive statistic that estimates the mean of a sequence by weighting older samples with exponentially decaying coefficients.
* **Hadamard Product ($\odot$):** The element-wise multiplication of two matrices or vectors of identical dimensions.

</div>

## 1. Conceptual Hook

In standard Gradient Descent, we apply a single global learning rate to update all model parameters. However, in deep neural networks, different parameters face vastly different loss landscape geometries. Some parameters are associated with dense features and receive frequent, large gradients; others are associated with sparse features and receive tiny, infrequent updates.

A global learning rate that is small enough to keep volatile parameters from oscillating and diverging will stall the learning of sparse parameters. Conversely, a learning rate large enough to push sparse parameters forward will cause volatile ones to explode.

**Adaptive optimization methods** (like **RMSprop** and **Adam**) solve this by giving each individual parameter its own customized learning rate.

By maintaining running estimates of the historical gradient magnitude, these optimizers automatically throttle back updates for highly volatile parameters and amplify updates for slow, steady ones. This ensures smooth, balanced convergence across all layers of a deep network.

---

## 2. Formal Definition

Let $\mathbf{w}_t \in \mathbb{R}^d$ be the parameter vector at iteration step $t$, and let $\mathbf{g}_t = \nabla f(\mathbf{w}_t)$ be the gradient of the objective function.

### 1. RMSprop (Root Mean Square Propagation)
RMSprop restricts the accumulation of historical gradients to a recent temporal window using an exponentially decaying average of squared gradients:
$$\mathbf{v}_t = \beta \mathbf{v}_{t-1} + (1 - \beta) \mathbf{g}_t^2$$
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \frac{\eta}{\sqrt{\mathbf{v}_t} + \epsilon} \odot \mathbf{g}_t$$
where:
*   **$\beta \in [0, 1)$:** The decay rate hyperparameter (typically $0.9$).
*   **$\eta > 0$:** The base learning rate.
*   **$\epsilon > 0$:** A tiny smoothing term to prevent division by zero (typically $10^{-8}$).
*   **$\odot$:** The element-wise Hadamard product. All vector square and square-root operations are evaluated element-wise.

### 2. Adam (Adaptive Moment Estimation)
Adam combines the properties of Polyak momentum (the first moment) and RMSprop (the second moment):
$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t \quad (\text{First Moment Estimation})$$
$$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2 \quad (\text{Second Moment Estimation})$$

#### Bias Correction
Because $\mathbf{m}_t$ and $\mathbf{v}_t$ are typically initialized as zero vectors, they are biased toward zero, especially during early iterations when the decay rates $\beta_1$ and $\beta_2$ are close to $1$. To correct this bias, we compute:
$$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t} \quad \text{and} \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$
where $t$ in $\beta^t$ represents the iteration step exponent.

#### Final Parameter Update
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \frac{\eta}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \odot \hat{\mathbf{m}}_t$$
Common default hyperparameters: $\beta_1 = 0.9$, $\beta_2 = 0.999$, and $\epsilon = 10^{-8}$.

---

## 3. Illustrative Derivation

### Derivation of the First-Moment Bias Correction Formula
We prove the algebraic correction term $\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}$ under the assumption of gradient stationarity.

*Proof:*
Let the recursive definition be $\mathbf{m}_t = \beta \mathbf{m}_{t-1} + (1-\beta)\mathbf{g}_t$ with initialization $\mathbf{m}_0 = \mathbf{0}$.
1.  **Unroll the recurrence relation:**
    $$m_1 = (1-\beta)g_1$$
    $$m_2 = \beta m_1 + (1-\beta)g_2 = \beta(1-\beta)g_1 + (1-\beta)g_2$$
    $$m_3 = \beta m_2 + (1-\beta)g_3 = \beta^2(1-\beta)g_1 + \beta(1-\beta)g_2 + (1-\beta)g_3$$
    By mathematical induction, for any step $t$:
    $$m_t = (1-\beta) \sum_{i=1}^{t} \beta^{t-i} g_i$$

2.  **Evaluate the expectation of both sides:**
    We assume the true gradient distribution has a stationary mean, so $\mathbb{E}[g_i] = \mathbb{E}[g_t]$ for all $i \in \{1, \dots, t\}$:
    $$\mathbb{E}[m_t] = \mathbb{E}\left[ (1-\beta) \sum_{i=1}^{t} \beta^{t-i} g_i \right]$$
    By linearity of expectation:
    $$\mathbb{E}[m_t] = (1-\beta) \sum_{i=1}^{t} \beta^{t-i} \mathbb{E}[g_i]$$
    Since $\mathbb{E}[g_i] = \mathbb{E}[g_t]$:
    $$\mathbb{E}[m_t] = \mathbb{E}[g_t] (1-\beta) \sum_{i=1}^{t} \beta^{t-i}$$

3.  **Sum the finite geometric series:**
    Let $j = t-i$. As $i$ ranges from $1$ to $t$, the index $j$ ranges from $t-1$ down to $0$:
    $$\sum_{i=1}^{t} \beta^{t-i} = \sum_{j=0}^{t-1} \beta^j$$
    Using the sum formula for a finite geometric series:
    $$\sum_{j=0}^{t-1} \beta^j = \frac{1 - \beta^t}{1 - \beta}$$

4.  **Substitute back to isolate the true mean:**
    $$\mathbb{E}[m_t] = \mathbb{E}[g_t] (1-\beta) \left( \frac{1 - \beta^t}{1 - \beta} \right) = \mathbb{E}[g_t] (1 - \beta^t)$$
This shows that the raw running average expectation is biased, scaled by $(1-\beta^t)$. To obtain an unbiased estimator $\hat{m}_t$ whose expectation equals the true mean $\mathbb{E}[g_t]$, we divide by the scaling factor:
$$\hat{m}_t = \frac{m_t}{1 - \beta^t} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Volatility Scaling in 2D (RMSprop)
We optimize a function with a steep axis ($g_{t,1} = 10.0$) and a flat axis ($g_{t,2} = 0.1$). Let learning rate $\eta = 0.01$, decay rate $\beta = 0.9$, and initial second moment $v_{t-1} = 0$.
1.  **Steep Dimension Update ($g_{t,1} = 10.0$):**
    $$v_{t,1} = 0.9 \cdot 0 + 0.1 \cdot (10.0)^2 = 10.0$$
    $$\Delta w_1 = \frac{\eta}{\sqrt{v_{t,1}}} \cdot g_{t,1} = \frac{0.01}{\sqrt{10.0}} \cdot 10.0 = 0.01 \cdot \sqrt{10.0} \approx 0.0316$$
2.  **Flat Dimension Update ($g_{t,2} = 0.1$):**
    $$v_{t,2} = 0.9 \cdot 0 + 0.1 \cdot (0.1)^2 = 0.001$$
    $$\Delta w_2 = \frac{\eta}{\sqrt{v_{t,2}}} \cdot g_{t,2} = \frac{0.01}{\sqrt{0.001}} \cdot 0.1 = \frac{0.001}{\sqrt{0.001}} = \sqrt{0.001} \approx 0.0316$$
Even though the steep gradient was $100$ times larger than the flat gradient, RMSprop scaled their updates to the exact same size, normalizing the optimization step.

### Example 2: Early Bias Correction (Adam)
We compute the bias-corrected first moment $\hat{m}_t$ at early steps. Let $g_1 = 2.0$ and $g_2 = 3.0$. Set $\beta_1 = 0.9$ and $m_0 = 0$.
1.  **Step 1:**
    $$m_1 = 0.9 \cdot 0 + 0.1 \cdot 2.0 = 0.2$$
    $$\hat{m}_1 = \frac{m_1}{1 - 0.9^1} = \frac{0.2}{0.1} = 2.0$$
2.  **Step 2:**
    $$m_2 = 0.9 \cdot 0.2 + 0.1 \cdot 3.0 = 0.18 + 0.30 = 0.48$$
    $$\hat{m}_2 = \frac{m_2}{1 - 0.9^2} = \frac{0.48}{1 - 0.81} = \frac{0.48}{0.19} \approx 2.526$$

---

## 5. Applied ML Context

1.  **Transformer Training (NLP):** Adam serves as the default optimizer for models like BERT and GPT. Because word frequencies follow a power law, gradients for rare tokens are sparse; adaptive scaling ensures these parameters receive sufficient updates.
2.  **Generative Adversarial Networks (GANs):** Mini-max optimization in GANs creates a highly non-stationary training landscape. Adam stabilizes learning and prevents mode collapse.
3.  **Speech Processing (DeepSpeech):** Audio spectrogram features vary widely across frequency bands. RMSprop balances optimization steps across different spectral dimensions.
4.  **Sparse Latent Recommendations:** In recommendation matrix factorization, adaptive methods adjust steps for user/item parameters that appear infrequently in the dataset.
5.  **Volatility Control in Reinforcement Learning:** Algorithms like A3C utilize RMSprop to stabilize optimization updates against the high variance of reward signals.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here comparing optimizer paths:
*   Draw a contour plot representing a narrow 2D valley.
*   Trace three optimization paths starting from the same coordinate:
    1.  **SGD Path:** Show it taking tiny, stalled steps along the flat valley axis.
    2.  **Momentum Path:** Show it oscillating back and forth across the steep ravine walls before slowly heading down the floor.
    3.  **Adam/RMSprop Path:** Show it instantly suppressing oscillations on the steep axis and accelerating straight down the flat valley floor toward the minimum.
*   Add a callout diagram illustrating the scaling penalty:
    *   Volatile parameters $\to$ large historical second moment $\to$ small step size.
    *   Stable parameters $\to$ small historical second moment $\to$ large step size.
