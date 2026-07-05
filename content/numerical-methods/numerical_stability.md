---
title: "Numerical Stability"
description: "Error propagation, forward and backward stability, overflow and underflow dynamics, catastrophic cancellation, and Log-Sum-Exp derivations."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Calculus: Derivatives", "Numerical Methods: Floating-Point Representation and Machine Epsilon"]
---

<h1 align="center"> Chapter 101: Numerical Stability </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Machine Epsilon ($\epsilon_{mach}$):** The relative precision limit of a floating-point system.
* **Backward Stability:** An algorithm is backward stable if it computes the exact solution to a slightly perturbed version of the original problem.

</div>

## 1. Conceptual Hook

In mathematical theory, equations behave perfectly: functions map inputs to exact outputs, and limits converge smoothly. However, when we implement these formulas on real computer hardware, we are forced to approximate infinite continuous numbers using finite, discrete bits. This introduces tiny rounding errors.

**Numerical stability** is the study of how these rounding errors propagate through an algorithm.

An algorithm is numerically stable if tiny rounding errors remain small and suppressed; it is unstable if the math amplifies these tiny errors into catastrophic failures—such as division-by-zero, overflows to infinity (`NaN`), or underflows to zero.

Think of this like negotiating a price for a house. If a one-cent rounding error in the contract causes the bank's transaction system to crash, your process is unstable. In machine learning, where we multiply millions of probabilities and compute long chains of derivatives, maintaining numerical stability is the difference between a successfully trained model and a training loop that collapses into a sea of `NaN` values.

---

## 2. Formal Definition

Let $f: \mathbb{R} \to \mathbb{R}$ be a mathematical function, and let $\hat{f}: \mathcal{F} \to \mathcal{F}$ be its floating-point implementation.

### 1. Forward Error
The forward error measures the absolute difference between the computed output and the true mathematical value:
$$\Delta_{\text{forward}} = |\hat{f}(x) - f(x)|$$

### 2. Backward Error and Stability
The backward error is the smallest perturbation in the input that yields the computed output:
$$\Delta_{\text{backward}} = \min \{ |\delta| \mid f(x + \delta) = \hat{f}(x) \}$$

An algorithm is defined as **backward stable** if the relative backward error is bounded by a small multiple of the machine epsilon, independent of the input:
$$\frac{|\delta|}{|x|} \le C \epsilon_{mach}$$
where $C > 0$ is a constant.

### Common Numerical Failures
*   **Overflow:** A computation yields a value larger than the maximum representable limit (e.g. $> 3.4 \times 10^{38}$ for FP32), causing the system to return $\infty$ or `NaN`.
*   **Underflow:** A computation yields a value smaller than the minimum representable positive normal value (e.g. $< 1.17 \times 10^{-38}$ for FP32), causing the system to round it to exactly $0.0$.
*   **Catastrophic Cancellation:** Subtracting two nearly identical large numbers, which cancels out their significant digits and amplifies rounding noise.

---

## 3. Illustrative Derivation

### Derivation of the Log-Sum-Exp Stability Trick
We derive the mathematical reformulation of the Log-Sum-Exp (LSE) function and prove how it prevents overflow and underflow in softmax evaluations.

We wish to compute the log-sum-exp value:
$$y = \ln \sum_{i=1}^{d} e^{x_i}$$

*Proof:*
Let $x_{max} = \max_{j} x_j$ be the maximum element in the input vector $\mathbf{x} \in \mathbb{R}^d$.
1.  **Incorporate $x_{max}$ inside the summation exponent:**
    We multiply and divide each term by $e^{x_{max}}$:
    $$\sum_{i=1}^{d} e^{x_i} = \sum_{i=1}^{d} e^{x_i - x_{max} + x_{max}} = \sum_{i=1}^{d} e^{x_i - x_{max}} e^{x_{max}}$$

2.  **Factor out the constant exponent term:**
    Since $e^{x_{max}}$ is independent of the summation index $i$, we pull it outside the sum:
    $$\sum_{i=1}^{d} e^{x_i} = e^{x_{max}} \sum_{i=1}^{d} e^{x_i - x_{max}}$$

