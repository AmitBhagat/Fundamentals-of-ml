---
title: "Maximum Likelihood Estimation"
description: "Parameter estimation, likelihood functions, log-likelihood transformations, normal parameter derivations, and MLE bias proofs."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Probability Distributions", "Discrete Probability Distributions", "Continuous Probability Distributions", "Mean and Expectation", "Variance"]
---

<h1 align="center"> Chapter 68: Maximum Likelihood Estimation </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Logarithm Rules:** Knowing how the natural logarithm converts products into sums: $\ln(ab) = \ln(a) + \ln(b)$.
* **Optimization Calculus:** Finding maximum points by taking derivatives and setting them to zero.

</div>

## 1. Conceptual Hook

When training a machine learning model, our goal is to find the optimal values for weights, biases, or probability parameters. But how do we mathematically define what makes a parameter "best"? The core philosophy that answers this is **Maximum Likelihood Estimation (MLE)**.

MLE reverses the standard flow of probability. Instead of asking, "Given a known parameter, what is the probability of seeing this data?", it asks, "Given the data we have observed, which parameter value makes this outcome the least surprising?" It is the math of reverse-engineering. By finding the parameter that maximizes the joint probability of our observed dataset, MLE provides the foundational loss functions—such as Binary Cross-Entropy and Mean Squared Error—that drive optimization across linear models, neural networks, and clustering algorithms.

---

## 2. Formal Definition

Let $\mathbf{X} = \{X_1, X_2, \dots, X_n\}$ be a sample of i.i.d. random variables drawn from a probability density or mass function $f(x; \theta)$, where $\theta \in \Theta$ is a vector of unknown parameters.

### The Likelihood Function
The **Likelihood Function** $\mathcal{L}(\theta; \mathbf{x})$ is the joint probability density of the observed data vector $\mathbf{x} = \{x_1, \dots, x_n\}$ evaluated as a function of the parameter $\theta$:
$$\mathcal{L}(\theta; \mathbf{x}) = \prod_{i=1}^{n} f(x_i; \theta)$$

### The Log-Likelihood Function
Because multiplying many small probabilities causes numerical underflow in computer arithmetic, we maximize the natural logarithm of the likelihood, the **Log-Likelihood** $\ell(\theta; \mathbf{x})$. Since the logarithm is a strictly increasing function, the values of $\theta$ that maximize $\ell(\theta; \mathbf{x})$ are identical to those that maximize $\mathcal{L}(\theta; \mathbf{x})$:
$$\ell(\theta; \mathbf{x}) = \ln \mathcal{L}(\theta; \mathbf{x}) = \sum_{i=1}^{n} \ln f(x_i; \theta)$$

The Maximum Likelihood Estimator (MLE) is defined as:
$$\hat{\theta}_{MLE} = \arg\max_{\theta \in \Theta} \ell(\theta; \mathbf{x})$$

### The Score Function
To find the maximum, we compute the **Score Function** $S(\theta)$, which is the gradient of the log-likelihood with respect to $\theta$:
$$S(\theta) = \nabla_{\theta} \ell(\theta; \mathbf{x}) = \mathbf{0}$$
We verify that the solution is a local maximum by checking that the Hessian matrix of second partial derivatives is negative definite:
$$\mathbf{H}(\theta) = \nabla_{\theta}^2 \ell(\theta; \mathbf{x}) \prec 0$$

---

## 3. Illustrative Derivation

### Derivation of the MLE for a Normal Distribution
We derive the maximum likelihood estimators for both the mean $\mu$ and variance $\sigma^2$ of a Normal distribution $\mathcal{N}(\mu, \sigma^2)$ from first principles.

Let $X_1, X_2, \dots, X_n$ be i.i.d. random variables sampled from $\mathcal{N}(\mu, \sigma^2)$. The PDF is:
$$f(x_i; \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right)$$

1.  **Formulate the Likelihood and Log-Likelihood:**
    $$\mathcal{L}(\mu, \sigma^2; \mathbf{x}) = \prod_{i=1}^{n} \left(2\pi\sigma^2\right)^{-1/2} \exp\left( -\frac{(x_i - \mu)^2}{2\sigma^2} \right) = \left(2\pi\sigma^2\right)^{-n/2} \exp\left( -\sum_{i=1}^{n} \frac{(x_i - \mu)^2}{2\sigma^2} \right)$$
    Taking the natural logarithm yields:
    $$\ell(\mu, \sigma^2; \mathbf{x}) = -\frac{n}{2}\ln(2\pi) - \frac{n}{2}\ln(\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^{n}(x_i - \mu)^2$$

2.  **Derive the MLE for the mean $\mu$:**
    Take the partial derivative of $\ell$ with respect to $\mu$ and set to zero:
    $$\frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2} \sum_{i=1}^{n} (x_i - \mu) = 0$$
    Multiply by $\sigma^2$:
    $$\sum_{i=1}^{n} x_i - n\mu = 0 \implies \hat{\mu}_{MLE} = \frac{1}{n} \sum_{i=1}^{n} X_i \quad \blacksquare$$

