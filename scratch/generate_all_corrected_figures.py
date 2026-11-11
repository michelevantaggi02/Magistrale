import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

# ==============================================================================
# FIG 7.2: 3D SIGMOID SURFACE FOR LDA
# ==============================================================================
def generate_fig_7_2(output_path):
    fig = plt.figure(figsize=(8.8, 5.8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#ffffff')

    x1 = np.linspace(-3.5, 3.5, 45)
    x2 = np.linspace(-3.5, 3.5, 45)
    X1, X2 = np.meshgrid(x1, x2)

    w1, w2, w0 = 1.2, 1.0, 0.0
    val = w1 * X1 + w2 * X2 + w0
    P = 1.0 / (1.0 + np.exp(-val))

    # Plot surface
    surf = ax.plot_surface(X1, X2, P, cmap=cm.Blues, alpha=0.60,
                           edgecolor='#94A3B8', linewidth=0.25, antialiased=True)

    # Base line (z=0)
    x1_line = np.linspace(-2.6, 2.6, 100)
    x2_line = -(w1 / w2) * x1_line
    mask = (x2_line >= -3.5) & (x2_line <= 3.5)
    x1_bnd = x1_line[mask]
    x2_bnd = x2_line[mask]
    z_base = np.zeros_like(x1_bnd)

    ax.plot(x1_bnd, x2_bnd, z_base, color='#059669', lw=2.5,
            label=r"Confine Decisionale: $\mathbf{w}^T\mathbf{x} + w_0 = 0$")

    # Isoline at z = 0.5 on surface
    z_half = np.full_like(x1_bnd, 0.5)
    ax.plot(x1_bnd, x2_bnd, z_half, color='#047857', lw=2.5, ls='--',
            label=r"Livello Soglia: $p(\mathcal{C}_1 \mid \mathbf{x}) = 0.5$")

    # Vertical drop lines
    for idx in [12, 42, 72]:
        if idx < len(x1_bnd):
            ax.plot([x1_bnd[idx], x1_bnd[idx]],
                    [x2_bnd[idx], x2_bnd[idx]],
                    [0.0, 0.5], color='#10B981', lw=1.2, ls=':')

    # Labels for classes
    ax.text(-2.4, 2.5, 0.95, r"$\mathcal{C}_1: p(\mathcal{C}_1 \mid \mathbf{x}) \to 1$",
            fontsize=8.5, weight='bold', color='#1E40AF')
    ax.text(2.0, -2.6, 0.05, r"$\mathcal{C}_2: p(\mathcal{C}_1 \mid \mathbf{x}) \to 0$",
            fontsize=8.5, weight='bold', color='#991B1B')

    ax.set_xlabel(r"$x_1$", fontsize=9.5, labelpad=4, color='#0F172A')
    ax.set_ylabel(r"$x_2$", fontsize=9.5, labelpad=4, color='#0F172A')
    ax.set_zlabel(r"$p(\mathcal{C}_1 \mid \mathbf{x})$", fontsize=9.5, labelpad=6, color='#0F172A')

    ax.set_zlim(0.0, 1.0)
    ax.set_zticks([0.0, 0.5, 1.0])
    ax.view_init(elev=24, azim=-58)

    ax.xaxis.pane.fill = True
    ax.yaxis.pane.fill = True
    ax.zaxis.pane.fill = True
    ax.xaxis.pane.set_facecolor('#F8FAFC')
    ax.yaxis.pane.set_facecolor('#F1F5F9')
    ax.zaxis.pane.set_facecolor('#FFFFFF')
    ax.xaxis.pane.set_edgecolor('#E2E8F0')
    ax.yaxis.pane.set_edgecolor('#E2E8F0')
    ax.zaxis.pane.set_edgecolor('#E2E8F0')

    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.96), fontsize=8.2, framealpha=0.9)
    ax.set_title("Superficie Sigmoide LDA e Confine Decisionale 3D",
                 fontsize=11.0, weight='bold', color='#0F172A', pad=12)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")


