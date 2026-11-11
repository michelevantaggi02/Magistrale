import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

def generate_fig_7_2_3d(output_path):
    fig = plt.figure(figsize=(8.5, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#ffffff')

    # Grid of x1 and x2
    x1 = np.linspace(-3.5, 3.5, 50)
    x2 = np.linspace(-3.5, 3.5, 50)
    X1, X2 = np.meshgrid(x1, x2)

    # Weights for decision boundary: w1*x1 + w2*x2 + w0 = 0
    # Let w1 = 1.2, w2 = 1.0, w0 = 0
    w1, w2, w0 = 1.2, 1.0, 0.0
    val = w1 * X1 + w2 * X2 + w0
    P = 1.0 / (1.0 + np.exp(-val))

    # Plot sigmoid surface
    surf = ax.plot_surface(X1, X2, P, cmap=cm.Blues, alpha=0.65,
                           edgecolor='#94A3B8', linewidth=0.3, antialiased=True)

    # Base plane grid at z = 0
    # Linear decision boundary on base plane: w1*x1 + w2*x2 + w0 = 0 => x2 = -w1/w2 * x1
    x1_line = np.linspace(-2.5, 2.5, 100)
    x2_line = -(w1 / w2) * x1_line
    mask = (x2_line >= -3.5) & (x2_line <= 3.5)
    x1_bnd = x1_line[mask]
    x2_bnd = x2_line[mask]
    z_base = np.zeros_like(x1_bnd)

    # Line on base plane (z=0)
    ax.plot(x1_bnd, x2_bnd, z_base, color='#059669', lw=2.5,
            label=r"Confine Decisionale: $\mathbf{w}^T\mathbf{x} + w_0 = 0$")

    # Isoline at z = 0.5 on the surface
    z_half = np.full_like(x1_bnd, 0.5)
    ax.plot(x1_bnd, x2_bnd, z_half, color='#047857', lw=2.5, ls='--',
            label=r"Livello Soglia: $p(\mathcal{C}_1 \mid \mathbf{x}) = 0.5$")

    # Vertical drop lines from z = 0.5 to z = 0 at several points
    for idx in [15, 45, 75]:
        if idx < len(x1_bnd):
            ax.plot([x1_bnd[idx], x1_bnd[idx]],
                    [x2_bnd[idx], x2_bnd[idx]],
                    [0.0, 0.5], color='#10B981', lw=1.2, ls=':')

    # Labels for regions / classes on the surface
    ax.text(-2.0, 2.5, 0.95, r"$\mathcal{C}_1: p(\mathcal{C}_1 \mid \mathbf{x}) \to 1$",
            fontsize=8.5, weight='bold', color='#1E40AF')
    ax.text(2.0, -2.5, 0.05, r"$\mathcal{C}_2: p(\mathcal{C}_1 \mid \mathbf{x}) \to 0$",
            fontsize=8.5, weight='bold', color='#991B1B')

    # Axis labels and ticks
    ax.set_xlabel(r"$x_1$", fontsize=9.5, labelpad=4, color='#0F172A')
    ax.set_ylabel(r"$x_2$", fontsize=9.5, labelpad=4, color='#0F172A')
    ax.set_zlabel(r"$p(\mathcal{C}_1 \mid \mathbf{x})$", fontsize=9.5, labelpad=6, color='#0F172A')

    ax.set_zlim(0.0, 1.0)
    ax.set_zticks([0.0, 0.5, 1.0])

    # View angle
    ax.view_init(elev=24, azim=-58)

    # Style panes
    ax.xaxis.pane.fill = True
    ax.yaxis.pane.fill = True
    ax.zaxis.pane.fill = True
    ax.xaxis.pane.set_facecolor('#F8FAFC')
    ax.yaxis.pane.set_facecolor('#F1F5F9')
    ax.zaxis.pane.set_facecolor('#FFFFFF')

    ax.xaxis.pane.set_edgecolor('#E2E8F0')
    ax.yaxis.pane.set_edgecolor('#E2E8F0')
    ax.zaxis.pane.set_edgecolor('#E2E8F0')

    # Legend
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.96), fontsize=8.2, framealpha=0.9)

    ax.set_title("Superficie Sigmoide LDA e Confine Decisionale 3D",
                 fontsize=11.0, weight='bold', color='#0F172A', pad=12)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_7_2_3d('scratch/fig_7_2_test.svg')