3.  **Substitute into the logarithm and simplify:**
    $$y = \ln \left( e^{x_{max}} \sum_{i=1}^{d} e^{x_i - x_{max}} \right)$$
    Using the log identity $\ln(ab) = \ln(a) + \ln(b)$:
    $$y = \ln\left(e^{x_{max}}\right) + \ln\left( \sum_{i=1}^{d} e^{x_i - x_{max}} \right)$$
    Since $\ln(e^u) = u$:
    $$y = x_{max} + \ln\left( \sum_{i=1}^{d} e^{x_i - x_{max}} \right) \quad \blacksquare$$

### Stability Analysis
1.  **Overflow Prevention:** By definition, $x_i - x_{max} \le 0$ for all $i$. Therefore, the exponent term $e^{x_i - x_{max}}$ is bounded in $(0, 1]$. Since no exponent is positive, overflow is mathematically impossible.
2.  **Underflow Prevention:** For the index $i^*$ corresponding to the maximum value ($x_{i^*} = x_{max}$), the term is $e^{x_{max} - x_{max}} = e^0 = 1$. The sum is guaranteed to be at least $1.0$, preventing the log input from underflowing to zero.

---

## 4. Concrete Examples

### Example 1: Catastrophic Cancellation
Let $x = 1.0000002$ and $y = 1.0000001$. We compute $z = x - y$ on a machine with $7$ decimal digits of significand precision.
1.  **Represent the values in floating-point format:**
    $$\hat{x} = 1.000000 \quad \text{and} \quad \hat{y} = 1.000000$$
2.  **Perform subtraction:**
    $$\hat{z} = \hat{x} - \hat{y} = 1.000000 - 1.000000 = 0.000000$$
The true difference is $0.0000001$. Due to subtraction of large similar values, all significant digits are canceled, leaving zero.

### Example 2: Log-Sum-Exp Computation
We evaluate the log-sum-exp value for $\mathbf{x} = [1000.0, 999.0]$ on a system where $e^{1000.0}$ overflows.
1.  **Identify the maximum value:**
    $$x_{max} = 1000.0$$
2.  **Apply the LSE formula:**
    $$y = 1000.0 + \ln\left( e^{1000.0 - 1000.0} + e^{999.0 - 1000.0} \right)$$
    $$y = 1000.0 + \ln\left( e^0 + e^{-1} \right)$$
    $$y = 1000.0 + \ln(1 + e^{-1})$$
    Since $e^{-1} \approx 0.367879$:
    $$y = 1000.0 + \ln(1.367879) \approx 1000.0 + 0.31326 = 1000.31326$$
The calculation completes successfully without intermediate overflows.

---

## 5. Applied ML Context

1.  **Softmax Activation Layers:** Implementing softmax ($\sigma(\mathbf{x})_i = e^{x_i - x_{max}} / \sum e^{x_j - x_{max}}$) with maximum-subtraction to prevent overflow in activations.
2.  **Batch Normalization Stabilizers:** Adding a small epsilon constant (e.g. $\epsilon = 10^{-5}$) to the mini-batch variance in the denominator ($1 / \sqrt{\sigma^2 + \epsilon}$) to prevent division-by-zero.
3.  **Naive Bayes Classifiers:** Summing log-probabilities ($\sum \ln P(x_i \mid y)$) rather than multiplying raw likelihoods ($\prod P(x_i \mid y)$) to prevent underflow in high-dimensional feature spaces.
4.  **Deep Network Gradient Clipping:** Enforcing a maximum norm cap on gradients during backpropagation to prevent exploding updates from exceeding floating-point limits.
5.  **Mixed-Precision Loss Scaling:** Scaling down loss values during mixed-precision training to keep small gradient updates within the representable range of FP16 formats.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating numerical stability paths:
*   Draw a flowchart comparing two calculation paths for Softmax:
    1.  **Path A (Unstable Path):** Shows raw inputs $\mathbf{x}$ entering an exponential block ($e^x$). Show a warning sign labeled "Overflow to $\infty$ / Underflow to $0$," resulting in `NaN` outputs.
    2.  **Path B (Stable Path):** Shows a Max-Finder block extracting $x_{max}$. Show $\mathbf{x} - x_{max}$ entering the exponential block, producing values in $(0, 1]$. Show these values dividing cleanly to output a stable probability vector.
*   Add a caption explaining that manual mathematical reformulations (like maximum subtraction) prevent intermediate values from exceeding floating-point limits, preserving precision.
