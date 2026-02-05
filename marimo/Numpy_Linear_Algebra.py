import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import mechanicskit as mk
    return mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # How to use this document

    This document serves to show the capabillities of numpy when used to do linear algebra but also *how* we work with scientific programming using notebooks. We experiment by trying different things in many cells.

    /// admonition | Heads up.

    This document is best viewed by **showing the code**. Click the hamburger menu in the top right corner and choose "show code". Follow along on our grand venture towards understanding linear algebra and scientifict programming!
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Linear Algebra
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NumPy provides robust support for linear algebra operations through its `numpy.linalg` module. This is essential for mechanics, where vectors and matrices are the primary language.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## MechanicsKit for visualization of vectors and matrices

    We shall use the MechanicsKit here to visualize the vectors and matrices and learn by experimentation! Marimo is a great tool for this. Since we can prototype code easy and fast.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(src="public/image.png").center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you don't have the mechanicskit package, you can install it by first closing the "Missing packages" box. Then go to the "Manage Packages" tool.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(src="public/image_1.png").center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the top edit box enter

    ```
    git+https://github.com/cenmir/MechanicsKit.git
    ```
    to install the package directly from github. Install any dependencies that might not be installed (there might be an additional "Packages missing" box)
    """)
    return


@app.cell
def _():
    from mechanicskit import la, ltx, labeled
    return la, ltx


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `la` stands for LatexArray and is a way to display arrays and matrices nicely.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vector Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We start by creating some arrays.
    """)
    return


@app.cell
def _(np):
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    return a, b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can display vectors and matrices by piping the output to the MechanicsKit function `la`
    """)
    return


@app.cell
def _(a, la):
    a | la
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dot Product

    The dot product is a fundamental operation for projections and calculating work.
    """)
    return


@app.cell
def _(a, b, np):
    np.dot(a, b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    OR using the @ operator
    """)
    return


@app.cell
def _(a, b):
    a @ b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cross Product

    The cross product is useful for computing moments, areas, getting orthogonal direction etc.
    """)
    return


@app.cell
def _(a, b, la, np):
    np.cross(a, b) | la
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check that it is correct by taking the dot product, we expect the result to be 0 if the vectors are orthogonal.
    """)
    return


@app.cell
def _(a, b, np):
    c = np.cross(a, b)
    a.dot(c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Norms

    Calculating the magnitude (length) of a vector.
    """)
    return


@app.cell
def _(a, np):
    a_norm = np.linalg.norm(a)
    return (a_norm,)


@app.cell(hide_code=True)
def _(a_norm, mo):
    mo.md(f"""
    The magnitude of the vector $a$ is given by $|a|$={a_norm:0.4f}.
    """)
    return


@app.cell
def _(np):
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    return A, B


@app.cell
def _(A, B, ltx):
    ltx("\\text{Let } \\mathbf{{A}}=", A, ",\\text{and } \\mathbf{{B}}=", B)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Transpose
    """)
    return


@app.cell
def _(A, ltx):
    ltx(r"\mathbf{A}^\mathsf T = ", A.T)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Matrix Operations

    ### Matrix Multiplication

    It is crucial to distinguish between element-wise multiplication (`*`) and matrix multiplication (`@` or `np.matmul`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Elementwise:
    """)
    return


@app.cell
def _(A, B, ltx):
    ltx(fr"\mathbf{{A}} * \mathbf{{B}} = ", A * B)
    return


@app.cell
def _(A, B, ltx):
    ltx(fr"\mathbf{{A}} @ \mathbf{{B}} = ", A @ B)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Determinants

    The determinant is a scalar value that can be computed from the elements of a square matrix. It provides important information about the matrix, such as whether it is invertible.
    """)
    return


@app.cell
def _(A, mo, np):
    mo.md(rf"""
    `np.linalg.det(A)` gives {np.linalg.det(A):0.4}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solving Linear Systems

    Solving systems of equations $\mathbf A \mathbf x = \mathbf b$.
    """)
    return


@app.cell
def _(ltx, np):
    A1 = np.array([[3, 1], [1, 2]])
    b1 = np.array([9, 8])
    ltx(fr"\text{{Let }}\mathbf{{A}} = ", A1, "\\text{and } \\mathbf{{b}}=",b1)
    return A1, b1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then we get
    """)
    return


@app.cell
def _(A1, b1, ltx, np):
    x1 = np.linalg.solve(A1, b1)
    ltx(rf"\mathbf x=", x1)
    return (x1,)


@app.cell
def _(A1, ltx, x1):
    ltx(rf"\text{{Check A@x}}:", A1,"@",x1,"=", A1 @ x1)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Eigenvalues and Eigenvectors

    Crucial for principal stress analysis, stability analysis, and vibrations.
    """)
    return


@app.cell
def _(ltx, np):
    S = np.array([[10.0, 2.0], [2.0, 5.0]])
    ltx(rf"\text{{Let }} \mathbf S=",S)
    return (S,)


@app.cell
def _(S, np):
    eigenvalues1, eigenvectors1 = np.linalg.eig(S)
    return eigenvalues1, eigenvectors1


@app.cell
def _(eigenvalues1, ltx):
    ltx(rf"\text{{Eigenvalues: }}", eigenvalues1)
    return


@app.cell
def _(eigenvectors1, ltx):
    ltx(rf"\text{{Eigenvectors: }}", eigenvectors1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | Heads up.

    The eigenvectors come normalized and **columnwise**, i.e., every column is an eigenvector.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotations

    Rotations in 3D space can be represented using rotation matrices.
    """)
    return


@app.cell
def _(mo):
    slider1 = mo.ui.slider(start=0, stop=90)
    return (slider1,)


@app.cell(hide_code=True)
def _(mo, slider1):
    mo.md(rf"""
    {slider1} $\theta = {slider1.value}^\circ$
    """)
    return


@app.cell
def _(np, slider1):
    theta1 = np.radians(slider1.value) # Convert degrees to radians
    c1, s1 = np.cos(theta1), np.sin(theta1)
    return c1, s1


@app.cell(hide_code=True)
def _(c1, np, s1):
    R_z = np.array([
        [c1, -s1, 0],
        [s1,  c1, 0],
        [0,  0, 1]
    ])
    v1 = np.array([1, 0, 0])
    return R_z, v1


@app.cell
def _(R_z, ltx, v1):
    ltx(rf"\mathbf{{R}}_z=",R_z, ",\\ \mathbf v_1=",v1)
    return


@app.cell
def _(R_z, ltx, v1):
    ltx(rf"\mathbf v_r = \mathbf{{R}}_z \mathbf v_1 = ", R_z @ v1)
    return


if __name__ == "__main__":
    app.run()
