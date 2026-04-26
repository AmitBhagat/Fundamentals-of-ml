<h1 align="center"> Chapter 25: Partial Derivatives </h1>

---

<div style="text-align: justify;">


<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite

- **Single-Variable Calculus:** Understanding the derivative as the instantaneous rate of change for functions of the form $f(x)$.
- **Multivariable Functions:** Familiarity with functions that accept multiple independent inputs, typically denoted as $f(x, y, z, \dots)$.
- **Limits and Continuity:** A basic grasp of how a function behaves as its inputs approach a specific point in space.

</div>

## Analogy

Managing a complex machine learning model is often like managing a modern **Bank Passbook**. In a perfect world, your balance is just one number, but in reality, your financial standing is a result of multiple independent streams: interest credits, ATM withdrawals, monthly fees, and direct deposits.

When you stand at that kiosk to update your passbook, you aren't just looking at the final balance; you are looking for the "why" behind the change. If your balance dropped by $500$, you need to isolate which specific "input"—the rent check or the weekend splurge—caused that shift. A partial derivative is the mathematical equivalent of looking at your passbook and asking: _"If I keep every other transaction exactly the same, but I increase my monthly interest credit by just one dollar, how much will my final balance change?"_ It is the art of freezing the world to see how one specific lever moves the needle.

## The Math Link

In formal terms, let $f$ be a scalar-valued function of $n$ variables, defined on an open set $\mathcal{S} \subseteq \mathbb{R}^n$. The partial derivative of $f$ with respect to the $i$-th variable $x_i$ at the point $\mathbf{a} = (a_1, a_2, \dots, a_n)$ is defined as the limit:

$$\frac{\partial f}{\partial x_i}(\mathbf{a}) = \lim_{h \to 0} \frac{f(a_1, \dots, a_i + h, \dots, a_n) - f(a_1, \dots, a_i, \dots, a_n)}{h}$$

To derive this logic for a multivariable system where $z = f(x, y)$, we treat the variable not being differentiated as a constant. If we are differentiating with respect to $x$, we treat $y$ as a fixed value $y_0$. The derivation follows the standard difference quotient:

1.  **Isolate the Variable:** Define a single-variable function $g(x) = f(x, y_0)$.
2.  **Apply Power/Chain Rules:** Compute $g'(x)$ using standard rules $\forall x \in \mathbb{R}$ where the derivative exists.
3.  **Result:** The resulting expression $\frac{\partial f}{\partial x}$ represents the slope of the tangent line to the surface $z = f(x, y)$ in the direction of the $x$-axis.

In our analogy:

- $f(x_1, x_2, \dots, x_n)$ is the **Final Passbook Balance**.
- $x_i$ is a **Specific Transaction Type** (e.g., Interest Rate).
- $\frac{\partial f}{\partial x_i}$ is the **Sensitivity** of your balance to that specific transaction.

<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
Think of partial derivatives as "blinders." You are intentionally ignoring the chaos of the other variables to see the pure, unadulterated influence of a single factor. If you change $x$ and $y$ at the same time, you'll never know who to blame for the error.

</div>

## Let's Run the Numbers

### Example 1: Standing in the machine queue

You are standing at the bank kiosk. Your total satisfaction $S$ depends on the number of people in the queue ($q$) and the cooling temperature of the lobby ($t$). The satisfaction function is $S(q, t) = 100 - q^2 - 0.5t^2$. You want to know how much more annoyed you get per person added to the queue, regardless of the temperature.

**Calculation:**
$$\text{Find } \frac{\partial S}{\partial q} \text{ at } q=5, t=72$$
$$\frac{\partial S}{\partial q} = \frac{\partial}{\partial q}(100 - q^2 - 0.5t^2)$$
$$\frac{\partial S}{\partial q} = 0 - 2q - 0 = -2q$$
$$\text{At } q=5: \frac{\partial S}{\partial q} = -2(5) = -10$$

