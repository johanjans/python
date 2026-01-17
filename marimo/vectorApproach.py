import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Vector approach
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(src="https://i.imgur.com/kLNnzkK.png", width=400, rounded=True, caption="Moving arm").center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The arm OA can rotate freely around $O$ and is actuated by the string attached in $A$ and around $B$.

    Let $a=400 \mathrm{~mm}, b=80 \mathrm{~mm}$ and the distence from $A$ to $B$ be $r_{O A}=350 \mathrm{~mm}$. Furthermore let the center of gravity (COG) be located at 120 mm from $O$ along the line $O A$.
    - Express the length $L=r_{A B}$ as a function of $\theta$ and find the minimum distance and at which $\theta$ this occurs for $\theta \in\left[0,180^{\circ}\right]$.
    - Find the above distance using an interactive visualisation.
    - How does the minimum vary with $b$ ?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solution
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the right-hand rule we define a coordinate system with $x$ positively defined to the right, $y$ positively defined up and thus $z$ is given positively outward from the screen following the right-hand rule. See the figure below
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Even if the problem is simplified into two dimensions (2D problem or plane problem), we will still use three dimensions in our modeling, to ensure that the cross product (vector product) is properly defined. The vector product is another vector which has the properties of being orthogonal to the input vectors.

    The point $B$ is a fix point, it does not vary with $\theta$, so it is easiest to describe:

    $$
    \boldsymbol r_{O B}=[400,-80,0]^{\top}
    $$

    The center of mass $\boldsymbol r_{O G}$ and $\boldsymbol r_{O A}$ are a little harder to describe, we have the distances $O A=350 \mathrm{~mm}$ and $O G=120 \mathrm{~mm}$, but the vectors need to vary with the angle $\theta$, we start by defining the unit vector

    $$
    e_{O A}=[\sin \theta,-\cos \theta, 0]^{\top}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sanity check: Testing the trogonometric functions as soon as the vector is described is a good idea, just set $\theta$ to some angle for which the outcome is trivial. For $\theta=0$ we expect the arm to point straight down, and we get $\left.e\right|_{\theta=0^{\circ}}=[0,-1,0]^{\top}$, which makes sense. For $\theta=90^{\circ}$ we expect the arm to point straight to the right, and we get $\left.e\right|_{\theta=90^{\circ}}=[1,0,0]^{\top}$, which also makes sense.

    Now we define $\boldsymbol r_{O G}=120 e_{O A}$ and $\boldsymbol r_{O A}=250 e_{O A}$ as well as the vector from $A$ to $B$

    $$
    \boldsymbol r_{AB} = \boldsymbol r_{OB} - \boldsymbol r_{OA}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The length is given by

    $$
    L(\theta)=r_{A B}=|\overrightarrow{A B}|=\sqrt{r_{A B x}^2+r_{A B y}^2}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use the slider below to set $\theta$ to various numeric values and it computes the length and updates the graph. Try it out! This site is responsive!
    """)
    return


@app.cell(hide_code=True)
def _():
    import numpy as np
    def sind(a):
        return np.sin(np.deg2rad(a))
    def cosd(a):
        return np.cos(np.deg2rad(a))
    def norm(a):
        return np.linalg.norm(a)
    return cosd, norm, np, sind


@app.cell
def _():
    r_OA = 350;
    return (r_OA,)


@app.cell(hide_code=True)
def _(mo):
    thetaSlider = mo.ui.slider(0, 90, value=30, step=1, label='$\\theta$:')
    return (thetaSlider,)


@app.cell(hide_code=True)
def _(mo, thetaSlider):
    theta = thetaSlider.value
    mo.md(
        f"""
        Rotational angle {thetaSlider} ${theta}^\\circ$
        """
    )
    return (theta,)


@app.cell(hide_code=True)
def _(cosd, mo, norm, np, r_OA, sind, theta):
    import matplotlib.pyplot as plt
    e_OA = np.array([sind(theta), -cosd(theta)])
    OA = r_OA*e_OA
    OB = np.array([400, -80])
    AB = OB-OA
    L = norm(AB)

    # Initial plot
    plt.style.use('default')
    fig, ax = plt.subplots()
    ax.set_xlim([0,450])
    ax.set_ylim([-400,0])
    ax.set_aspect('equal', 'box')

    hline1, = ax.plot([], [], '-ko',lw=2)
    hline2, = ax.plot([], [], '-ko',lw=1)
    htext1 = ax.text(0, 0, "A")
    htext2 = ax.text(0, 0, "B")

    htext3 = ax.text(0, 0, f"{L:0.2f}", color='blue')

    mo.md(
        f"""

        $\\bm e_{{OA}}(\\theta={theta}^\\circ) = [{sind(theta):0.2f}, {-cosd(theta):0.2f}, {0:0.2f}]^\\mathsf T$

        Thus, the length is $r_{{AB}}(\\theta={theta}^\\circ) \\approx {L:0.2f}$
        """
    )
    return AB, L, OA, OB, ax, fig, hline1, hline2, htext1, htext2, htext3, plt


@app.cell(hide_code=True)
def _(AB, L, OA, OB, ax, fig, hline1, hline2, htext1, htext2, htext3, mo):
    OM = OA + AB/2

    hline1.set_data([0,OA[0]], [0,OA[1]])
    hline2.set_data([OA[0],OB[0]], [OA[1],OB[1]])
    htext1.set_position((OA[0]+10, OA[1]-10))
    htext2.set_position((OB[0]+10, OB[1]-10))
    htext3.set_position((OM[0]+10, OM[1]-10))

    ax.set_title(f"Length: {L:0.2f}mm")

    mo.center(fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Symbolic solution
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    compute_btn = mo.ui.run_button(label="Compute symbolic solution")
    compute_btn
    return (compute_btn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The vector $\overrightarrow{A B}$ is given symbolically as
    """)
    return


