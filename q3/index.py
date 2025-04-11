import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from matplotlib.animation import FuncAnimation

# Parameters based on roll number 2023101026
k = 3  # spring constant
m = 1  # mass

def analytical_solution():
    # The mass matrix is just the identity matrix for m=1
    M = np.eye(3)
    
    # The stiffness matrix K for the system
    # Each mass is connected to adjacent masses and the walls with springs of constant k
    K = np.array([
        [2*k, -k, 0],
        [-k, 2*k, -k],
        [0, -k, 2*k]
    ])
    
    # Solve the eigenvalue problem: K·v = ω²·M·v
    eigenvalues, eigenvectors = eigh(K, M)
    
    # The eigenvalues are ω² (squared angular frequencies)
    frequencies = np.sqrt(eigenvalues)
    
    return frequencies, eigenvectors

def plot_normal_modes(frequencies, eigenvectors):
    plt.figure(figsize=(12, 10))
    mode_names = ["First", "Second", "Third"]
    
    for i in range(3):
        plt.subplot(3, 1, i+1)
        plt.bar(np.arange(1, 4), eigenvectors[:, i], width=0.5)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.xticks(np.arange(1, 4), ['Mass 1', 'Mass 2', 'Mass 3'])
        plt.ylabel('Amplitude')
        plt.title(f"{mode_names[i]} Normal Mode: ω = {frequencies[i]:.4f} rad/s")
        
    plt.tight_layout()
    plt.savefig('normal_modes.png')
    # plt.show()

def simulate_motion_euler(mode_index, duration=10, dt=0.01):
    frequencies, eigenvectors = analytical_solution()
    omega = frequencies[mode_index]
    normal_mode = eigenvectors[:, mode_index]
    
    t = np.arange(0, duration, dt)
    
    positions = np.zeros((len(t), 3))
    velocities = np.zeros((len(t), 3))
    
    positions[0] = normal_mode
    
    velocities[0] = np.zeros(3)
    
    for i in range(1, len(t)):
        positions[i] = positions[i-1] + velocities[i-1] * dt
        
        accelerations = -omega**2 * positions[i-1]
        
        velocities[i] = velocities[i-1] + accelerations * dt
    
    return t, positions

def plot_trajectories():
    frequencies, eigenvectors = analytical_solution()
    
    plt.figure(figsize=(15, 12))
    mode_names = ["First", "Second", "Third"]
    
    for mode_index in range(3):
        t, positions = simulate_motion_euler(mode_index)
        
        plt.subplot(3, 1, mode_index+1)
        for mass_index in range(3):
            plt.plot(t, positions[:, mass_index], label=f'Mass {mass_index+1}')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement')
        plt.title(f"{mode_names[mode_index]} Normal Mode (ω = {frequencies[mode_index]:.4f} rad/s)")
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('trajectories.png')

def animate_normal_mode(mode_index):
    t, positions = simulate_motion_euler(mode_index, duration=10, dt=0.05)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    
    # Set axis labels
    ax.set_xlabel('Position')
    ax.set_ylabel('Displacement')
    
    # Add a second y-axis on the right for time
    ax2 = ax.twinx()
    ax2.set_ylabel('Time (s)')
    ax2.set_ylim(0, 10)  # Set to match duration
    
    wall_left = -0.5
    wall_right = 4.5
    
    left_wall = plt.Rectangle((wall_left-0.1, -1), 0.1, 2, color='gray')
    right_wall = plt.Rectangle((wall_right, -1), 0.1, 2, color='gray')
    ax.add_patch(left_wall)
    ax.add_patch(right_wall)
    
    block_width = 0.5
    block_height = 0.5
    blocks = []
    for i in range(3):
        block = plt.Rectangle((i+1-block_width/2, -block_height/2), block_width, block_height, 
                            color='blue', alpha=0.7)
        ax.add_patch(block)
        blocks.append(block)
    
    spring_lines = []
    line1, = ax.plot([], [], 'k-', lw=1.5)
    line2, = ax.plot([], [], 'k-', lw=1.5)
    line3, = ax.plot([], [], 'k-', lw=1.5)
    line4, = ax.plot([], [], 'k-', lw=1.5)
    spring_lines = [line1, line2, line3, line4]
    
    # Create time text with better positioning and formatting
    time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, 
                        bbox=dict(facecolor='white', alpha=0.7))
    
    # Add displacement markers
    displacement_labels = []
    for i in range(3):
        label = ax.text(0, 0, '', ha='center', va='bottom', color='blue')
        displacement_labels.append(label)
    
    frequencies, eigenvectors = analytical_solution()
    
    def init():
        for line in spring_lines:
            line.set_data([], [])
        time_text.set_text('')
        for label in displacement_labels:
            label.set_text('')
        return spring_lines + blocks + [time_text] + displacement_labels
    
    def animate(i):
        x_pos = np.array([1, 2, 3]) + positions[i]
        
        for j, block in enumerate(blocks):
            block.set_xy((x_pos[j]-block_width/2, -block_height/2))
            
            # Update displacement label positions
            displacement_labels[j].set_position((x_pos[j], block_height/2))
            displacement_labels[j].set_text(f"{positions[i, j]:.2f}")
        
        line1.set_data([wall_left, x_pos[0]], [0, 0])
        line2.set_data([x_pos[0], x_pos[1]], [0, 0])
        line3.set_data([x_pos[1], x_pos[2]], [0, 0])
        line4.set_data([x_pos[2], wall_right], [0, 0])
        
        time_text.set_text(f'Time: {t[i]:.2f} s')
        # Update time on the right y-axis
        ax2.set_ylim(0, 10)
        ax2.set_yticks([0, t[i], 10])
        ax2.set_yticklabels(['0', f'{t[i]:.2f}', '10'])
        
        return spring_lines + blocks + [time_text] + displacement_labels
    
    anim = FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=50, blit=False)
    
    plt.title(f"Normal Mode {mode_index+1} (ω = {frequencies[mode_index]:.4f} rad/s)")
    
    anim.save(f'normal_mode_{mode_index+1}.gif', writer='pillow', fps=20)
    
    plt.close()
    
frequencies, eigenvectors = analytical_solution()
print("Analytical solution:")
print(f"Frequencies (rad/s): {frequencies}")
print("\nEigenvectors (normal modes):")
for i in range(3):
    print(f"Mode {i+1}: {eigenvectors[:, i]}")

plot_normal_modes(frequencies, eigenvectors)

plot_trajectories()

for i in range(3):
    animate_normal_mode(i)

def euler_method_full_system(duration=10, dt=0.01):
    t = np.arange(0, duration, dt)
    
    state = np.zeros((len(t), 6))
    
    state[0, 0] = 1.0  # x1 = 1
    
    K = np.array([
        [2*k, -k, 0],
        [-k, 2*k, -k],
        [0, -k, 2*k]
    ])
    
    for i in range(1, len(t)):
        x = state[i-1, 0:3]
        v = state[i-1, 3:6]
        
        a = -np.dot(K, x) / m
        
        new_v = v + a * dt
        
        new_x = x + v * dt
        
        state[i, 0:3] = new_x
        state[i, 3:6] = new_v
    
    return t, state

t_full, state_full = euler_method_full_system()

plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(t_full, state_full[:, i], label=f'Mass {i+1}')
plt.xlabel('Time (s)')
plt.ylabel('Displacement')
plt.title('Full System Simulation (Initial condition: First mass displaced)')
plt.legend()
plt.grid(True)
plt.savefig('full_system.png')