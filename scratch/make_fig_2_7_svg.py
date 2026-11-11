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
    fig_w, fig_h = 13.6, 5.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    # Title & Subtitle
    ax.text(6.8, 4.85, "Protocollo di K-Fold Cross-Validation e Valutazione Finale",
            fontsize=13.5, weight='bold', ha='center', va='center', color='#0F172A')
    ax.text(6.8, 4.52, "Partizione in fold per la Model Selection e collaudo finale imparziale su Test Set congelato",
            fontsize=9.2, ha='center', va='center', color='#475569')

    # 1. Top Section: Dataset Completo Split (Train+Val vs Test)
    top_y = 3.65
    ax.text(1.0, top_y + 0.40, "FASE 1: SPLIT INIZIALE DEL DATASET", fontsize=8.2, weight='bold', color='#64748B')
    
    # Train+Val Bar (80%)
    tv_w = 7.0
    tv_box = patches.FancyBboxPatch((1.0, top_y - 0.25), tv_w, 0.50, boxstyle='round,pad=0.0',
                                    facecolor='#EFF6FF', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(tv_box)
    ax.text(1.0 + tv_w/2, top_y, r"$\mathcal{D}_{\mathrm{train+val}}$ (80% del Dataset: usato per Model Selection via K-Fold CV)",
            fontsize=8.5, weight='bold', ha='center', va='center', color='#1E3A8A')

    # Test Bar (20%)
    test_x = 1.0 + tv_w + 0.3
    test_w = 2.4
    test_box = patches.FancyBboxPatch((test_x, top_y - 0.25), test_w, 0.50, boxstyle='round,pad=0.0',
                                      facecolor='#F1F5F9', edgecolor='#64748B', linewidth=1.5, linestyle='--')
    ax.add_patch(test_box)
    ax.text(test_x + test_w/2, top_y, r"$\mathcal{D}_{\mathrm{test}}$ (20% Congelato)",
            fontsize=8.5, weight='bold', ha='center', va='center', color='#334155')

    # 2. Middle Section: K-Fold Iterations (K=5)
    ax.text(1.0, 3.05, "FASE 2: MODEL SELECTION SUI K FOLD (K = 5)", fontsize=8.2, weight='bold', color='#64748B')
    
    k_folds = 5
    fold_w = tv_w / k_folds # 1.4 each
    fold_gap = 0.08
    effective_w = fold_w - fold_gap
    row_h = 0.32
    y_start = 2.60
    y_step = 0.42

    for r in range(k_folds):
        y_r = y_start - r * y_step
        # Iteration Label
        ax.text(0.90, y_r + row_h/2, f"Iter {r+1}:", fontsize=8.2, weight='bold', ha='right', va='center', color='#334155')
        
        # Folds
        for f in range(k_folds):
            f_x = 1.0 + f * fold_w
            if f == r:
                # Validation fold
                fb = patches.FancyBboxPatch((f_x, y_r), effective_w, row_h, boxstyle='round,pad=0.0',
                                            facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.2)
                ax.add_patch(fb)
                ax.text(f_x + effective_w/2, y_r + row_h/2, "Val Fold", fontsize=7.8, weight='bold',
                        ha='center', va='center', color='#92400E')
            else:
                # Training fold
                fb = patches.FancyBboxPatch((f_x, y_r), effective_w, row_h, boxstyle='round,pad=0.0',
                                            facecolor='#DBEAFE', edgecolor='#3B82F6', linewidth=1.0)
                ax.add_patch(fb)
                ax.text(f_x + effective_w/2, y_r + row_h/2, "Train", fontsize=7.8,
                        ha='center', va='center', color='#1E40AF')
        
        # Error formula
        err_x = 1.0 + tv_w + 0.30
        ax.text(err_x, y_r + row_h/2, rf"$\to\quad E_{{\mathrm{{val}}, {r+1}}}$ (su Val Fold)",
                fontsize=8.0, va='center', color='#475569')

    # Side Summary for Mean Error
    mean_x = 1.0 + tv_w + 2.7
    mean_box = patches.FancyBboxPatch((mean_x, y_start - 4.0*y_step), 2.5, 2.0, boxstyle='round,pad=0.0',
                                     facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.2)
    ax.add_patch(mean_box)
    ax.text(mean_x + 1.25, y_start - 0.9*y_step, r"$\mathbf{Errore\;Medio:}$",
            fontsize=8.5, weight='bold', ha='center', va='center', color='#1E3A8A')
    ax.text(mean_x + 1.25, y_start - 1.9*y_step, r"$E_{\mathrm{val}} = \frac{1}{K}\sum_{k=1}^K E_{\mathrm{val}, k}$",
            fontsize=8.8, ha='center', va='center', color='#0F172A')
    ax.text(mean_x + 1.25, y_start - 3.1*y_step, r"$\Downarrow$" + "\n" + r"Scelta $\lambda^*, M^*$",
            fontsize=8.2, weight='bold', ha='center', va='center', color='#059669')

    # 3. Bottom Banner: Model Assessment
    bot_y = 0.20
    bot_h = 0.45
    banner = patches.FancyBboxPatch((1.0, bot_y), 11.6, bot_h, boxstyle='round,pad=0.0',
                                    facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(banner)
    ax.text(6.8, bot_y + bot_h/2,
            r"$\mathbf{FASE\;3\;(Model\;Assessment):}$ Scelto l'iperparametro ottimo, si riaddestra il modello finale su tutto " +
            r"$\mathcal{D}_{\mathrm{train+val}}$ e si valuta una sola volta su $\mathcal{D}_{\mathrm{test}}$.",
            fontsize=8.2, ha='center', va='center', color='#0F172A')

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path} successfully.")

if __name__ == '__main__':
    generate_svg('Anno 1/Machine Learning/immagini/fig_2_7_cross_validation_schema.svg')
