import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_fig_14_1(output_path):
    fig_w, fig_h = 7.5, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    np.random.seed(123)
    # Generate correlated 2D data centered at origin
    n_pts = 45
    u_true = np.array([np.cos(np.radians(35)), np.sin(np.radians(35))])
    v_true = np.array([-np.sin(np.radians(35)), np.cos(np.radians(35))])
    
    s1 = np.random.randn(n_pts) * 1.8
    s2 = np.random.randn(n_pts) * 0.45
    pts = np.outer(s1, u_true) + np.outer(s2, v_true)

    # Plot scatter
    ax.scatter(pts[:, 0], pts[:, 1], color='#3B82F6', s=28, alpha=0.75, edgecolors='#1D4ED8', zorder=3)

    # Axes u1 and u2
    origin = np.array([0.0, 0.0])
    len1 = 3.2
    len2 = 1.6

    # Axis line u1
    ax.plot([-u_true[0]*len1*1.1, u_true[0]*len1*1.1], [-u_true[1]*len1*1.1, u_true[1]*len1*1.1],
            color='#EF4444', lw=1.5, ls='--', zorder=2)
    ax.annotate('', xy=u_true*len1, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#B91C1C', lw=2.2))
    ax.text(u_true[0]*len1 + 0.15, u_true[1]*len1, r"$\mathbf{u}_1$ (Max Varianza $\lambda_1$)",
            fontsize=8.8, weight='bold', color='#B91C1C', va='center')

    # Axis line u2
    ax.plot([-v_true[0]*len2*1.1, v_true[0]*len2*1.1], [-v_true[1]*len2*1.1, v_true[1]*len2*1.1],
            color='#059669', lw=1.2, ls='--', zorder=2)
    ax.annotate('', xy=v_true*len2, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#047857', lw=1.8))
    ax.text(v_true[0]*len2 - 0.2, v_true[1]*len2 + 0.2, r"$\mathbf{u}_2$ (Min Varianza $\lambda_2$)",
            fontsize=8.5, weight='bold', color='#047857', ha='right', va='bottom')

    # Right angle marker
    ra_sz = 0.35
    ra_pt1 = u_true * ra_sz
    ra_pt2 = (u_true + v_true) * ra_sz
    ra_pt3 = v_true * ra_sz
    ax.plot([ra_pt1[0], ra_pt2[0], ra_pt3[0]], [ra_pt1[1], ra_pt2[1], ra_pt3[1]], color='#64748B', lw=1.0)

    # Ellipse showing data covariance
    cov_ellipse = patches.Ellipse((0, 0), 2*1.8*2, 2*0.45*2, angle=35, fill=False,
                                  edgecolor='#94A3B8', lw=1.2, ls=':')
    ax.add_patch(cov_ellipse)

    ax.set_xlim(-4.2, 4.8)
    ax.set_ylim(-3.0, 3.2)
    ax.set_xlabel(r"Feature $x_1$ (Abilità del pilota)", fontsize=8.8, color='#1E293B')
    ax.set_ylabel(r"Feature $x_2$ (Divertimento percepito)", fontsize=8.8, color='#1E293B')
    ax.set_title("PCA: Direzione Principale di Massima Dispersione",
                 fontsize=10.5, weight='bold', color='#0F172A', pad=10)

    # Clean axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.tick_params(colors='#64748B', labelsize=8.0)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_14_2(output_path):
    fig_w, fig_h = 7.5, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Vector geometry: origin (0, 0)
    # Unit vector u along 30 degrees
    theta = np.radians(30)
    u = np.array([np.cos(theta), np.sin(theta)])
    
    # Point x^(i)
    x_pt = np.array([2.2, 2.5])
    
    # Scalar projection z = x^T u
    z = np.dot(x_pt, u)
    x_proj = z * u

    # Projection axis line
    ax.plot([-u[0]*1.0, u[0]*4.5], [-u[1]*1.0, u[1]*4.5], color='#94A3B8', ls='--', lw=1.2, zorder=1)
    
    # Unit vector u arrow
    ax.annotate('', xy=u*1.2, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#B91C1C', lw=2.2))
    ax.text(u[0]*1.25, u[1]*1.25 - 0.25, r"$\mathbf{u}$ ($\|\mathbf{u}\|=1$)",
            fontsize=9.0, weight='bold', color='#B91C1C')

    # Vector x^(i)
    ax.annotate('', xy=x_pt, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#1D4ED8', lw=2.0))
    ax.plot(x_pt[0], x_pt[1], 'o', color='#1D4ED8', markersize=7)
    ax.text(x_pt[0] - 0.1, x_pt[1] + 0.25, r"$\mathbf{x}^{(i)}$", fontsize=9.5, weight='bold', color='#1D4ED8')

    # Projected point
    ax.plot(x_proj[0], x_proj[1], 's', color='#059669', markersize=7)
    ax.text(x_proj[0] + 0.15, x_proj[1] - 0.35, r"$\mathbf{x}_{\mathrm{proj}}^{(i)} = z^{(i)}\mathbf{u}$",
            fontsize=9.0, weight='bold', color='#059669')

    # Orthogonal projection dashed line (error vector)
    ax.plot([x_pt[0], x_proj[0]], [x_pt[1], x_proj[1]], color='#D97706', ls=':', lw=1.8)
    mid_err = (x_pt + x_proj) / 2.0
    ax.text(mid_err[0] + 0.15, mid_err[1] + 0.1, r"$\mathbf{e}^{(i)} = \mathbf{x}^{(i)} - z^{(i)}\mathbf{u}$",
            fontsize=8.5, weight='bold', color='#D97706')

    # Right angle symbol at x_proj
    # direction from x_proj to 0 is -u
    # direction from x_proj to x_pt is perp
    perp_dir = (x_pt - x_proj) / np.linalg.norm(x_pt - x_proj)
    ra_s = 0.22
    p1 = x_proj + perp_dir * ra_s
    p2 = x_proj + perp_dir * ra_s - u * ra_s
    p3 = x_proj - u * ra_s
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#64748B', lw=1.0)

    # Pythagorean note pill
    box = patches.FancyBboxPatch((-0.8, -1.3), 5.6, 0.65, boxstyle='round,pad=0.0',
                                facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.0)
    ax.add_patch(box)
    ax.text(2.0, -0.97, r"$\|\mathbf{x}^{(i)}\|^2 = (z^{(i)})^2 + \|\mathbf{e}^{(i)}\|^2 \;\Rightarrow\; \max \mathrm{Var}(z) \Leftrightarrow \min \|\mathbf{e}\|^2$",
            fontsize=8.0, ha='center', va='center', color='#1E3A8A', weight='bold')

    ax.set_xlim(-1.0, 5.0)
    ax.set_ylim(-1.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Geometria della Proiezione Ortogonale e Ricostruzione",
                 fontsize=10.5, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_14_1('Anno 1/Machine Learning/immagini/fig_14_1_direzione_massima_variazione_pca.svg')
    generate_fig_14_2('Anno 1/Machine Learning/immagini/fig_14_2_proiezione_campione_direzione_variazione.svg')
