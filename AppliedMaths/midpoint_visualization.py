"""
Visualization of the Midpoint Method (Modified Euler Method)

This script creates an animation showing how the midpoint method works step-by-step.
The midpoint method:
1. Calculates the slope at the current point
2. Uses this slope to estimate the midpoint
3. Evaluates the slope at the midpoint
4. Uses the midpoint slope for the full step

Example: y' = x + y, y(0) = 1, find y(0.4) with h = 0.2
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mechanicskit as mk

# ODE: y' = x + y, y(0) = 1
def f(x, y):
    """Right-hand side of ODE: y' = f(x,y) = x + y"""
    return x + y

# Simulation parameters
x0 = 0.0
y0 = 1.0
h = 0.2  # Step size
n_steps = 2  # Two steps to reach x = 0.4
x_end = x0 + n_steps * h

# Compute midpoint method steps and store data
x_midpoint = [x0]
y_midpoint = [y0]
step_data = []

for i in range(n_steps):
    x_curr = x_midpoint[-1]
    y_curr = y_midpoint[-1]

    # Midpoint method:
    k1 = f(x_curr, y_curr)
    x_mid = x_curr + h/2
    y_mid = y_curr + (h/2) * k1
    k2 = f(x_mid, y_mid)
    y_new = y_curr + h * k2

    x_midpoint.append(x_curr + h)
    y_midpoint.append(y_new)

    step_data.append({
        'x': x_curr, 'y': y_curr, 'k1': k1,
        'x_mid': x_mid, 'y_mid': y_mid, 'k2': k2,
        'y_new': y_new
    })

# Exact solution: y = -x - 1 + 2*e^x
x_exact = np.linspace(x0, x_end, 100)
y_exact = -x_exact - 1 + 2*np.exp(x_exact)

# Create animation
fig, ax = plt.subplots(figsize=(10, 7), dpi=150)

