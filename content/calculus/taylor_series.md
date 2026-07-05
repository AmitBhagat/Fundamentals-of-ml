---
title: "Taylor Series"
description: "Infinite power series, Maclaurin expansions, Taylor's theorem, convergence proofs, and local quadratic approximations."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Derivatives", "Partial Derivatives"]
---

<h1 align="center"> Chapter 39: Taylor Series </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Higher-Order Derivatives:** Knowing how to compute second-order and third-order derivatives.
* **Sequences and Series:** Understanding power series convergence concepts.

</div>

## 1. Conceptual Hook

In machine learning, we frequently encounter complex, highly non-linear functions (like neural network loss landscapes or probability density functions) that are analytically intractable to optimize or integrate directly. How do we make these complex curves manageable? We break them down into simple polynomials using the **Taylor series**.

The Taylor series is the ultimate mathematical translator. It takes any infinitely differentiable function and represents it as an infinite sum of polynomial terms calculated from the function's derivatives at a single anchor point. This allows us to take a highly complex function and approximate it locally with a simple line (first-order approximation) or a parabola (second-order approximation). The Taylor series acts as the mathematical engine behind optimization algorithms (like Newton's method) and model interpretability techniques, allowing us to approximate global complexity with local simplicity.

---

## 2. Formal Definition

Let $f: \mathbb{R} \to \mathbb{R}$ be an infinitely differentiable function in a neighborhood of a point $a \in \mathbb{R}$. The **Taylor series** of $f$ centered at $a$ is the power series:
$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x-a)^n$$
where $f^{(n)}(a)$ represents the $n$-th derivative of $f$ evaluated at $a$ (with $f^{(0)}(a) = f(a)$ and $0! = 1$).

When the series is centered at $a = 0$, it is specifically referred to as the **Maclaurin series**:
$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(0)}{n!} x^n$$

### Taylor Polynomials and Remainder
For practical computation, we truncate the infinite series at a finite degree $k$. The resulting function is the $k$-th degree **Taylor polynomial**, $P_k(x)$:
$$P_k(x) = \sum_{n=0}^{k} \frac{f^{(n)}(a)}{n!} (x-a)^n$$

**Taylor's Theorem:** If $f$ is $k+1$ times differentiable, then for any $x$ in the neighborhood of $a$:
$$f(x) = P_k(x) + R_k(x)$$
where $R_k(x)$ is the remainder (approximation error). Under the **Lagrange form of the remainder**:
$$R_k(x) = \frac{f^{(k+1)}(c)}{(k+1)!} (x-a)^{k+1}$$
for some point $c$ strictly between $a$ and $x$.

---

## 3. Illustrative Derivation

### Derivation of the Exponential Maclaurin Series and Convergence Proof
We derive the Maclaurin series expansion of the exponential function $f(x) = e^x$, and prove that the series converges to the function for all real numbers $x$.

*Step 1: Compute coefficients:*
The exponential function is unique because it is its own derivative:
$$f(x) = e^x \implies f^{(n)}(x) = e^x \quad \forall n \ge 0$$
To find the Maclaurin series, we center the expansion at $a = 0$:
$$f^{(n)}(0) = e^0 = 1 \quad \forall n \ge 0$$
Substitute these derivative values into the Maclaurin formula:
$$e^x = \sum_{n=0}^{\infty} \frac{f^{(n)}(0)}{n!} x^n = \sum_{n=0}^{\infty} \frac{1}{n!} x^n = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$$

*Step 2: Prove convergence using the Ratio Test:*
To find the values of $x$ for which this infinite series converges, we apply the Ratio Test. Let the $n$-th term of the series be $u_n = \frac{x^n}{n!}$. We evaluate the limit of the absolute ratio:
$$L = \lim_{n \to \infty} \left| \frac{u_{n+1}}{u_n} \right|$$
$$L = \lim_{n \to \infty} \left| \frac{x^{n+1}}{(n+1)!} \cdot \frac{n!}{x^n} \right|$$
Using factorial properties $(n+1)! = (n+1) \cdot n!$:
$$L = \lim_{n \to \infty} \left| \frac{x \cdot x^n}{(n+1)n!} \cdot \frac{n!}{x^n} \right| = \lim_{n \to \infty} \frac{|x|}{n+1}$$
For any fixed, finite real number $x \in \mathbb{R}$, as $n$ approaches infinity, the denominator $n+1$ grows without bound, yielding:
$$L = 0$$
Since the limit $L = 0$ is strictly less than 1 for all real numbers $x$:
$$L < 1 \quad \forall x \in \mathbb{R}$$
By the Ratio Test, the series converges absolutely for all $x \in \mathbb{R}$. The radius of convergence is $R = \infty$. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Maclaurin Expansion of $\ln(1+x)$
Find the third-degree Maclaurin polynomial $P_3(x)$ for $f(x) = \ln(1+x)$.
1.  **Evaluate derivatives at $a = 0$:**
    *   $f(x) = \ln(1+x) \implies f(0) = \ln(1) = 0$
    *   $f'(x) = (1+x)^{-1} \implies f'(0) = 1$
    *   $f''(x) = -(1+x)^{-2} \implies f''(0) = -1$
    *   $f'''(x) = 2(1+x)^{-3} \implies f'''(0) = 2$
