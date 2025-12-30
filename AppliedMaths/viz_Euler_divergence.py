from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter

# Pendulum parameters
g = 9.81  # gravitational acceleration (m/s^2)
L = 1.0   # length of pendulum (m)

# Initial conditions: start horizontally
theta_0 = np.pi / 2  # 90 degrees
omega_0 = 0.0        # initially at rest

# Time parameters
h = 0.01  # time step (s)
T_approx = 2 * np.pi * np.sqrt(L / g) * 1.2  # Approximate period (with factor for large amplitude)
t_max = 5* T_approx  # Simulate one period
t_vals = np.arange(0, t_max, h)

# Euler-Cromer method
theta_vals = [theta_0]
omega_vals = [omega_0]

for i in range(len(t_vals) - 1):
    omega_new = omega_vals[-1] - h * (g / L) * np.sin(theta_vals[-1])
    theta_new = theta_vals[-1] + h * omega_vals[-1]  # original Euler method
    
    omega_vals.append(omega_new)
    theta_vals.append(theta_new)

# Create animation with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=150)

def animate(frame):
    ax1.clear()
    ax2.clear()
    
    # Left plot: Pendulum visualization in xy coordinates
    theta_curr = theta_vals[frame]
    x = L * np.sin(theta_curr)
    y = -L * np.cos(theta_curr)
    
    # Draw pendulum
    ax1.plot([0, x], [0, y], 'k-', lw=2)  # Rod
    ax1.plot(0, 0, 'ko', markersize=8)    # Pivot point
    ax1.plot(x, y, 'ro', markersize=15)   # Bob
    
    # Reference circle
    circle_theta = np.linspace(0, 2*np.pi, 100)
    circle_x = L * np.sin(circle_theta)
    circle_y = -L * np.cos(circle_theta)
    ax1.plot(circle_x, circle_y, 'b--', lw=0.5, alpha=0.3)
    
    ax1.set_xlim(-1.5*L, 1.5*L)
    ax1.set_ylim(-1.5*L, 0.5*L)
    ax1.set_aspect('equal')
    ax1.set_xlabel('$x$ (m)')
    ax1.set_ylabel('$y$ (m)')
    ax1.set_title(f'Pendulum Motion')
    ax1.grid(True, alpha=0.3)
    
    # Info box for pendulum
    info_text = (
        f"$t = {t_vals[frame]:.2f}$ s\n"
        f"$\\theta = {theta_curr*180/np.pi:.1f}^\\circ$\n"
        f"$\\omega = {omega_vals[frame]:.2f}$ rad/s"
    )
    ax1.text(0.02, 0.98, info_text,
             transform=ax1.transAxes,
             fontsize=9,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Right plot: Angle vs time
    ax2.plot(t_vals[:frame+1], np.array(theta_vals[:frame+1]) * 180/np.pi, 
             'b-', lw=2)
    ax2.plot(t_vals[frame], theta_vals[frame] * 180/np.pi, 
             'ro', markersize=6)
    
    ax2.set_xlim(0, t_max)
    ax2.set_ylim(-100, 100)
    ax2.set_xlabel('Time $t$ (s)')
    ax2.set_ylabel(r'Angle $\theta$ (degrees)')
    ax2.set_title(r'$\theta$ vs $t$')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='--', lw=0.5, alpha=0.5)
    
    # IVP info box at top
    ivp_text = (
        r"$\ddot{\theta}(t) + \frac{g}{L}\sin\theta(t) = 0, \quad \theta(0) = 90^\circ, \quad \dot{\theta}(0) = 0$"
    )
    fig.text(0.5, 0.96, ivp_text,
             fontsize=11,
             ha='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Create animation with appropriate number of frames (sample every 5th frame for speed)
frame_skip = 5
frames = range(0, len(t_vals), frame_skip)

anim = FuncAnimation(fig, animate, frames=frames, interval=50, repeat=True)
plt.close()

# Progress callback for video rendering
print(f"Rendering animation ({len(frames)} frames)...")
def progress_callback(current_frame, total_frames):
    progress = current_frame / total_frames
    bar_length = 40
    filled = int(bar_length * progress)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f'\r  [{bar}] {current_frame}/{total_frames} ({progress*100:.1f}%)', end='', flush=True)

writer = FFMpegWriter(fps=30)

anim.save('Euler_divengence.mp4', dpi=150, writer=writer, progress_callback=progress_callback)
print("\n✓ Animation rendering complete!")

# video_html = anim.to_html5_video()
# video_html = video_html.replace('controls', 'controls autoplay loop muted')
# video_html = video_html.replace(
#     '<video ', 
#     '<video style="width: 100%; height: auto;" '
# )
# HTML(video_html)