def animate(frame):
    ax.clear()

    # Plot exact solution
    ax.plot(x_exact, y_exact, 'r-', lw=2, label='Exact Solution', zorder=1)

    # Determine substep
    step = frame // 5
    substep = frame % 5

    # Plot midpoint trajectory
    if step > 0:
        ax.plot(x_midpoint[:step+1], y_midpoint[:step+1], 'o-b',
                lw=2, markersize=6, label='Midpoint Method', zorder=2)
    else:
        ax.plot(x_midpoint[0], y_midpoint[0], 'ob', markersize=6,
                label='Midpoint Method', zorder=2)

    # Show current step construction
    if step < n_steps:
        data = step_data[step]
        x_curr, y_curr = data['x'], data['y']
        k1 = data['k1']
        x_mid, y_mid = data['x_mid'], data['y_mid']
        k2 = data['k2']
        y_new = data['y_new']

        # Current point
        ax.plot(x_curr, y_curr, 'go', markersize=12, zorder=5)

        if substep >= 1:
            # Slope at current point
            slope_len = 0.08
            slope_x = np.array([x_curr - slope_len, x_curr + slope_len])
            slope_y = y_curr + k1 * (slope_x - x_curr)
            ax.plot(slope_x, slope_y, 'orange', lw=3, alpha=0.8, zorder=3)

        if substep >= 2:
            # Arrow to midpoint
            ax.annotate('', xy=(x_mid, y_mid), xytext=(x_curr, y_curr),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='orange',
                                     alpha=0.7, linestyle='--'), zorder=3)
            ax.plot(x_mid, y_mid, 's', color='purple', markersize=12, zorder=4)

        if substep >= 3:
            # Slope at midpoint
            slope_x = np.array([x_mid - slope_len, x_mid + slope_len])
            slope_y = y_mid + k2 * (slope_x - x_mid)
            ax.plot(slope_x, slope_y, 'purple', lw=3, alpha=0.8, zorder=3)

        if substep >= 4:
            # Full step with midpoint slope
            tangent_x = np.array([x_curr, x_curr + h])
            tangent_y = y_curr + k2 * (tangent_x - x_curr)
            ax.plot(tangent_x, tangent_y, '-', color='cyan', lw=3, alpha=0.6, zorder=3)

            ax.annotate('', xy=(x_curr + h, y_new), xytext=(x_curr, y_curr),
                       arrowprops=dict(arrowstyle='->', lw=3.5, color='blue',
                                     alpha=0.9), zorder=4)
            ax.plot(x_curr + h, y_new, 'bs', markersize=12, zorder=5)

    # Labels
    ax.set_xlabel('$x$', fontsize=13)
    ax.set_ylabel('$y$', fontsize=13)
    ax.set_title(f"Midpoint Method: Step {step+1}/{n_steps}", fontsize=15, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.05, x_end + 0.05)
    ax.set_ylim(0.8, y_exact[-1] + 0.2)

    # Values textbox (bottom left)
    if step < n_steps:
        data = step_data[step]

        if substep == 0:
            values_text = (
                f"Starting point:\n"
                f"$x_i = {data['x']:.1f}$\n"
                f"$y_i = {data['y']:.4f}$"
            )
        elif substep == 1:
            values_text = (
                f"Current point:\n"
                f"$x_i = {data['x']:.1f}, \\quad y_i = {data['y']:.4f}$\n"
                f"\nSlope at current point:\n"
                f"$k_1 = f(x_i, y_i) = {data['k1']:.4f}$"
            )
        elif substep == 2:
            values_text = (
                f"Midpoint estimate:\n"
                f"$x_{{mid}} = x_i + h/2 = {data['x_mid']:.2f}$\n"
                f"$y_{{mid}} = y_i + (h/2)k_1 = {data['y_mid']:.4f}$\n"
                f"\nwhere $k_1 = {data['k1']:.4f}$"
            )
        elif substep == 3:
            values_text = (
                f"Slope at midpoint:\n"
                f"$k_2 = f(x_{{mid}}, y_{{mid}})$\n"
                f"$k_2 = f({data['x_mid']:.2f}, {data['y_mid']:.4f})$\n"
                f"$k_2 = {data['k2']:.4f}$"
            )
        else:  # substep >= 4
            values_text = (
                f"Final step:\n"
                f"$y_{{i+1}} = y_i + h \\cdot k_2$\n"
                f"$y_{{i+1}} = {data['y']:.4f} + {h:.1f} \\cdot {data['k2']:.4f}$\n"
                f"$y_{{i+1}} = {data['y_new']:.4f}$"
            )

        ax.text(0.02, 0.02, values_text,
                transform=ax.transAxes,
                fontsize=11,
                verticalalignment='bottom',
                horizontalalignment='left',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    else:
        # Final summary
        exact_val = y_exact[-1]
        approx_val = y_midpoint[-1]
        error = abs(exact_val - approx_val)
        values_text = (
            f"Final result at $x = {x_end}$:\n"
            f"Midpoint: $y({x_end}) \\approx {approx_val:.6f}$\n"
            f"Exact: $y({x_end}) = {exact_val:.6f}$\n"
            f"Error: ${error:.2e}$"
        )
        ax.text(0.02, 0.02, values_text,
                transform=ax.transAxes,
                fontsize=11,
                verticalalignment='bottom',
                horizontalalignment='left',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))

    # Info box (top right)
    substep_names = [
        "Initial point",
        "1. Slope at current point",
        "2. Estimate midpoint",
        "3. Slope at midpoint",
        "4. Full step with midpoint slope"
    ]

    if step < n_steps:
        info_text = (
            r"ODE: $y' = x + y, \quad y(0) = 1$" + "\n"
            f"Step size: $h = {h}$\n"
            f"Target: $y({x_end})$\n\n"
            f"{substep_names[substep]}"
        )
    else:
        info_text = (
            r"ODE: $y' = x + y, \quad y(0) = 1$" + "\n"
            f"Step size: $h = {h}$\n"
            "Completed!"
        )

    ax.text(0.98, 0.98, info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

# Total frames: 5 substeps per step + 1 final frame
n_frames = n_steps * 5 + 1
anim = FuncAnimation(fig, animate, frames=n_frames, interval=1000, repeat=True)
plt.close()

# Generate responsive HTML using mechanicskit
html_obj = mk.to_responsive_html(anim, container_id='midpoint_method_visualization')

# Extract HTML string from IPython.display.HTML object
html_output = html_obj.data

# Save to file
with open('midpoint_method_visualization.html', 'w') as f:
    f.write(html_output)

print("Animation saved to 'midpoint_method_visualization.html'")
print("Open this file in a web browser to view the animation.")
