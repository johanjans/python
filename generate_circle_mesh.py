"""
Generate a unit circle mesh with triangular elements.
Output in PAM-CRASH format for consistency with the example.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

def generate_circle_mesh(radius=1.0, num_radial=5, num_angular=20):
    """
    Generate a circle mesh using polar coordinates.

    Parameters:
    -----------
    radius : float
        Circle radius (default 1.0 for unit circle)
    num_radial : int
        Number of radial divisions
    num_angular : int
        Number of angular divisions

    Returns:
    --------
    nodes : ndarray
        Node coordinates [node_id, x, y, z]
    elements : ndarray
        Element connectivity [elem_id, n1, n2, n3]
    """
    nodes = []
    node_id = 1

    # Create center node
    nodes.append([node_id, 0.0, 0.0, 0.0])
    node_id += 1

    # Create nodes in concentric rings
    node_map = {0: [1]}  # ring_index -> list of node IDs

    for i_ring in range(1, num_radial + 1):
        r = radius * i_ring / num_radial
        ring_nodes = []

        for i_angle in range(num_angular):
            theta = 2 * np.pi * i_angle / num_angular
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            nodes.append([node_id, x, y, 0.0])
            ring_nodes.append(node_id)
            node_id += 1

        node_map[i_ring] = ring_nodes

    # Create triangular elements
    elements = []
    elem_id = 1

    # Elements around center
    for i in range(num_angular):
        n1 = 1  # center node
        n2 = node_map[1][i]
        n3 = node_map[1][(i + 1) % num_angular]
        elements.append([elem_id, n1, n2, n3])
        elem_id += 1

    # Elements in outer rings
    for i_ring in range(1, num_radial):
        inner_ring = node_map[i_ring]
        outer_ring = node_map[i_ring + 1]

        for i in range(num_angular):
            i_next = (i + 1) % num_angular

            # First triangle (pointing inward)
            n1 = inner_ring[i]
            n2 = outer_ring[i]
            n3 = inner_ring[i_next]
            elements.append([elem_id, n1, n2, n3])
            elem_id += 1

            # Second triangle (pointing outward)
            n1 = inner_ring[i_next]
            n2 = outer_ring[i]
            n3 = outer_ring[i_next]
            elements.append([elem_id, n1, n2, n3])
            elem_id += 1

    return np.array(nodes), np.array(elements)


def write_pamcrash_format(filename, nodes, elements):
    """Write mesh to PAM-CRASH format file."""
    with open(filename, 'w') as f:
        # Header
        f.write("$#--1----|----2----|----3----|----4----|----5----|----6----|----7----|----8----|----9----|---10----|\n")
        f.write("$#\n")
        f.write("$# PAM-CRASH input deck - Unit circle mesh with triangular elements\n")
        f.write("$# Generated mesh for area calculation example\n")
        f.write("$#\n")
        f.write("$# NODES\n")
        f.write("$#      NODE                   X                   Y                   Z\n")

        # Write nodes
        for node in nodes:
            nid, x, y, z = node
            f.write(f"NODE   {int(nid):7d}    {x:16.8f}    {y:16.8f}    {z:16.8f}\n")

        # Write elements
        f.write("$#\n")
        f.write("$# SHELL ELEMENTS (Triangular)\n")
        f.write("$#    SHELL     PART       N1       N2       N3\n")

        for elem in elements:
            eid, n1, n2, n3 = elem
            f.write(f"SHELL  {int(eid):7d}        1{int(n1):8d}{int(n2):8d}{int(n3):8d}\n")

        f.write("$#\n")
        f.write("$# End of file\n")


def visualize_mesh(nodes, elements, title="Circle Mesh"):
    """Visualize the generated mesh."""
    x = nodes[:, 1]
    y = nodes[:, 2]
    triangles = elements[:, 1:4] - 1  # Convert to 0-based for matplotlib

    fig, ax = plt.subplots(figsize=(8, 8))

    triang = Triangulation(x, y, triangles)
    ax.triplot(triang, 'k-', linewidth=0.5)
    ax.plot(x, y, 'o', markersize=3, color='blue')

    ax.set_aspect('equal')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    return fig, ax


if __name__ == "__main__":
    # Generate mesh with target of ~100 elements
    # num_angular * num_radial * 2 ≈ 100 elements
    # 20 * 4 * 2 = 160 elements (close enough, or adjust)
    # Try: 16 * 3 * 2 = 96 elements

    print("Generating unit circle mesh...")
    nodes, elements = generate_circle_mesh(radius=1.0, num_radial=4, num_angular=16)

    print(f"Generated {len(nodes)} nodes and {len(elements)} elements")

    # Calculate theoretical area
    theoretical_area = np.pi * 1.0**2
    print(f"Theoretical area: π = {theoretical_area:.6f}")

    # Write to file
    output_file = "assets/unit_circle_mesh.pc"
    write_pamcrash_format(output_file, nodes, elements)
    print(f"Mesh written to {output_file}")

    # Visualize
    fig, ax = visualize_mesh(nodes, elements, f"Unit Circle Mesh ({len(elements)} elements)")
    plt.savefig("assets/unit_circle_mesh.png", dpi=150, bbox_inches='tight')
    print("Visualization saved to assets/unit_circle_mesh.png")
    plt.show()
