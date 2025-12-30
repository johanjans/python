"""
Visualization of Heun's Method (Improved Euler Method)

This script creates an animation showing how Heun's method works step-by-step.
Heun's method is a second-order Runge-Kutta method that:
1. Makes a predictor step using Euler's method
2. Evaluates the slope at the predicted point
3. Takes the average of the initial and predicted slopes

The animation shows these steps with arrows for a visual understanding.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mechanicskit as mk

# ODE: y' = y, y(0) = 1
# Exact solution: y(x) = e^x
def f(x, y):
    """Right-hand side of ODE: y' = f(x,y) = y"""
    return y

def exact_solution(x):
    """Exact solution: y = e^x"""
    return np.exp(x)

# Simulation parameters
x0 = 0.0
y0 = 1.0
h = 1  # Step size
n_steps = 4  # Number of steps to take
x_end = x0 + n_steps * h

# Compute Heun's method steps
x_heun = [x0]
y_heun = [y0]

for i in range(n_steps):
    x_curr = x_heun[-1]
    y_curr = y_heun[-1]

    # Heun's method:
    # 1. Predictor (Euler step)
    k1 = f(x_curr, y_curr)
    y_pred = y_curr + h * k1

    # 2. Evaluate slope at predicted point
    k2 = f(x_curr + h, y_pred)

    # 3. Corrector (average of slopes)
    y_new = y_curr + h * (k1 + k2) / 2

    x_heun.append(x_curr + h)
    y_heun.append(y_new)

# Exact solution for comparison
x_exact = np.linspace(x0, x_end, 100)
y_exact = exact_solution(x_exact)

# Create animation
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

def animate(frame):
    ax.clear()

    # Plot exact solution
    ax.plot(x_exact, y_exact, 'r-', lw=2, label='Exact Solution', zorder=1)

    # Determine which step we're visualizing
    step = frame // 4  # 4 substeps per step
    substep = frame % 4

    # Plot Heun trajectory up to current step
    if step > 0:
        ax.plot(x_heun[:step+1], y_heun[:step+1], 'o-b',
                lw=2, markersize=6, label='Heun Method', zorder=2)
    else:
        ax.plot(x_heun[0], y_heun[0], 'ob', markersize=6, label='Heun Method', zorder=2)

    # Show current step construction
    if step < n_steps:
        x_curr = x_heun[step]
        y_curr = y_heun[step]

        # Compute predictor and corrector for this step
        k1 = f(x_curr, y_curr)
        y_pred = y_curr + h * k1
        k2 = f(x_curr + h, y_pred)
        y_new = y_curr + h * (k1 + k2) / 2

        # Current point
        ax.plot(x_curr, y_curr, 'go', markersize=10, zorder=5)

        if substep >= 1:
            # Substep 1: Show Euler predictor step with tangent line
            # Draw tangent line at current point
            tangent_x = np.array([x_curr, x_curr + h])
            tangent_y = y_curr + k1 * (tangent_x - x_curr)
            ax.plot(tangent_x, tangent_y, '--', color='orange', lw=3, alpha=0.8,
                   label='Euler tangent', zorder=3)

            # Arrow for predictor
            ax.annotate('', xy=(x_curr + h, y_pred), xytext=(x_curr, y_curr),
                       arrowprops=dict(arrowstyle='->', lw=3, color='orange', alpha=0.8),
                       zorder=4)
            ax.plot(x_curr + h, y_pred, 's', color='orange', markersize=10,
                   label='Euler Predictor', zorder=5)

        if substep >= 2:
            # Substep 2: Show slope at predicted point
            slope_len = h * 0.4
            slope_x = np.array([x_curr + h - slope_len, x_curr + h + slope_len])
            slope_y = y_pred + k2 * (slope_x - (x_curr + h))
            ax.plot(slope_x, slope_y, color='purple', lw=3, alpha=0.8,
                   label='Slope at predictor', zorder=3)

        if substep >= 3:
            # Substep 3: Show final Heun step (average slope)
            # Draw the averaged tangent
            avg_slope = (k1 + k2) / 2
            avg_tangent_x = np.array([x_curr, x_curr + h])
            avg_tangent_y = y_curr + avg_slope * (avg_tangent_x - x_curr)
            ax.plot(avg_tangent_x, avg_tangent_y, '-', color='cyan', lw=3, alpha=0.6,
                   label='Averaged slope', zorder=3)

            # Arrow for corrector
            ax.annotate('', xy=(x_curr + h, y_new), xytext=(x_curr, y_curr),
                       arrowprops=dict(arrowstyle='->', lw=4, color='blue', alpha=0.9),
                       zorder=6)
            ax.plot(x_curr + h, y_new, 'bs', markersize=10,
                   label='Heun Corrector', zorder=7)

    # Labels and formatting
    ax.set_xlabel('$x$', fontsize=13)
    ax.set_ylabel('$y$', fontsize=13)
    ax.set_title(f"Heun's Method: Step {step+1}/{n_steps}", fontsize=15, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.15, x_end + 0.15)
    ax.set_ylim(0.5, exact_solution(x_end) + 1.0)

    # Info box
    if step < n_steps:
        substep_names = [
            "Initial point",
            "1. Euler predictor step",
            "2. Evaluate slope at predictor",
            "3. Heun corrector (average slope)"
        ]
        info_text = (
            r"ODE: $y' = y, \quad y(0) = 1$" + "\n"
            f"Step size: $h = {h}$\n"
            f"{substep_names[substep]}"
        )
    else:
        info_text = r"ODE: $y' = y, \quad y(0) = 1$" + f"\nStep size: $h = {h}$\nCompleted!"

    ax.text(0.98, 0.02, info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Total frames: 4 substeps per step + 1 final frame showing complete result
n_frames = n_steps * 4 + 1
anim = FuncAnimation(fig, animate, frames=n_frames, interval=800, repeat=True)
plt.close()

# Generate responsive HTML using mechanicskit
html_obj = mk.to_responsive_html(anim, container_id='heun_method_visualization')

# Extract HTML string from IPython.display.HTML object
html_output = html_obj.data

# Save to file
with open('heun_method_visualization.html', 'w') as f:
    f.write(html_output)

print("Animation saved to 'heun_method_visualization.html'")
print("Open this file in a web browser to view the animation.")
