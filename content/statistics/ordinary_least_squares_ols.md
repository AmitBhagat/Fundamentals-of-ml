---
title: "Ordinary Least Squares (OLS)"
description: "Mastering the mathematical foundations of artificial intelligence."
complexity: "Intermediate"
estimated_time: "20 min"
---

<h1 align="center"> Chapter 69: Ordinary Least Squares (OLS) </h1>

---




<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite

- **Linear Algebra Fundamentals:** Comfort with matrix-vector multiplication and the concept of a transpose.
- **Calculus Basics:** Understanding that the minimum of a function is found where the derivative (gradient) equals zero.
- **Summation Notation:** Familiarity with the $\sum$ operator for aggregating errors.

</div>

---

## Analogy

Think about the logistical nightmare of booking a 5-a-side football turf. You have a target—a specific time slot on a specific Friday night—and you need exactly 10 players to show up so the cost splits perfectly and the game actually happens.

Ordinary Least Squares is the logic you use to manage the "gap" between your ideal plan and the messy reality of people's schedules. You are trying to find a "line of best fit" for your Friday nights. You know that if you invite exactly 10 people, 2 might flake. If you invite 15, the game is too crowded and people get annoyed. OLS is the mental calculation you perform over several weeks to find that "sweet spot" number of invites that minimizes the total frustration (the error) of having too few or too many players. You aren't looking for one perfect night; you're looking for the strategy that, on average, leaves you with the smallest possible mess to clean up.

---

## The Math Link

In formal terms, Ordinary Least Squares (OLS) is a method for estimating the unknown parameters in a linear regression model. We seek to minimize the sum of the squares of the vertical deviations between each observed data point and the fitted line.

Given a dataset of $n$ observations $\{ (y_i, \mathbf{x}_i) \}_{i=1}^n$, where $y_i$ is the dependent variable (the actual number of players who showed up) and $\mathbf{x}_i$ is a vector of regressors (factors like weather, day of the week), the linear model is defined as:

$$y_i = \mathbf{x}_i^\top \boldsymbol{\beta} + \varepsilon_i$$

Where $\boldsymbol{\beta}$ is a $p \times 1$ vector of parameters we want to estimate, and $\varepsilon_i$ is the error term. To find the optimal $\boldsymbol{\beta}$, we minimize the Residual Sum of Squares ($RSS$):

$$S(\boldsymbol{\beta}) = \sum_{i=1}^n (y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2$$

In matrix notation, where $\mathbf{y}$ is an $n \times 1$ vector and $\mathbf{X}$ is an $n \times p$ matrix, this becomes:

$$S(\boldsymbol{\beta}) = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^\top (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})$$

To find the minimum, we take the gradient with respect to $\boldsymbol{\beta}$ and set it to zero:

$$\frac{\partial S}{\partial \boldsymbol{\beta}} = -2\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) = 0$$

Solving for $\boldsymbol{\beta}$ gives us the **Normal Equations**:

$$\mathbf{X}^\top\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}^\top\mathbf{y}$$

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$$

In our analogy:

- $\mathbf{y}$: The actual turnout recorded over past bookings.
- $\mathbf{X}$: The variables you controlled (number of invites sent, deposit required).
- $\hat{\boldsymbol{\beta}}$: The "weight" or importance of each variable in predicting the final turnout.
- $(\mathbf{y} - \mathbf{X}\boldsymbol{\beta})$: The "frustration" or "gap" between the expected 10 players and reality.

---

<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
OLS doesn't care about a single "perfect" game. It penalizes large misses more than small ones because we square the errors. It’s better to be off by 1 player twice ($1^2 + 1^2 = 2$) than to be spot on once and off by 2 players the next time ($0^2 + 2^2 = 4$). It forces the model to stay "honest" across all your data.

</div>



## Let's Run the Numbers

### Example 1: Finding 10 people to play

You want to predict turnout ($y$) based solely on how many people ($x$) you invite. You have data from two weeks:
Week 1: Invited 12, 10 showed up.
Week 2: Invited 14, 11 showed up.

