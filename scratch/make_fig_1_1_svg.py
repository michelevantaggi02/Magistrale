import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_svg(output_path, arrow_style='-|>'):
    fig_w, fig_h = 13.0, 3.6
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 3.6)
    ax.axis('off')

    # Root Node: Tutte le Variabili (Perfettamente centrato a y=1.825)
    root_x, root_y, root_w, root_h = 0.5, 1.475, 2.2, 0.70
    root_box = patches.FancyBboxPatch((root_x, root_y), root_w, root_h, boxstyle='round,pad=0.0,rounding_size=0.08',
                                     facecolor='#F1F5F9', edgecolor='#475569', linewidth=1.5)
    ax.add_patch(root_box)
    ax.text(root_x + root_w/2, root_y + root_h/2, "Tutte le Variabili\n(Feature e Target)",
            fontsize=9.5, weight='bold', ha='center', va='center', color='#0F172A')

    # Main Branches: Numeriche (Top) e Categoriche (Bottom)
    # Branch 1: Numeriche (Centrato verticalmente rispetto alle sue 2 foglie a y=2.675)
    b1_x, b1_y, b1_w, b1_h = 3.5, 2.35, 2.5, 0.65
    b1_box = patches.FancyBboxPatch((b1_x, b1_y), b1_w, b1_h, boxstyle='round,pad=0.0,rounding_size=0.08',
                                    facecolor='#DBEAFE', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(b1_box)
    ax.text(b1_x + b1_w/2, b1_y + b1_h/2, "1. Variabili Numeriche\n(Dati Quantitativi)",
            fontsize=9.0, weight='bold', ha='center', va='center', color='#1E3A8A')

    # Branch 2: Categoriche (Centrato verticalmente rispetto alle sue 2 foglie a y=0.975)
    b2_x, b2_y, b2_w, b2_h = 3.5, 0.65, 2.5, 0.65
    b2_box = patches.FancyBboxPatch((b2_x, b2_y), b2_w, b2_h, boxstyle='round,pad=0.0,rounding_size=0.08',
                                    facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    ax.add_patch(b2_box)
    ax.text(b2_x + b2_w/2, b2_y + b2_h/2, "2. Variabili Categoriche\n(Dati Qualitativi)",
            fontsize=9.0, weight='bold', ha='center', va='center', color='#92400E')

    # Sub-leaves for Numeriche: Continue and Discrete
    # Leaf 1.1: Continue (center y = 3.075)
    l11_x, l11_y, l11_w, l11_h = 6.8, 2.75, 5.7, 0.65
    l11_box = patches.FancyBboxPatch((l11_x, l11_y), l11_w, l11_h, boxstyle='round,pad=0.0,rounding_size=0.06',
                                     facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(l11_box)
    ax.text(l11_x + 0.25, l11_y + 0.43, r"• $\mathbf{Continue:}$ $x \in \mathbb{R}$ su scala continua",
            fontsize=8.8, color='#1E293B')
    ax.text(l11_x + 0.25, l11_y + 0.18, "   Es: temperatura, peso, pressione, coordinate fisiche",
            fontsize=8.2, color='#475569')

    # Leaf 1.2: Discrete (center y = 2.275)
    l12_x, l12_y, l12_w, l12_h = 6.8, 1.95, 5.7, 0.65
    l12_box = patches.FancyBboxPatch((l12_x, l12_y), l12_w, l12_h, boxstyle='round,pad=0.0,rounding_size=0.06',
                                     facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(l12_box)
    ax.text(l12_x + 0.25, l12_y + 0.43, r"• $\mathbf{Discrete:}$ $x \in \mathcal{S} \, \subset \, \mathbb{Z}$ o $\mathbb{N}$ (conteggi finiti/numerabili)",
            fontsize=8.8, color='#1E293B')
    ax.text(l12_x + 0.25, l12_y + 0.18, "   Es: numero di stanze, accessi web, conteggio di eventi",
            fontsize=8.2, color='#475569')

    # Sub-leaves for Categoriche: Nominali and Ordinali
    # Leaf 2.1: Nominali (center y = 1.375)
    l21_x, l21_y, l21_w, l21_h = 6.8, 1.05, 5.7, 0.65
    l21_box = patches.FancyBboxPatch((l21_x, l21_y), l21_w, l21_h, boxstyle='round,pad=0.0,rounding_size=0.06',
                                     facecolor='#FFFBEB', edgecolor='#FCD34D', linewidth=1.2)
    ax.add_patch(l21_box)
    ax.text(l21_x + 0.25, l21_y + 0.43, r"• $\mathbf{Nominali:}$ categorie mutue prive di ordinamento matematico",
            fontsize=8.8, color='#1E293B')
    ax.text(l21_x + 0.25, l21_y + 0.18, "   Es: professione, colore, genere, tag semantico (richiede one-hot encoding)",
            fontsize=8.2, color='#475569')

    # Leaf 2.2: Ordinali (center y = 0.575)
    l22_x, l22_y, l22_w, l22_h = 6.8, 0.25, 5.7, 0.65
    l22_box = patches.FancyBboxPatch((l22_x, l22_y), l22_w, l22_h, boxstyle='round,pad=0.0,rounding_size=0.06',
                                     facecolor='#FFFBEB', edgecolor='#FCD34D', linewidth=1.2)
    ax.add_patch(l22_box)
    ax.text(l22_x + 0.25, l22_y + 0.43, r"• $\mathbf{Ordinali:}$ categorie qualitative dotate di relazione d'ordine",
            fontsize=8.8, color='#1E293B')
    ax.text(l22_x + 0.25, l22_y + 0.18, "   Es: livello rischio (basso < medio < alto), grado di soddisfazione",
            fontsize=8.2, color='#475569')

    # Funzione per disegnare diramazioni ortogonali a T perfettamente raccordate
    def draw_orthogonal_fork(p_pt, c_pts, color, lw):
        x_p, y_p = p_pt
        x_c = c_pts[0][0]
        x_mid = (x_p + x_c) / 2
        # Tronco orizzontale in uscita dal nodo genitore
        ax.plot([x_p, x_mid], [y_p, y_p], color=color, lw=lw, solid_capstyle='round')
        # Linea verticale di diramazione (tra i rami superiore e inferiore)
        min_y = min(c[1] for c in c_pts)
        max_y = max(c[1] for c in c_pts)
        ax.plot([x_mid, x_mid], [min_y, max_y], color=color, lw=lw, solid_capstyle='round')
        # Frecce orizzontali perfettamente orientate verso i nodi figli
        for c in c_pts:
            ax.annotate('', xy=c, xytext=(x_mid, c[1]),
                        arrowprops=dict(arrowstyle=arrow_style, color=color, lw=lw,
                                        shrinkA=0, shrinkB=1, mutation_scale=12))

    # Collegamento da Root a Numeriche e Categoriche
    draw_orthogonal_fork((root_x + root_w, root_y + root_h/2),
                         [(b1_x, b1_y + b1_h/2), (b2_x, b2_y + b2_h/2)],
                         color='#64748B', lw=1.5)

    # Collegamento da Numeriche a Continue e Discrete
    draw_orthogonal_fork((b1_x + b1_w, b1_y + b1_h/2),
                         [(l11_x, l11_y + l11_h/2), (l12_x, l12_y + l12_h/2)],
                         color='#2563EB', lw=1.3)

    # Collegamento da Categoriche a Nominali e Ordinali
    draw_orthogonal_fork((b2_x + b2_w, b2_y + b2_h/2),
                         [(l21_x, l21_y + l21_h/2), (l22_x, l22_y + l22_h/2)],
                         color='#D97706', lw=1.3)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path} successfully.")

if __name__ == '__main__':
    generate_svg('Anno 1/Machine Learning/immagini/fig_1_1_tipi_di_variabili.svg')
