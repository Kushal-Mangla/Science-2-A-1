import numpy as np
import matplotlib.pyplot as plt

a = -2  
b = 12  

num_simulations = 10000

def simulate_random_walk(initial_position, num_steps):
    """Simulate a 1D random walk starting from initial_position for num_steps"""
    position = initial_position
    steps = np.random.choice([-1, 1], size=num_steps)
    positions = np.zeros(num_steps + 1)
    positions[0] = initial_position
    
    for i in range(num_steps):
        position += steps[i]
        positions[i + 1] = position
    
    return positions

N_values_part1 = np.arange(1, 101)
return_probabilities = np.zeros(len(N_values_part1))

for i, N in enumerate(N_values_part1):
    returns = 0
    for _ in range(num_simulations):
        final_position = simulate_random_walk(a, N)[-1]
        if final_position == 0:  
            returns += 1
    
    return_probabilities[i] = returns / num_simulations

plt.figure(figsize=(10, 6))
plt.plot(N_values_part1, return_probabilities, 'o-', markersize=4)
plt.xlabel('Number of Steps (N)')
plt.ylabel('Probability of Return to Origin')
plt.title(f'Probability of Return to Origin Starting from Position {a}')
plt.grid(True)
plt.savefig('return_probability.png')

N_values_part2 = np.arange(100, 1001, 50)
meeting_probabilities = np.zeros(len(N_values_part2))

for i, N in enumerate(N_values_part2):
    meetings = 0
    for _ in range(num_simulations):
        person1_positions = simulate_random_walk(a, N)
        person2_positions = simulate_random_walk(b, N)
        
        if person1_positions[-1] == person2_positions[-1]:
            meetings += 1
    
    meeting_probabilities[i] = meetings / num_simulations

plt.figure(figsize=(10, 6))
plt.plot(N_values_part2, meeting_probabilities, 'o-', markersize=4)
plt.xlabel('Number of Steps (N)')
plt.ylabel('Probability of Meeting')
plt.title(f'Probability of Two People Meeting (Starting at {a} and {b})')
plt.grid(True)
plt.savefig('meeting_probability.png')

plt.figure(figsize=(12, 6))

for i in range(5):
    positions = simulate_random_walk(a, 100)
    plt.plot(np.arange(101), positions, alpha=0.7, label=f'Walk {i+1}')

plt.axhline(y=0, color='r', linestyle='--', label='Origin')
plt.xlabel('Time Step')
plt.ylabel('Position')
plt.title(f'Example Random Walks Starting from Position {a}')
plt.legend()
plt.grid(True)
plt.savefig('example_walks.png')

plt.figure(figsize=(12, 6))

for i in range(3):
    positions1 = simulate_random_walk(a, 200)
    positions2 = simulate_random_walk(b, 200)
    plt.plot(np.arange(201), positions1, alpha=0.7, label=f'Person 1 - Walk {i+1}')
    plt.plot(np.arange(201), positions2, alpha=0.7, linestyle='--', label=f'Person 2 - Walk {i+1}')

plt.xlabel('Time Step')
plt.ylabel('Position')
plt.title(f'Example Pairs of Random Walks Starting from Positions {a} and {b}')
plt.legend()
plt.grid(True)
plt.savefig('example_pairs.png')