**The Story:** The math shows that for every extra person who joins the queue, your satisfaction drops by 10 units. Because we held $t$ constant, we know this frustration is purely about the crowd, not the heat.

### Example 2: Checking for missing entries

You notice your balance $B$ is calculated based on monthly deposits $d$ and the number of months $m$, modeled by $B(d, m) = d \cdot m + 0.01d^2$. You realize a deposit entry is missing. You need to see how sensitive your balance is to the deposit amount to see if it's worth arguing with the teller.

**Calculation:**
$$\text{Find } \frac{\partial B}{\partial d} \text{ at } d=1000, m=12$$
$$\frac{\partial B}{\partial d} = \frac{\partial}{\partial d}(dm + 0.01d^2)$$
$$\frac{\partial B}{\partial d} = m + 0.02d$$
$$\text{At } d=1000, m=12: 12 + 0.02(1000) = 12 + 20 = 32$$

**The Story:**
This result ($32$) tells you that for every $\$1$ increase in your deposit amount, your balance increases by $\$32$ over the year (due to the compounding-like effect of the squared term). This tells you that missing deposits are a high-priority fix.

### Example 3: The thrill of interest credit

The bank applies a complex interest credit $C$ based on your principal $P$ and the current annual rate $r$: $C(P, r) = P \cdot e^{2r}$. You want to see how much "thrill" (extra credit) you get if the bank raises the rate by a tiny fraction.

**Calculation:**
$$\text{Find } \frac{\partial C}{\partial r} \text{ at } P=5000, r=0.05$$
$$\frac{\partial C}{\partial r} = \frac{\partial}{\partial r}(P \cdot e^{2r})$$
$$\frac{\partial C}{\partial r} = P \cdot e^{2r} \cdot 2 = 2Pe^{2r}$$
$$\text{At } P=5000, r=0.05: 2(5000)e^{2(0.05)} = 10000 \cdot e^{0.1} \approx 10000 \cdot 1.105 = 11051.7$$

**The Story:**
The partial derivative w.r.t rate is massive ($11,051.7$). This tells you that even a microscopic nudge in the interest rate yields a huge "thrill" in credit because your principal is high.

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**CRITICAL INSIGHT**
In ML, we rarely deal with two variables. We deal with millions. The collection of all partial derivatives of a function is the **Gradient Vector** $\nabla f$. A common "gotcha" is forgetting that a partial derivative only gives you the slope in an axis-aligned direction. If you want to move in a diagonal direction, the partial derivative alone isn't enough—you need the full gradient.

</div>

## ML Applications

- **Gradient Descent in Backpropagation:** Partial derivatives of the loss function $L$ with respect to each weight $w_{ij}$ and bias $b_i$ are calculated to update parameters using $w_{new} = w_{old} - \eta \frac{\partial L}{\partial w}$.
- **Jacobian Matrices in Robotics:** In inverse kinematics, the Jacobian matrix (a matrix of first-order partial derivatives) maps joint velocities to end-effector velocities in 3D space.
- **Feature Importance in Sensitivity Analysis:** By calculating $\frac{\partial \hat{y}}{\partial x_i}$, researchers determine which input feature $x_i$ has the greatest marginal impact on the model's prediction $\hat{y}$.
- **Convolutional Neural Networks (CNNs):** During the backward pass of a convolution layer, partial derivatives are computed with respect to the filter kernels to learn spatial patterns like edges and textures.
- **Regularization Tuning:** Partial derivatives of the penalty terms (like $L1$ or $L2$ norms) are added to the loss gradient to ensure the model weights remain small and avoid overfitting.

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your model isn't learning, check your partial derivatives. A "Vanishing Gradient" happens when the partial derivative w.r.t. a weight becomes so small that the update $w_{new} = w_{old} - \eta \cdot 0$ effectively stops the learning process. Always monitor the magnitude of your partials during training.

</div>


</div>