import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_fig_13_1(output_path):
    fig_w, fig_h = 12.8, 5.2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    np.random.seed(42)
    # 2 clusters for clear visual simplicity
    c1 = np.random.randn(14, 2) * 0.55 + np.array([2.0, 2.5])
    c2 = np.random.randn(14, 2) * 0.55 + np.array([5.5, 3.5])

    # Initial centroids (slightly displaced from actual centers)
    mu1_init = np.array([1.5, 3.2])
    mu2_init = np.array([6.0, 2.6])

    # --- PANEL 1: FASE E (Assegnamento Punti) ---
    ax1.set_title("Fase E: Assegnamento Ottimo dei Campioni\n" + r"$r_{nk} = 1 \Leftrightarrow k = \arg\min_j \|\mathbf{x}^{(n)} - \boldsymbol{\mu}_j\|^2$",
                  fontsize=9.2, weight='bold', color='#1E3A8A', pad=12)

    # Plot points colored by nearest initial centroid
    for p in c1:
        d1 = np.linalg.norm(p - mu1_init)
        d2 = np.linalg.norm(p - mu2_init)
        col = '#3B82F6' if d1 < d2 else '#EF4444'
        ax1.plot(p[0], p[1], 'o', color=col, markersize=6, alpha=0.85)

    for p in c2:
        d1 = np.linalg.norm(p - mu1_init)
        d2 = np.linalg.norm(p - mu2_init)
        col = '#3B82F6' if d1 < d2 else '#EF4444'
        ax1.plot(p[0], p[1], 'o', color=col, markersize=6, alpha=0.85)

    # Plot centroids
    ax1.plot(mu1_init[0], mu1_init[1], 'X', color='#1D4ED8', markersize=11, markeredgecolor='black', markeredgewidth=1.2)
    ax1.text(mu1_init[0] - 0.2, mu1_init[1] + 0.35, r"$\boldsymbol{\mu}_1$ (Fisso)", fontsize=8.6, weight='bold', color='#1D4ED8')

    ax1.plot(mu2_init[0], mu2_init[1], 'X', color='#B91C1C', markersize=11, markeredgecolor='black', markeredgewidth=1.2)
    ax1.text(mu2_init[0] - 0.2, mu2_init[1] - 0.45, r"$\boldsymbol{\mu}_2$ (Fisso)", fontsize=8.6, weight='bold', color='#B91C1C')

    # Voronoi separating hyperline between mu1_init and mu2_init
    mid_init = (mu1_init + mu2_init) / 2.0
    diff_init = mu2_init - mu1_init
    perp_init = np.array([-diff_init[1], diff_init[0]]) / np.linalg.norm(diff_init)
    line1 = mid_init - perp_init * 3.5
    line2 = mid_init + perp_init * 3.5
    ax1.plot([line1[0], line2[0]], [line1[1], line2[1]], color='#059669', ls='--', lw=1.5)
    ax1.text(mid_init[0] + 0.1, 4.8, "Confine di Voronoi", fontsize=7.8, color='#059669', weight='bold')

    ax1.set_xlim(0.5, 7.5)
    ax1.set_ylim(0.5, 5.2)
    ax1.axis('off')

    # --- PANEL 2: FASE M (Aggiornamento Centroidi) ---
    ax2.set_title("Fase M: Ricalcolo dei Centroidi come Baricentri\n" + r"$\boldsymbol{\mu}_k = \frac{1}{N_k} \sum_{n \in \mathcal{C}_k} \mathbf{x}^{(n)}$",
                  fontsize=9.2, weight='bold', color='#065F46', pad=12)

    # Actual cluster means
    mu1_new = np.mean(c1, axis=0)
    mu2_new = np.mean(c2, axis=0)

    # Plot points
    for p in c1: ax2.plot(p[0], p[1], 'o', color='#3B82F6', markersize=6, alpha=0.85)
    for p in c2: ax2.plot(p[0], p[1], 'o', color='#EF4444', markersize=6, alpha=0.85)

    # Old centroids ghost
    ax2.plot(mu1_init[0], mu1_init[1], 'X', color='#93C5FD', markersize=9, alpha=0.6)
    ax2.plot(mu2_init[0], mu2_init[1], 'X', color='#FCA5A5', markersize=9, alpha=0.6)

    # New centroids
    ax2.plot(mu1_new[0], mu1_new[1], 'X', color='#1D4ED8', markersize=11, markeredgecolor='black', markeredgewidth=1.2)
    ax2.text(mu1_new[0] - 0.2, mu1_new[1] + 0.35, r"$\boldsymbol{\mu}_1^{\mathrm{nuovo}}$", fontsize=8.6, weight='bold', color='#1D4ED8')

    ax2.plot(mu2_new[0], mu2_new[1], 'X', color='#B91C1C', markersize=11, markeredgecolor='black', markeredgewidth=1.2)
    ax2.text(mu2_new[0] - 0.2, mu2_new[1] - 0.45, r"$\boldsymbol{\mu}_2^{\mathrm{nuovo}}$", fontsize=8.6, weight='bold', color='#B91C1C')

    # Arrows showing centroid movement
    ax2.annotate('', xy=(mu1_new[0], mu1_new[1]), xytext=(mu1_init[0], mu1_init[1]),
                 arrowprops=dict(arrowstyle='->', color='#1D4ED8', lw=1.6, ls='--'))
    ax2.annotate('', xy=(mu2_new[0], mu2_new[1]), xytext=(mu2_init[0], mu2_init[1]),
                 arrowprops=dict(arrowstyle='->', color='#B91C1C', lw=1.6, ls='--'))

    ax2.set_xlim(0.5, 7.5)
    ax2.set_ylim(0.5, 5.2)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_13_2(output_path):
    fig_w, fig_h = 11.2, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    x = np.linspace(-1.0, 11.0, 400)

    # 3 Gaussian components
    pi = [0.35, 0.40, 0.25]
    mu = [2.0, 5.5, 8.5]
    sigma = [0.9, 1.2, 0.8]

    def norm_pdf(val, m, s):
        return (1.0 / (s * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((val - m) / s)**2)

    c1 = pi[0] * norm_pdf(x, mu[0], sigma[0])
    c2 = pi[1] * norm_pdf(x, mu[1], sigma[1])
    c3 = pi[2] * norm_pdf(x, mu[2], sigma[2])
    mix = c1 + c2 + c3

    # Plot components (dashed with fill)
    ax.plot(x, c1, '--', color='#2563EB', lw=1.6, label=r"$\pi_1 \mathcal{N}(x \mid \mu_1, \sigma_1^2)$")
    ax.fill_between(x, c1, color='#DBEAFE', alpha=0.35)

    ax.plot(x, c2, '--', color='#059669', lw=1.6, label=r"$\pi_2 \mathcal{N}(x \mid \mu_2, \sigma_2^2)$")
    ax.fill_between(x, c2, color='#D1FAE5', alpha=0.35)

    ax.plot(x, c3, '--', color='#D97706', lw=1.6, label=r"$\pi_3 \mathcal{N}(x \mid \mu_3, \sigma_3^2)$")
    ax.fill_between(x, c3, color='#FEF3C7', alpha=0.35)

    # Total mixture (bold solid curve)
    ax.plot(x, mix, '-', color='#0F172A', lw=2.4, label=r"Densità di mistura $p(x) = \sum_{k=1}^3 \pi_k \mathcal{N}(x \mid \mu_k, \sigma_k^2)$")

    # Sample point x0 showing soft responsibilities
    x0 = 3.8
    y0 = np.interp(x0, x, mix)
    ax.axvline(x0, color='#64748B', ls=':', lw=1.2)
    ax.plot(x0, y0, 'ko', markersize=6)
    ax.text(x0 + 0.15, 0.22, r"Punto di test $x_0$" + "\n" + r"$\gamma(z_k) = p(z_k=1 \mid x_0)$" + "\n(Assegnamento soft)",
            fontsize=8.0, color='#334155', weight='bold')

    ax.set_xlim(-1.0, 11.0)
    ax.set_ylim(-0.02, 0.32)
    ax.set_xlabel(r"Spazio delle feature $x$", fontsize=9.0, color='#1E293B')
    ax.set_ylabel(r"Densità di probabilità $p(x)$", fontsize=9.0, color='#1E293B')

    ax.set_title("Modello a Mistura di Gaussiane (GMM): Densità Marginale e Componenti Ponderate",
                 fontsize=10.5, weight='bold', color='#0F172A', pad=12)

    # Clean axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')
    ax.tick_params(colors='#475569', labelsize=8.0)
    ax.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#CBD5E1', fontsize=7.8)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_13_1('Anno 1/Machine Learning/immagini/fig_13_1_iterazione_kmeans_centroidi.svg')
    generate_fig_13_2('Anno 1/Machine Learning/immagini/fig_13_2_mistura_gaussiane_unidimensionale.svg')
