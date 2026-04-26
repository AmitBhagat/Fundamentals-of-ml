<h1 align="center"> Chapter 61: Chi-Square Test </h1>

---

<div style="text-align: justify;">


<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

### Prerequisite

- **Probability Distributions:** A solid grasp of the Normal distribution and the concept of "sampling distribution."
- **Hypothesis Testing:** Understanding the Null Hypothesis ($H_0$), Alternative Hypothesis ($H_a$), and the $p$-value.
- **Categorical Data:** Distinction between nominal/ordinal variables and continuous numerical data.

</div>

---

## Analogy

When you sit down to renew your car insurance, you aren't just blindly paying a bill; you are performing a mental audit. You have an internal expectation of what the premium "should" look like based on your clean driving record, the age of your vehicle, and market trends. However, the quote the insurance company sends over—the "observed" reality—rarely aligns perfectly with your "expected" reality.

The Chi-Square test is essentially the mathematical equivalent of that audit. It measures the friction between what you expected to see and what actually showed up in your inbox. If the gap between your expected quote and the observed quote is small, you chalk it up to minor market fluctuations. But if that gap is massive, you know something fundamental has changed—perhaps your "no-claim" status wasn't applied, or the car's value was miscalculated. The test quantifies this discrepancy to tell you if the difference is just "noise" or if there is a statistically significant reason to pick up the phone and dispute the quote.

---

## The Math Link

In formal terms, the Chi-Square ($\chi^2$) statistic measures the normalized squared deviation between observed frequencies and expected frequencies under a null hypothesis $H_0$.

Let $\mathcal{O}$ be the set of observed frequencies and $\mathcal{E}$ be the set of expected frequencies for $k$ mutually exclusive categories. The Chi-Square statistic is defined as:

$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$

Where:

- $O_i \in \mathcal{O}$ represents the observed frequency for category $i$.
- $E_i \in \mathcal{E}$ represents the expected frequency for category $i$, calculated as $E_i = n \cdot p_i$ for a sample size $n$ and hypothesized probability $p_i$.
- $k$ is the number of categories.

To determine if the result is significant, we compare $\chi^2$ to a distribution with degrees of freedom $df = k - 1$ (for Goodness of Fit) or $df = (r-1)(c-1)$ (for Independence, where $r$ and $c$ are rows and columns in a contingency table).

The logic follows a squared distance metric:

1.  **The Residual $(O_i - E_i)$:** The raw difference between your insurance quote and your expectation.
2.  **Squaring $(O_i - E_i)^2$:** This ensures that "underpaying" and "overpaying" both contribute positively to the total error, preventing differences from canceling each other out.
3.  **Normalization $(\div E_i)$:** This scales the error. A \$500 discrepancy matters more on a \$1,000 policy than on a \$10,000 commercial fleet policy.

---



<div style="background-color: #f0fff4; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**THE INTUITION**
Think of $\chi^2$ as a "surprise meter." If the value is near zero, your data is exactly what you predicted. As the value climbs, your "surprise" increases. Once the value crosses a specific threshold (the critical value), the surprise is so great that you must reject your original assumptions.

</div>

## Let's Run the Numbers

### 1. Comparing Quotes (Goodness of Fit)

You are looking at premium quotes across three different providers. Based on last year's market share, you expect quotes to be distributed evenly (33.3% each) among 300 neighbors. However, you observe: Provider A (120), Provider B (90), Provider C (90).

**Calculation:**
$E_A = 100, E_B = 100, E_C = 100$
$$\chi^2 = \frac{(120-100)^2}{100} + \frac{(90-100)^2}{100} + \frac{(90-100)^2}{100}$$
$$\chi^2 = \frac{400}{100} + \frac{100}{100} + \frac{100}{100} = 4 + 1 + 1 = 6.0$$

**The Story:** With $df = 2$, a $\chi^2$ of $6.0$ yields a $p$-value of approximately $0.049$. Since this is below $0.05$, you conclude the quotes are not distributed as expected; Provider A is significantly more dominant in your neighborhood than the "even share" theory suggested.

### 2. Checking the IDV (Test of Independence)

You want to see if the Insured Declared Value (IDV) (High vs. Low) is independent of the likelihood of a claim being filed. You track 200 policies.

|              | Claim | No Claim | Total |
| ------------ | ----- | -------- | ----- |
| **High IDV** | 40    | 60       | 100   |
| **Low IDV**  | 20    | 80       | 100   |
| **Total**    | 60    | 140      | 200   |

**Calculation:**
$E_{1,1} = \frac{100 \times 60}{200} = 30$
$$\chi^2 = \frac{(40-30)^2}{30} + \frac{(60-70)^2}{70} + \frac{(20-30)^2}{30} + \frac{(80-70)^2}{70}$$
$$\chi^2 = 3.33 + 1.43 + 3.33 + 1.43 = 9.52$$

**The Story:** With $df = 1$, a $\chi^2$ of $9.52$ is much higher than the critical value ($3.84$). This proves the IDV and Claim status are **dependent**. High-value cars are statistically more likely to result in claims.

### 3. The No-Claim Bonus (NCB) Retention

An insurer claims that 80% of their clients maintain their 50% No-Claim Bonus year-over-year. You sample 100 clients and find only 70 kept their bonus.

**Calculation:**
$O_{kept} = 70, E_{kept} = 80$
$O_{lost} = 30, E_{lost} = 20$
$$\chi^2 = \frac{(70-80)^2}{80} + \frac{(30-20)^2}{20} = \frac{100}{80} + \frac{100}{20} = 1.25 + 5.0 = 6.25$$

**The Story:** The high $\chi^2$ value suggests the insurer’s claim is misleading. The "lost" bonus category contributed most to the score, indicating a significantly higher-than-expected rate of accidents or claims among their pool.

---

<div style="background-color: #fff5f5; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**The Frequency Fallacy:** Chi-Square MUST be performed on raw frequency counts, never on percentages or ratios. If you run a Chi-Square on percentages (e.g., using 0.70 instead of 70), the denominator $E_i$ will be tiny, blowing the $\chi^2$ value out of proportion and leading to a Type I error (false positive).

</div>

## ML Applications

- **Feature Selection:** In supervised learning, the Chi-Square test is used to rank categorical features. By measuring the independence between a feature and the target label, we can discard features that provide zero information gain.
- **Deciding Discretization Bins:** When converting continuous variables into categorical "bins," Chi-Square analysis helps determine if the bin boundaries maintain the statistical relationship with the target variable.
- **Model Calibration Checks:** Used to evaluate if the predicted probabilities of a classifier match the observed frequencies of the classes (e.g., if a model predicts 10% probability of churn, do 10 out of 100 samples actually churn?).
- **Data Drift Detection:** In MLOps, Chi-Square is used to compare the distribution of categorical features in production data vs. training data. A high $\chi^2$ score triggers an alert that the model’s environment has changed.
- **Image Histogram Comparison:** While often replaced by Earth Mover's Distance, Chi-Square is a classic method for comparing the distribution of pixel intensities (stored as frequency bins) between two images for similarity detection.

---

<div style="background-color: #fffaf0; padding: 15px; border-radius: 8px; color: #1f2328; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05);">

**Debugging Tip:** If your expected frequency $E_i$ in any cell is less than 5, the Chi-Square test becomes unreliable. In these cases, your "insurance audit" is underpowered. You should either increase your sample size or use **Fisher’s Exact Test** instead.

</div>


</div>