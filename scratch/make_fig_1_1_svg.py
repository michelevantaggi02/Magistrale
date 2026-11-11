import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg

def generate_svg(output_path):
    fig_w, fig_h = 13.0, 3.6
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 3.6)
    ax.axis('off')

    # Root Node: Tutte le Variabili
    root_x, root_y, root_w, root_h = 0.5, 1.45, 2.2, 0.70
    root_box = patches.FancyBboxPatch((root_x, root_y), root_w, root_h, boxstyle='round,pad=0.0',
                                     facecolor='#F1F5F9', edgecolor='#475569', linewidth=1.5)
    ax.add_patch(root_box)
    ax.text(root_x + root_w/2, root_y + root_h/2, "Tutte le Variabili\n(Feature e Target)",
            fontsize=9.5, weight='bold', ha='center', va='center', color='#0F172A')

    # Main Branches: Numeriche (Top) and Categoriche (Bottom)
    # Connecting arrows from root to branches
    # Branch 1: Numeriche
    b1_x, b1_y, b1_w, b1_h = 3.5, 2.05, 2.5, 0.65
    b1_box = patches.FancyBboxPatch((b1_x, b1_y), b1_w, b1_h, boxstyle='round,pad=0.0',
                                    facecolor='#DBEAFE', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(b1_box)
    ax.text(b1_x + b1_w/2, b1_y + b1_h/2, "1. Variabili Numeriche\n(Dati Quantitativi)",
            fontsize=9.0, weight='bold', ha='center', va='center', color='#1E3A8A')

    # Branch 2: Categoriche
    b2_x, b2_y, b2_w, b2_h = 3.5, 0.90, 2.5, 0.65
    b2_box = patches.FancyBboxPatch((b2_x, b2_y), b2_w, b2_h, boxstyle='round,pad=0.0',
                                    facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    ax.add_patch(b2_box)
    ax.text(b2_x + b2_w/2, b2_y + b2_h/2, "2. Variabili Categoriche\n(Dati Qualitativi)",
            fontsize=9.0, weight='bold', ha='center', va='center', color='#92400E')

    # Arrows from Root to Branches
    ax.annotate('', xy=(b1_x, b1_y + b1_h/2), xytext=(root_x + root_w, root_y + root_h*0.75),
                arrowprops=dict(arrowstyle='->', color='#64748B', lw=1.5, connectionstyle='angle,angleA=0,angleB=90,rad=5'))
    ax.annotate('', xy=(b2_x, b2_y + b2_h/2), xytext=(root_x + root_w, root_y + root_h*0.25),
                arrowprops=dict(arrowstyle='->', color='#64748B', lw=1.5, connectionstyle='angle,angleA=0,angleB=-90,rad=5'))

    # Sub-leaves for Numeriche: Continue and Discrete
    # Leaf 1.1: Continue
    l11_x, l11_y, l11_w, l11_h = 6.8, 2.75, 5.7, 0.65
    l11_box = patches.FancyBboxPatch((l11_x, l11_y), l11_w, l11_h, boxstyle='round,pad=0.0',
                                     facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(l11_box)
    ax.text(l11_x + 0.25, l11_y + 0.43, r"• $\mathbf{Continue:}$ $x \in \mathbb{R}$ su scala continua",
            fontsize=8.8, color='#1E293B')
    ax.text(l11_x + 0.25, l11_y + 0.18, "   Es: temperatura, peso, pressione, coordinate fisiche",
            fontsize=8.2, color='#475569')

    # Leaf 1.2: Discrete
    l12_x, l12_y, l12_w, l12_h = 6.8, 1.95, 5.7, 0.65
    l12_box = patches.FancyBboxPatch((l12_x, l12_y), l12_w, l12_h, boxstyle='round,pad=0.0',
                                     facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(l12_box)
    ax.text(l12_x + 0.25, l12_y + 0.43, r"• $\mathbf{Discrete:}$ $x \in \mathcal{S} \subset \mathbb{Z}$ o $\mathbb{N}$ (conteggi finiti/numerabili)",
            fontsize=8.8, color='#1E293B')
    ax.text(l12_x + 0.25, l12_y + 0.18, "   Es: numero di stanze, accessi web, conteggio di eventi",
            fontsize=8.2, color='#475569')

    # Arrows to Leaves 1.1 and 1.2
    ax.annotate('', xy=(l11_x, l11_y + l11_h/2), xytext=(b1_x + b1_w, b1_y + b1_h*0.75),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.2, connectionstyle='angle,angleA=0,angleB=90,rad=4'))
    ax.annotate('', xy=(l12_x, l12_y + l12_h/2), xytext=(b1_x + b1_w, b1_y + b1_h*0.25),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.2, connectionstyle='angle,angleA=0,angleB=-90,rad=4'))

    # Sub-leaves for Categoriche: Nominali and Ordinali
    # Leaf 2.1: Nominali
    l21_x, l21_y, l21_w, l21_h = 6.8, 1.05, 5.7, 0.65
    l21_box = patches.FancyBboxPatch((l21_x, l21_y), l21_w, l21_h, boxstyle='round,pad=0.0',
                                     facecolor='#FFFBEB', edgecolor='#FCD34D', linewidth=1.2)
    ax.add_patch(l21_box)
    ax.text(l21_x + 0.25, l21_y + 0.43, r"• $\mathbf{Nominali:}$ categorie mutue prive di ordinamento matematico",
            fontsize=8.8, color='#1E293B')
    ax.text(l21_x + 0.25, l21_y + 0.18, "   Es: professione, colore, genere, tag semantico (richiede one-hot encoding)",
            fontsize=8.2, color='#475569')

    # Leaf 2.2: Ordinali
    l22_x, l22_y, l22_w, l22_h = 6.8, 0.25, 5.7, 0.65
    l22_box = patches.FancyBboxPatch((l22_x, l22_y), l22_w, l22_h, boxstyle='round,pad=0.0',
                                     facecolor='#FFFBEB', edgecolor='#FCD34D', linewidth=1.2)
    ax.add_patch(l22_box)
    ax.text(l22_x + 0.25, l22_y + 0.43, r"• $\mathbf{Ordinali:}$ categorie qualitative dotate di relazione d'ordine",
            fontsize=8.8, color='#1E293B')
    ax.text(l22_x + 0.25, l22_y + 0.18, "   Es: livello rischio (basso < medio < alto), grado di soddisfazione",
            fontsize=8.2, color='#475569')

    # Arrows to Leaves 2.1 and 2.2
    ax.annotate('', xy=(l21_x, l21_y + l21_h/2), xytext=(b2_x + b2_w, b2_y + b2_h*0.75),
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=1.2, connectionstyle='angle,angleA=0,angleB=90,rad=4'))
    ax.annotate('', xy=(l22_x, l22_y + l22_h/2), xytext=(b2_x + b2_w, b2_y + b2_h*0.25),
                arrowprops=dict(arrowstyle='->', color='#D97706', lw=1.2, connectionstyle='angle,angleA=0,angleB=-90,rad=4'))

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path} successfully.")

if __name__ == '__main__':
    generate_svg('Anno 1/Machine Learning/immagini/fig_1_1_tipi_di_variabili.svg')
