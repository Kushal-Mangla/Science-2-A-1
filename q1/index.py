import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

def monte_carlo_integrate_cos(N):
    a, b = -np.pi, np.pi
    x = np.random.uniform(a, b, N)
    y = np.cos(x)
    integral = (b - a) * np.mean(y)
    return integral

def monte_carlo_integrate_x2_cos(N):
    a, b = -np.pi/2, np.pi/2
    x = np.random.uniform(a, b, N)
    y = x**2 * np.cos(x)
    integral = (b - a) * np.mean(y)
    return integral

exact_cos = integrate.quad(lambda x: np.cos(x), -np.pi, np.pi)[0]
exact_x2cos = integrate.quad(lambda x: x**2 * np.cos(x), -np.pi/2, np.pi/2)[0]

print(f"Exact value for cos(x): {exact_cos}")
print(f"Exact value for x^2*cos(x): {exact_x2cos}")

N_values = [10, 100, 1000, 10000]
num_trials = 100  # multiple trials
results_cos = []
results_x2cos = []
errors_cos = []
errors_x2cos = []

for N in N_values:
    cos_trials = []
    x2cos_trials = []
    
    for _ in range(num_trials):
        cos_trials.append(monte_carlo_integrate_cos(N))
        x2cos_trials.append(monte_carlo_integrate_x2_cos(N))
    
    avg_cos = np.mean(cos_trials)
    avg_x2cos = np.mean(x2cos_trials)
    
    std_cos = np.std(cos_trials)
    std_x2cos = np.std(x2cos_trials)
    
    results_cos.append(avg_cos)
    results_x2cos.append(avg_x2cos)
    errors_cos.append(std_cos)
    errors_x2cos.append(std_x2cos)
    
    print(f"N={N}:")
    print(f"  cos(x): {avg_cos:.6f} ± {std_cos:.6f} (Error: {abs(avg_cos - exact_cos):.6f})")
    print(f"  x^2*cos(x): {avg_x2cos:.6f} ± {std_x2cos:.6f} (Error: {abs(avg_x2cos - exact_x2cos):.6f})")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.errorbar(N_values, results_cos, yerr=errors_cos, marker='o', label='Monte Carlo estimate')
plt.axhline(y=exact_cos, color='r', linestyle='--', label=f'Exact value: {exact_cos:.6f}')
plt.xscale('log')
plt.title('Monte Carlo Integration: cos(x)')
plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated Integral')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.errorbar(N_values, results_x2cos, yerr=errors_x2cos, marker='o', color='orange', label='Monte Carlo estimate')
plt.axhline(y=exact_x2cos, color='r', linestyle='--', label=f'Exact value: {exact_x2cos:.6f}')
plt.xscale('log')
plt.title('Monte Carlo Integration: x^2 * cos(x)')
plt.xlabel('Number of samples (N)')
plt.ylabel('Estimated Integral')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('monte_carlo_integration_improved.png')
print("Plot saved as 'monte_carlo_integration_improved.png'")