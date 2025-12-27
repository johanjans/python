import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import sympy as sp
    import numpy as np
    import scipy as sc
    import matplotlib.pyplot as plt
    from scipy.optimize import fsolve
    return fsolve, mo, np, plt


@app.cell
def _():
    # Input data

    # Coordinates of C
    C_x = 250
    C_y = 50

    # Lengths of the three rods
    l_1 = 100
    l_3 = 100
    l_2 = 210

    return C_x, C_y, l_1, l_2, l_3


@app.cell
def _(C_x, C_y, l_1, l_2, l_3, np):
    # Define the system of equations with parameters
    def constraint_equations(q, param_phi):

        # q is the generalized coordinates for the three rods where x and y are the coordinates for the center of mass for each rod.
        # q = [x1, y1, theta1, x2, y2, theta2, x3, y3, theta3]
    
        C = [
            q[2] - param_phi, # OA is controled by the angle phi
            q[0] - l_1/2 * np.cos(q[2]), # the first rod is pinned to the origin
            q[1] - l_1/2 * np.sin(q[2]), # the first rod is pinned to the origin
            q[0] + l_1/2 * np.cos(q[2]) - (q[3] - l_2/2 * np.cos(q[5])), # the first and second rod have a pin joint
            q[1] + l_1/2 * np.sin(q[2]) - (q[4] - l_2/2 * np.sin(q[5])), # the first and second rod have a pin joint
            q[3] + l_2/2 * np.cos(q[5]) - (q[6] - l_3/2 * np.cos(q[8])), # the second and third rod have a pin joint
            q[4] + l_2/2 * np.sin(q[5]) - (q[7] - l_3/2 * np.sin(q[8])), # the second and third rod have a pin joint
            q[6] + l_3/2 * np.cos(q[8]) - C_x, # the third rod is pinned to C
            q[7] + l_3/2 * np.sin(q[8]) - C_y # the third rod is pinned to C
        ]
        return C
    return (constraint_equations,)


@app.cell
def _(constraint_equations, fsolve, l_1, l_2, np):
    # Solve the system
    n = 100
    phi_n = np.linspace(np.pi/2,-np.pi/2,n)
    state = [0, l_1/2, phi_n[0], l_2/2, l_1, 0, 200, 50, 0.1] # guess of the initial state for q
    q_n = []

    for i, phi in enumerate(phi_n):
        q = fsolve(constraint_equations, state, args=(phi))
        q_n.append(q)

        state = q
    return n, q_n


@app.cell(hide_code=True)
def _(mo, n, np):
    slider = mo.ui.slider(steps=np.linspace(0,n-1,n), label="Step:")
    return (slider,)


@app.cell(hide_code=True)
def _(slider):
    slider
    return


@app.cell(hide_code=True)
def _(C_x, C_y, l_1, l_2, mo, np, plt, q_n, slider):
    # --- Create the Plot ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots()

    j = int(slider.value)
    rr_OA = l_1 * np.array([np.cos(q_n[j][2]), np.sin(q_n[j][2])])
    rr_OB = rr_OA + l_2 * np.array([np.cos(q_n[j][5]), np.sin(q_n[j][5])])
    rr_OC = np.array([C_x, C_y])

    # Plot the links of the mechanism
    ax.plot(*zip([0,0], rr_OA), '-ko',lw=2)
    ax.plot(*zip(rr_OC, rr_OB), '-ko',lw=2)
    ax.plot(*zip(rr_OA, rr_OB), '-ko',lw=2)

    ax.text(rr_OA[0] + 5, rr_OA[1], 'A', fontsize=12)
    ax.text(rr_OB[0] + 5, rr_OB[1], 'B', fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Three-Bar Linkage')
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box') # Ensures correct proportions
    ax.set_xlim(-50, 350)
    ax.set_ylim(-150, 150)


    mo.as_html(fig).center()
    return


if __name__ == "__main__":
    app.run()
