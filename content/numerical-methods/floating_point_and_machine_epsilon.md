---
title: "Floating-Point Representation and Machine Epsilon"
description: "Binary representations, significand-exponent scaling, IEEE 754 precision limits, machine epsilon derivations, and underflow/overflow controls."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Foundations"]
---

<h1 align="center"> Chapter 98: Floating-Point Representation and Machine Epsilon </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Binary Floating-Point:** Storing real numbers in computers using sign, exponent, and significand (mantissa) bitfields.
* **Underflow and Overflow:** Numerical errors occurring when a number is too close to zero to be represented, or exceeds the maximum representable limit.

</div>

## 1. Conceptual Hook

When writing machine learning code, we tend to treat real numbers as if they live on the infinite, continuous real line $\mathbb{R}$. However, computer hardware is physical and finite. It must represent numbers using a fixed set of bits. To do this, computers use **floating-point arithmetic**—a digital scientific notation in base-2.

This system splits a number into a sign, a significand (the significant digits), and an exponent. To cover a vast range of scales, from subatomic probabilities to astronomical dataset sizes, the spacing between representable numbers is not uniform. Instead, the gap scales with the magnitude of the number. The closer you are to zero, the denser the numbers; the further you go, the wider the gaps.

**Machine Epsilon** is the mathematical measure of this precision limit. It is the gap between $1.0$ and the next larger representable number.

In deep learning, if your parameter updates (gradients) fall below this relative limit, the hardware rounds them to zero. The model effectively freezes, and learning stops. Understanding these floating-point limits is essential for stable, large-scale model training.

---

## 2. Formal Definition

Let $\mathcal{F}(\beta, p, e_{min}, e_{max})$ be a normalized floating-point system, where:
*   **$\beta \in \mathbb{Z}^+$ ($\beta \ge 2$):** The radix or base of the system (typically $\beta = 2$ for digital hardware).
*   **$p \in \mathbb{Z}^+$:** The precision, representing the number of digits in the significand.
*   **$e \in [e_{min}, e_{max}]$:** The integer exponent range.

Any normalized floating-point number $x \in \mathcal{F}$ is written as:
$$x = \pm \left( d_0 + \frac{d_1}{\beta} + \frac{d_2}{\beta^2} + \dots + \frac{d_{p-1}}{\beta^{p-1}} \right) \times \beta^e = \pm \left( \sum_{i=0}^{p-1} d_i \beta^{-i} \right) \times \beta^e$$
where $d_i \in \{0, 1, \dots, \beta-1\}$ and the leading digit is non-zero: $d_0 \neq 0$.

### Machine Epsilon
Let $\text{fl}(r): \mathbb{R} \to \mathcal{F}$ be the rounding operator that maps a real number $r$ to its nearest representable floating-point neighbor in $\mathcal{F}$. **Machine Epsilon** ($\epsilon_{mach}$) is defined as the distance between $1.0$ and its next larger represent not-equal-to-$1.0$ neighbor:
$$\epsilon_{mach} = \min \{ \delta > 0 \mid \text{fl}(1.0 + \delta) > 1.0 \}$$

Depending on the rounding mode, the value is:
*   **Rounding-to-nearest:** $\epsilon_{mach} = \frac{1}{2} \beta^{1-p}$ (often called unit roundoff $u$).
*   **Rounding-by-truncation (chopping):** $\epsilon_{mach} = \beta^{1-p}$.

### IEEE 754 Standard Formats
*   **Single Precision (FP32):** $p = 24$. Under truncation, $\epsilon_{mach} = 2^{-23} \approx 1.19 \times 10^{-7}$.
*   **Double Precision (FP64):** $p = 53$. Under truncation, $\epsilon_{mach} = 2^{-52} \approx 2.22 \times 10^{-16}$.
*   **Half Precision (FP16):** $p = 11$. Under truncation, $\epsilon_{mach} = 2^{-10} \approx 9.77 \times 10^{-4}$.

---

## 3. Illustrative Derivation

### Derivation of Machine Epsilon and Absolute Spacing
We derive the formula for the spacing between adjacent floating-point numbers at a given exponent scale, proving that absolute error scales with magnitude while relative error remains bounded by $\epsilon_{mach}$.

*Proof:*
Let $x \in \mathcal{F}$ be a normalized floating-point number at exponent scale $e$:
$$x = (d_0 . d_1 d_2 \dots d_{p-1})_\beta \times \beta^e$$
The next larger representable number, $x_{next}$, is obtained by incrementing the least significant digit (LSD) of the significand at position $p-1$ by $1$:
$$x_{next} = \left[ (d_0 . d_1 d_2 \dots d_{p-1})_\beta + \beta^{-(p-1)} \right] \times \beta^e$$

1.  **Calculate the absolute spacing ($\Delta x$):**
    $$\Delta x = x_{next} - x = \beta^{-(p-1)} \times \beta^e = \beta^{e - p + 1}$$
    This proves that the absolute gap between representable numbers is not constant; it scales exponentially with the exponent $e$.

