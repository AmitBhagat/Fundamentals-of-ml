---
title: "Quantization Math"
description: "Mastering the physics of shrinking AI models from floating-point giants to integer speedsters."
complexity: "Advanced"
estimated_time: "25 min"
prerequisites: ["Foundations", "Floating Point & Machine Epsilon"]
---

<h1 align="center"> Chapter 7: Quantization Math </h1>

---

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite

- **Floating Point (FP32):** Understanding how decimals are stored with high precision.
- **Dynamic Range:** The difference between the largest and smallest numbers in a set.
- **Basic Algebra:** Comfort with linear mapping ($y = mx + c$).

</div>

---

## Analogy

Imagine you are a professional painter with a palette of 16 million colors (FP32 precision). You’ve painted a masterpiece. Now, you are told you have to recreate that same masterpiece using only a 256-color "Crayola" box (INT8 quantization). 

If you just pick random colors, the painting will look like a mess. But if you carefully **map** your palette—assigning "Crayola Forest Green" to represent all the shades of deep green in your painting—you can maintain the "Essence" of the image while using a fraction of the memory. 

Quantization is the art of **Numerical Binning**. We are rounding the "cents" of our model's weights to the nearest "dollar." You lose the tiny details, but the "Big Picture" (the model's logic) stays the same, and the "Paperwork" (the computation) becomes 4x faster and takes 4x less space.

---

## The Math Link

The most common form of quantization is **Affine Quantization**, which maps a floating-point range $[min, max]$ to an integer range $[0, 255]$ (for unsigned INT8).

**The Quantization Formula:**
$$x_q = \text{round}\left( \frac{x}{S} + Z \right)$$

Where:
- $x$: The original floating-point value.
- $x_q$: The quantized integer value.
- $S$ (**Scale**): A floating-point number that "stretches" the range.
- $Z$ (**Zero-point**): An integer that maps the real-world $0.0$ to a specific quantized value.

**Deriving the Scale ($S$):**
If we want to map the float range $[r_{min}, r_{max}]$ to the integer range $[q_{min}, q_{max}]$:
$$S = \frac{r_{max} - r_{min}}{q_{max} - q_{min}}$$

**Deriving the Zero-point ($Z$):**
$$Z = \text{round}(q_{min} - \frac{r_{min}}{S})$$

---

<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
Quantization is just a **Linear Transformation**. We are sliding ($Z$) and squashing ($S$) the continuous world into a grid of discrete buckets. If $S$ is large, the buckets are wide and we lose a lot of detail (high quantization error). If $S$ is small, we keep more detail but cover less range.

</div>

---

## Let's Run the Numbers

### Example 1: Calculating the Scale and Zero-point

You have a set of weights ranging from $r_{min} = -2.0$ to $r_{max} = 3.0$. You want to quantize them to an unsigned 8-bit integer ($q_{min}=0, q_{max}=255$).

**Calculation:**
1. Calculate Scale ($S$):
   $$S = \frac{3.0 - (-2.0)}{255 - 0} = \frac{5.0}{255} \approx 0.0196$$
2. Calculate Zero-point ($Z$):
   $$Z = \text{round}(0 - \frac{-2.0}{0.0196}) = \text{round}(102.04) = 102$$

**The Story:** A float value of $-2.0$ will be stored as the integer $0$. A float value of $0.0$ will be stored as the integer $102$. The math ensures that $0.0$ always has an exact representation in the integer space.

### Example 2: Quantizing a Specific Weight

Using the parameters from Example 1 ($S = 0.0196, Z = 102$), what is the quantized value for a weight $x = 1.2$?

**Calculation:**
$$x_q = \text{round}\left( \frac{1.2}{0.0196} + 102 \right)$$
1. $\frac{1.2}{0.0196} \approx 61.22$
2. $61.22 + 102 = 163.22$
3. $\text{round}(163.22) = 163$

**The Story:** Our high-precision $1.2$ is now simply $163$. We saved 3 bytes of memory, but we lost $0.22$ "units" of precision (the rounding error).

### Example 3: De-quantization (The Reconstruction)

After doing integer math, your GPU outputs a result $y_q = 200$. What is the actual floating-point value $y$?

**Notation:**
$$y = S \cdot (y_q - Z)$$

**Calculation:**
1. $(200 - 102) = 98$
2. $y = 0.0196 \times 98 = 1.9208$

**The Story:** By subtracting the zero-point and scaling back up, we "recover" the decimal. Note that if the original value was $1.9215$, we would have lost that tiny difference forever. This is the "Price of Speed."

---

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**CRITICAL TECHNICAL INSIGHT: The Outlier Trap**
If your weight range is $[-1.0, 1.0]$ but you have one "Outlier" at $100.0$, your $S$ becomes huge: $\frac{100 - (-1)}{255} \approx 0.4$. Now, every small weight in the $[-1, 1]$ range will be rounded to the same bucket (likely zero or one). **Always clip your outliers** or use "Group-wise" quantization to prevent one loud weight from muting the entire layer!

</div>

---

## ML Applications

1.  **llama.cpp & GGUF:** The backbone of local LLMs. Quantizing Llama-3 from 140GB (FP16) to 40GB (Q4_K_M) so it fits on a single Mac.
2.  **Mobile AI (CoreML/TFLite):** Converting models to INT8 so they can run on the low-power Neural Engine of a smartphone.
3.  **NVIDIA TensorRT:** Uses INT8 quantization and hardware acceleration to double the throughput of GPUs in data centers.
4.  **BitNet / 1-bit LLMs:** The extreme frontier where weights are quantized to just $\{-1, 0, 1\}$. No multiplications are needed—only additions.
5.  **Quantization-Aware Training (QAT):** Simulating the "rounding error" during training so the model learns to be robust to its own future precision loss.

---

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your model's accuracy tanks after quantization, check the **Weight Distribution** histograms. If you see "Spikes" at zero, your zero-point is likely off, or your dynamic range is too wide due to unclipped outliers. Use **Per-Channel Quantization** instead of Per-Tensor to give each filter its own scale.

</div>
