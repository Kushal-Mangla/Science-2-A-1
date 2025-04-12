import numpy as np
import matplotlib.pyplot as plt

def random_walk(num_steps, initial_pos=0, num_simulations=1000):
    """Simulate multiple 1D random walks."""
    steps = np.random.choice([-1, 1], size=(num_simulations, num_steps))
    positions = np.cumsum(steps, axis=1) + initial_pos
    return positions

def probability_return_to_start(a, N_range):
    probabilities = []
    for N in N_range:
        final_positions = random_walk(N, initial_pos=a)[:, -1]
        prob = np.sum(final_positions == a) / len(final_positions)
        probabilities.append(prob)
    return probabilities

def probability_meeting(a, b, N_range):
    probabilities = []
    for N in N_range:
        positions_a = random_walk(N, initial_pos=a)
        positions_b = random_walk(N, initial_pos=b)
        
        meetings = np.zeros(positions_a.shape[0], dtype=bool)
        for t in range(N):
            meetings = meetings | (positions_a[:, t] == positions_b[:, t])
        
        prob = np.sum(meetings) / positions_a.shape[0]
        probabilities.append(prob)
    return probabilities

a = -2  
b = 12   
NUM_SIMULATIONS = 1000

# Part (i)
N_range_i = np.arange(1, 101)
prob_return = probability_return_to_start(a, N_range_i)

plt.figure(figsize=(8, 5))
plt.plot(N_range_i, prob_return, 'b-')
plt.xlabel('Number of Steps (N)')
plt.ylabel('Probability of Returning to Start')
plt.title(f'Probability of Ending at Position a={a}\nStarting from a={a}')
plt.grid(True)
plt.savefig('return_probability.png')
print("Return probability plot saved as 'return_probability.png'")

# Part (ii)
N_range_ii = np.arange(100, 1001, 50)
prob_meet = probability_meeting(a, b, N_range_ii)

plt.figure(figsize=(8, 5))
plt.plot(N_range_ii, prob_meet, 'r-')
plt.xlabel('Number of Steps (N)')
plt.ylabel('Probability of Meeting')
plt.title(f'Probability of Two Walkers Meeting\na={a}, b={b}')
plt.grid(True)
plt.savefig('meeting_probability.png')
print("Meeting probability plot saved as 'meeting_probability.png'")

even_indices_i = [i for i, N in enumerate(N_range_i) if N % 2 == 0]
print("\nProbability of returning to starting position:")
for i, N in enumerate(N_range_i[::20]):
    print(f"N = {N}: {prob_return[::20][i]:.4f}")
    
print("\nProbability of returning to starting position (even N values):")
for i in even_indices_i[::10]:  # Sample every 10th even N value
    N = N_range_i[i]
    print(f"N = {N}: {prob_return[i]:.4f}")

print("\nProbability of meeting:")
for i, N in enumerate(N_range_ii[::5]):
    print(f"N = {N}: {prob_meet[::5][i]:.4f}")