"""
Interactive sine curve with slider control.

This example demonstrates how to create an interactive plot where a slider
controls the position of a point along a sine curve. The matplotlib.widgets
module provides the Slider widget for user interaction.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Create the sine curve data
x = np.linspace(0, 2*np.pi, 200)
y = np.sin(x)

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # Make room for slider

# Plot the sine curve
line, = ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
ax.set_xlabel('x [rad]')
ax.set_ylabel('y')
ax.set_title('Interactive Sine Curve with Slider')
ax.grid(True, alpha=0.3)
ax.legend()

# Create the initial dot at x = 0
x_initial = 0
y_initial = np.sin(x_initial)
dot, = ax.plot(x_initial, y_initial, 'ro', markersize=12, label='Current point')

# Add text to display coordinates
coord_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                     fontsize=10, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Create slider axis (position: [left, bottom, width, height])
slider_ax = plt.axes([0.15, 0.1, 0.7, 0.03])

# Create slider widget
slider = Slider(
    ax=slider_ax,
    label='x position',
    valmin=0,
    valmax=2*np.pi,
    valinit=x_initial,
    color='lightblue'
)

# Define update function called when slider value changes
def update(val):
    """Update dot position when slider moves."""
    x_pos = slider.val
    y_pos = np.sin(x_pos)

    # Update dot position
    dot.set_data([x_pos], [y_pos])

    # Update text with current coordinates
    coord_text.set_text(f'x = {x_pos:.3f} rad\ny = sin(x) = {y_pos:.3f}')

    # Redraw the figure (works with all backends)
    fig.canvas.draw()

# Register the update function with the slider
slider.on_changed(update)

# Initialize the coordinate text
update(x_initial)

plt.show()
