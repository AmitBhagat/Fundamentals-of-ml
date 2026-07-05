---
title: "Integral Calculus"
description: "Riemann sums, limits of partitions, the Fundamental Theorem of Calculus, integration by parts, and probability densities."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Derivatives", "Fundamental Theorem of Calculus"]
---

<h1 align="center"> Chapter 36: Integral Calculus </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Differential Calculus:** Knowing how to compute derivatives as local slopes.
* **Summation Notation:** Familiarity with the $\sum$ operator.

</div>

## 1. Conceptual Hook

In differential calculus, we isolate variables and evaluate local slopes to optimize parameters. However, in machine learning, we also need to aggregate continuous information globally. For example, how do we calculate the probability of a continuous variable falling within a range, find the expected reward of an agent in reinforcement learning, or calculate the Area Under the Curve (AUC) for model evaluation? To sum up these continuous variations, we use **integral calculus**.

Integral calculus is the mathematics of accumulation. It allows us to reconstruct total quantities from continuous rates of change. If a derivative tells us the instantaneous velocity of a process at a specific millisecond, the integral sums up those velocities over time to find the net distance traveled. It is the core mathematical framework behind continuous probability distributions, expectation formulas, and information entropy.

---

## 2. Formal Definition

### The Riemann Integral
Let $f: [a, b] \to \mathbb{R}$ be a bounded function. Let $P = \{x_0, x_1, \dots, x_n\}$ be a partition of the interval $[a, b]$ such that:
$$a = x_0 < x_1 < \dots < x_n = b$$
The width of the $i$-th sub-interval is $\Delta x_i = x_i - x_{i-1}$. Let $x_i^* \in [x_{i-1}, x_i]$ be an arbitrary sample point.

The **Riemann integral** of $f$ over $[a, b]$ is defined as the limit of the Riemann sum as the mesh size of the partition $\|P\| = \max_i \Delta x_i$ approaches zero:
$$\int_{a}^{b} f(x) \, dx = \lim_{\|P\| \to 0} \sum_{i=1}^{n} f(x_i^*) \Delta x_i$$
provided the limit exists and is independent of the choice of partition and sample points.

