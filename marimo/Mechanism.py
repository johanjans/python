import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rigid body mechanisms with relative motion analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(
        src="https://python.ju.se/Applications/graphics/ThreeBars.png"
    ).center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We want to compute the positions of the links as well as the velocities and accelerations of the points $A$ and $B$ and also the angular velocties $\omega_{O A}, \omega_{A B}$ and accelerations, $\alpha_{O A}, \alpha_{A B}$ of the links
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The kinematic analysis is easy enough for a textbook example where the mechanism is set up such that the positions are trivial. In general, a mechanism is coupled and one needs to involve unknown variables and solve a system of equations, one for every body to determine the kinematics. There is no guarantee that the solution is unique in general so conditions need to be applied on these variables, i.e., they need to be defined such that a certain kinematic solution is aquired.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kinematic analysis
    """)
    return


@app.cell
def _(mo):
    mo.image(
        src="https://python.ju.se/Applications/graphics/Three_bar_sketch.png"
    ).center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the unknown position can be solved for by defining the point $B$ from both the point $O$ and well as from the point $C$ using vector addition, we "walk" from $O$ to $B$ via $A$.

    The direction towards $A$ is given by defining $r_{O A}$ using a direction given by an angle $\varphi$ defined as the angle between the $y$-axis and the line $O A$.

    We get the $r_{A B}$ direction, similarly, by defining the angle, $\gamma$ between the $y$-axis and the line $A B O B$.
    Additionally we can "walk" to the point $B$ from $C$. This way we have two ways of getting to OB , thus a system of equations is established from which we can solve for the two unknowns, $\varphi$ and $\gamma$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Equations of constraint
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We have the following kinematics

    $$
    \boldsymbol{r}_B=\boldsymbol{r}_{O B}=\boldsymbol{r}_C+\boldsymbol{r}_{C B}=\boldsymbol{r}_{O A}+\boldsymbol{r}_{A B}
    $$

    or

    $$
    \boxed{\boldsymbol{r}_C+\boldsymbol{r}_{C B}(\theta)=\boldsymbol{r}_{O A}(\varphi)+\boldsymbol{r}_{A B}(\varphi, \gamma)}
    $$


    For a valid $\theta$ we get two equations, where we can solve for the two unknown variables $\varphi(\theta)$ and $\gamma(\theta)$.

    $$
    r_{O A}(\varphi)=r_{O A}\left[\begin{array}{l}
    \sin \varphi \\
    \cos \varphi
    \end{array}\right], r_{A B}(\gamma)=r_{A B}\left[\begin{array}{l}
    \sin \gamma \\
    \cos \gamma
    \end{array}\right], r_{C B}(\theta)=r_{C B}\left[\begin{array}{c}
    -\sin \varphi \\
    \cos \varphi
    \end{array}\right]
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Numerical solution
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy
    return np, plt, scipy


@app.cell
def _(mo):
    theta_slider = mo.ui.slider(
        start=-2, stop=204, step=1, value=30, label="Angle θ:"
    )
    return (theta_slider,)


@app.cell(hide_code=True)
def _(mo, theta_slider):
    mo.md(
        f"""
    Adjust the angle **θ** to see the linkage move.

    {theta_slider} {theta_slider.value}$^\\circ$
    """
    ).center()
    return


@app.cell(hide_code=True)
def _(np, r_AB, r_CB, r_OA, rr_OC, theta_rad):
    def equations(vars):
        """
        Args:
            vars: A list or tuple [phi, gamma] containing the angles
                  of links OA and AB in radians.
        Returns:
            The distance between points B from A and B from C, this distance is zero for the correct set of phi and gamma.
        """
        phi, gamma = vars

        # Position of B calculated from chain O->A->B
        rr_OAB = r_OA * np.array([np.sin(phi), np.cos(phi)]) + r_AB * np.array(
            [np.sin(gamma), np.cos(gamma)]
        )

        # Position of B calculated from chain C->B
        # [-sind(θ), cosd(θ)] which corresponds to an angle measured from the +y axis
        rr_CB = r_CB * np.array([-np.sin(theta_rad), np.cos(theta_rad)])
        rr_OCB = rr_OC + rr_CB

        return rr_OAB - rr_OCB
    return (equations,)


@app.cell(hide_code=True)
def _(np, theta_slider):
    r_OA = 100.0  # Length of link OA
    r_CB = 75.0  # Length of link CB

    r_AB = np.sqrt((250 - 75) ** 2 + (100 - 50) ** 2)

    rr_OC = np.array([250, 50])

    theta_deg = theta_slider.value
    theta_rad = np.deg2rad(theta_deg)
    return r_AB, r_CB, r_OA, rr_OC, theta_rad


@app.cell(hide_code=True)
def _(equations, np, scipy):
    # Provide an initial guess for the angles [phi, gamma] in radians
    initial_guess = np.deg2rad([50, 70])
    solution_rad = scipy.optimize.fsolve(equations, initial_guess)
    phi_sol, gamma_sol = solution_rad
    # np.rad2deg(solution_rad)
    return gamma_sol, phi_sol


@app.cell(hide_code=True)
def _(gamma_sol, np, phi_sol, r_AB, r_OA):
    rr_OA = r_OA * np.array([np.sin(phi_sol), np.cos(phi_sol)])

    rr_OB = rr_OA + r_AB * np.array([np.sin(gamma_sol), np.cos(gamma_sol)])
    return rr_OA, rr_OB


@app.cell(hide_code=True)
def _(mo, plt, rr_OA, rr_OB, rr_OC):
    # --- Create the Plot ---
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots()


    # Plot the links of the mechanism
    ax.plot(*zip([0, 0], rr_OA), "-ko", lw=2)
    ax.plot(*zip(rr_OC, rr_OB), "-ko", lw=2)
    ax.plot(*zip(rr_OA, rr_OB), "-ko", lw=2)

    ax.text(rr_OA[0] + 5, rr_OA[1], "A", fontsize=12)
    ax.text(rr_OB[0] + 5, rr_OB[1], "B", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Three-Bar Linkage")
    ax.grid(True)
    ax.set_aspect("equal", adjustable="box")  # Ensures correct proportions
    ax.set_xlim(-50, 300)
    ax.set_ylim(-50, 150)


    mo.as_html(fig).center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analytical kinematics - Creating velocity and acceleration plots
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will do the above for many values of $\theta$. The natural way is in a loop, storing the results in a list for later visualisation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    run_btn1 = mo.ui.run_button(label="Click to compute and visualize")
    run_btn1
    return (run_btn1,)


@app.cell(hide_code=True)
def _(mo, rr_OC, run_btn1):
    def _():
        import marimo as mo
        import numpy as np
        import sympy as sp
        import matplotlib.pyplot as plt
        import scipy

        # --- 1. Constants and Setup ---
        r_OA = 100.0
        r_CB = 75.0
        r_AB = np.sqrt((250 - 75)**2 + (100 - 50)**2)
        O = np.array([0, 0])
        C = np.array([250, 50])
        omega_CB = 5.0  # Input angular velocity in rad/s

        # Define the range of input angles in degrees
        # We got this from playing around in CAD
        thetas_deg = np.arange(-1, 204, 0.1)

        # Initialize lists to store results
        phis, gammas = [], []

        for theta_deg in mo.status.progress_bar(thetas_deg):
            theta_rad = np.deg2rad(theta_deg)

            # --- Position Analysis (Nonlinear Solve) ---
            def position_equations(vars):
                phi, gamma = vars

                # Position of B calculated from chain O->A->B
                rr_OAB = r_OA * np.array([np.sin(phi), np.cos(phi)]) + \
                         r_AB * np.array([np.sin(gamma), np.cos(gamma)])

                # Position of B calculated from chain C->B
                # [-sind(θ), cosd(θ)] which corresponds to an angle measured from the +y axis
                rr_CB = r_CB * np.array([-np.sin(theta_rad), np.cos(theta_rad)])
                rr_OCB = rr_OC + rr_CB

                return rr_OAB - rr_OCB

            # Use the last solution as the initial guess for the next step
            initial_guess = [np.deg2rad(50), np.deg2rad(70)]
            if phis:
                initial_guess = [phis[-1], gammas[-1]]

            phi_sol, gamma_sol = scipy.optimize.fsolve(position_equations, initial_guess)
            phis.append(phi_sol)
            gammas.append(gamma_sol)


            # Define 3D position vectors directly from the numerical position solution
            R_A = r_OA * sp.Matrix([sp.sin(phi_sol), sp.cos(phi_sol), 0])
            R_AB = r_AB * sp.Matrix([sp.sin(gamma_sol), sp.cos(gamma_sol), 0])
            R_CB = r_CB * sp.Matrix([-sp.sin(theta_rad), sp.cos(theta_rad), 0])



        # --- Plotting ---
        # Convert angles back to degrees for plotting
        gammas_deg = np.rad2deg(gammas)
        phis_deg = np.rad2deg(phis)

        # Plot 1: Angles
        fig1, ax1 = plt.subplots()
        ax1.plot(thetas_deg, gammas_deg, 'b', linewidth=2, label=r'$\gamma(\theta)$')
        ax1.plot(thetas_deg, phis_deg, 'r', linewidth=2, label=r'$\varphi(\theta)$')
        ax1.set_xlabel(r'Input Angle $\theta$ (degrees)')
        ax1.set_ylabel(r'Output Angles (degrees)')
        ax1.set_title('Link Angles vs. Input Angle')
        ax1.grid(True)
        ax1.legend()
        plt.close(fig1)

        return fig1
    mo.stop(not run_btn1.value)
    fig1 = _()
    mo.as_html(fig1).center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Animation - Render GIF
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    gif_btn = mo.ui.run_button(label="Click to render GIF")
    gif_btn
    return (gif_btn,)


@app.cell(hide_code=True)
def _(gif_btn, mo, np, plt, r_AB, r_CB, r_OA, rr_OC, scipy):
    mo.stop(not gif_btn.value)
    def _():
        import matplotlib.animation as animation

    

        # --- Compute all positions for the animation ---
        thetas_deg_anim = np.arange(-1, 204, 1)
        positions = []

        initial_guess = [np.deg2rad(50), np.deg2rad(70)]
        for theta_deg in thetas_deg_anim:
            theta_rad = np.deg2rad(theta_deg)

            def position_equations(vars):
                phi, gamma = vars
                rr_OAB = r_OA * np.array([np.sin(phi), np.cos(phi)]) + \
                         r_AB * np.array([np.sin(gamma), np.cos(gamma)])
                rr_CB_vec = r_CB * np.array([-np.sin(theta_rad), np.cos(theta_rad)])
                rr_OCB = rr_OC + rr_CB_vec
                return rr_OAB - rr_OCB

            phi_sol, gamma_sol = scipy.optimize.fsolve(position_equations, initial_guess)
            initial_guess = [phi_sol, gamma_sol]

            # Compute positions
            rr_OA_i = r_OA * np.array([np.sin(phi_sol), np.cos(phi_sol)])
            rr_OB_i = rr_OA_i + r_AB * np.array([np.sin(gamma_sol), np.cos(gamma_sol)])

            positions.append({
                'theta': theta_deg,
                'rr_OA': rr_OA_i,
                'rr_OB': rr_OB_i
            })

        # --- Animation setup ---
        target_FPS = 25
        frame_interval_ms = 1000 / target_FPS

        plt.style.use('default')
        _fig_anim, _ax_anim = plt.subplots(figsize=(8, 6))

        # Initialize plot elements
        line_OA, = _ax_anim.plot([], [], 'o-b', lw=2, label='OA')
        line_AB, = _ax_anim.plot([], [], 'o-r', lw=2, label='AB')
        line_CB, = _ax_anim.plot([], [], 'o-g', lw=2, label='CB')

        _ax_anim.set_aspect('equal', adjustable='box')
        _ax_anim.set_xlim(-50, 300)
        _ax_anim.set_ylim(-50, 150)
        _ax_anim.grid(True)
        _ax_anim.set_xlabel('x')
        _ax_anim.set_ylabel('y')
        _ax_anim.legend()

        def init_anim():
            line_OA.set_data([], [])
            line_AB.set_data([], [])
            line_CB.set_data([], [])
            return line_OA, line_AB, line_CB

        def animate_frame(i):
            pos = positions[i]
            theta_deg_i = pos['theta']
            rr_OA_i = pos['rr_OA']
            rr_OB_i = pos['rr_OB']

            # Link OA: from O(0,0) to A
            line_OA.set_data([0, rr_OA_i[0]], [0, rr_OA_i[1]])

            # Link AB: from A to B
            line_AB.set_data([rr_OA_i[0], rr_OB_i[0]], [rr_OA_i[1], rr_OB_i[1]])

            # Link CB: from C to B
            line_CB.set_data([rr_OC[0], rr_OB_i[0]], [rr_OC[1], rr_OB_i[1]])

            _ax_anim.set_title(f"Three-Bar Linkage  θ = {theta_deg_i:.0f}°")

            return line_OA, line_AB, line_CB

        ani = animation.FuncAnimation(
            _fig_anim, animate_frame, init_func=init_anim,
            frames=len(positions),
            interval=frame_interval_ms,
            blit=False
        )

        filepath = "three_bar_linkage.gif"
        ani.save(filepath, writer='pillow', fps=target_FPS, dpi=100)
        return mo.md(f"GIF saved to **{filepath}**")


    _()
    return


@app.cell
def _(gif_btn, mo):
    mo.stop(not gif_btn.value)
    mo.image(src="three_bar_linkage.gif").center()
    return


if __name__ == "__main__":
    app.run()
