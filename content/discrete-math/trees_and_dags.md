---
title: "Trees and DAGs"
description: "Tree axioms, Directed Acyclic Graphs (DAGs), topological sorting, acyclicity trace criteria derivations, and computational graphs."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Discrete Math: Graph Theory Basics"]
---

<h1 align="center"> Chapter 107: Trees and DAGs </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Rooted Tree:** A tree where one vertex is designated as the root, defining parent-child hierarchies.
* **Topological Sort:** A linear ordering of vertices in a directed graph such that for every directed edge $(u, v)$, vertex $u$ comes before $v$.

</div>

## 1. Conceptual Hook

While general graphs allow arbitrary connections between nodes, many computational systems require directed, loop-free channels.

A **Tree** is a simple, cycle-free connected network where any two nodes are connected by exactly one path. A **Directed Acyclic Graph (DAG)** generalizes the tree, allowing multiple pathways to converge on a single node without ever looping back to a previous state.

Think of planning a project. Every task is a node, and dependencies are directed edges. You can work on multiple prerequisite tasks in parallel, and they can merge into a single milestone. However, you can never have a cycle (such as Task C requiring Task B, which requires Task A, which in turn requires Task C); otherwise, you could never begin.

In machine learning, trees form the core of models like Random Forests and XGBoost. DAGs are the foundational representation of computational graphs in frameworks like PyTorch and TensorFlow, ensuring that calculations flow in a single direction and gradients can be calculated via backpropagation.

---

## 2. Formal Definition

### 1. Trees
An undirected graph $G = (V, E)$ is a **tree** if it satisfies any of the following equivalent conditions:
*   $G$ is connected and has no cycles.
*   $G$ is connected and has exactly $|E| = |V| - 1$ edges.
*   For any two vertices $u, v \in V$, there exists exactly one unique path between them.

### 2. Directed Acyclic Graphs (DAGs)
A directed graph $G = (V, E)$ is a **DAG** if it contains no directed cycles.
A sequence of vertices $(v_0, v_1, \dots, v_k)$ is a directed cycle if:
$$(v_i, v_{i+1}) \in E \quad \forall i \in \{0, \dots, k-1\} \quad \text{and} \quad v_0 = v_k \quad \text{with} \quad k \ge 1$$

### 3. Trace Criterion for Acyclicity
Let $\mathbf{A} \in \{0, 1\}^{n \times n}$ be the adjacency matrix of a directed graph $G$ with $n$ vertices. $G$ is a DAG if and only if the trace of all powers of $\mathbf{A}$ up to $n$ is zero:
$$\text{Tr}(\mathbf{A}^k) = 0 \quad \forall k \in \{1, 2, \dots, n\}$$
where $\text{Tr}(\mathbf{M}) = \sum_{i=1}^n M_{ii}$ denotes the trace of matrix $\mathbf{M}$.

---

## 3. Illustrative Derivation

### Proof: The Acyclicity Trace Theorem
We prove that a directed graph $G$ is acyclic if and only if $\text{Tr}(\mathbf{A}^k) = 0$ for all $k \ge 1$.

*Proof:*

1.  **Prove "If $G$ is acyclic, then $\text{Tr}(\mathbf{A}^k) = 0$ for all $k \ge 1$":**
    Recall that the $(i, j)$-th entry of $\mathbf{A}^k$, denoted $(A^k)_{ij}$, represents the number of directed walks of length $k$ from vertex $v_i$ to vertex $v_j$.
    The diagonal entry $(A^k)_{ii}$ represents the number of directed walks of length $k$ starting and ending at the same vertex $v_i$.
    By definition, a closed walk of length $k \ge 1$ starting and ending at $v_i$ is a directed cycle containing $v_i$.
    Since $G$ is a DAG, it contains no directed cycles. Therefore, no closed walks of any length exist:
    $$(A^k)_{ii} = 0 \quad \forall i \in \{1, \dots, n\}$$
    Summing over all vertices:
    $$\text{Tr}(\mathbf{A}^k) = \sum_{i=1}^n (A^k)_{ii} = \sum_{i=1}^n 0 = 0 \quad \forall k \ge 1$$