### The Fundamental Theorem of Calculus
Let $f$ be continuous on $[a, b]$.
1.  If $F(x) = \int_a^x f(t) dt$, then $F'(x) = f(x)$ for all $x \in (a, b)$.
2.  If $F$ is any antiderivative of $f$ on $[a, b]$ (meaning $F'(x) = f(x)$), then:
    $$\int_{a}^{b} f(x) \, dx = F(b) - F(a)$$

---

## 3. Illustrative Derivation

### Derivation of the Integration by Parts Formula
In probability theory, we often integrate products of functions (for example, when deriving the expectation of a normal distribution $\int x \cdot p(x) dx$). We derive the **Integration by Parts** formula directly from the product rule of differentiation.

*Proof:*
Let $u(x)$ and $v(x)$ be differentiable functions. The product rule for differentiation states:
$$\frac{d}{dx} \left[ u(x)v(x) \right] = u'(x)v(x) + u(x)v'(x)$$
Using alternative notation $u' = \frac{du}{dx}$ and $v' = \frac{dv}{dx}$:
$$\frac{d}{dx} \left[ u(x)v(x) \right] = v(x)\frac{du}{dx} + u(x)\frac{dv}{dx}$$

We integrate both sides of the equation with respect to $x$ over the interval $[a, b]$:
$$\int_{a}^{b} \frac{d}{dx} \left[ u(x)v(x) \right] dx = \int_{a}^{b} v(x)\frac{du}{dx} dx + \int_{a}^{b} u(x)\frac{dv}{dx} dx$$
By the Fundamental Theorem of Calculus, the integral of the derivative on the left-hand side simplifies to the net change in the product function:
$$\int_{a}^{b} \frac{d}{dx} \left[ u(x)v(x) \right] dx = \left[ u(x)v(x) \right]_a^b$$
Substitute this back:
$$\left[ u(x)v(x) \right]_a^b = \int_{a}^{b} v(x) du + \int_{a}^{b} u(x) dv$$
Rearranging the terms to isolate the integral of $u(x) dv$:
$$\int_{a}^{b} u(x) dv = \left[ u(x)v(x) \right]_a^b - \int_{a}^{b} v(x) du \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Definite Area Integration
Evaluate the definite integral of $f(t) = 3t^2 + 2t$ over the interval $[1, 3]$.
1.  **Find the antiderivative $F(t)$:**
    $$F(t) = \int (3t^2 + 2t) dt = t^3 + t^2 + C$$
2.  **Apply the Fundamental Theorem of Calculus:**
    $$\int_{1}^{3} (3t^2 + 2t) dt = \left[ t^3 + t^2 \right]_1^3$$
3.  **Evaluate at the limits:**
    $$F(3) = 3^3 + 3^2 = 27 + 9 = 36$$
    $$F(1) = 1^3 + 1^2 = 1 + 1 = 2$$
    $$\int_{1}^{3} (3t^2 + 2t) dt = F(3) - F(1) = 36 - 2 = 34$$

### Example 2: Normalizing continuous probability distributions
A continuous random variable has a probability density function defined by $p(x) = c e^{-x}$ for $x \ge 0$. Find the normalizing constant $c$ such that $p(x)$ is a valid PDF.
1.  **Set up the normalization constraint:**
    The total area under any probability density function must equal 1:
    $$\int_{0}^{\infty} c e^{-x} dx = 1$$
2.  **Evaluate the improper integral:**
    $$c \lim_{b \to \infty} \int_{0}^{b} e^{-x} dx = 1$$
    Find the antiderivative of $e^{-x}$, which is $-e^{-x}$:
    $$c \lim_{b \to \infty} \left[ -e^{-x} \right]_0^b = 1$$
    $$c \lim_{b \to \infty} \left( -e^{-b} - (-e^0) \right) = 1$$
    Since $\lim_{b \to \infty} e^{-b} = 0$:
    $$c (0 + 1) = 1 \implies c = 1$$
The normalized PDF is $p(x) = e^{-x}$.

---

## 5. Applied ML Context

1.  **Continuous Probability Calculations:** In Bayesian modeling, the probability of a continuous feature $X$ falling within a range $[a, b]$ is calculated by evaluating the definite integral of its density function: $P(a \le X \le b) = \int_a^b p(x) dx$.
2.  **Area Under the ROC Curve (AUC):** The AUC-ROC score is a scalar metric used to evaluate binary classification models. It is computed by integrating the True Positive Rate (TPR) function with respect to the False Positive Rate (FPR): $AUC = \int_0^1 TPR(FPR) d(FPR)$.
3.  **Expected Returns in Reinforcement Learning:** The expected return of a policy trajectory $\tau$ is calculated by integrating the product of the trajectory probability and its reward over all possible paths: $\mathbb{E}_{\tau \sim \pi}[R(\tau)] = \int p(\tau; \pi) R(\tau) d\tau$.
4.  **Differential Entropy:** In information theory, the uncertainty of a continuous distribution is measured using differential entropy, which requires integrating the density function weighted by its log-density: $H(X) = -\int_{-\infty}^{\infty} p(x) \log p(x) dx$.
5.  **Monte Carlo Integration:** Many integrals in Bayesian models (like the marginal likelihood denominator $p(x) = \int p(x|z)p(z)dz$) are analytically intractable. ML researchers approximate them using Monte Carlo integration, averaging random samples: $\int f(x)p(x)dx \approx \frac{1}{N} \sum_{i=1}^N f(x_i)$.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the Riemann sum definition of integration:
*   Show a curved function graph $y = f(x)$ over an interval $[a, b]$.
*   Draw vertical lines partitioning the area under the curve into several narrow vertical rectangles of width $\Delta x$.
*   Highlight a single rectangle. Show its height is determined by the function value at a sample point $f(x_i^*)$, and its area is $f(x_i^*) \Delta x$.
*   Show a second side-by-side graph where the partition is much finer (many more rectangles with a smaller width $\Delta x$). Illustrate how the jagged top edge of the rectangles matches the true curve much more closely.
*   Draw arrows demonstrating that as the partition width $\Delta x$ shrinks to an infinitesimal differential $dx$, the sum of the rectangular areas converges to the exact area under the curve, visualizing the integral $\int_a^b f(x) dx$.