2.  **Apply Maclaurin polynomial formula:**
    $$P_3(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \frac{f'''(0)}{3!}x^3$$
    $$P_3(x) = 0 + (1)x + \frac{-1}{2}x^2 + \frac{2}{6}x^3 = x - \frac{x^2}{2} + \frac{x^3}{3}$$
This polynomial approximates $\ln(1+x)$ very well for values of $x$ close to $0$.

### Example 2: Maclaurin Expansion of $\sin(x)$
Find the third-degree Maclaurin polynomial for $f(x) = \sin(x)$.
1.  **Evaluate derivatives at $a = 0$:**
    *   $f(x) = \sin(x) \implies f(0) = 0$
    *   $f'(x) = \cos(x) \implies f'(0) = 1$
    *   $f''(x) = -\sin(x) \implies f''(0) = 0$
    *   $f'''(x) = -\cos(x) \implies f'''(0) = -1$
2.  **Formulate the polynomial:**
    $$P_3(x) = f(0) + f'(0)x + \frac{f''(0)}{2}x^2 + \frac{f'''(0)}{6}x^3$$
    $$P_3(x) = 0 + 1x + 0 - \frac{1}{6}x^3 = x - \frac{x^3}{6}$$

---

## 5. Applied ML Context

1.  **Newton's Method in Optimization:** Newton's optimization steps are derived from a second-order Taylor expansion of the loss function $L(\theta)$ around the current weights $\theta_t$: $L(\theta_t + h) \approx L(\theta_t) + \nabla L(\theta_t)^T h + \frac{1}{2} h^T H_L(\theta_t) h$. Finding the minimum of this quadratic approximation leads directly to the update rule: $h = -H^{-1} \nabla L(\theta_t)$.
2.  **Activation Function Approximations:** In low-power Edge AI or microcontroller environments, transcendental functions like $\tanh(x)$ or $\text{sigmoid}(x)$ are slow to compute. Developers replace them with low-order Taylor polynomials to save computational cycles during forward passes.
3.  **Automatic Differentiation (Autograd):** Gradient descent relies on a first-order Taylor approximation where we assume the change in loss $\Delta L$ satisfies $\Delta L \approx \nabla L(\theta)^T \Delta \theta$.
4.  **Bayesian Laplace Approximation:** To estimate parameter posterior uncertainty, the log-posterior $\log p(\theta | D)$ is expanded as a second-order Taylor series around the MAP estimate $\theta_{MAP}$. Since the gradient vanishes at the mode, this yields a multivariate Gaussian approximation with covariance $H^{-1}$.
5.  **Explainable AI (LIME Surrogates):** Local Interpretable Model-agnostic Explanations (LIME) explain complex black-box model predictions by training a simple linear surrogate model locally around the prediction coordinates, acting like a first-order Taylor approximation of the model's boundary.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the convergence of Taylor polynomials:
*   Draw the curve of the exponential function $f(x) = e^x$.
*   Plot the anchor point $(0, 1)$ on the curve.
*   Draw the following successive polynomial approximations matching the curve at $(0, 1)$:
    1.  A tangent straight line $P_1(x) = 1 + x$ (first-order linear approximation).
    2.  A tangent parabola $P_2(x) = 1 + x + \frac{x^2}{2}$ (second-order quadratic approximation).
    3.  A cubic curve $P_3(x) = 1 + x + \frac{x^2}{2} + \frac{x^3}{6}$ (third-order approximation).
*   Illustrate how each subsequent higher-degree polynomial matches the true curve over a wider horizontal interval, visually demonstrating how Taylor polynomials converge to the function.