3.  **Derive the MLE for the variance $\sigma^2$:**
    Let $v = \sigma^2$. Differentiate the log-likelihood with respect to $v$ and set to zero:
    $$\frac{\partial \ell}{\partial v} = -\frac{n}{2v} + \frac{1}{2v^2} \sum_{i=1}^{n} (x_i - \mu)^2 = 0$$
    Multiply by $2v^2$:
    $$-n v + \sum_{i=1}^{n} (x_i - \mu)^2 = 0 \implies v = \frac{1}{n} \sum_{i=1}^{n} (x_i - \mu)^2$$
    Substitute the estimator $\hat{\mu}_{MLE}$ for $\mu$:
    $$\hat{\sigma}^2_{MLE} = \frac{1}{n} \sum_{i=1}^{n} (X_i - \hat{\mu}_{MLE})^2 \quad \blacksquare$$
    *Note:* This MLE variance estimator is biased because $\mathbb{E}[\hat{\sigma}^2_{MLE}] = \frac{n-1}{n}\sigma^2$, which explains why sample variance formulas use Bessel's correction divisor $(n-1)$ to ensure unbiasedness.

---

## 4. Concrete Examples

### Example 1: Quiet Hours Audit (Bernoulli Trial)
You track quiet ($x=1$) vs. noisy ($x=0$) study sessions over $n=10$ hours, observing 8 quiet sessions and 2 noisy ones. Assuming a Bernoulli distribution with parameter $p$:
1.  **Formulate Log-Likelihood:**
    $$\mathcal{L}(p) = p^8(1-p)^2 \implies \ell(p) = 8\ln(p) + 2\ln(1-p)$$
2.  **Maximize with respect to $p$:**
    $$\frac{d\ell}{dp} = \frac{8}{p} - \frac{2}{1-p} = 0 \implies 8(1-p) = 2p \implies 8 - 8p = 2p \implies 10p = 8$$
    $$\hat{p}_{MLE} = 0.8$$
The most likely probability of a quiet study session is $80\%$.

### Example 2: Normal Focus Duration (Unknown Mean and Variance)
You record focus session lengths for two days ($n=2$): $60$ minutes and $100$ minutes.
1.  **Calculate the MLE Mean:**
    $$\hat{\mu}_{MLE} = \frac{60 + 100}{2} = 80 \text{ minutes}$$
2.  **Calculate the MLE Variance:**
    $$\hat{\sigma}^2_{MLE} = \frac{(60-80)^2 + (100-80)^2}{2} = \frac{(-20)^2 + 20^2}{2} = \frac{400 + 400}{2} = 400 \text{ minutes}^2$$
The MLE standard deviation is $\sqrt{400} = 20$ minutes.

---

## 5. Applied ML Context

1.  **Logistic Regression Classification:** The optimal weights of a logistic regression classifier are obtained by maximizing the joint Bernoulli likelihood of the binary class labels, which is equivalent to minimizing the Binary Cross-Entropy loss.
2.  **Neural Network Training:** For multi-class classifications using a Softmax output layer, backpropagation updates weights by minimizing the Negative Log-Likelihood (NLL) of the categorical targets.
3.  **Gaussian Mixture Models (GMM):** The Expectation-Maximization (EM) algorithm uses MLE in its M-step to update the means, covariances, and mixing coefficients of clustering distributions.
4.  **Language Token Modeling:** Large language models calculate parameter updates by using MLE to maximize the probability of predicting the next token $w_t$ given a sequence of context tokens: $P(w_t \mid w_1, \dots, w_{t-1})$.
5.  **Linear Regression Parameter Fitting:** Under the assumption that the prediction errors (residuals) are normally distributed with zero mean, minimizing the Mean Squared Error (MSE) is mathematically identical to finding the MLE for weight coefficients.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating the likelihood maximization:
*   Draw a 2D Cartesian coordinate plot:
    *   **Horizontal Axis:** The parameter space $\theta$.
    *   **Vertical Axis:** The log-likelihood function value $\ell(\theta; \mathbf{x})$.
*   Draw a smooth, continuous, concave-down curve that starts low, rises to a single local maximum, and descends.
*   Draw a vertical dashed line from the peak of the curve down to the horizontal axis. Label the intersection point as $\hat{\theta}_{MLE}$.
*   Add a tangent line resting on the peak of the curve showing a slope of zero, with a label pointing out that at the MLE point: $\frac{d\ell}{d\theta} = 0$, visually demonstrating how optimization calculus identifies the most likely parameters.
