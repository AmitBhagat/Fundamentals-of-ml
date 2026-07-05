---
title: "Information Geometry"
description: "Probability manifolds, the Fisher-Rao metric, and the derivation of the Natural Gradient."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Foundations", "Entropy", "Multivariate Calculus"]
---

<h1 align="center"> Chapter 78: Information Geometry </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **KL Divergence:** Measuring the information-theoretic divergence between two probability distributions.
* **Hessian Matrix:** Curvature of multivariate functions.
* **Vector Calculus:** Gradients and expectation operators over continuous distributions.

</div>

## Analogy

Think of information geometry as **navigating a sailboat across a windy, curved ocean where distances stretch based on how much the sails catch the wind**.

In standard flat land (Euclidean space), a distance of "one step" is always exactly one meter, whether you are walking north, south, or on sand. 

But on the **probability ocean**, a distance step represents how much your model's **predictions** change, not how much you tweak the dial of the steering wheel (the parameters). 

If your sailboat is near a shallow reef where a tiny turn of the wheel will crash the boat (equivalent to a probability output shifting from $0.99$ to $0.01$), then that tiny turn is a massive "distance" in information space. If you are in the deep, open ocean where a huge turn of the wheel does almost nothing to your course (probability shifting from $0.50$ to $0.51$), then that turn is a tiny distance. The **Fisher Information Matrix** is the local underwater topography map of this ocean, and the **Natural Gradient** is the steering algorithm that adjusts your wheel turns so that the sailboat makes steady, safe progress regardless of how turbulent the local currents are.

## The Math Link

### 1. The Probability Manifold and the Fisher Metric
Let $\mathcal{M} = \{ p(x \mid \theta) \mid \theta \in \Theta \subset \mathbb{R}^d \}$ be a parametric family of probability distributions. We view $\mathcal{M}$ as a Riemannian manifold, where each point corresponds to a distribution. The **Fisher Information Matrix (FIM)** $G(\theta) \in \mathbb{R}^{d \times d}$ serves as the Riemannian metric tensor:
$$G(\theta)_{ij} = \mathbb{E}_{p(x \mid \theta)} \left[ \frac{\partial \log p(x \mid \theta)}{\partial \theta_i} \frac{\partial \log p(x \mid \theta)}{\partial \theta_j} \right]$$
The FIM defines the inner product of tangent vectors on the manifold, providing a local measure of distance.

### 2. KL Divergence as the Local Metric
The Kullback-Leibler (KL) divergence measures the divergence between $p(x \mid \theta)$ and a nearby distribution $p(x \mid \theta + d\theta)$. Using a Taylor expansion of the KL divergence around $d\theta = 0$:
$$D_{KL}(p(x \mid \theta) \parallel p(x \mid \theta + d\theta)) = \int p(x \mid \theta) \log \frac{p(x \mid \theta)}{p(x \mid \theta + d\theta)} \, dx$$
Expanding $\log p(x \mid \theta + d\theta)$ to second order:
$$\log p(x \mid \theta + d\theta) \approx \log p(x \mid \theta) + \nabla_\theta \log p(x \mid \theta)^T d\theta + \frac{1}{2} d\theta^T \nabla^2_\theta \log p(x \mid \theta) d\theta$$
Substituting this back into the KL integral:
$$D_{KL}(p(x \mid \theta) \parallel p(x \mid \theta + d\theta)) \approx -\mathbb{E}_{p(x \mid \theta)} \left[ \nabla_\theta \log p(x \mid \theta)^T d\theta + \frac{1}{2} d\theta^T \nabla^2_\theta \log p(x \mid \theta) d\theta \right]$$
Using the identity $\mathbb{E}_{p(x \mid \theta)}[\nabla_\theta \log p(x \mid \theta)] = 0$, the first-order term vanishes. Under regularity conditions, the expectation of the Hessian of the log-likelihood is the negative FIM:
$$\mathbb{E}_{p(x \mid \theta)} \left[ \nabla^2_\theta \log p(x \mid \theta) \right] = -G(\theta)$$
Thus, we obtain the local quadratic approximation:
$$D_{KL}(p(x \mid \theta) \parallel p(x \mid \theta + d\theta)) \approx \frac{1}{2} d\theta^T G(\theta) d\theta$$
The FIM is the Hessian of the KL divergence.

---

## Proof-Based Exercises

### Exercise 1: Lagrangian Derivation of the Natural Gradient Update
**Theorem:** Prove that the update step $d\theta$ that minimizes a loss $L(\theta)$ subject to a constraint on the KL divergence $D_{KL}(p(x \mid \theta) \parallel p(x \mid \theta + d\theta)) \le \epsilon$ is given by $d\theta \propto -G(\theta)^{-1} \nabla_\theta L(\theta)$.

