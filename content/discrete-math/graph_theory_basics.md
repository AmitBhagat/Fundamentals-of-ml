---
title: "Graph Theory Basics"
description: "Graph definitions, adjacency and degree matrices, Graph Laplacians, path count proofs via matrix powers, and Graph Neural Networks."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Linear Algebra: Matrices", "Discrete Math: Sets, Relations, and Functions"]
---

<h1 align="center"> Chapter 105: Graph Theory Basics </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Adjacency Matrix ($\mathbf{A}$):** A square matrix representation where entries indicate whether pairs of vertices are adjacent in the graph.
* **Graph Laplacian ($\mathbf{L}$):** The matrix operator defined as the difference between the degree matrix and the adjacency matrix, describing diffusion on a graph.

</div>

## 1. Conceptual Hook

Many datasets cannot be arranged in clean, independent grids of rows and columns. Instead, they represent complex networks of relationships—such as social networks, chemical molecules, website hyperlinks, or traffic routing maps.

**Graph theory** is the mathematical language we use to analyze these systems.

Instead of looking at data points in isolation, graph theory focuses on the topology of their relationships. It models systems as sets of objects (vertices) and the connections between them (edges).

Think of a transit map. The stations are vertices, and the rails connecting them are edges. The strength of a station is determined by its degree—how many lines feed into it.

In machine learning, graph theory is the foundation of Graph Neural Networks (GNNs) and knowledge graphs. It allows models to pass messages along edges, aggregating information from local neighborhoods to reason about interconnected data.

---

## 2. Formal Definition

A **graph** $G$ is an ordered pair $G = (V, E)$, where:
*   **$V = \{v_1, v_2, \dots, v_n\}$:** The set of vertices (or nodes).
*   **$E \subseteq V \times V$ (for directed graphs):** The set of edges representing ordered pairs. For undirected graphs, $E$ consists of unordered $2$-element subsets of $V$.

### Adjacency Matrix
For a graph with $n$ vertices, the **adjacency matrix** $\mathbf{A} \in \mathbb{R}^{n \times n}$ contains entries:
$$A_{ij} = \begin{cases} w_{ij} & \text{if } (v_i, v_j) \in E \\ 0 & \text{otherwise} \end{cases}$$
where $w_{ij}$ represents the edge weight (or $1$ for unweighted graphs).

### Degree Matrix
The **degree matrix** $\mathbf{D} \in \mathbb{R}^{n \times n}$ is a diagonal matrix where:
$$D_{ii} = d(v_i) = \sum_{j=1}^{n} A_{ij}$$

### Graph Laplacians
*   **Unnormalized Graph Laplacian:**
    $$\mathbf{L} = \mathbf{D} - \mathbf{A}$$
*   **Symmetric Normalized Graph Laplacian:**
    $$\mathbf{L}_{sym} = \mathbf{D}^{-1/2} \mathbf{L} \mathbf{D}^{-1/2} = \mathbf{I} - \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$$

---

## 3. Illustrative Derivation

### Proof: Path Counting via Adjacency Matrix Powers
We prove that the number of unique walks of length $k$ between vertex $v_i$ and vertex $v_j$ is given by the $(i, j)$-th entry of the matrix power $\mathbf{A}^k$.

*Proof:*
We use mathematical induction on the walk length $k$.

1.  **Establish the base case ($k = 1$):**
    By definition of the adjacency matrix, $A_{ij} = 1$ if there is a direct edge (a walk of length $1$) from $v_i$ to $v_j$, and $0$ otherwise. Thus, the $(i,j)$ entry of $\mathbf{A}^1$ is exactly the number of walks of length $1$. The base case holds.

2.  **Formulate the inductive hypothesis:**
    Assume the theorem holds for walks of length $k - 1$. That is, the $(i, l)$ entry of $\mathbf{A}^{k-1}$, denoted $(A^{k-1})_{il}$, equals the number of walks of length $k-1$ from $v_i$ to $v_l$.

3.  **Evaluate walks of length $k$:**
    Any walk of length $k$ from $v_i$ to $v_j$ consists of a walk of length $k-1$ from $v_i$ to some intermediate vertex $v_l$, followed by a single edge from $v_l$ to $v_j$.
    The number of such walks passing through intermediate node $v_l$ is:
    $$\text{Walks via } v_l = (A^{k-1})_{il} \cdot A_{lj}$$

4.  **Sum over all possible intermediate nodes $v_l \in V$:**
    $$\text{Total walks of length } k = \sum_{l=1}^{n} (A^{k-1})_{il} A_{lj}$$
    Notice that this summation matches the algebraic definition of matrix multiplication for the product $\mathbf{A}^{k-1} \cdot \mathbf{A}$:
    $$\sum_{l=1}^{n} (A^{k-1})_{il} A_{lj} = \left( \mathbf{A}^{k-1} \mathbf{A} \right)_{ij} = \left( \mathbf{A}^k \right)_{ij}$$
By the principle of mathematical induction, the theorem holds for all integers $k \ge 1$. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Walk Counting on a 3-Node Graph
Consider a directed graph with $V = \{A, B, C\}$ and edges $E = \{(A, B), (B, C)\}$.
1.  **Construct the Adjacency Matrix:**
    $$\mathbf{A} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$$
2.  **Compute the square of the Adjacency Matrix:**
    $$\mathbf{A}^2 = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$$
The entry $(\mathbf{A}^2)_{1,3} = 1$ indicates that there is exactly $1$ walk of length $2$ from $A$ to $C$ (the path $A \to B \to C$).

### Example 2: Calculating the Graph Laplacian
Consider an undirected graph with $V = \{1, 2, 3\}$ and edges $E = \{\{1, 2\}, \{2, 3\}\}$.
1.  **Construct the Adjacency and Degree Matrices:**
    $$\mathbf{A} = \begin{bmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{bmatrix}, \quad \mathbf{D} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$
2.  **Compute the Laplacian:**
    $$\mathbf{L} = \mathbf{D} - \mathbf{A} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{bmatrix} - \begin{bmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{bmatrix} = \begin{bmatrix} 1 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 1 \end{bmatrix}$$

---

## 5. Applied ML Context

1.  **Graph Neural Network Message Passing:** GNNs use normalized Laplacians $\mathbf{L}_{sym}$ to aggregate and smooth feature vectors across neighboring nodes during convolution operations.
2.  **Recommender Link Prediction:** E-commerce systems model user-item purchases as a bipartite graph, using link prediction algorithms to recommend new item edges to users.
3.  **Entity Knowledge Graphs:** LLMs leverage structured knowledge graphs linking semantic entities (e.g. countries, capitals) to improve contextual reasoning.
4.  **Social Network Centrality:** Social platforms analyze user graphs using centrality metrics like PageRank to identify key users and communities.
5.  **Traffic Congestion Forecasting:** Modeling road systems as weighted directed graphs where edge weights represent real-time traffic density to forecast route latencies.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating graph matrices:
*   Draw a simple 4-node undirected graph on the left, with vertices and edges labeled.
*   Draw its corresponding Adjacency Matrix $\mathbf{A}$ and Graph Laplacian $\mathbf{L}$ on the right:
    *   Use colored boxes to show how edge connections map to $1$ values in $\mathbf{A}$.
    *   Show how vertex degrees map to the diagonal of $\mathbf{D}$, and how subtraction yields the negative off-diagonal entries in $\mathbf{L}$.
*   Add a caption explaining that graph theory translates physical topological connections into algebraic matrix operators, enabling message passing on graph manifolds.
