---
title: "Decision Trees Geometry"
description: "Mastering the recursive partitioning of space and the 'Twenty Questions' of data."
complexity: "Intermediate"
estimated_time: "20 min"
prerequisites: ["Foundations", "Probability Basics", "Entropy"]
---

<h1 align="center"> Chapter 115: Decision Trees Geometry </h1>

---

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite

- **Probability ($p$):** Understanding the likelihood of a class occurring in a set.
- **Entropy:** The measurement of "Disorder" or "Uncertainty" in a group.
- **Recursion:** The idea of solving a large problem by breaking it into smaller, identical sub-problems.

</div>

---

## Analogy

Imagine you are playing a game of **"Twenty Questions."** You are trying to guess a mystery object. 

If your first question is "Is it made of atoms?", it’s a terrible question because the answer is always "Yes." You haven't gained any information. But if you ask "Is it alive?", you have instantly cut the possibilities in half. 

A **Decision Tree** is a machine that plays "Twenty Questions" with your data. It looks at every feature (Age, Salary, Location) and asks: "Which question will split this messy pile of data into two cleaner, more 'Pure' piles?" 
- The **Geometry** of a Decision Tree is a series of **Axis-aligned Cuts**. It’s like taking a block of wood and making straight saw-cuts until you’ve isolated every knot.

---

## The Math Link

How do we decide which "Question" is the best? we use **Purity Metrics**.

### 1. Entropy ($H$)
Measures the "Surprise" in a set. If a set is 50/50, entropy is 1 (Max). If it's 100/0, entropy is 0 (Min).
$$H = -\sum_{i=1}^c p_i \log_2(p_i)$$

### 2. Gini Impurity ($G$)
Measures the chance of a "Mistake." If you randomly pick a point and randomly label it, how often would you be wrong?
$$G = 1 - \sum_{i=1}^c p_i^2$$

### 3. Information Gain ($IG$)
The "Reward" for a split. It’s the difference between the messiness before the split and the average messiness after.
$$IG = H(parent) - [ \frac{N_{left}}{N} H(left) + \frac{N_{right}}{N} H(right) ]$$

---

<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
A Decision Tree is **Greedy**. At every step, it only cares about making the *next* split the best one possible. It doesn't plan for the future. This is why trees can easily "Overfit"—they chase tiny, insignificant patterns in the data until they’ve isolated every single data point into its own leaf.

</div>

---

## Let's Run the Numbers

### Example 1: Calculating Gini Impurity

You have a bucket of 10 balls: 7 Red and 3 Blue.

**Calculation:**
1. $p_{red} = 0.7, p_{blue} = 0.3$.
2. Sum of squares: $0.7^2 + 0.3^2 = 0.49 + 0.09 = 0.58$.
3. $G = 1 - 0.58 = 0.42$.

**The Story:** A Gini of $0.42$ means the bucket is fairly "Impure." We want to find a split that brings this number closer to $0.0$.

### Example 2: The "Information Gain" of a Split

You split the 10 balls into two buckets based on "Size":
- Small Bucket: 4 Red, 0 Blue ($G=0$).
- Large Bucket: 3 Red, 3 Blue ($G=0.5$).

**Calculation:**
1. Parent Gini: $0.42$.
2. Weighted Child Gini: $(\frac{4}{10} \times 0) + (\frac{6}{10} \times 0.5) = 0 + 0.3 = 0.3$.
3. **Gain:** $0.42 - 0.3 = 0.12$.

**The Story:** The split provided a gain of $0.12$. If another split (like "Texture") provides a gain of $0.2$, the tree will choose "Texture" as the better question.

### Example 3: The Leaf Prediction

A tree reaches a "Leaf" (a terminal node) where there are 100 samples: 90 "Fraud" and 10 "Safe."

**Calculation:**
The tree calculates the majority class. 
- Probability(Fraud) = 0.9.
- Prediction = "Fraud".

**The Story:** The tree doesn't just give a label; it gives a **Confidence**. In this case, it is 90% sure about its decision.

---

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**CRITICAL TECHNICAL INSIGHT: High Cardinality Bias**
Decision Trees have a "Crush" on features with many unique values (like "User ID" or "Exact Timestamp"). Because these features can create "Perfect Splits" (one ID per leaf), they look like they have massive Information Gain. In reality, they are just memorizing the data. **Always drop unique identifiers** before training a tree!

</div>

---

## ML Applications

1.  **Credit Scoring:** "If Income > 50k AND Debt < 10k $\to$ Approved."
2.  **Medical Triage:** Identifying the most critical symptoms to check first in an ER.
3.  **Random Forests:** Combining 100 different "Weak" trees to create a "Strong" voting bloc.
4.  **XGBoost:** The king of tabular data, which builds trees sequentially to fix the mistakes of previous ones.
5.  **Game AI:** Simple decision trees are used for NPC behavior (e.g., "If Player in range AND Health > 20% $\to$ Attack").

---

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your tree has a depth of 50, it is **Overfitting**. It has built a specific rule for every single outlier in your dataset. Use **Pruning** or set a `max_depth` to force the tree to learn "General Rules" instead of "Specific Gossip."

</div>
