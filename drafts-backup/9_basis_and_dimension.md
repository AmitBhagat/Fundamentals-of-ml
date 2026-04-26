<h1 align="center"> Chapter 9: Basis and Dimension </h1>

***

<div style="text-align: justify;">



<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Linear Independence:** Understanding that a set of vectors is independent if no vector in the set can be built by scaling and adding the others.
* **Span:** The concept that a collection of vectors can "reach" or cover a specific geometric space through linear combinations.
* **Vector Spaces:** A formal playground (like $\mathbb{R}^n$) where addition and scaling follow consistent rules.

</div>


## Analogy

Think of a **Basis** as the "Minimum Shopping List" required to stock a kitchen, and **Dimension** as the "Number of Aisles" you are forced to navigate. 

When you deal with a **Local Vendor**, you are often restricted by a very specific, small basis. The vendor has a fixed inventory; if they only sell potatoes and onions, your "culinary space" is limited. You can make many things with them (different linear combinations), but you can't suddenly produce a beef Wellington. The "Dimension" here is low because the variety of independent ingredients is capped.

In contrast, the **Supermarket** provides a massive, diverse basis. You have access to every spice, grain, and protein. This increases the "Dimension" of what you can create. However, a Basis isn't just about having everything; it's about having the *efficient* minimum. If you have two different brands of the exact same salt, your list is redundant. A true Basis is the leanest possible list of unique items that still allows you to cook every single recipe possible in that store.


## The Math Link

In formal terms, a set of vectors $\mathcal{B} = \{v_1, v_2, \dots, v_n\}$ is a **Basis** for a vector space $\mathcal{V}$ if it satisfies two rigorous conditions:
1.  **Linear Independence:** $\sum_{i=1}^{n} c_i v_i = \mathbf{0}$ implies $c_1 = c_2 = \dots = c_n = 0$.
2.  **Spanning:** $\forall u \in \mathcal{V}, \exists \{c_1, c_2, \dots, c_n\} \in \mathbb{R}$ such that $u = \sum_{i=1}^{n} c_i v_i$.

The **Dimension**, denoted as $\dim(\mathcal{V})$, is the cardinality of the basis set:
$$\dim(\mathcal{V}) = |\mathcal{B}| = n$$

**The Derivation of Coordinates:**
If $\mathcal{B}$ is a basis, any vector $x$ is uniquely represented. Suppose there were two representations:
$$x = \sum_{i=1}^{n} a_i v_i \quad \text{and} \quad x = \sum_{i=1}^{n} b_i v_i$$
Subtracting these yields:
$$\mathbf{0} = \sum_{i=1}^{n} (a_i - b_i) v_i$$
By the definition of linear independence, $(a_i - b_i) = 0$ for all $i$, proving that $a_i = b_i$. 

**The Link:** * The **Basis vectors** $v_i$ represent the "unique items" on your shopping list (e.g., milk, eggs). 
* The **Coefficients** $c_i$ represent the "quantity" of each item you choose to buy.
* The **Dimension** $n$ is the total count of unique categories you need to track to describe any possible grocery bag.





<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
Basis is about **Efficiency** (no redundant items on the list). Dimension is about **Capacity** (how much "room" you have to move). If you have more items than the dimension, you're carrying dead weight. If you have fewer, you're starving.

</div>


## Let's Run the Numbers

### 1. Comparing Prices (The Change of Basis)
Imagine a local vendor sells "Bundle A" (2 apples, 1 orange) and "Bundle B" (1 apple, 2 oranges). You want to see how these compare to the supermarket's standard unit prices.
* Supermarket Basis (Standard): $e_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ (1 apple), $e_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ (1 orange).
* Vendor Basis: $b_1 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$, $b_2 = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$.