2.  **Prove "If $\text{Tr}(\mathbf{A}^k) = 0$ for all $k \ge 1$, then $G$ is acyclic":**
    Suppose for contradiction that $G$ is not acyclic. Then $G$ contains at least one directed cycle $C = (v_1, v_2, \dots, v_m, v_1)$ of length $m \ge 1$.
    This cycle represents a closed walk of length $m$ starting and ending at $v_1$. Thus:
    $$(A^m)_{11} \ge 1$$
    Since the entries of $\mathbf{A}$ are non-negative, the entries of all powers $\mathbf{A}^k$ are also non-negative: $(A^k)_{ii} \ge 0$ for all $i, k$.
    Therefore, the trace of $\mathbf{A}^m$ must satisfy:
    $$\text{Tr}(\mathbf{A}^m) = \sum_{i=1}^n (A^m)_{ii} = (A^m)_{11} + \sum_{i \neq 1} (A^m)_{ii} \ge 1 + 0 = 1 > 0$$
    This contradicts the assumption that $\text{Tr}(\mathbf{A}^k) = 0$ for all $k \ge 1$.
    Hence, $G$ must be acyclic. $\blacksquare$

---

## 4. Concrete Examples

### Example 1: Node and Edge Counts in a Balanced Ternary Tree
Consider a balanced ternary tree (branching factor $m = 3$) of depth $d = 2$.
1.  **Calculate the total number of nodes $N$:**
    $$N = \sum_{i=0}^{d} m^i = 3^0 + 3^1 + 3^2 = 1 + 3 + 9 = 13 \text{ nodes}$$
2.  **Verify the tree edge equation:**
    $$|E| = |V| - 1 = 13 - 1 = 12 \text{ edges}$$

### Example 2: Topological Sorting and Adjacency Trace on a DAG
Consider a DAG with $V = \{A, B, C\}$ and directed edges $E = \{(A, C), (B, C)\}$.
1.  **Formulate the Adjacency Matrix:**
    $$\mathbf{A} = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$$
2.  **Verify the Trace condition:**
    $$\mathbf{A}^2 = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix} \implies \text{Tr}(\mathbf{A}) = 0, \quad \text{Tr}(\mathbf{A}^2) = 0$$
    Since all traces are $0$, the graph is acyclic.
3.  **Find valid topological sorts:**
    An ordering $(v_1, v_2, v_3)$ is topological if for all edges $(u, v)$, index $(u) < \text{index}(v)$.
    *   For edge $(A, C)$: $A$ must precede $C$.
    *   For edge $(B, C)$: $B$ must precede $C$.
    The valid permutations are $(A, B, C)$ and $(B, A, C)$.

---

## 5. Applied ML Context

1.  **Decision Tree Classifiers:** Tree-based architectures (like Random Forests or Gradient Boosting) recursively partition the feature space into hierarchical branches to reach a leaf node prediction.
2.  **Neural Network Computational Graphs:** Frameworks like PyTorch construct dynamic DAGs of operations where nodes represent tensors or operators, ensuring correct backpropagation.
3.  **Bayesian Networks:** Representing conditional probabilities between random variables as DAGs; acyclicity is required to formulate joint probability distributions.
4.  **Hierarchical Clustering Dendrograms:** Agglomerative clustering algorithms build tree diagrams (dendrograms) to represent nested data similarity groups.
5.  **Neural Architecture Search (NAS):** NAS algorithms define topological search spaces as DAGs, where layers are nodes and data channels are directed edges.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here comparing trees, DAGs, and cyclic graphs:
*   Draw three graph structures side-by-side:
    1.  **Tree:** A root node branching down to children (no loops, exactly one path between any two nodes).
    2.  **DAG:** A directed graph with merging pathways (e.g. two paths leading to the same node) but no cycles.
    3.  **Cyclic Graph:** A directed graph with a cycle loop ($u \to v \to w \to u$).
*   Add a caption explaining that trees and DAGs organize computations hierarchically, and the acyclic property protects backpropagation from falling into infinite loops.
