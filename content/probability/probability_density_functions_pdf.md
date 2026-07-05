---
title: "Probability Density Functions (PDF)"
description: "Continuous random variables, probability densities, Gaussian normalization proofs, and continuous likelihoods."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Scalars", "Vectors", "Integral Calculus", "Jacobian Matrix", "Probability Distributions", "Random Variables"]
---

<h1 align="center"> Chapter 53: Probability Density Functions (PDF) </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Continuous Random Variables:** Variables defined on an uncountable interval of real numbers.
* **Double Integrals:** Basic comfort with integrating over two-dimensional regions.

</div>

## 1. Conceptual Hook

In machine learning, when we deal with continuous variables—like the weight of a neural network, the physical dimensions of an object, or audio frequencies—the probability of obtaining any single, infinitely precise value (like a sweet box weighing exactly $452.342158...$ grams) is mathematically zero. If we attempted to calculate individual probabilities, our model would assign $0$ to every event, rendering statistical learning impossible. To model continuous uncertainty, we use **Probability Density Functions (PDFs)**.

A PDF does not represent the probability of a single point. Instead, it describes the **concentration** or density of probability across a continuous spectrum. We obtain actual probabilities by integrating the PDF over an interval, measuring the area under the curve. Think of a PDF as describing the thickness of butter spread across a slice of bread: the height of the butter at one coordinate is its density, but you only consume a measurable amount of butter when you look at a slice of non-zero width.

---

## 2. Formal Definition

Let $X$ be a continuous random variable. A integrable function $f_X: \mathbb{R} \to \mathbb{R}$ is the **Probability Density Function (PDF)** of $X$ if it satisfies the following three conditions:
1.  **Non-negativity:** The probability density must be non-negative everywhere:
    $$f_X(x) \ge 0 \quad \forall x \in \mathbb{R}$$
2.  **Normalization:** The total area under the entire density curve must equal exactly 1 (100% of the probability budget):
    $$\int_{-\infty}^{\infty} f_X(x) dx = 1$$
3.  **Interval Probability:** The probability that the random variable $X$ falls within a Borel set $B \subseteq \mathbb{R}$ is the integral of the PDF over $B$. For an interval $[a, b]$:
    $$P(a \le X \le b) = \int_{a}^{b} f_X(x) dx$$

### Relation to the Cumulative Distribution Function (CDF)
The CDF $F_X(x)$ represents the accumulated probability up to point $x$:
$$F_X(x) = P(X \le x) = \int_{-\infty}^{x} f_X(t) dt$$
If $F_X(x)$ is continuous and differentiable, then by the Fundamental Theorem of Calculus, the PDF is the first derivative of the CDF:
$$f_X(x) = \frac{d}{dx} F_X(x)$$

---

## 3. Illustrative Derivation

### Derivation of the Gaussian (Normal) Normalization Constant
The most famous continuous PDF in machine learning is the Gaussian distribution: $f(x) = C e^{-\frac{x^2}{2}}$. We derive the normalization constant $C$ using polar coordinate transformation, proving that $C = \frac{1}{\sqrt{2\pi}}$.

*Proof:*
To ensure $f(x)$ is a valid PDF, we must satisfy the normalization axiom:
$$\int_{-\infty}^{\infty} C e^{-\frac{x^2}{2}} dx = 1 \implies C \int_{-\infty}^{\infty} e^{-\frac{x^2}{2}} dx = 1$$
Let the Gaussian integral be $I = \int_{-\infty}^{\infty} e^{-\frac{x^2}{2}} dx$. We evaluate $I^2$ by writing it as the product of two independent integrals:
$$I^2 = \left( \int_{-\infty}^{\infty} e^{-\frac{x^2}{2}} dx \right) \left( \int_{-\infty}^{\infty} e^{-\frac{y^2}{2}} dy \right) = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} e^{-\frac{x^2 + y^2}{2}} dx dy$$

This is a double integral over the entire 2D Cartesian plane. We evaluate this by transforming to polar coordinates:
$$x = r \cos\theta, \quad y = r \sin\theta \implies x^2 + y^2 = r^2$$
The Jacobian determinant of this transformation is $r$, meaning the area differential scales as:
$$dx dy = r dr d\theta$$
The integration bounds change from the infinite Cartesian grid to the polar plane: $0 \le r < \infty$ and $0 \le \theta < 2\pi$.
$$I^2 = \int_{0}^{2\pi} \int_{0}^{\infty} e^{-\frac{r^2}{2}} r dr d\theta$$

