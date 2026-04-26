<h1 align="center"> Chapter 22: PCA </h1>

***





<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite
* **Linear Transformations:** Understanding how a matrix $A$ can rotate and stretch a vector space.
* **Variance and Covariance:** Grasping how much a single variable spreads out and how two variables move together.
* **Eigenvalues and Eigenvectors:** The ability to find vectors that maintain their direction under a specific linear transformation.

</div>


  

## Analogy
In the world of high-end bespoke tailoring, a **Boutique Trial and Fitting** is the ultimate exercise in simplification without loss of essence. When you stand before the mirror in a complex, multi-layered wedding outfit, you are initially overwhelmed by dozens of measurements: the drape of the silk, the tension of the embroidery, the hemline, and the shoulder width. 

However, you don't need to adjust fifty different threads to make the outfit look perfect. Instead, you look for the "primary lines" of the garment—the core structural seams that dictate how the rest of the fabric falls. By identifying these critical axes of the fit, you can ignore the minor wrinkles that don't affect the overall silhouette. PCA is exactly that: it is the process of finding the most influential "seams" in your data so you can describe the entire "outfit" using only the directions that actually matter.


  

## The Math Link
Principal Component Analysis (PCA) is formally defined as an orthogonal linear transformation that transforms the data to a new coordinate system such that the greatest variance by some scalar projection of the data comes to lie on the first coordinate (called the first principal component), the second greatest variance on the second coordinate, and so on.

Let $X \in \mathbb{R}^{n \times d}$ be a data matrix with $n$ observations and $d$ variables, where the columns are centered such that $\sum_{i=1}^{n} X_{ij} = 0$. The objective is to find a weight vector $w_{(1)} = (w_1, \dots, w_d)^T$ that maximizes the variance:

$$w_{(1)} = \arg\max_{\|w\|=1} \left\{ \|Xw\|^2 \right\} = \arg\max_{\|w\|=1} \left\{ w^T X^T X w \right\}$$

Since $w$ is a unit vector, this is equivalent to finding the largest eigenvalue $\lambda$ of the covariance matrix $\Sigma$:

$$\Sigma = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})(x_i - \bar{x})^T$$

The full decomposition is derived via the spectral theorem, where we solve the characteristic equation for the covariance matrix $\Sigma$:

$$\det(\Sigma - \lambda I) = 0$$

**The Link:**
* **The Covariance Matrix ($\Sigma$):** Represents the "interconnectedness" of every stitch and measurement in the wedding outfit.
* **The Eigenvectors ($w$):** These are the "Principal Seams"—the directions of maximum spread or "fit."
* **The Eigenvalues ($\lambda$):** These represent the "Importance" of each seam. A large $\lambda$ means that specific alteration changes the look of the outfit significantly; a near-zero $\lambda$ is just a loose thread you can ignore.


  

<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
Before crunching numbers, remember: PCA isn't deleting data; it’s re-orienting your perspective. You are rotating the room until you are looking at the data from the one specific angle where its "shape" is most obvious and the "depth" is most pronounced.

</div>






  

## Let's Run the Numbers

### Example 1: Trying the Wedding Outfit
Imagine you are measuring the fit of a heavy velvet sherwani. You have two measurements: $x_1$ (Chest width) and $x_2$ (Waist width). In a sample of 3 fittings, the centered measurements (in cm) are:
$X = \begin{pmatrix} 1 & 1 \\ 0 & 0 \\ -1 & -1 \end{pmatrix}$.

**The Calculation:**
1. Compute the Covariance Matrix $\Sigma$ (assuming $n-1$ for unbiased):
$$\Sigma = \frac{1}{2} \begin{pmatrix} (1^2 + 0^2 + (-1)^2) & (1(1) + 0(0) + (-1)(-1)) \\ (1(1) + 0(0) + (-1)(-1)) & (1^2 + 0^2 + (-1)^2) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$$
2. Find Eigenvalues: $\det \begin{pmatrix} 1-\lambda & 1 \\ 1 & 1-\lambda \end{pmatrix} = (1-\lambda)^2 - 1 = 0 \implies \lambda_1 = 2, \lambda_2 = 0$.
3. The first Principal Component (Eigenvector for $\lambda=2$):
$$
\begin{aligned}
  \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} w_1 \\ w_2 \end{pmatrix} &= 2 \begin{pmatrix} w_1 \\ w_2 \end{pmatrix} \\
  w_1 &= w_2 \\
  v_1 &= \begin{pmatrix} \frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} \end{pmatrix}