@app.cell(hide_code=True)
def _(compute_btn, mo):
    mo.stop(not compute_btn.value)
    import sympy as sp

    theta_s = sp.symbols("theta_s", real=True, positive=True)

    e_OAs = sp.Matrix([sp.sin(theta_s), -sp.cos(theta_s), 0])

    OAs = 350 * e_OAs
    OBs = sp.Matrix([400, -80, 0])
    ABs = OBs - OAs

    mo.md(f"""
        $$
        \\vec{{AB}} = {sp.latex(ABs)}
        $$
    """)
    return ABs, sp, theta_s


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The length is then given by
    """)
    return


@app.cell(hide_code=True)
def _(ABs, mo, sp):
    L_s = ABs.norm()
    mo.md(f"""
        $$
        r_{{AB}} = {sp.latex(L_s)}
        $$
    """)
    return (L_s,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This expression can now be plotted and we can easily see the solution.
    """)
    return


@app.cell(hide_code=True)
def _(L_s, mo, np, plt, sp, theta_s):
    # Convert L_s into a numerical function using lambdify, but now using degrees
    L_s_function = sp.lambdify(theta_s, L_s.subs(theta_s, sp.rad(theta_s)), "numpy")

    # Define a range of theta_s values in degrees (e.g., from 0 to 90)
    theta_values_deg = np.linspace(0, 90, 90)
    # Plot the function
    plt.figure()
    plt.plot(theta_values_deg, L_s_function(theta_values_deg), label=r'$L_s(\theta_s)$', color='b')
    plt.title(r'$L_s(\theta_s)$', fontsize=14)
    plt.xlabel(r'$\theta_s$ (degrees)', fontsize=12)
    plt.ylabel(r'$L_s$ (mm)', fontsize=12)
    plt.grid(True)
    plt.legend()

    mo.center(plt.gca())
    return (theta_values_deg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also compute the minimum point by solving the equation $\frac{d}{d \theta} L=0$
    """)
    return


@app.cell(hide_code=True)
def _(L_s, mo, sp, theta_s):
    dL_s = sp.diff(L_s, theta_s)
    mo.md(f"""
        $$
        \\frac{{d}}{{d\\theta_s}}L = {sp.latex(dL_s)}
        $$
    """)
    return (dL_s,)


@app.cell(hide_code=True)
def _(dL_s, sp, theta_s):
    dL_s_function = sp.lambdify(theta_s, dL_s.subs(theta_s, sp.rad(theta_s)), "numpy")
    return (dL_s_function,)


@app.cell(hide_code=True)
def _(dL_s_function, mo, plt, theta_min, theta_values_deg):
    plt.figure()
    plt.plot(theta_values_deg, dL_s_function(theta_values_deg), label=r'$\frac{L_s(\theta_s)}{d\theta_s}$', color='b')
    plt.plot([0,90],[0,0], color='k', linestyle='--')
    plt.plot([theta_min],[0], 'o', markersize=8, color='red')
    plt.text(theta_min, 0-50, f"[{theta_min:0.2f},0]")
    plt.title("Derivative", fontsize=14)
    plt.xlabel(r'$\theta_s$ (degrees)', fontsize=12)
    plt.ylabel(r'$dL_s$ (mm)', fontsize=12)
    plt.grid(True)
    plt.legend()
    mo.center(plt.gca())
    return


@app.cell
def _(mo):
    mo.md(r"""
    We find a unique solution since we have defined our variable to be positive and real, also, solve is pretty good!
    """)
    return


@app.cell(hide_code=True)
def _(dL_s, mo, sp, theta_s):
    theta_min = (sp.solve(dL_s, theta_s)[0] * 180/sp.pi).evalf()
    mo.md(f"""
        $$
        \\theta_{{min}}= {sp.latex(theta_min)}
        $$
    """)
    return (theta_min,)


if __name__ == "__main__":
    app.run()