*Proof:*
Using the local quadratic approximation of the KL divergence, the optimization problem is:
$$\min_{d\theta} L(\theta) + \nabla_\theta L(\theta)^T d\theta \quad \text{subject to} \quad \frac{1}{2} d\theta^T G(\theta) d\theta \le \epsilon$$
We formulate the Lagrangian with multiplier $\lambda \ge 0$:
$$\mathcal{L}(d\theta, \lambda) = L(\theta) + \nabla_\theta L(\theta)^T d\theta + \lambda \left( \frac{1}{2} d\theta^T G(\theta) d\theta - \epsilon \right)$$
Take the derivative with respect to $d\theta$ and set it to zero:
$$\nabla_{d\theta} \mathcal{L} = \nabla_\theta L(\theta) + \lambda G(\theta) d\theta = 0$$
Solving for $d\theta$ (since $G(\theta)$ is positive definite and thus invertible):
$$d\theta = -\frac{1}{\lambda} G(\theta)^{-1} \nabla_\theta L(\theta)$$
By defining the learning rate $\eta = \frac{1}{\lambda}$, we obtain the Natural Gradient step:
$$d\theta = -\eta G(\theta)^{-1} \nabla_\theta L(\theta)$$
This completes the derivation. $\blacksquare$

---

## Let's Run the Numbers

### Example: Fisher Information of a Bernoulli Distribution

Let $X \sim \text{Bernoulli}(\theta)$ where $\theta \in (0, 1)$ represents the success probability. The probability mass function is:
$$p(x \mid \theta) = \theta^x (1-\theta)^{1-x} \quad (x \in \{0, 1\})$$

1. **Calculate the Log-Likelihood:**
   $$\log p(x \mid \theta) = x \log \theta + (1-x) \log(1-\theta)$$

2. **Differentiate with respect to $\theta$:**
   $$\frac{\partial \log p(x \mid \theta)}{\partial \theta} = \frac{x}{\theta} - \frac{1-x}{1-\theta} = \frac{x - \theta}{\theta(1-\theta)}$$

3. **Compute the Fisher Information $G(\theta)$:**
   $$G(\theta) = \mathbb{E}_{p(x \mid \theta)} \left[ \left( \frac{\partial \log p(x \mid \theta)}{\partial \theta} \right)^2 \right] = \mathbb{E} \left[ \frac{(X - \theta)^2}{\theta^2(1-\theta)^2} \right]$$
   Since $\mathbb{E}[(X-\theta)^2] = \text{Var}(X) = \theta(1-\theta)$:
   $$G(\theta) = \frac{\theta(1-\theta)}{\theta^2(1-\theta)^2} = \frac{1}{\theta(1-\theta)}$$

4. **Interpret the Curvature:**
   * If $\theta = 0.5$, then $G(0.5) = 4$.
   * If $\theta = 0.01$, then $G(0.01) \approx 101$.
   The information space is $25\times$ more sensitive near the boundaries ($\theta \to 0$ or $1$) than in the center. A standard gradient step of size $0.05$ at $\theta = 0.5$ shifts the predictions slightly, but the same step at $\theta = 0.01$ would blow up the model's log-likelihood, demonstrating why the natural gradient scale $G(\theta)^{-1}$ is necessary for stable learning.

---

## ML Applications

1. **Natural Gradient Descent (NGD):**
   NGD accelerates training in neural networks by taking the steepest descent direction along the manifold of network predictions rather than parameter coordinates, preventing slow convergence in flat plateau regions of the loss landscape.
2. **Trust Region Policy Optimization (TRPO):**
   In reinforcement learning, policy updates are highly sensitive. TRPO restricts policy updates by placing a hard constraint on the average KL divergence between the old policy $\theta_{old}$ and the new policy $\theta$:
   $$\mathbb{E}_{s \sim \rho} \left[ D_{KL}(\pi_{\theta_{old}}(\cdot|s) \parallel \pi_\theta(\cdot|s)) \right] \le \delta$$
   This constraint is solved using conjugate gradient updates to approximate the action of the inverse FIM.
3. **Kronecker-Factored Approximate Curvature (K-FAC):**
   Inverting the FIM for deep networks with millions of parameters is computationally prohibitive ($O(d^3)$). K-FAC approximates the FIM by assuming layer-wise activations and backpropagated derivatives are independent, factoring the FIM into Kronecker products of small matrices:
   $$G \approx A \otimes S$$
   allowing cheap inversion in $O(d)$ time.
4. **Diffusion Models:**
   Continuous-time diffusion models leverage score-matching objectives. The score function $\nabla_x \log p_t(x)$ represents the gradient of the log-density, guiding the denoising trajectory along the high-density manifolds of the probability landscape.

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** When implementing Natural Gradient approximations, the empirical Fisher matrix (which uses training labels rather than sampling from the model's distribution) is often used. Be careful: the empirical Fisher can overfit to the training labels and fail to approximate the true FIM, leading to poor optimization updates. Always verify if your implementation samples model predictions $y \sim p(y \mid x, \theta)$ to compute the true FIM.

</div>
