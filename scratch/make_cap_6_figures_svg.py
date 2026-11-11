import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_fig_8_1(output_path):
    fig_w, fig_h = 6.4, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Curve h(x) = 0: a smooth curve
    s = np.linspace(0.8, 5.2, 200)
    curve_y = 1.2 + 0.9 * np.sin(s * 0.8)

    ax.plot(s, curve_y, color='#0284C7', lw=2.2, label=r"Curva del vincolo $h(\mathbf{x}) = 0$")

    # Point x0 on curve
    idx = 100
    x0 = s[idx]
    y0 = curve_y[idx]
    ax.plot(x0, y0, 'ko', markersize=6)
    ax.text(x0 - 0.15, y0 - 0.35, r"$\mathbf{x}$", fontsize=9.5, weight='bold', color='#0F172A')

    # Tangent vector epsilon
    dx = s[idx+1] - s[idx-1]
    dy = curve_y[idx+1] - curve_y[idx-1]
    tan_u = np.array([dx, dy]) / np.hypot(dx, dy)
    t_len = 1.6
    ax.annotate('', xy=(x0 + tan_u[0]*t_len, y0 + tan_u[1]*t_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2.0))
    ax.text(x0 + tan_u[0]*t_len + 0.1, y0 + tan_u[1]*t_len, r"$\boldsymbol{\epsilon}$ (Tangente)",
            fontsize=8.5, weight='bold', color='#1D4ED8')

    # Normal gradient nabla h
    norm_u = np.array([-tan_u[1], tan_u[0]])
    n_len = 1.4
    ax.annotate('', xy=(x0 + norm_u[0]*n_len, y0 + norm_u[1]*n_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=2.0))
    ax.text(x0 + norm_u[0]*n_len - 0.2, y0 + norm_u[1]*n_len + 0.15, r"$\nabla h(\mathbf{x})$",
            fontsize=9.0, weight='bold', color='#B45309')

    # Right angle symbol
    ra_sz = 0.25
    p1 = np.array([x0, y0]) + tan_u * ra_sz
    p2 = np.array([x0, y0]) + (tan_u + norm_u) * ra_sz
    p3 = np.array([x0, y0]) + norm_u * ra_sz
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#64748B', lw=1.0)

    # Note
    ax.text(3.0, 0.4, r"Ortogonalità analitica: $(\nabla h)^T \boldsymbol{\epsilon} = 0$",
            fontsize=8.2, weight='bold', ha='center', color='#0F172A')

    ax.set_xlim(0.5, 5.8)
    ax.set_ylim(0.2, 4.4)
    ax.axis('off')
    ax.set_title("Ortogonalità tra Gradiente del Vincolo e Tangente", fontsize=9.2, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_8_2(output_path):
    fig_w, fig_h = 6.4, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Curve h(x) = 0
    s = np.linspace(0.8, 5.2, 200)
    curve_y = 1.2 + 0.9 * np.sin(s * 0.8)
    ax.plot(s, curve_y, color='#0284C7', lw=2.2)

    # Point x away from optimum
    idx = 75
    x0 = s[idx]
    y0 = curve_y[idx]
    ax.plot(x0, y0, 'ko', markersize=6)
    ax.text(x0 - 0.15, y0 - 0.35, r"$\mathbf{x}$", fontsize=9.5, weight='bold', color='#0F172A')

    # Tangent vector epsilon
    dx = s[idx+1] - s[idx-1]
    dy = curve_y[idx+1] - curve_y[idx-1]
    tan_u = np.array([dx, dy]) / np.hypot(dx, dy)
    ax.annotate('', xy=(x0 + tan_u[0]*1.4, y0 + tan_u[1]*1.4), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.8))
    ax.text(x0 + tan_u[0]*1.4 + 0.1, y0 + tan_u[1]*1.4, r"$\boldsymbol{\epsilon}$", fontsize=9.0, weight='bold', color='#1D4ED8')

    # Gradient nabla f has non-zero tangential component
    grad_f = tan_u * 1.1 + np.array([-tan_u[1], tan_u[0]]) * 1.2
    ax.annotate('', xy=(x0 + grad_f[0], y0 + grad_f[1]), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#EF4444', lw=2.0))
    ax.text(x0 + grad_f[0] + 0.1, y0 + grad_f[1], r"$\nabla f(\mathbf{x})$", fontsize=9.0, weight='bold', color='#B91C1C')

    # Projection of nabla f on tangent
    proj = tan_u * 1.1
    ax.plot([x0 + grad_f[0], x0 + proj[0]], [y0 + grad_f[1], y0 + proj[1]], color='#94A3B8', ls=':', lw=1.2)
    ax.plot(x0 + proj[0], y0 + proj[1], 's', color='#2563EB', markersize=5)
    ax.text(x0 + proj[0] + 0.15, y0 + proj[1] - 0.25, r"$(\nabla f)^T \boldsymbol{\epsilon} \neq 0$",
            fontsize=8.0, color='#2563EB', weight='bold')

    ax.text(3.0, 0.4, r"Punto Non Ottimo: la funzione $f$ varia lungo il vincolo",
            fontsize=8.2, weight='bold', ha='center', color='#0F172A')

    ax.set_xlim(0.5, 5.8)
    ax.set_ylim(0.2, 4.4)
    ax.axis('off')
    ax.set_title("Variazione di f Lungo il Vincolo Fuori dall'Ottimo", fontsize=9.2, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_8_3(output_path):
    fig_w, fig_h = 6.4, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Curve h(x) = 0
    s = np.linspace(0.8, 5.2, 200)
    curve_y = 1.0 + 1.2 * np.sin(s * 0.8)
    ax.plot(s, curve_y, color='#0284C7', lw=2.2, label=r"$h(\mathbf{x}) = 0$")

    # Optimum point x* at crest
    idx = 98 # near peak
    x_star = s[idx]
    y_star = curve_y[idx]
    ax.plot(x_star, y_star, 'ko', markersize=7)
    ax.text(x_star + 0.15, y_star - 0.35, r"$\mathbf{x}^*$ (Ottimo)", fontsize=9.5, weight='bold', color='#0F172A')

    # Tangent is purely horizontal at crest
    tan_u = np.array([1.0, 0.0])
    ax.annotate('', xy=(x_star + 1.5, y_star), xytext=(x_star, y_star),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.6))
    ax.text(x_star + 1.55, y_star, r"$\boldsymbol{\epsilon}$", fontsize=9.0, weight='bold', color='#1D4ED8')

    # Gradient nabla h (perpendicular to tangent, points upwards)
    ax.annotate('', xy=(x_star, y_star + 1.4), xytext=(x_star, y_star),
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=2.0))
    ax.text(x_star + 0.15, y_star + 1.35, r"$\nabla h(\mathbf{x}^*)$", fontsize=9.0, weight='bold', color='#B45309')

    # Gradient nabla f (antiparallel to nabla h, points downwards or upwards)
    ax.annotate('', xy=(x_star, y_star - 1.2), xytext=(x_star, y_star),
                arrowprops=dict(arrowstyle='->', color='#EF4444', lw=2.0))
    ax.text(x_star + 0.15, y_star - 1.15, r"$\nabla f(\mathbf{x}^*)$", fontsize=9.0, weight='bold', color='#B91C1C')

    # Collinearity note
    box = patches.FancyBboxPatch((0.8, 0.35), 4.8, 0.60, boxstyle='round,pad=0.0',
                                facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.0)
    ax.add_patch(box)
    ax.text(3.2, 0.65, r"All'ottimo: $(\nabla f)^T \boldsymbol{\epsilon} = 0 \;\Rightarrow\; \nabla f(\mathbf{x}^*) = -\lambda \nabla h(\mathbf{x}^*)$",
            fontsize=7.8, ha='center', va='center', color='#1E3A8A', weight='bold')

    ax.set_xlim(0.5, 5.8)
    ax.set_ylim(0.2, 4.4)
    ax.axis('off')
    ax.set_title("Parallelismo dei Gradienti all'Ottimo Vincolato", fontsize=9.2, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_8_4(output_path):
    fig_w, fig_h = 6.4, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Contour circles of f(x): f(x) = x1^2 + x2^2 (minimum at 0, 0)
    center = np.array([2.0, 2.0])
    for r in [0.7, 1.2, 1.7, 2.2]:
        c = patches.Circle(center, r, fill=False, edgecolor='#CBD5E1', lw=1.1, ls='--')
        ax.add_patch(c)
        ax.text(center[0] + r*0.7, center[1] + r*0.7, f"f={r*r:.1f}", fontsize=7.2, color='#94A3B8')

    # Tangent constraint curve h(x) = 0: a line or curve touching r=1.7
    r_opt = 1.7
    angle = np.radians(45)
    opt_pt = center + np.array([np.cos(angle), np.sin(angle)]) * r_opt

    # Tangent line at opt_pt
    tan_dir = np.array([-np.sin(angle), np.cos(angle)])
    t1 = opt_pt - tan_dir * 1.8
    t2 = opt_pt + tan_dir * 1.6
    ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color='#0284C7', lw=2.2)
    ax.text(t1[0] + 0.1, t1[1] - 0.25, r"Vincolo $h(\mathbf{x}) = 0$", fontsize=8.2, weight='bold', color='#0284C7')

    # Optimum point
    ax.plot(opt_pt[0], opt_pt[1], 'ko', markersize=7)
    ax.text(opt_pt[0] - 0.45, opt_pt[1] + 0.25, r"$\mathbf{x}^*$", fontsize=9.5, weight='bold', color='#0F172A')

    # Note
    box = patches.FancyBboxPatch((0.5, 0.25), 4.6, 0.60, boxstyle='round,pad=0.0',
                                facecolor='#F0FDF4', edgecolor='#16A34A', lw=1.0)
    ax.add_patch(box)
    ax.text(2.8, 0.55, r"Tangenza tra Curva di Livello $f(\mathbf{x})=c^*$ e Vincolo $h(\mathbf{x})=0$",
            fontsize=7.6, ha='center', va='center', color='#166534', weight='bold')

    ax.set_xlim(0.2, 5.5)
    ax.set_ylim(0.1, 4.6)
    ax.axis('off')
    ax.set_title("Tangenza Geometrica tra Curve di Livello e Vincolo", fontsize=9.2, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def generate_fig_8_5(output_path):
    fig_w, fig_h = 10.5, 4.8
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    ax2.set_facecolor('#ffffff')

    # --- Scenario A: Vincolo Inattivo ---
    ax1.set_title("1. Vincolo Inattivo (Interno)\n" + r"$h(\mathbf{x}^*) > 0 \Rightarrow \lambda = 0$",
                  fontsize=9.2, weight='bold', color='#1E3A8A', pad=10)

    # Feasible region h(x) >= 0 (shaded half plane / circular region)
    circ = patches.Circle((2.5, 2.2), 1.6, facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.5)
    ax1.add_patch(circ)
    ax1.text(1.2, 3.4, r"Regione $\mathcal{F}: h(\mathbf{x}) \geq 0$", fontsize=8.0, color='#1D4ED8', weight='bold')

    # Optimum x* falls inside
    opt_in = np.array([2.5, 2.2])
    ax1.plot(opt_in[0], opt_in[1], 'ko', markersize=7)
    ax1.text(opt_in[0] + 0.15, opt_in[1] - 0.1, r"$\mathbf{x}^*$", fontsize=9.2, weight='bold', color='#0F172A')

    # Level curves inside
    for r in [0.4, 0.8, 1.2]:
        c = patches.Circle(opt_in, r, fill=False, edgecolor='#93C5FD', lw=1.0, ls=':')
        ax1.add_patch(c)

    ax1.text(2.5, 0.65, r"$\nabla f(\mathbf{x}^*) = \mathbf{0}$, $\lambda = 0$" + "\nIl vincolo non influenza l'ottimo",
            fontsize=7.8, ha='center', va='center', color='#334155')

    ax1.set_xlim(0.5, 4.5)
    ax1.set_ylim(0.4, 4.2)
    ax1.axis('off')

    # --- Scenario B: Vincolo Attivo ---
    ax2.set_title("2. Vincolo Attivo (Frontiera)\n" + r"$h(\mathbf{x}^*) = 0 \Rightarrow \lambda > 0$",
                  fontsize=9.2, weight='bold', color='#B91C1C', pad=10)

    # Feasible region
    circ2 = patches.Circle((2.5, 2.2), 1.6, facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.5)
    ax2.add_patch(circ2)
    ax2.text(1.2, 3.4, r"Frontiera $\partial \mathcal{F}: h(\mathbf{x}) = 0$", fontsize=8.0, color='#1D4ED8', weight='bold')

    # Optimum arrested at boundary
    angle = np.radians(35)
    opt_bnd = np.array([2.4, 2.2]) + np.array([np.cos(angle), np.sin(angle)]) * 1.5
    ax2.plot(opt_bnd[0], opt_bnd[1], 'ko', markersize=7)
    ax2.text(opt_bnd[0] - 0.35, opt_bnd[1] + 0.15, r"$\mathbf{x}^*$", fontsize=9.2, weight='bold', color='#0F172A')

    # Gradients at boundary: nabla h points inwards, nabla f points outwards
    inward = -np.array([np.cos(angle), np.sin(angle)]) * 0.75
    outward = np.array([np.cos(angle), np.sin(angle)]) * 0.75

    ax2.annotate('', xy=opt_bnd + inward, xytext=opt_bnd,
                 arrowprops=dict(arrowstyle='->', color='#D97706', lw=2.0))
    ax2.text(opt_bnd[0] + inward[0] - 0.25, opt_bnd[1] + inward[1], r"$\nabla h$", fontsize=8.5, weight='bold', color='#B45309')

    ax2.annotate('', xy=opt_bnd + outward, xytext=opt_bnd,
                 arrowprops=dict(arrowstyle='->', color='#EF4444', lw=2.0))
    ax2.text(opt_bnd[0] + outward[0] + 0.08, opt_bnd[1] + outward[1] - 0.05, r"$\nabla f$", fontsize=8.5, weight='bold', color='#B91C1C')

    ax2.text(2.5, 0.65, r"Slackness: $\lambda h(\mathbf{x}^*) = 0$" + "\n" + r"$\nabla f = -\lambda \nabla h$ ($\lambda > 0$)",
            fontsize=7.8, ha='center', va='center', color='#334155')

    ax1.set_xlim(0.3, 4.9)
    ax1.set_ylim(0.4, 4.2)
    ax2.set_xlim(0.3, 4.9)
    ax2.set_ylim(0.4, 4.2)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_8_1('Anno 1/Machine Learning/immagini/fig_8_1_gradiente_e_tangente_vincolo.svg')
    generate_fig_8_2('Anno 1/Machine Learning/immagini/fig_8_2_componente_gradiente_non_nullo.svg')
    generate_fig_8_3('Anno 1/Machine Learning/immagini/fig_8_3_parallelismo_gradienti_punto_estremale.svg')
    generate_fig_8_4('Anno 1/Machine Learning/immagini/fig_8_4_curve_di_livello_minimo_vincolato.svg')
    generate_fig_8_5('Anno 1/Machine Learning/immagini/fig_8_5_vincoli_disuguaglianza_kkt.svg')
