import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_fig_7_1(output_path):
    fig_w, fig_h = 6.8, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(-1.0, 7.5)
    ax.set_ylim(-1.0, 5.5)

    # Title
    ax.text(3.25, 5.15, r"Linear Discriminant Analysis: Confine Lineare",
            fontsize=10.5, weight='bold', ha='center', va='center', color='#0F172A')

    # Parameters for 2 Gaussians with shared covariance
    mu1 = np.array([1.8, 1.8])
    mu2 = np.array([4.6, 3.4])
    
    # Draw elliptical contours (shared covariance Sigma, tilted at 35 degrees)
    for r in [0.7, 1.3, 1.9]:
        e1 = patches.Ellipse(mu1, r*1.6, r*0.9, angle=35, fill=False, edgecolor='#3B82F6', lw=1.1, ls='--', alpha=0.8)
        e2 = patches.Ellipse(mu2, r*1.6, r*0.9, angle=35, fill=False, edgecolor='#EF4444', lw=1.1, ls='--', alpha=0.8)
        ax.add_patch(e1)
        ax.add_patch(e2)

    # Centers
    ax.plot(mu1[0], mu1[1], 'o', color='#1D4ED8', markersize=7)
    ax.text(mu1[0] - 0.25, mu1[1] + 0.35, r"$\boldsymbol{\mu}_1$ ($\mathcal{C}_1$)", fontsize=9.2, weight='bold', color='#1D4ED8')
    
    ax.plot(mu2[0], mu2[1], 'o', color='#B91C1C', markersize=7)
    ax.text(mu2[0] + 0.25, mu2[1] - 0.35, r"$\boldsymbol{\mu}_2$ ($\mathcal{C}_2$)", fontsize=9.2, weight='bold', color='#B91C1C')

    # Midpoint and line connecting means
    mid = (mu1 + mu2) / 2.0
    ax.plot([mu1[0], mu2[0]], [mu1[1], mu2[1]], color='#94A3B8', lw=1.2, ls=':')
    ax.plot(mid[0], mid[1], 'ks', markersize=5)

    # Vector w = Sigma^-1 (mu1 - mu2)
    # Direction is roughly mu1 - mu2
    diff = mu1 - mu2
    diff_u = diff / np.linalg.norm(diff)
    ax.annotate('', xy=(mid[0] + diff_u[0]*1.4, mid[1] + diff_u[1]*1.4), xytext=(mid[0], mid[1]),
                arrowprops=dict(arrowstyle='->', color='#0F172A', lw=1.8))
    ax.text(mid[0] + diff_u[0]*1.45, mid[1] + diff_u[1]*1.45, r"$\mathbf{w} = \mathbf{\Sigma}^{-1}(\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2)$",
            fontsize=8.5, weight='bold', color='#0F172A', ha='right', va='bottom')

    # Linear Decision Boundary (orthogonal to w, passing through mid if priors equal)
    # Normal to diff_u is [-diff_u[1], diff_u[0]]
    perp = np.array([-diff_u[1], diff_u[0]])
    line_start = mid - perp * 3.0
    line_end = mid + perp * 3.0
    ax.plot([line_start[0], line_end[0]], [line_start[1], line_end[1]], color='#059669', lw=2.2)
    ax.text(line_end[0] - 0.2, line_end[1] + 0.25, r"$\mathbf{w}^T \mathbf{x} + w_0 = 0$",
            fontsize=9.2, weight='bold', color='#059669', ha='left')

    # Explanatory pill
    box = patches.FancyBboxPatch((0.2, -0.75), 6.1, 0.65, boxstyle='round,pad=0.0',
                                facecolor='#ECFDF5', edgecolor='#10B981', lw=1.0)
    ax.add_patch(box)
    ax.text(3.25, -0.42, r"Covarianza condivisa $\mathbf{\Sigma} \to$ cancellazione forme quadratiche $\to$ confine lineare",
            fontsize=7.8, ha='center', va='center', color='#065F46')

    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_7_2(output_path):
    fig_w, fig_h = 6.8, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Title
    ax.text(0.0, 1.25, r"Probabilità a Posteriori: Funzione Sigmoide",
            fontsize=10.5, weight='bold', ha='center', va='center', color='#0F172A')

    # Sigmoid curve along projection axis y = w^T x + w0
    z = np.linspace(-4.5, 4.5, 200)
    sig = 1.0 / (1.0 + np.exp(-z))

    ax.plot(z, sig, color='#2563EB', lw=2.5, label=r"$p(\mathcal{C}_1 \mid \mathbf{x}) = \sigma(\mathbf{w}^T\mathbf{x} + w_0)$")
    
    # Threshold at z = 0, p = 0.5
    ax.axhline(0.5, color='#94A3B8', ls='--', lw=1.2)
    ax.axvline(0.0, color='#059669', ls='--', lw=1.5)
    ax.plot(0.0, 0.5, 'o', color='#059669', markersize=6)
    ax.text(0.15, 0.45, r"Soglia $p = 0.5$ ($\mathbf{w}^T\mathbf{x} + w_0 = 0$)", fontsize=8.2, color='#059669', weight='bold')

    # Asymptotes
    ax.axhline(1.0, color='#CBD5E1', ls=':', lw=1.0)
    ax.axhline(0.0, color='#CBD5E1', ls=':', lw=1.0)
    ax.text(3.0, 0.92, r"Classe $\mathcal{C}_1$ ($p \to 1$)", fontsize=8.2, color='#1D4ED8', weight='bold')
    ax.text(-4.2, 0.08, r"Classe $\mathcal{C}_2$ ($p \to 0$)", fontsize=8.2, color='#B91C1C', weight='bold')

    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-0.25, 1.35)
    ax.set_xlabel(r"Proiezione scalare: $a(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + w_0$", fontsize=8.8, color='#1E293B')
    ax.set_ylabel(r"Probabilità $p(\mathcal{C}_1 \mid \mathbf{x})$", fontsize=8.8, color='#1E293B')

    # Clean axes design
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')
    ax.tick_params(colors='#475569', labelsize=8.0)
    ax.set_yticks([0.0, 0.5, 1.0])

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_7_1('Anno 1/Machine Learning/immagini/fig_7_1_lda_decision_boundary.svg')
    generate_fig_7_2('Anno 1/Machine Learning/immagini/fig_7_2_sigmoide_lda_superficie.svg')
