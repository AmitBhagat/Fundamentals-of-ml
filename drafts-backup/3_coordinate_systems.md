<h1 align="center"> Chapter 3: Coordinate Systems </h1>

---

<div style="text-align: justify;">


<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite

- **Vector Definition:** Understanding a vector as an ordered list of numbers representing a point in space.
- **Basis Vectors:** The concept that complex locations can be broken down into a combination of fundamental "steps" (unit vectors).
- **Scalar Multiplication:** The ability to scale a direction by a real number to reach a specific magnitude.

</div>

## Analogy

In the world of online grocery shopping, a coordinate system is your **Digital Address**. Without it, the app has no way to bridge the gap between your craving for sourdough and the physical loaf sitting in a dark store.

Think of the coordinate system as the "Aisle and Shelf" logic of the warehouse. To locate an item, you don't just wander aimlessly; you follow a structured set of instructions. If the app says an item is at $[3, 12]$, it means you go to Aisle 3, then move 12 units down to find the shelf. The coordinate system provides the universal language that translates a physical reality—the location of your "essentials"—into a set of numbers the delivery system can process. Without this shared "map," the delivery driver is just driving in circles, and your groceries remain "out of stock" simply because they couldn't be found.

## The Math Link

Formally, a coordinate system is defined by a basis $\mathcal{B} = \{ \mathbf{b}_1, \mathbf{b}_2, \dots, \mathbf{b}_n \}$ for a vector space $\mathcal{V}$. For any vector $\mathbf{v} \in \mathcal{V}$, there exists a unique set of scalars $c_1, c_2, \dots, c_n$ such that:

$$\mathbf{v} = \sum_{i=1}^{n} c_i \mathbf{b}_i = c_1 \mathbf{b}_1 + c_2 \mathbf{b}_2 + \dots + c_n \mathbf{b}_n$$

The coordinate vector of $\mathbf{v}$ with respect to $\mathcal{B}$ is denoted as:

$$[\mathbf{v}]_{\mathcal{B}} = \begin{bmatrix} c_1 \\ c_2 \\ \vdots \\ c_n \end{bmatrix}$$

**The Link:**

- $\mathbf{v}$: The actual "Essential Item" (the physical location in the warehouse).
- $\mathcal{B}$: The "Warehouse Layout" (the defined directions of the aisles).
- $c_i$: The "Navigation Steps" (how many aisles over and how many shelves down you must go).
- $[\mathbf{v}]_{\mathcal{B}}$: The "Digital Receipt" (the numeric representation stored in the app).

<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
A coordinate is just a set of instructions. It doesn't tell you _what_ the object is; it tells you exactly how much of each "standard movement" you need to perform to arrive at its location. Change the basis (the warehouse layout), and the numbers change, even if the item hasn't moved an inch.

</div>

## Let's Run the Numbers

### 1. Stocking up on essentials

You are a warehouse picker looking for the "Organic Milk" essential. The warehouse uses a standard Cartesian basis $\mathbf{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ (one meter North) and $\mathbf{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ (one meter East). The item is located at $\mathbf{v} = 4\mathbf{e}_1 + 7\mathbf{e}_2$.

**The Calculation:**
$$[\mathbf{v}]_{\mathcal{B}} = \begin{bmatrix} 4 \\ 7 \end{bmatrix}$$
The displacement from the origin $(0,0)$ is:
$$\|\mathbf{v}\| = \sqrt{4^2 + 7^2} = \sqrt{16 + 49} = \sqrt{65} \approx 8.06 \text{ meters}$$

**The Story:**
The math tells the picker that to grab the milk, they need to travel exactly 4 meters North and 7 meters East. The Euclidean distance of $8.06$ represents the "as-the-crow-flies" distance the app uses to estimate the picker's travel time.

---

### 2. The 10-minute delivery wait

A delivery rider is at point $A(2, 3)$ and your house is at $B(5, -1)$. The app needs to calculate the distance to update your "Time to Arrival" timer.

**The Calculation:**
The displacement vector $\mathbf{d}$ is:
$$\mathbf{d} = \mathbf{B} - \mathbf{A} = \begin{bmatrix} 5 \\ -1 \end{bmatrix} - \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} 5-2 \\ -1-3 \end{bmatrix} = \begin{bmatrix} 3 \\ -4 \end{bmatrix}$$
The magnitude of the delivery path is:
$$\|\mathbf{d}\| = \sqrt{3^2 + (-4)^2} = \sqrt{9 + 16} = \sqrt{25} = 5 \text{ units}$$

**The Story:**
By subtracting the coordinate vectors, the system determines the rider must move 3 units on one axis and -4 on another. The result, 5 units, is used to calculate the 10-minute wait—if 1 unit takes 2 minutes, the math confirms you’ll be eating in exactly 10 minutes.

---

### 3. Handling out-of-stock items

An item is "Out of Stock" in the main warehouse (Basis $\mathcal{B}$), so the app checks the "Local Hub" (Basis $\mathcal{B}'$). We need to convert the coordinates from the Hub's system to the Main system using a transition matrix $P$.
Let $P = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ and the item's location in the Hub be $[\mathbf{v}]_{\mathcal{B}'} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$.

**The Calculation:**
$$[\mathbf{v}]_{\mathcal{B}} = P [\mathbf{v}]_{\mathcal{B}'} = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
$$[\mathbf{v}]_{\mathcal{B}} = \begin{bmatrix} (2 \times 1) + (1 \times 1) \\ (1 \times 1) + (2 \times 1) \end{bmatrix} = \begin{bmatrix} 3 \\ 3 \end{bmatrix}$$

**The Story:**
The math translates the "Local Hub" language into the "Main Warehouse" language. While the Hub saw the item at $[1, 1]$, the Main system now knows it needs to look at $[3, 3]$ to fulfill the order from the secondary source.

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**CRITICAL INSIGHT**
Coordinates are meaningless without their Basis. In ML, we often transform data into "Latent Space" (a different coordinate system). If you try to calculate the distance between two points where one is in the original coordinate system and the other is in a transformed space, your model will yield garbage results. Always ensure your vectors live in the same basis before performing operations.

</div>

## ML Applications

- **Image Representation:** Digital images are represented in a 2D coordinate system where each $(x, y)$ coordinate maps to a pixel value or a vector of values (RGB).
- **Word Embeddings:** Algorithms like Word2Vec map words into a high-dimensional coordinate system (e.g., 300D). The "location" of a word vector determines its semantic meaning relative to others.
- **Principal Component Analysis (PCA):** PCA finds a new coordinate system (basis) for the data such that the first coordinate (first principal component) captures the maximum variance.
- **Object Detection:** Models like YOLO (You Only Look Once) predict coordinates $[x, y, w, h]$ to define bounding boxes around objects in a frame.
- **Latent Space Navigation:** In Generative Adversarial Networks (GANs), we navigate the coordinate system of the latent space to modify specific features of generated output (e.g., changing hair color in a face-generation model).

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your loss function isn't converging, check your coordinate scales. If one feature (coordinate) ranges from $0$ to $1$ and another from $0$ to $1,000,000$, the "distance" calculations will be dominated by the larger scale, effectively ignoring the first feature. Normalize your coordinates!

</div>


</div>