First, evaluate the inner integral w.r.t $r$ using u-substitution:
Let $u = \frac{r^2}{2} \implies du = r dr$. The integration limits remain $0$ to $\infty$.
$$\int_{0}^{\infty} e^{-\frac{r^2}{2}} r dr = \int_{0}^{\infty} e^{-u} du = \left[ -e^{-u} \right]_0^{\infty} = 0 - (-1) = 1$$
Now, substitute this result back into the double integral:
$$I^2 = \int_{0}^{2\pi} 1 d\theta = [ \theta ]_0^{2\pi} = 2\pi$$
Taking the square root:
$$I = \sqrt{2\pi}$$
Substitute $I = \sqrt{2\pi}$ back into our normalization equation:
$$C \cdot I = 1 \implies C \cdot \sqrt{2\pi} = 1 \implies C = \frac{1}{\sqrt{2\pi}} \quad \blacksquare$$

---

## 4. Concrete Examples

### Example 1: Piecewise Quadratic Density
A continuous random variable $X$ has PDF defined by $f(x) = C x^2$ for $0 \le x \le 2$, and $f(x) = 0$ otherwise. Find the constant $C$ and calculate the probability $P(1.5 \le X \le 2)$.
1.  **Solve for $C$ using the normalization constraint:**
    $$\int_{0}^{2} C x^2 dx = 1 \implies C \left[ \frac{x^3}{3} \right]_0^2 = 1$$
    $$C \left( \frac{8}{3} - 0 \right) = 1 \implies C = \frac{3}{8}$$
2.  **Calculate the interval probability:**
    $$P(1.5 \le X \le 2) = \int_{1.5}^{2} \frac{3}{8} x^2 dx = \frac{3}{8} \left[ \frac{x^3}{3} \right]_{1.5}^2 = \frac{1}{8} \left[ x^3 \right]_{1.5}^2$$
    $$P(1.5 \le X \le 2) = \frac{1}{8} \left( 2^3 - 1.5^3 \right) = \frac{1}{8} (8 - 3.375) = \frac{4.625}{8} = 0.578125$$
There is approximately a $57.81\%$ chance that $X$ lies in the interval $[1.5, 2]$.

### Example 2: Exponential Density
An exponential PDF is defined as $f(x) = 0.2 e^{-0.2 x}$ for $x \ge 0$. Find the probability that $X$ falls between $3$ and $6$.
1.  **Set up the integral:**
    $$P(3 \le X \le 6) = \int_{3}^{6} 0.2 e^{-0.2 x} dx$$
2.  **Evaluate:**
    $$P(3 \le X \le 6) = \left[ -e^{-0.2 x} \right]_3^6 = -e^{-1.2} - (-e^{-0.6}) = e^{-0.6} - e^{-1.2}$$
    $$P(3 \le X \le 6) \approx 0.5488 - 0.3012 = 0.2476$$

---

## 5. Applied ML Context

1.  **Gaussian Mixture Models (GMMs):** GMMs represent cluster distributions as a weighted combination of multiple continuous multivariate Gaussian PDFs. Data points are clustered based on their relative densities.
2.  **Anomaly Detection:** We fit a multidimensional PDF to normal data. For any new query $x$, we evaluate its density. If $f(x) < \epsilon$ (where $\epsilon$ is a threshold), the query is classified as an anomaly.
3.  **Kullback-Leibler (KL) Divergence:** KL divergence measures the distance between two continuous distributions by integrating their PDFs: $D_{KL}(P \parallel Q) = \int_{-\infty}^{\infty} p(x) \log \frac{p(x)}{q(x)} dx$.
4.  **Maximum Likelihood Estimation (MLE):** MLE estimates parameters by maximizing the joint likelihood (PDF product) of independent data points: $\theta_{MLE} = \arg\max_\theta \prod_{i=1}^N f(x_i; \theta)$.
5.  **Kernel Density Estimation (KDE):** KDE is a non-parametric method used in visualization to estimate the continuous PDF of features by summing up local Gaussian "kernels" placed at each data point.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating probability density concepts:
*   Draw a smooth, continuous PDF curve $y = f(x)$.
*   Add a vertical label pointing to the peak of the curve. Highlight that the vertical axis represents "Probability Density," and the height of the curve *can* exceed $1.0$ (unlike discrete probabilities) if the distribution is narrow.
*   Draw an infinitesimal interval $[x_0, x_0 + dx]$ on the horizontal axis. Draw a thin vertical rectangle of height $f(x_0)$ and width $dx$. Label the area of this rectangle as the probability element: $dP = f(x_0) dx$.
*   Draw two markers $a$ and $b$ on the horizontal axis. Shade the entire region under the curve between $a$ and $b$. Label this shaded area as the cumulative interval probability: $P(a \le X \le b) = \int_a^b f(x) dx$, visually demonstrating that probability in continuous spaces is represented by area, not height.
