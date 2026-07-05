---
title: "Convolutional Geometry"
description: "Spatial transformations, output dimension formulas, cross-correlation equations, and receptive field expansion math."
complexity: "Advanced"
estimated_time: "40 min"
prerequisites: ["Linear Algebra: Matrices", "Linear Algebra: Orthogonality and Projections"]
---

<h1 align="center"> Chapter 114: Convolutional Geometry </h1>

***

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **2D Cross-Correlation:** The mathematical operation of sweeping a sliding matrix window (kernel) across a 2D grid, computing the sum of element-wise products.
* **Translation Invariance:** The property where a feature detector outputs the same activation regardless of where the target feature resides in the input plane.

</div>

## 1. Conceptual Hook

Images are extremely high-dimensional grids of raw pixel values. Feeding these directly into standard fully connected neural networks is a recipe for parameter explosion and overfitting, as it ignores the spatial structure of visual data. A **Convolutional Layer** solves this by imposing spatial logic (a strong inductive bias) directly onto the network's architecture.

Instead of looking at the entire image at once, the network sweeps a tiny parameter filter (or kernel) across the input, computing local dot products to extract local features such as edges, textures, and shapes.

The geometry of this operation—defined by kernel size, stride, padding, and dilation—determines how the output feature maps shrink and how the network's "Receptive Field" (its view of the input world) expands. Stacking these simple geometric operations allows deep neural networks to assemble low-level edges into high-level object concepts.

---

## 2. Formal Definition

Let $\mathbf{X} \in \mathbb{R}^{H \times W \times C_{in}}$ be the input tensor, where $H, W$ are the height and width, and $C_{in}$ is the number of input channels. Let $\mathbf{K} \in \mathbb{R}^{K_h \times K_w \times C_{in} \times C_{out}}$ be the kernel tensor.

### 2D Cross-Correlation (Convolution in ML)
For a stride of $S_h$ vertically and $S_w$ horizontally, the output tensor $\mathbf{Y} \in \mathbb{R}^{H_{out} \times W_{out} \times C_{out}}$ at channel $c$ and coordinate $(i, j)$ is:
$$\mathbf{Y}_{i, j, c} = b_c + \sum_{m=0}^{K_h - 1} \sum_{n=0}^{K_w - 1} \sum_{k=0}^{C_{in} - 1} \mathbf{X}_{i \cdot S_h + m, \quad j \cdot S_w + n, \quad k} \cdot \mathbf{K}_{m, n, k, c}$$
where $b_c$ is the bias term for output channel $c$.

### Output Dimension Formula
Given input size $I$, kernel size $K$, padding $P$, stride $S$, and dilation rate $D$, the output dimension $O$ along that axis is:
$$O = \left\lfloor \frac{I - (K - 1) \cdot D - 1 + 2P}{S} \right\rfloor + 1$$

Under standard, non-dilated convolution ($D = 1$), this simplifies to:
$$O = \left\lfloor \frac{I - K + 2P}{S} \right\rfloor + 1$$

---

## 3. Illustrative Derivation

### Derivation of Receptive Field Growth in Deep Architectures
We derive the recursive formula for the Receptive Field ($RF_L$) of layer $L$, proving how strides and kernel sizes interact to scale the network's spatial view.

*Proof:*
The receptive field $RF_L$ is the physical coordinate span in the original input image that directly contributes to the value of a single pixel in the feature map of layer $L$. Let $K_i$ be the kernel size and $S_i$ be the stride at layer $i$.

1.  **Evaluate the base case (Layer 1):**
    A single pixel in the output feature map of Layer 1 is computed directly from a $K_1 \times K_1$ grid of input pixels:
    $$RF_1 = K_1$$

2.  **Evaluate Layer 2:**
    A single pixel in Layer 2 is computed from a $K_2 \times K_2$ grid of pixels in Layer 1. The step size (or jump) between adjacent pixels in Layer 1, measured in input coordinates, is equal to the stride $S_1$.
    Therefore, the span of $K_2$ pixels in Layer 1 translates to:
    $$RF_2 = RF_1 + (K_2 - 1) \cdot S_1 = K_1 + (K_2 - 1) \cdot S_1$$

