<h1 align="center"> Chapter 12: Matrices </h1>

***

<div style="text-align: justify;">



<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Scalar Operations:** Understanding basic arithmetic (addition, multiplication) on individual real numbers.
* **Vector Foundations:** Knowledge of ordered lists of numbers representing points or directions in space.
* **System of Linear Equations:** Familiarity with solving for multiple unknowns using substitution or elimination.

</div>


---


## Analogy

Think of a **Carrom Tournament**. In a single game, you aren't just tracking one movement; you are managing a collective state of play. A Matrix is the "Tournament Spreadsheet." It isn't just a list of numbers; it is a structured grid that captures the entire configuration of the board—where every black, white, and queen coin sits relative to the pockets.

When you look at a Matrix, you are looking at the potential for transformation. Just as a tournament director looks at a table of player scores to determine the next bracket, or a player looks at the arrangement of coins to decide the force of their shot, a Matrix organizes data so we can manipulate the entire "board" at once. It allows us to scale, rotate, and shift every element of our system simultaneously rather than calculating every single coin’s trajectory in isolation. It is the language of collective influence.


---


## The Math Link

A matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$ is a rectangular array of real numbers arranged in $m$ rows and $n$ columns. We define the individual element located at the $i$-th row and $j$-th column as $a_{ij}$. Formally, the matrix is represented as:

$$\mathbf{A} = \begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{bmatrix}$$

In the context of our Carrom Tournament, let $m$ represent the number of players and $n$ represent the types of coins (Black, White, Queen). The entry $a_{ij}$ represents the count of coin type $j$ collected by player $i$.

To understand how matrices transform space, we look at **Matrix-Vector Multiplication**. If we have a vector $\mathbf{x} \in \mathbb{R}^n$ representing the "points" assigned to each coin type, the resulting vector $\mathbf{y} \in \mathbb{R}^m$ (the total score for each player) is calculated via the dot product of each row with the vector $\mathbf{x}$:

$$y_i = \sum_{j=1}^{n} a_{ij}x_j$$

For the entire system, this is expressed as:

$$\mathbf{y} = \mathbf{A}\mathbf{x}$$

Where:
* $\mathbf{A}$ is the state of the tournament (the counts).
* $\mathbf{x}$ is the weight/value of each action.
* $\mathbf{y}$ is the objective outcome.


---


<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### THE INTUITION
Don't view a matrix as a "box of numbers." View it as a **linear operator**. It is a set of instructions that tells you how to stretch, flip, or squish a coordinate system. If you change the matrix, you change the physics of the Carrom board itself.

</div>





## Let's Run the Numbers

### 1. The Perfect Striker Angle
To calculate the final position of a striker after a deflection, we use a rotation matrix. Suppose the striker is at coordinates $(1, 0)$ and we need to rotate its trajectory by $90^\circ$ ($\frac{\pi}{2}$ radians) to hit a pocket.

**The Setup:**
Vector $\mathbf{v} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$. Rotation Matrix $\mathbf{R} = \begin{bmatrix} \cos(\theta) & -\sin(\theta) \\ \sin(\theta) & \cos(\theta) \end{bmatrix}$ where $\theta = \frac{\pi}{2}$.

**The Calculation:**
$$\mathbf{R} = \begin{bmatrix} \cos(\frac{\pi}{2}) & -\sin(\frac{\pi}{2}) \\ \sin(\frac{\pi}{2}) & \cos(\frac{\pi}{2}) \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$$

$$\mathbf{v'} = \mathbf{R}\mathbf{v} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} (0)(1) + (-1)(0) \\ (1)(1) + (0)(0) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

**The Story:**
The math confirms that a $90^\circ$ rotation moves our striker from the horizontal axis to the vertical axis. By applying this matrix, the player identifies the exact new "heading" required to sink the coin.


### 2. Managing the Coins
In a tournament, we need to track the total points for two players across two different rounds. Matrix addition allows us to merge these states.

**The Setup:**
Round 1 Scores $\mathbf{M_1} = \begin{bmatrix} 20 & 5 \\ 10 & 0 \end{bmatrix}$ (Rows: Player A, B; Columns: White, Queen).
Round 2 Scores $\mathbf{M_2} = \begin{bmatrix} 10 & 0 \\ 30 & 5 \end{bmatrix}$.

**The Calculation:**
$$\mathbf{M_{total}} = \mathbf{M_1} + \mathbf{M_2} = \begin{bmatrix} 20+10 & 5+0 \\ 10+30 & 0+5 \end{bmatrix} = \begin{bmatrix} 30 & 5 \\ 40 & 5 \end{bmatrix}$$

**The Story:**
The tournament director uses matrix addition to aggregate performance. We can instantly see that Player B had a massive Round 2, overtaking Player A in White coins (40 vs 30).


### 3. The Intense Final Board
During the finals, the "value" of coins might be scaled due to a multiplier rule. We use Matrix-Scalar multiplication to update the entire board's worth.

**The Setup:**
Current point values $\mathbf{V} = \begin{bmatrix} 20 \\ 50 \end{bmatrix}$ (White, Queen). The "Finals Multiplier" $k = 1.5$.

**The Calculation:**
$$\mathbf{V_{final}} = k \cdot \mathbf{V} = 1.5 \cdot \begin{bmatrix} 20 \\ 50 \end{bmatrix} = \begin{bmatrix} 1.5 \times 20 \\ 1.5 \times 50 \end{bmatrix} = \begin{bmatrix} 30 \\ 75 \end{bmatrix}$$

**The Story:**
The "Intense Final Board" math shifts the stakes. Every white coin is now worth 30 points instead of 20. This forces players to adjust their risk-reward strategy for the final game.


---


<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Critical Insight:** Matrix multiplication is **not commutative** ($AB \neq BA$). In ML, the order of transformations matters. If you rotate an image and then translate it, you get a different result than if you translate it first and then rotate it. Swapping the order in your code will break your geometry.

</div>


---


## ML Applications

* **Image Representation:** Images are encoded as matrices where $I \in \mathbb{R}^{H \times W \times C}$. For a grayscale image, it is a 2D matrix of pixel intensities; for color, it is a 3D tensor representing Height, Width, and 3 Color channels (RGB).
* **Weight Matrices in Neural Networks:** The core of Deep Learning involves $\mathbf{y} = \sigma(\mathbf{W}\mathbf{x} + \mathbf{b})$. The matrix $\mathbf{W}$ stores the learned strengths of connections between layers of neurons.
* **Embeddings and Latent Space:** In Natural Language Processing, words are converted into high-dimensional vectors. A collection of these vectors forms an Embedding Matrix, allowing models to calculate semantic similarity.
* **Principal Component Analysis (PCA):** This dimensionality reduction technique uses the Eigen-decomposition of a Covariance Matrix to find the directions (Principal Components) of maximum variance in a dataset.
* **Attention Mechanisms:** In Transformer models (like LLMs), the "Attention" score is calculated using matrix products of Queries ($Q$), Keys ($K$), and Values ($V$), specifically $Softmax(\frac{QK^T}{\sqrt{d_k}})V$.


---


<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** Always check your **Matrix Dimensions** before performing operations. The number of columns in the first matrix must match the number of rows in the second. In Python/NumPy, `shape` mismatches are the #1 cause of runtime crashes in production ML models.

</div>

</div>