Find the coordinates of a bag $x = \begin{bmatrix} 5 \\ 4 \end{bmatrix}$ (standard units) in the Vendor's basis.
Solve $x = c_1 b_1 + c_2 b_2$:
$$\begin{bmatrix} 5 \\ 4 \end{bmatrix} = c_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + c_2 \begin{bmatrix} 1 \\ 2 \end{bmatrix}$$
Represented as a system:
$$2c_1 + 1c_2 = 5$$
$$1c_1 + 2c_2 = 4$$
Subtracting twice the second from the first: $2c_1 - 2c_1 + c_2 - 4c_2 = 5 - 8 \implies -3c_2 = -3 \implies c_2 = 1$.
Substitute back: $c_1 + 2(1) = 4 \implies c_1 = 2$.
**The Story:** To get exactly 5 apples and 4 oranges, you don't buy items individually; you buy 2 of the Vendor's "Bundle A" and 1 of "Bundle B". The math translates your "needs" into the "vendor's language."

### 2. Convenience of Home Delivery (Dimension Deficiency)
A delivery app only allows you to order in "Health Packs": $v_1 = \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}$ (Kale and Spinach) and $v_2 = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}$ (Spinach and Carrots). You want a pure "Carrot" bag $u = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$. 
Check if $u$ is in the span of the Basis provided by the app:
$$c_1 \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix} + c_2 \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$$
From row 1: $c_1 = 0$.
From row 3: $c_2 = 1$.
Check row 2: $c_1 + c_2 = 0 + 1 = 1$. But the target is $0$.
$1 \neq 0$.
**The Story:** The dimension of the "grocery space" is 3, but the delivery app only provides a 2-dimensional basis. Because your specific carrot needs fall outside that 2D plane, the delivery service literally cannot fulfill your request.

### 3. Picking by Hand (Redundancy Check)
At the supermarket, you grab three pre-mixed bags: $v_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$, $v_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, and $v_3 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. You want to know if these three bags form a Basis for your 2D recipe space.
Calculate the determinant of the augmented set or check for linear independence:
$$c_1 \begin{bmatrix} 1 \\ 0 \end{bmatrix} + c_2 \begin{bmatrix} 0 \\ 1 \end{bmatrix} + c_3 \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \mathbf{0}$$
If $c_3 = -1$, then $c_1 = 1$ and $c_2 = 1$ satisfies the equation.
**The Story:** Since $c_1, c_2, c_3$ are not all zero, the items are linearly dependent. You are carrying too much. You only need $v_1$ and $v_2$ to create anything $v_3$ offers. The "Dimension" is 2, but you have 3 items; one is redundant "picking by hand" effort.


## ML Applications

1.  **Principal Component Analysis (PCA):** PCA finds a new basis (Principal Components) for the data where the first few basis vectors capture the maximum variance. Reducing the number of basis vectors used is the core of dimensionality reduction.
2.  **Word Embeddings (NLP):** In models like Word2Vec, words are projected into a high-dimensional vector space. The "Dimension" of this space (e.g., 300 or 768) determines the model's capacity to represent nuanced semantic relationships.
3.  **Latent Space in Autoencoders:** The "bottleneck" layer of an autoencoder represents a lower-dimensional basis for the input data. The model learns to compress a high-dimensional input (like a $28 \times 28$ image) into a small dimension (e.g., 32) that still spans the essential features of the dataset.
4.  **Matrix Rank in Recommendation Systems:** In Collaborative Filtering, we decompose a user-item matrix. The "Rank" of the matrix is the dimension of the vector space spanned by its columns/rows, representing the number of independent "latent factors" (like movie genres) driving user preferences.
5.  **Kernel Methods (SVM):** The "Kernel Trick" implicitly maps data into a much higher-dimensional basis where a linear separator (hyperplane) can be found. This allows models to solve non-linear problems by temporarily increasing the dimension of the feature space.


<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Critical Insight:** In ML, "High Dimension" is a double-edged sword. While it allows for more complex representations, the **Curse of Dimensionality** means that as dimension increases, data points become exponentially sparse. A basis that is too large often leads to overfitting, capturing noise as if it were a fundamental component of the space.

</div>


<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your model's covariance matrix is non-invertible (singular), it’s usually because your features are not linearly independent—meaning your "Basis" has redundant "Shopping List" items. Check for multicollinearity!

</div>

</div>