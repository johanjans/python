"""
Comparison of Euler and Midpoint Methods

Compares the accuracy of Euler's method vs the Midpoint method for:
ODE: y' = 1.2*x*y
Initial condition: y(0) = 1
Domain: x in [0, 2]
Step size: h = 0.2

Generates a static comparison plot.
"""

import numpy as np
import matplotlib.pyplot as plt

# ODE: y' = 1.2*x*y
def f(x, y):
    """Right-hand side: y' = 1.2*x*y"""
    return 1.2 * x * y

# Exact solution: y = exp(0.6*x^2)
def exact_solution(x):
    """Exact solution for y' = 1.2*x*y with y(0) = 1"""
    return np.exp(0.6 * x**2)

# Parameters
x0 = 0.0
y0 = 1.0
h = 0.2
x_end = 2.0
n_steps = int((x_end - x0) / h)

# Euler's method
x_euler = [x0]
y_euler = [y0]

for i in range(n_steps):
    x_curr = x_euler[-1]
    y_curr = y_euler[-1]

    y_new = y_curr + h * f(x_curr, y_curr)

    x_euler.append(x_curr + h)
    y_euler.append(y_new)

# Midpoint method
x_midpoint = [x0]
y_midpoint = [y0]

for i in range(n_steps):
    x_curr = x_midpoint[-1]
    y_curr = y_midpoint[-1]

    # Midpoint method
    k1 = f(x_curr, y_curr)
    x_mid = x_curr + h/2
    y_mid = y_curr + (h/2) * k1
    k2 = f(x_mid, y_mid)
    y_new = y_curr + h * k2

    x_midpoint.append(x_curr + h)
    y_midpoint.append(y_new)

# Exact solution
x_exact = np.linspace(x0, x_end, 200)
y_exact = exact_solution(x_exact)

# Calculate errors at endpoint
euler_error = abs(y_euler[-1] - exact_solution(x_end))
midpoint_error = abs(y_midpoint[-1] - exact_solution(x_end))

# Create comparison plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)

# Left plot: Solution comparison
ax1.plot(x_exact, y_exact, 'r-', lw=3, label='Exact Solution', zorder=1)
ax1.plot(x_euler, y_euler, 'o--', color='orange', lw=2, markersize=6,
         label='Euler Method', zorder=2)
ax1.plot(x_midpoint, y_midpoint, 's-', color='blue', lw=2, markersize=6,
         label='Midpoint Method', zorder=3)

ax1.set_xlabel('$x$', fontsize=14)
ax1.set_ylabel('$y$', fontsize=14)
ax1.set_title('Method Comparison', fontsize=16, fontweight='bold')
ax1.legend(fontsize=12, loc='upper left')
ax1.grid(True, alpha=0.3)

# Add info box
info_text = (
    r"ODE: $y' = 1.2xy$" + "\n"
    r"IC: $y(0) = 1$" + "\n"
    f"Step size: $h = {h}$\n"
    f"Exact: $y(2) = {exact_solution(x_end):.4f}$\n"
    f"Euler: $y(2) \\approx {y_euler[-1]:.4f}$\n"
    f"Midpoint: $y(2) \\approx {y_midpoint[-1]:.4f}$"
)
ax1.text(0.98, 0.02, info_text,
         transform=ax1.transAxes,
         fontsize=11,
         verticalalignment='bottom',
         horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

# Right plot: Error comparison
x_eval = np.array(x_euler)
euler_errors = np.abs(np.array(y_euler) - exact_solution(x_eval))
midpoint_errors = np.abs(np.array(y_midpoint) - exact_solution(x_eval))

ax2.semilogy(x_eval, euler_errors, 'o--', color='orange', lw=2,
            markersize=6, label='Euler Error')
ax2.semilogy(x_eval, midpoint_errors, 's-', color='blue', lw=2,
            markersize=6, label='Midpoint Error')

ax2.set_xlabel('$x$', fontsize=14)
ax2.set_ylabel('Absolute Error (log scale)', fontsize=14)
ax2.set_title('Error Comparison', fontsize=16, fontweight='bold')
ax2.legend(fontsize=12)
ax2.grid(True, alpha=0.3, which='both')

# Add error summary
error_text = (
    f"Final errors at $x=2$:\n"
    f"Euler: ${euler_error:.2e}$\n"
    f"Midpoint: ${midpoint_error:.2e}$\n"
    f"Improvement: ${euler_error/midpoint_error:.1f}\\times$"
)
ax2.text(0.98, 0.98, error_text,
         transform=ax2.transAxes,
         fontsize=11,
         verticalalignment='top',
         horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

plt.tight_layout()
plt.savefig('euler_vs_midpoint_comparison.png', dpi=150, bbox_inches='tight')
plt.savefig('euler_vs_midpoint_comparison.svg', bbox_inches='tight')
print("Comparison plot saved:")
print("  - euler_vs_midpoint_comparison.png")
print("  - euler_vs_midpoint_comparison.svg")
print(f"\nResults at x = {x_end}:")
print(f"  Exact solution:    y({x_end}) = {exact_solution(x_end):.6f}")
print(f"  Euler method:      y({x_end}) = {y_euler[-1]:.6f}  (error: {euler_error:.2e})")
print(f"  Midpoint method:   y({x_end}) = {y_midpoint[-1]:.6f}  (error: {midpoint_error:.2e})")
print(f"  Improvement factor: {euler_error/midpoint_error:.1f}x")