We want to find $y = \beta x$.
$$\mathbf{X} = \begin{bmatrix} 12 \\ 14 \end{bmatrix}, \mathbf{y} = \begin{bmatrix} 10 \\ 11 \end{bmatrix}$$
$$\mathbf{X}^\top\mathbf{X} = [12 \quad 14] \begin{bmatrix} 12 \\ 14 \end{bmatrix} = 144 + 196 = 340$$
$$\mathbf{X}^\top\mathbf{y} = [12 \quad 14] \begin{bmatrix} 10 \\ 11 \end{bmatrix} = 120 + 154 = 274$$
$$\hat{\beta} = \frac{274}{340} \approx 0.806$$
**The Story:** The math tells you your "yield" is about $80.6\%$. To get exactly 10 people, you shouldn't invite 10; you should invite $10 / 0.806 \approx 12.4$ (so, 12 or 13 people).

### Example 2: Checking the slots

You notice the time of the slot affects turnout. Let $x_1$ be invites and $x_2$ be the hour of the game (24h format).
Week 1: 12 invites, 18:00 slot $\rightarrow$ 10 showed up.
Week 2: 12 invites, 22:00 slot $\rightarrow$ 8 showed up.

$$\mathbf{X} = \begin{bmatrix} 12 & 18 \\ 12 & 22 \end{bmatrix}, \mathbf{y} = \begin{bmatrix} 10 \\ 8 \end{bmatrix}$$
Using $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$:
$$\mathbf{X}^\top\mathbf{X} = \begin{bmatrix} 288 & 480 \\ 480 & 808 \end{bmatrix}$$
Calculating the inverse and multiplying (simplified for brevity):
$$\hat{\boldsymbol{\beta}} \approx \begin{bmatrix} 1.58 \\ -0.5 \end{bmatrix}$$
**The Story:** Each hour later the slot is ($x_2$), you lose $0.5$ players. The math quantifies exactly how much that "late-night" slot is killing your game.

### Example 3: The 'no-show' frustration

You want to measure the "Base Flake Rate" (the intercept $\beta_0$) regardless of invites.
Data: (Invites: 10, Turnout: 7), (Invites: 15, Turnout: 12).
We use $y = \beta_0 + \beta_1 x$.
$$\mathbf{X} = \begin{bmatrix} 1 & 10 \\ 1 & 15 \end{bmatrix}, \mathbf{y} = \begin{bmatrix} 7 \\ 12 \end{bmatrix}$$
$$\mathbf{X}^\top\mathbf{X} = \begin{bmatrix} 2 & 25 \\ 25 & 325 \end{bmatrix}$$
Solving the system:
$$\hat{\beta}_1 = \frac{12-7}{15-10} = 1, \quad \hat{\beta}_0 = -3$$
**The Story:** The intercept $\beta_0 = -3$ suggests that even if you invite people, there's a systemic "drag" on your turnout. You need to invite more than 3 people just to see the first person walk through the gate.

---

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**CRITICAL INSIGHT: The Multicollinearity Trap**
OLS relies on the matrix $\mathbf{X}^\top\mathbf{X}$ being invertible. If your features are perfectly correlated—for example, if you include "Number of Invites" and "Number of Invites $\times$ 1"—the matrix becomes singular. In practical terms, the math "breaks" because it can't distinguish which variable is actually responsible for the change in the outcome. Always check your Feature Correlation Matrix before fitting.

</div>

---

## ML Applications

- **Financial Forecasting:** Predicting stock price movements based on historical indicators where the relationship is assumed to be linear over short intervals.
- **Advertising Attribution:** Determining the Return on Investment (ROI) for different marketing channels (TV, Social, Search) by regressing total sales against spend per channel.
- **Health Diagnostics:** Estimating physiological markers (like blood pressure) based on demographic features like age, BMI, and sodium intake.
- **Real Estate Valuation:** Calculating the base price of property per square foot by training an OLS model on historical sales data while controlling for bedrooms and location.
- **Resource Allocation in Cloud Computing:** Predicting CPU utilization trends to proactively scale virtual machine instances based on time-of-day and request volume.

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your OLS model is performing poorly, check for outliers. Because OLS squares the residuals, a single data point that is far from the mean can "pull" the entire line toward it, ruining the fit for the rest of the players.

</div>