# ==============================================================================
# FIG 8.2: GRADIENT AND INVERSE GRADIENT (NOT ORTHOGONAL)
# ==============================================================================
def generate_fig_8_2(output_path):
    fig_w, fig_h = 7.5, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Curve h(x1, x2) = 0
    t = np.linspace(-1.5, 3.5, 200)
    # y = 1.0 + 0.3*x + 0.15*x^2
    curve_x = t
    curve_y = 1.2 + 0.35 * t + 0.12 * t**2
    ax.plot(curve_x, curve_y, color='#0284C7', lw=2.4)
    ax.text(3.1, 3.4, r"$h(x_1, x_2) = 0$", fontsize=9.5, weight='bold', color='#0284C7')

    # Point x on curve
    x0 = 0.8
    y0 = 1.2 + 0.35 * x0 + 0.12 * x0**2
    ax.plot(x0, y0, 'ko', markersize=6)
    ax.text(x0 - 0.25, y0 - 0.35, r"$\mathbf{x}$", fontsize=10.0, weight='bold', color='#0F172A')

    # Tangent vector epsilon
    # Slope of curve at x0: dy/dx = 0.35 + 0.24*x0
    slope = 0.35 + 0.24 * x0
    u_eps = np.array([1.0, slope])
    u_eps = u_eps / np.linalg.norm(u_eps)
    eps_len = 1.3
    ax.annotate('', xy=(x0 + u_eps[0]*eps_len, y0 + u_eps[1]*eps_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2.2))
    ax.text(x0 + u_eps[0]*eps_len + 0.1, y0 + u_eps[1]*eps_len, r"$\boldsymbol{\epsilon}$ (tangente)",
            fontsize=8.8, weight='bold', color='#1D4ED8')

    # Non-orthogonal gradient grad f at acute angle
    # Normal would be [-u_eps[1], u_eps[0]]
    # Let grad f be rotated away from normal towards epsilon (e.g. angle ~ 40 deg with epsilon)
    # So (grad f)^T epsilon != 0
    grad_dir = np.array([0.45, 1.1])
    grad_dir = grad_dir / np.linalg.norm(grad_dir)
    grad_len = 1.4

    # Gradient +nabla f
    ax.annotate('', xy=(x0 + grad_dir[0]*grad_len, y0 + grad_dir[1]*grad_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.2))
    ax.text(x0 + grad_dir[0]*grad_len - 0.05, y0 + grad_dir[1]*grad_len + 0.12,
            r"$\nabla f$ (incremento di $f$)", fontsize=8.8, weight='bold', color='#DC2626')

    # Inverse gradient -nabla f
    ax.annotate('', xy=(x0 - grad_dir[0]*grad_len, y0 - grad_dir[1]*grad_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#B91C1C', lw=2.0, ls='--'))
    ax.text(x0 - grad_dir[0]*grad_len - 0.1, y0 - grad_dir[1]*grad_len - 0.25,
            r"$-\nabla f$ (decremento di $f$)", fontsize=8.8, weight='bold', color='#B91C1C')

    # Explanatory card
    box = patches.FancyBboxPatch((-1.2, 0.15), 4.3, 0.70, boxstyle='round,pad=0.0',
                                facecolor='#FEF2F2', edgecolor='#EF4444', lw=1.0)
    ax.add_patch(box)
    ax.text(0.95, 0.50,
            r"$(\nabla f)^T \boldsymbol{\epsilon} \neq 0 \Rightarrow \mathbf{x}$ NON è un punto estremale" + "\n" +
            r"Spostandosi lungo $\boldsymbol{\epsilon}$ si incrementa $f$; lungo $-\boldsymbol{\epsilon}$ si riduce $f$",
            fontsize=7.8, ha='center', va='center', color='#991B1B')

    ax.set_xlim(-1.4, 3.8)
    ax.set_ylim(0.0, 4.0)
    ax.axis('off')
    ax.set_title(r"Componente del Gradiente non Nulla Lungo il Vincolo: $(\nabla f)^T \boldsymbol{\epsilon} \neq 0$",
                 fontsize=9.8, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")


# ==============================================================================
# FIG 8.3: PARALLELISM OF GRADIENTS AT EXTREMA (PERPENDICULAR TO CURVE)
# ==============================================================================
def generate_fig_8_3(output_path):
    fig_w, fig_h = 7.5, 4.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Curve h(x1, x2) = 0
    t = np.linspace(-1.5, 3.5, 200)
    curve_x = t
    curve_y = 1.2 + 0.35 * t + 0.12 * t**2
    ax.plot(curve_x, curve_y, color='#0284C7', lw=2.4)
    ax.text(3.1, 3.4, r"$h(x_1, x_2) = 0$", fontsize=9.5, weight='bold', color='#0284C7')

    # Extremal point x*
    x0 = 0.8
    y0 = 1.2 + 0.35 * x0 + 0.12 * x0**2
    ax.plot(x0, y0, 'ko', markersize=6)
    ax.text(x0 - 0.35, y0 - 0.15, r"$\mathbf{x}^*$", fontsize=10.5, weight='bold', color='#0F172A')

    # Tangent vector epsilon
    slope = 0.35 + 0.24 * x0
    u_eps = np.array([1.0, slope])
    u_eps = u_eps / np.linalg.norm(u_eps)
    eps_len = 1.3
    ax.annotate('', xy=(x0 + u_eps[0]*eps_len, y0 + u_eps[1]*eps_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=2.2))
    ax.text(x0 + u_eps[0]*eps_len + 0.1, y0 + u_eps[1]*eps_len, r"$\boldsymbol{\epsilon}$ (tangente)",
            fontsize=8.8, weight='bold', color='#1D4ED8')

    # Normal vector n (EXACTLY ORTHOGONAL to u_eps)
    # n = [-u_eps[1], u_eps[0]]
    u_norm = np.array([-u_eps[1], u_eps[0]])
    u_norm = u_norm / np.linalg.norm(u_norm)

    # nabla h points along +u_norm (orthogonal to curve!)
    nh_len = 1.3
    ax.annotate('', xy=(x0 + u_norm[0]*nh_len, y0 + u_norm[1]*nh_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=2.2))
    ax.text(x0 + u_norm[0]*nh_len - 0.35, y0 + u_norm[1]*nh_len + 0.15,
            r"$\nabla h(\mathbf{x}^*)$", fontsize=9.2, weight='bold', color='#B45309')

    # nabla f points along -u_norm (anti-parallel, or +u_norm parallel)
    # Both are on the EXACT SAME line, strictly perpendicular to epsilon!
    nf_len = 1.2
    ax.annotate('', xy=(x0 - u_norm[0]*nf_len, y0 - u_norm[1]*nf_len), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.2))
    ax.text(x0 - u_norm[0]*nf_len + 0.12, y0 - u_norm[1]*nf_len - 0.20,
            r"$\nabla f(\mathbf{x}^*)$", fontsize=9.2, weight='bold', color='#DC2626')

    # Right-angle symbols at x0 between epsilon and norm, and epsilon and -norm
    ra_s = 0.22
    # Upper right angle (epsilon and +norm)
    p1 = np.array([x0, y0]) + u_eps * ra_s
    p2 = p1 + u_norm * ra_s
    p3 = np.array([x0, y0]) + u_norm * ra_s
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color='#64748B', lw=1.1)

    # Lower right angle (epsilon and -norm)
    p4 = np.array([x0, y0]) + u_eps * ra_s
    p5 = p4 - u_norm * ra_s
    p6 = np.array([x0, y0]) - u_norm * ra_s
    ax.plot([p4[0], p5[0], p6[0]], [p4[1], p5[1], p6[1]], color='#64748B', lw=1.1)

    # Explanatory card
    box = patches.FancyBboxPatch((-1.2, 0.15), 4.3, 0.70, boxstyle='round,pad=0.0',
                                facecolor='#F0FDF4', edgecolor='#16A34A', lw=1.0)
    ax.add_patch(box)
    ax.text(0.95, 0.50,
            r"$\nabla f \perp \boldsymbol{\epsilon}$ e $\nabla h \perp \boldsymbol{\epsilon} \Rightarrow \nabla f \parallel \nabla h$" + "\n" +
            r"Esiste $\lambda \neq 0$ tale che $\nabla f(\mathbf{x}^*) + \lambda \nabla h(\mathbf{x}^*) = \mathbf{0}$",
            fontsize=7.8, ha='center', va='center', color='#166534', weight='bold')

    ax.set_xlim(-1.4, 3.8)
    ax.set_ylim(0.0, 4.0)
    ax.axis('off')
    ax.set_title(r"Parallelismo dei Gradienti all'Ottimo Vincolato: $\nabla f = -\lambda \nabla h$",
                 fontsize=9.8, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")


# ==============================================================================
# FIG 8.4: LEVEL CURVES OF MINIMIZATION WITH CONSTRAINED OPTIMUM
# ==============================================================================
def generate_fig_8_4(output_path):
    fig_w, fig_h = 7.5, 5.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Unconstrained minimum of f(x1, x2) at center (x1_0, x2_0)
    center = np.array([2.8, 2.3])
    ax.plot(center[0], center[1], 'o', color='#475569', markersize=6)
    ax.text(center[0] + 0.15, center[1] - 0.05, r"$(x_1^0, x_2^0)$ Minimo Libero ($f = c_3$)",
            fontsize=8.5, weight='bold', color='#334155')

    # Level curves of f: c3 < c2 < c* < c1 (expanding outward from center)
    # We use ellipses tilted slightly
    angle = 30
    radii = [
        (0.6, 0.4, r"$c_3$", '#94A3B8'),
        (1.3, 0.85, r"$c_2$", '#64748B'),
        (2.0, 1.30, r"$c^*$", '#2563EB'),
        (2.7, 1.75, r"$c_1$", '#94A3B8'),
    ]

    for rx, ry, label, col in radii:
        lw = 2.0 if label == r"$c^*$" else 1.1
        ls = '-' if label == r"$c^*$" else '--'
        e = patches.Ellipse(center, rx*2, ry*2, angle=angle, fill=False,
                            edgecolor=col, lw=lw, ls=ls)
        ax.add_patch(e)

    # Label the level curves along the bottom right
    ax.text(center[0] + 0.5, center[1] - 0.55, r"$f = c_3$", fontsize=7.5, color='#64748B')
    ax.text(center[0] + 1.1, center[1] - 0.95, r"$f = c_2$", fontsize=7.5, color='#475569')
    ax.text(center[0] + 1.7, center[1] - 1.35, r"$f = c^*$", fontsize=8.2, weight='bold', color='#1D4ED8')
    ax.text(center[0] + 2.3, center[1] - 1.75, r"$f = c_1$", fontsize=7.5, color='#64748B')

    # Constrained optimum point x* on contour c*
    # At angle around 145 degrees
    rad_ang = np.radians(angle + 115)
    # Point on ellipse: rx=2.0, ry=1.3
    # in local coords:
    lx = 2.0 * np.cos(np.radians(115))
    ly = 1.3 * np.sin(np.radians(115))
    rot = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                    [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])
    opt_pt = center + rot @ np.array([lx, ly])

    ax.plot(opt_pt[0], opt_pt[1], 'ko', markersize=7)
    ax.text(opt_pt[0] - 0.35, opt_pt[1] + 0.25, r"$\mathbf{x}^* = (x_1^*, x_2^*)$",
            fontsize=9.5, weight='bold', color='#0F172A')

    # Tangent vector to ellipse at opt_pt
    # local tangent is [-rx*sin(115), ry*cos(115)]
    ltan = np.array([-2.0 * np.sin(np.radians(115)), 1.3 * np.cos(np.radians(115))])
    gtan = rot @ ltan
    u_tan = gtan / np.linalg.norm(gtan)

    # Constraint curve h(x1, x2) = 0 is tangent to c* at opt_pt
    # Let's draw it as a curved arc passing through opt_pt with curvature bending AWAY from center
    t_vals = np.linspace(-1.8, 1.8, 100)
    u_out = -(center - opt_pt) / np.linalg.norm(center - opt_pt)
    # curve bends outward: opt_pt + t*u_tan + 0.18*t^2*u_out
    h_curve = np.array([opt_pt + t*u_tan + 0.15*(t**2)*u_out for t in t_vals])
    ax.plot(h_curve[:, 0], h_curve[:, 1], color='#0284C7', lw=2.4)
    ax.text(h_curve[-1, 0] + 0.1, h_curve[-1, 1], r"$h(x_1, x_2) = 0$",
            fontsize=9.2, weight='bold', color='#0284C7')

    # Gradient vectors at opt_pt:
    # nabla f points outward towards c1 (increasing f)
    ax.annotate('', xy=opt_pt + u_out * 1.1, xytext=opt_pt,
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.2))
    ax.text(opt_pt[0] + u_out[0]*1.15 - 0.1, opt_pt[1] + u_out[1]*1.15 + 0.1,
            r"$\nabla f(\mathbf{x}^*)$", fontsize=8.8, weight='bold', color='#DC2626')

    # nabla h points opposite (or collinear with) nabla f
    ax.annotate('', xy=opt_pt - u_out * 0.95, xytext=opt_pt,
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=2.0))
    ax.text(opt_pt[0] - u_out[0]*0.95 + 0.1, opt_pt[1] - u_out[1]*0.95 - 0.15,
            r"$\nabla h(\mathbf{x}^*)$", fontsize=8.8, weight='bold', color='#B45309')

    # Tangent vector epsilon
    ax.annotate('', xy=opt_pt + u_tan * 1.0, xytext=opt_pt,
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.8))
    ax.text(opt_pt[0] + u_tan[0]*1.05, opt_pt[1] + u_tan[1]*1.05 - 0.15,
            r"$\boldsymbol{\epsilon}$", fontsize=9.0, weight='bold', color='#1D4ED8')

    # Hierarchy note pill at top
    box_note = patches.FancyBboxPatch((0.2, 0.2), 6.8, 0.60, boxstyle='round,pad=0.0',
                                     facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.0)
    ax.add_patch(box_note)
    ax.text(3.6, 0.50,
            r"Problema di Minimo: $c_1 > c^* > c_2 > c_3$." +
            r" All'ottimo vincolato $\mathbf{x}^*$, $\nabla f \parallel \nabla h$ con valore $c^* > c_3$",
            fontsize=8.0, ha='center', va='center', color='#1E293B', weight='bold')

    ax.set_xlim(-0.2, 7.0)
    ax.set_ylim(0.0, 5.0)
    ax.axis('off')
    ax.set_title(r"Curve di Livello di $f$ e Vincolo $h=0$ nel Problema di Minimo Vincolato",
                 fontsize=10.0, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")


# ==============================================================================
# FIG 8.5: INEQUALITY CONSTRAINTS AND KKT (FEASIBLE REGION AND GRADIENTS)
# ==============================================================================
def generate_fig_8_5(output_path):
    fig_w, fig_h = 7.8, 5.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Feasible region F: h(x1, x2) >= 0 bounded by curve h = 0
    t = np.linspace(-1.0, 5.5, 200)
    bnd_y = 2.0 + 0.20 * (t - 2.0)**2
    ax.plot(t, bnd_y, color='#0284C7', lw=2.5)

    # Shade feasible region F: h >= 0 (above the curve)
    ax.fill_between(t, bnd_y, 5.2, color='#EFF6FF', alpha=0.65)
    ax.text(0.2, 4.6, r"Regione Ammissibile $\mathcal{F}: h(x_1, x_2) \geq 0$",
            fontsize=9.2, weight='bold', color='#1E40AF')
    ax.text(3.8, 1.7, r"Regione Vietata: $h(x_1, x_2) < 0$",
            fontsize=8.2, color='#94A3B8', style='italic')
    ax.text(4.2, 3.2, r"Frontiera $\partial\mathcal{F}: h(x_1, x_2) = 0$",
            fontsize=8.8, weight='bold', color='#0284C7')

    # Function f to be MAXIMIZED: unconstrained maximum lies in forbidden region
    f_center = np.array([2.0, 0.8])

    # Concentric level curves of f (expanding towards feasible region)
    for r in [0.6, 1.2, 1.8, 2.4]:
        lw = 2.0 if r == 1.2 else 1.0
        col = '#DC2626' if r == 1.2 else '#FCA5A5'
        ls = '-' if r == 1.2 else '--'
        c = patches.Circle(f_center, r, fill=False, edgecolor=col, lw=lw, ls=ls)
        ax.add_patch(c)

    ax.text(f_center[0] - 1.5, f_center[1] + 1.0, r"$f(\mathbf{x}) = c^*$",
            fontsize=8.2, weight='bold', color='#DC2626')

    # Constrained maximum x* occurs at vertex of parabola (2.0, 2.0)
    opt_bnd = np.array([2.0, 2.0])
    ax.plot(opt_bnd[0], opt_bnd[1], 'ko', markersize=7)
    ax.text(opt_bnd[0] - 0.45, opt_bnd[1] + 0.15, r"$\mathbf{x}^*$",
            fontsize=10.0, weight='bold', color='#0F172A')

    # Gradients at opt_bnd:
    u_h = np.array([0.0, 1.0])
    ax.annotate('', xy=opt_bnd + u_h * 1.0, xytext=opt_bnd,
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=2.2))
    ax.text(opt_bnd[0] + 0.12, opt_bnd[1] + 0.85,
            r"$\nabla h(\mathbf{x}^*)$ (verso l'interno, $h > 0$)",
            fontsize=8.5, weight='bold', color='#B45309')

    ax.annotate('', xy=opt_bnd - u_h * 0.85, xytext=opt_bnd,
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.2))
    ax.text(opt_bnd[0] + 0.12, opt_bnd[1] - 0.70,
            r"$\nabla f(\mathbf{x}^*)$ (verso l'esterno, aumento di $f$)",
            fontsize=8.5, weight='bold', color='#DC2626')

    # Inactive scenario point inside region
    in_pt = np.array([1.2, 3.8])
    ax.plot(in_pt[0], in_pt[1], 's', color='#1E40AF', markersize=6)
    ax.text(in_pt[0] + 0.15, in_pt[1] - 0.05,
            r"Caso Inattivo: $h(\mathbf{x}) > 0 \Rightarrow \lambda = 0$, $\nabla f = \mathbf{0}$",
            fontsize=8.0, color='#1E40AF')

    # Summary box
    box_kkt = patches.FancyBboxPatch((0.2, 0.10), 7.2, 0.55, boxstyle='round,pad=0.0',
                                    facecolor='#FEF3C7', edgecolor='#F59E0B', lw=1.0)
    ax.add_patch(box_kkt)
    ax.text(3.8, 0.38,
            r"Condizioni KKT (Massimizzazione con $h \geq 0$):" + "\n" +
            r"Vincolo attivo su frontiera: $\nabla f = -\lambda \nabla h$ con $\lambda > 0$, $\lambda h(\mathbf{x}^*) = 0$",
            fontsize=8.0, ha='center', va='center', color='#92400E', weight='bold')

    ax.set_xlim(-0.2, 5.6)
    ax.set_ylim(0.0, 5.2)
    ax.axis('off')
    ax.set_title(r"Metodo dei Moltiplicatori di Lagrange con Vincoli di Disuguaglianza $h(\mathbf{x}) \geq 0$",
                 fontsize=10.0, weight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_7_2('Anno 1/Machine Learning/immagini/fig_7_2_sigmoide_lda_superficie.svg')
    generate_fig_8_2('Anno 1/Machine Learning/immagini/fig_8_2_componente_gradiente_non_nullo.svg')
    generate_fig_8_3('Anno 1/Machine Learning/immagini/fig_8_3_parallelismo_gradienti_punto_estremale.svg')
    generate_fig_8_4('Anno 1/Machine Learning/immagini/fig_8_4_curve_di_livello_minimo_vincolato.svg')
    generate_fig_8_5('Anno 1/Machine Learning/immagini/fig_8_5_vincoli_disuguaglianza_kkt.svg')