3.  **Inductive step for Layer $L$:**
    Assume that at layer $L-1$, the receptive field is $RF_{L-1}$. The cumulative step size (jump) of a single coordinate increment in Layer $L-1$ features, relative to the input image coordinates, is:
    $$J_{L-1} = \prod_{i=1}^{L-1} S_i$$
    When we apply a kernel of size $K_L$ at layer $L$, the pixels in this kernel are separated by a stride step of $J_{L-1}$ input pixels. The new receptive field is:
    $$RF_L = RF_{L-1} + (K_L - 1) \cdot J_{L-1}$$
    Substitute the product form of $J_{L-1}$:
    $$RF_L = RF_{L-1} + (K_L - 1) \cdot \prod_{i=1}^{L-1} S_i \quad \blacksquare$$

This proves that strides in early layers act as multipliers on the receptive field growth of downstream layers, allowing deep networks to rapidly capture global context.

---

## 4. Concrete Examples

### Example 1: Output Dimension Calculation
We compute the output size of an ImageNet input image of size $I = 224$ passing through a kernel of size $K = 7$ with stride $S = 2$ and padding $P = 3$.
1.  **Formulate the equation:**
    $$O = \left\lfloor \frac{224 - 7 + 2(3)}{2} \right\rfloor + 1$$
2.  **Calculate the value:**
    $$O = \left\lfloor \frac{217 + 6}{2} \right\rfloor + 1 = \left\lfloor \frac{223}{2} \right\rfloor + 1 = 111 + 1 = 112$$
The resulting feature map has a dimension of $112 \times 112$.

### Example 2: Receptive Field Calculation
We compute the receptive field of a 3-layer network:
*   Layer 1: $K_1 = 3, S_1 = 1$.
*   Layer 2: $K_2 = 3, S_2 = 2$.
*   Layer 3: $K_3 = 3, S_3 = 1$.
1.  **Calculate Layer 1 RF:**
    $$RF_1 = K_1 = 3$$
2.  **Calculate Layer 2 RF:**
    $$RF_2 = RF_1 + (K_2 - 1) \cdot S_1 = 3 + (3 - 1) \cdot 1 = 5$$
3.  **Calculate Layer 3 RF:**
    $$RF_3 = RF_2 + (K_3 - 1) \cdot (S_1 \cdot S_2) = 5 + (3 - 1) \cdot (1 \cdot 2) = 5 + 2 \cdot 2 = 9$$
Thus, a single pixel in Layer 3 has an effective receptive field of $9 \times 9$ in the input image.

---

## 5. Applied ML Context

1.  **Biometric Face Identification:** Deep CNNs extract features hierarchically (edges $\to$ components $\to$ faces) to match faces in datasets.
2.  **Clinical MRI Lesion Detection:** Convolution filters sweep scans to identify micro-textures indicative of anomalies.
3.  **Self-Driving Car Vision (YOLO):** Real-time bounding box systems use strided convolutional networks to detect pedestrians.
4.  **Satellite Forest Analysis:** Dilated convolutions ($D > 1$) capture macro-scale geological formations without losing local resolution.
5.  **Generative Up-scaling (Transposed Convolution):** Generator networks reconstruct low-dimensional latent vectors into high-resolution images.

---

## 6. Visual/Intuitive Summary

A diagram should be placed here illustrating 2D convolution geometry:
*   Draw a 3D projection comparing the input, kernel, and output grids:
    *   **Input Map:** Draw a $5 \times 5$ grid of blue squares, surrounded by a dashed border of zeros to show Padding ($P=1$).
    *   **Kernel Window:** Draw a $3 \times 3$ semi-transparent yellow grid hovering over the top-left corner of the input.
    *   **Output Map:** Draw a $3 \times 3$ grid of green squares, with a projection line connecting the $3 \times 3$ input region to a single cell in the output map.
*   Draw a horizontal arrow showing Stride ($S=1$) moving the kernel window.
*   Add a caption explaining that 2D convolution slides a small weight filter across an input tensor, computing local dot products to project spatial patterns into localized activation maps.