\end{aligned}
$$

**The Story:** The math shows $\lambda_2 = 0$, meaning the waist and chest measurements move in perfect lockstep. Instead of tracking two numbers, the tailor only needs one "Master Fit" dimension (the diagonal) to describe how the outfit fits the client.

---

### Example 2: Checking the Stitch
A tailor checks the "Stitch Tension" ($x_1$) and "Fabric Elasticity" ($x_2$). For a specific silk, the covariance is $\Sigma = \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$.

**The Calculation:**
$$
\begin{aligned}
  (3-\lambda)^2 - 1 &= 0 \\
  3-\lambda &= \pm 1 \\
  \lambda_1 = 4, &\quad \lambda_2 = 2
\end{aligned}
$$
$$
\begin{aligned}
  \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix} \begin{pmatrix} w_1 \\ w_2 \end{pmatrix} &= 0 \\
  w_1 &= w_2 \\
  \text{Ratio} &= \frac{\lambda_1}{\lambda_1 + \lambda_2} = \frac{4}{4+2} = 66.7\%
\end{aligned}
$$

**The Story:**
By focusing on the first principal component (where tension and elasticity increase together), the tailor captures $66.7\%$ of the structural integrity of the garment. The remaining $33.3\%$ is "noise" or minor variations in the stitch that don't threaten the seam.

---

### Example 3: Deciding on Alterations
The tailor looks at three alterations: Sleeve Length ($x_1$), Cuff Width ($x_2$), and Shoulder Pitch ($x_3$). The data suggests the variance is mostly on the $x_3$ axis. Let $\Sigma = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 10 \end{pmatrix}$.

**The Calculation:**
1. Since the matrix is diagonal, the eigenvalues are the diagonal elements: $\lambda_1 = 10, \lambda_2 = 1, \lambda_3 = 1$.
2. Total Variance $V_{total} = 10 + 1 + 1 = 12$.
3. Contribution of PC1: $\frac{10}{12} \approx 83.3\%$.
4. PC1 Eigenvector: $v_1 = [0, 0, 1]^T$.

**The Story:**
The math tells the tailor that $83.3\%$ of the "discomfort" in the outfit comes from the Shoulder Pitch ($x_3$). Altering the sleeve length or cuff width will only solve a tiny fraction of the problem. Fix the shoulder, and you've fixed the outfit.


  

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Critical Insight:** PCA is extremely sensitive to the scale of your features. If you measure one "stitch" in millimeters and another in kilometers, PCA will assume the millimeter measurement is just "noise" because its variance is numerically tiny. **Always standardize your data (mean=0, variance=1) before performing PCA.**

</div>


  

## ML Applications
* **Facial Recognition (Eigenfaces):** PCA is used to reduce the high-dimensional space of pixel intensities (e.g., $100 \times 100 = 10,000$ dimensions) into a lower-dimensional subspace that captures the most significant facial features.
* **Data Visualization:** Projecting high-dimensional feature sets (like gene expression data) onto 2D or 3D planes to identify clusters or outliers visually.
* **Noise Reduction:** By discarding components with low eigenvalues, PCA effectively filters out the dimensions that contain primarily Gaussian noise, retaining only the signal.
* **Preprocessing for Supervised Learning:** PCA is often applied to remove multicollinearity between features before training linear regression or logistic regression models, which improves numerical stability.
* **Latent Semantic Analysis (LSA):** In NLP, PCA (or the related SVD) is used on term-document matrices to identify underlying "concepts" or "topics" across a corpus of text.


  

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your first principal component explains $99\%$ of the variance but your model performance drops, check if you’ve accidentally included your target variable (label leakage) or a unique ID column in your PCA input. PCA loves high variance, even if that variance is "cheating."

</div>