2.  **Evaluate at $1.0$ to find Machine Epsilon under truncation:**
    The number $1.0$ is represented as $1.000\dots0 \times \beta^0$, meaning $e = 0$. Substituting $e = 0$ into the spacing formula yields:
    $$\epsilon_{mach} = \Delta(1.0) = \beta^{0 - p + 1} = \beta^{1 - p}$$

3.  **Evaluate the relative spacing:**
    For any normalized number $x$, its magnitude is bounded below by the minimum significand value ($d_0 = 1$ and all other digits zero):
    $$|x| \ge 1.000\dots0 \times \beta^e = \beta^e$$
    The relative spacing is:
    $$\frac{\Delta x}{|x|} \le \frac{\beta^{e - p + 1}}{\beta^e} = \beta^{1 - p} = \epsilon_{mach} \quad \blacksquare$$

This proves that while the absolute gap grows larger for larger numbers, the relative gap between adjacent numbers remains bounded by Machine Epsilon.

---

## 4. Concrete Examples

### Example 1: Toy 4-bit Binary Floating-Point System
We construct a toy system with base $\beta = 2$ and precision $p = 4$.
1.  **Calculate Machine Epsilon under truncation:**
    $$\epsilon_{mach} = 2^{1 - 4} = 2^{-3} = 0.125$$
2.  **Verify the representable numbers near $1.0$:**
    The representation of $1.0$ is $1.000_2 \times 2^0 = 1$. The next larger number is $1.001_2 \times 2^0 = 1 + 2^{-3} = 1.125$.
3.  **Simulate addition underflow:**
    Suppose we attempt to add $\delta = 0.05$ to $1.0$, using round-to-nearest:
    $$1.0 + 0.05 = 1.05$$
    Since $1.05$ is closer to $1.0$ than to $1.125$, the rounding operator rounds it back to $1.0$:
    $$\text{fl}(1.0 + 0.05) = 1.0$$
The small update is completely lost.

### Example 2: FP16 vs. FP32 Machine Epsilon in GPU Calculations
Compare the machine epsilon of Half Precision (FP16) and Single Precision (FP32) under truncation.
*   **FP16 ($\beta=2, p=11$):**
    $$\epsilon_{mach} = 2^{1-11} = 2^{-10} \approx 9.77 \times 10^{-4}$$
*   **FP32 ($\beta=2, p=24$):**
    $$\epsilon_{mach} = 2^{1-24} = 2^{-23} \approx 1.19 \times 10^{-7}$$
FP16 has a machine epsilon roughly $8000$ times larger than FP32. If gradient updates are smaller than $\approx 10^{-3}$, training on FP16 will fail due to underflow, unless a loss scaling factor is applied to shift the gradients into a range with smaller gaps.

---

## 5. Applied ML Context

1.  **Mixed-Precision Training:** Accelerating training by running matrix operations in FP16 or BF16. Since FP16 has a high machine epsilon ($\approx 10^{-3}$), gradient values can underflow to zero. We apply Loss Scaling (multiplying loss by $2^{S}$) to prevent underflow.
2.  **Optimizer Stabilizers:** In Adam and RMSprop, the division stabilizer $\epsilon$ (usually $10^{-8}$) must be set relative to the precision. If training in FP16, a stabilizer of $10^{-8}$ is useless because it is below the format's machine epsilon; it must be bumped to $10^{-4}$ or $10^{-5}$ to prevent underflow.
3.  **Log-Sum-Exp Trick:** Computing softmax values ($e^{x_i} / \sum e^{x_j}$) causes overflow for large $x_i$. Subtracting the maximum value ($x_i - \max(\mathbf{x})$) keeps exponent values negative and in a range where the floating-point spacing is dense.
4.  **Gradient Clipping Bounds:** Restricting gradient vectors to a maximum norm to prevent activations from scaling to large values where absolute floating-point gaps are huge, which would cause coarse updates.
5.  **Glorot/He Weight Initializations:** Setting initial weight variances so that activations are normalized around $1.0$, keeping them in the region where the relative resolution of floating-point numbers is maximized.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating floating-point spacing:
*   Draw a horizontal number line representing the real numbers.
*   Place vertical tick marks representing representable floating-point numbers:
    *   Make the ticks extremely dense near $0$.
    *   Show the spacing between ticks widening as you move away from $0$.
*   At $1.0$, draw a tick mark and show the gap to the next tick mark. Label this gap as $\epsilon_{mach}$.
*   At a larger number (e.g. $10^3$), show that the gap between representable numbers is visibly larger than at $1.0$.
*   Add a callout box showing the "dead zone" $[1.0, 1.0 + \frac{1}{2}\epsilon_{mach}]$ where any real number added to $1.0$ is rounded back to $1.0$, demonstrating precision loss.
*   Add a caption explaining that floating-point numbers have variable spacing, meaning absolute resolution decreases as numbers grow, though relative precision remains constant.
