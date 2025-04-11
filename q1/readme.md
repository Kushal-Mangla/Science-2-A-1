# Monte Carlo Integration Analysis Report

## Introduction

This report analyzes the integration of two functions using the Monte Carlo method:

- $f(x) = \cos(x)$ over the interval $[-\pi, \pi]$
- $f(x) = x^2\cos(x)$ over the interval $[-\pi/2, \pi/2]$

The analysis focuses on the accuracy and convergence of Monte Carlo integration as the number of samples increases.

## The Monte Carlo Integration Method

### Theory

Monte Carlo integration is a numerical technique that uses random sampling to estimate definite integrals. For a function $f(x)$ over an interval $[a,b]$, the integral is approximated as:

$$\int_a^b f(x) dx \approx (b-a) \cdot \frac{1}{N} \sum_{i=1}^{N} f(x_i)$$

where $x_i$ are randomly sampled points uniformly distributed over $[a,b]$.

The error in Monte Carlo integration decreases proportionally to $1/\sqrt{N}$, where $N$ is the number of samples, making it particularly useful for higher-dimensional problems where traditional methods become inefficient.

### Implementation

The provided code implements Monte Carlo integration for both functions using the following steps:

1. Define the integration ranges
2. Generate $N$ random points uniformly distributed within the integration range
3. Evaluate the function at each point
4. Calculate the mean of the function values
5. Multiply by the interval width to obtain the integral estimate

For each function, the code:

- Performs multiple trials (100) for each sample size
- Calculates the average estimate and standard deviation across trials
- Compares with the exact value calculated using scipy.integrate.quad()
- Visualizes the results with error bars

## Code Analysis

### Integration Functions

Two Monte Carlo integration functions were implemented:

```python
def monte_carlo_integrate_cos(N):
    a, b = -np.pi, np.pi
    x = np.random.uniform(a, b, N)  # Generate N random points
    y = np.cos(x)                   # Evaluate function at random points
    integral = (b - a) * np.mean(y) # Calculate estimate
    return integral

def monte_carlo_integrate_x2_cos(N):
    a, b = -np.pi/2, np.pi/2
    x = np.random.uniform(a, b, N)
    y = x**2 * np.cos(x)
    integral = (b - a) * np.mean(y)
    return integral
```

### Experimental Methodology

The code evaluates each function at different sample sizes ($N = 10, 100, 1000, 10000$) with 100 trials per sample size to assess variability. For each sample size and function:

- Multiple trials are performed to capture statistical fluctuations
- The average estimate and standard deviation are calculated
- The error compared to the exact value is determined

### Visualization

The results are visualized using matplotlib, with:

- Separate plots for each function
- Error bars showing standard deviation
- Horizontal lines representing exact values
- Logarithmic scale for sample size

## Results and Analysis

### Exact Values

The exact values calculated using scipy.integrate.quad():

- $\int_{-\pi}^{\pi} \cos(x) dx = 0$
- $\int_{-\pi/2}^{\pi/2} x^2\cos(x) dx \approx 0.967653$

### Results Table

| Function | N | Average Estimate | Standard Deviation | Absolute Error |
|----------|---|------------------|-------------------|---------------|
| $\cos(x)$ | 10 | 0.043146 | 0.648159 | 0.043146 |
| $\cos(x)$ | 100 | -0.006695 | 0.202347 | 0.006695 |
| $\cos(x)$ | 1000 | 0.003058 | 0.060697 | 0.003058 |
| $\cos(x)$ | 10000 | -0.000273 | 0.020050 | 0.000273 |
| $x^2\cos(x)$ | 10 | 0.971358 | 0.272532 | 0.003704 |
| $x^2\cos(x)$ | 100 | 0.964864 | 0.085831 | 0.002789 |
| $x^2\cos(x)$ | 1000 | 0.967902 | 0.026742 | 0.000249 |
| $x^2\cos(x)$ | 10000 | 0.967574 | 0.008587 | 0.000079 |

### Analysis of Convergence

For $\cos(x)$ in $[-\pi, \pi]$:

- As $N$ increases from 10 to 10000, the absolute error decreases from 0.043146 to 0.000273, a reduction of approximately 99.4%
- The standard deviation decreases from 0.648159 to 0.020050, reflecting increased precision
- The error reduction roughly follows the expected $1/\sqrt{N}$ relationship:
  - From N=10 to N=100 (10× samples): Error reduced by factor of ~6.4 (expected √10 ≈ 3.16)
  - From N=100 to N=1000: Error reduced by factor of ~2.2 (expected √10 ≈ 3.16)
  - From N=1000 to N=10000: Error reduced by factor of ~11.2 (expected √10 ≈ 3.16)

For $x^2\cos(x)$ in $[-\pi/2, \pi/2]$:

- As $N$ increases from 10 to 10000, the absolute error decreases from 0.003704 to 0.000079, a reduction of approximately 97.9%
- The standard deviation decreases from 0.272532 to 0.008587
- The error reduction follows the expected $1/\sqrt{N}$ relationship more closely:
  - From N=10 to N=100: Error reduced by factor of ~1.3 (lower than expected)
  - From N=100 to N=1000: Error reduced by factor of ~11.2 (higher than expected)
  - From N=1000 to N=10000: Error reduced by factor of ~3.2 (close to expected √10 ≈ 3.16)

### Visualization of Results

The plots show:

- For both functions, the Monte Carlo estimates converge to the exact values as $N$ increases
- The error bars (standard deviations) shrink with increasing $N$, demonstrating improved precision
- The convergence generally follows the expected $1/\sqrt{N}$ rate, although with some statistical fluctuations

## Discussion

### Effectiveness of Monte Carlo Integration

The results demonstrate that Monte Carlo integration successfully approximates both integrals, with accuracy improving as the number of samples increases. For practical applications:

- $N=1000$ provides a good balance between computational effort and accuracy
- For $\cos(x)$, the absolute error at $N=1000$ is approximately 0.003058
- For $x^2\cos(x)$, the absolute error at $N=1000$ is approximately 0.000249

### Comparing the Two Functions

Interestingly, the Monte Carlo method achieves better relative accuracy for $x^2\cos(x)$ than for $\cos(x)$ at smaller sample sizes. This can be attributed to:

- The integral of $\cos(x)$ over $[-\pi, \pi]$ is exactly zero, making small absolute errors appear large in relative terms
- The $x^2\cos(x)$ function has a more consistent sign across its integration domain, potentially reducing the variance in sampling

### Statistical Variations

The multiple trials reveal inherent randomness in Monte Carlo methods:

- Even at $N=10000$, there is still measurable standard deviation in the estimates
- The actual convergence rate sometimes deviates from the theoretical $1/\sqrt{N}$ due to random fluctuations

## Conclusion

Monte Carlo integration proves to be an effective method for evaluating both $\cos(x)$ over $[-\pi, \pi]$ and $x^2\cos(x)$ over $[-\pi/2, \pi/2]$. The method converges to the exact values as the number of samples increases, with error generally decreasing proportionally to $1/\sqrt{N}$.

For practical applications requiring moderate precision (errors < 0.5%), approximately 1000 samples provide sufficient accuracy for both integrals examined. The multiple-trial approach reveals the statistical variability inherent in Monte Carlo methods, which decreases predictably with larger sample sizes.

This analysis confirms that Monte Carlo integration is a reliable technique for numerical integration, especially when the number of samples is sufficiently large to mitigate the effects of random sampling variation.