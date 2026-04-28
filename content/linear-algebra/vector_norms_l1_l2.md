---
title: "Vector Norms (L1, L2)"
description: "Mastering the mathematical foundations of artificial intelligence."
complexity: "Intermediate"
estimated_time: "20 min"
---

<h1 align="center"> Chapter 26: Vector Norms (L1, L2) </h1>

***





<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Vector Representation:** Understanding that a list of numbers (a vector) can represent various features of an object in a coordinate space.
* **Absolute Values:** Knowing that the magnitude of a change matters more than the direction when calculating distance.
* **Summation Notation:** Familiarity with the $\sum$ symbol to aggregate values across multiple dimensions.

</div>


## Analogy
When you’re hosting a house party, the "size" of your food order isn't just one number; it’s a measurement of the total impact your guests will have on your kitchen. A vector norm is essentially a way to quantify the magnitude of a multi-dimensional problem—like food logistics—into a single, actionable value. 

Think of your guests as different variables. One guest might be extremely hungry, another might have strict dietary restrictions, and another might just be there for the drinks. Each guest adds a "dimension" of complexity to your order. The "Norm" is the mathematical ruler you use to summarize all that individual chaos into a single "total effort" score. Depending on whether you care about the total volume of food or the most extreme outliers among your guests, you’ll choose a different way to measure that "size."


## The Math Link
In a formal sense, a norm is a function $f: V \to \mathbb{R}$ that assigns a strictly positive length or size to all vectors in a vector space $V$ (except for the zero vector). For any vector $\mathbf{x} \in \mathbb{R}^n$, the $p$-norm is defined as:

$$||\mathbf{x}||_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p}$$

Where:
* $n$: The number of guests at your party (dimensions).
* $x_i$: The specific "requirement" or value associated with guest $i$.
* $||\mathbf{x}||$: The total "magnitude" of the food order.

### Derivation of L1 Norm (Manhattan Norm)
For $p=1$, the formula simplifies to the sum of absolute values. We define the L1 norm for a vector $\mathbf{x} \in \mathbb{R}^n$ as:

$$||\mathbf{x}||_1 = \sum_{i=1}^n |x_i|$$

In our analogy, this represents the **Total Food Volume**. If Guest A wants 3 slices and Guest B wants 2, you need 5 slices. You are simply summing up the individual magnitudes.

### Derivation of L2 Norm (Euclidean Norm)
For $p=2$, we derive the standard distance formula. We define the L2 norm as:

$$||\mathbf{x}||_2 = \sqrt{\sum_{i=1}^n x_i^2}$$

This is derived from the Pythagorean theorem extended to $n$-dimensions. In our analogy, this represents the **Logistical Complexity**. Because we square the values before summing, a single guest with a massive, outlier order (e.g., 10 pizzas) creates a much larger "norm" than ten guests ordering one slice each.


<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
Think of L1 as the "Total Count" and L2 as the "Shortest Path." L1 cares about the sum of the parts, while L2 is sensitive to large individual values because it squares them, making outliers stand out.

</div>





## Let's Run the Numbers

### Example 1: Estimating how many pizzas to order (L1 Norm)
We have a vector $\mathbf{x}$ representing the pizza slice requests of 4 guests: $\mathbf{x} = [3, 0, 5, 2]$. We need the L1 norm to find the total volume.

**Calculation:**
$$||\mathbf{x}||_1 = |3| + |0| + |5| + |2|$$
$$||\mathbf{x}||_1 = 3 + 0 + 5 + 2 = 10$$

**The Story:**
The L1 norm tells you the absolute total. You don't care about the "geometry" of the hunger; you just need to know that 10 slices must exist in the house to satisfy the group. This is the most "honest" count of total resources required.

### Example 2: Managing dietary preferences (L2 Norm)
You have two groups of guests. Group A has three people who are slightly picky (level 2). Group B has one person who is extremely allergic to everything (level 6). 
Vector $A = [2, 2, 2]$ and Vector $B = [6, 0, 0]$.

**Calculation for Group B:**
$$||B||_2 = \sqrt{6^2 + 0^2 + 0^2}$$
$$||B||_2 = \sqrt{36} = 6$$

**Calculation for Group A:**
$$||A||_2 = \sqrt{2^2 + 2^2 + 2^2}$$
$$||A||_2 = \sqrt{4 + 4 + 4} = \sqrt{12} \approx 3.46$$

**The Story:**
Even though both groups have a "Total Pickiness" (L1) of 6, the L2 norm for Group B is much higher (6 vs 3.46). The L2 norm warns you that Group B is a bigger logistical "risk" because the outlier (the severe allergy) dominates the calculation. It tells you that one extreme person is harder to manage than three mildly picky ones.

### Example 3: The delivery delay (L1 vs L2 for Error)
Your delivery driver provides a vector of "Minutes Late" for three different orders: $\mathbf{x} = [10, 0, 10]$. You want to calculate the "Total Disappointment" score.

**L1 Calculation:**
$$||\mathbf{x}||_1 = 10 + 0 + 10 = 20$$

**L2 Calculation:**
$$||\mathbf{x}||_2 = \sqrt{10^2 + 0^2 + 10^2} = \sqrt{200} \approx 14.14$$

**The Story:**
If you use L1, you see the total time lost (20 minutes). If you use L2, the "distance" from a perfect on-time delivery is roughly 14.14. In ML, using L2 here would punish the driver more heavily for a single 20-minute delay ($20^2=400$) than for two 10-minute delays ($10^2+10^2=200$), because L2 squares the "lateness."


<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Critical Insight:** L1 regularization (Lasso) produces sparse solutions, meaning it actively drives less important feature weights to exactly zero. L2 regularization (Ridge) only shrinks weights toward zero but rarely hits it. If you need feature selection, use L1; if you just want to prevent any single feature from having too much influence, use L2.

</div>


## ML Applications
* **Lasso Regularization (L1):** Used in high-dimensional datasets to perform automatic feature selection by penalizing the absolute sum of weights, effectively zeroing out redundant predictors.
* **Ridge Regularization (L2):** Adds a penalty equal to the square of the magnitude of coefficients to the loss function to prevent overfitting and improve numerical stability in Matrix Inversion.
* **Mean Absolute Error (MAE):** A loss function based on the L1 norm that is robust to outliers, as it does not square the residual terms.
* **Mean Squared Error (MSE):** A loss function based on the L2 norm (squared) that is mathematically advantageous for optimization because it is differentiable everywhere, unlike L1.
* **Cosine Similarity:** Often involves L2 normalization of vectors where the dot product of two L2-normalized vectors represents the cosine of the angle between them, commonly used in Natural Language Processing for document similarity.


<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your model gradient is "jumping" or failing to converge near the minimum, check your loss function. L1 norms have a discontinuous derivative at zero, which can cause oscillations if your learning rate is too high.

</div>

