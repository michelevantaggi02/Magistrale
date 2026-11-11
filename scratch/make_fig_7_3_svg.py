import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_fig_7_3(output_path):
    fig_w, fig_h = 12.6, 4.4
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 4.4)
    ax.axis('off')

    # Title
    ax.text(6.3, 4.05, "Modello Bag of Words (BoW): Vettorizzazione Documento-Termine",
            fontsize=12.5, weight='bold', ha='center', va='center', color='#0F172A')

    # 1. Left Box: Testi Grezzi e Preprocessing
    box_doc = patches.FancyBboxPatch((0.6, 0.95), 3.4, 2.70, boxstyle='round,pad=0.0',
                                    facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.2)
    ax.add_patch(box_doc)
    ax.text(2.3, 3.35, "1. CORPUS TESTUALE GREZZO", fontsize=8.2, weight='bold', ha='center', color='#475569')

    # Doc 1
    d1 = patches.FancyBboxPatch((0.8, 2.50), 3.0, 0.60, boxstyle='round,pad=0.0',
                                facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0)
    ax.add_patch(d1)
    ax.text(0.95, 2.85, r"$\mathbf{d}_1:$ \"Il gatto salta sul divano\"", fontsize=7.8, color='#1E293B')
    ax.text(0.95, 2.65, "Lemmi: {gatto, salta, divano}", fontsize=7.4, color='#3B82F6', weight='bold')

    # Doc 2
    d2 = patches.FancyBboxPatch((0.8, 1.75), 3.0, 0.60, boxstyle='round,pad=0.0',
                                facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.0)
    ax.add_patch(d2)
    ax.text(0.95, 2.10, r"$\mathbf{d}_2:$ \"Il cane insegue il gatto\"", fontsize=7.8, color='#1E293B')
    ax.text(0.95, 1.90, "Lemmi: {cane, insegue, gatto}", fontsize=7.4, color='#3B82F6', weight='bold')

    # Doc 3
    d3 = patches.FancyBboxPatch((0.8, 1.05), 3.0, 0.55, boxstyle='round,pad=0.0',
                                facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=1.0)
    ax.add_patch(d3)
    ax.text(0.95, 1.35, "Filtro Stop-words:", fontsize=7.4, weight='bold', color='#64748B')
    ax.text(0.95, 1.15, "Rimossi: \"il\", \"sul\", \"e\", \"di\"...", fontsize=7.2, color='#94A3B8')

    # Arrow 1: To Vocabulary
    ax.annotate('', xy=(4.5, 2.30), xytext=(4.1, 2.30),
                arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.8))
    ax.text(4.3, 2.50, "Estrai\nLemmi", fontsize=7.2, ha='center', va='bottom', color='#2563EB', weight='bold')

    # 2. Middle Box: Vocabolario V
    box_voc = patches.FancyBboxPatch((4.7, 1.10), 2.5, 2.40, boxstyle='round,pad=0.0',
                                     facecolor='#FEF3C7', edgecolor='#D97706', lw=1.2)
    ax.add_patch(box_voc)
    ax.text(5.95, 3.25, "2. VOCABOLARIO " + r"$\mathcal{V}$", fontsize=8.2, weight='bold', ha='center', color='#92400E')
    ax.text(5.95, 2.95, r"Dimensione $D = 4$", fontsize=7.6, ha='center', color='#B45309')

    words = [r"$w_0:$ cane", r"$w_1:$ divano", r"$w_2:$ gatto", r"$w_3:$ salta"]
    for i, w in enumerate(words):
        y_w = 2.55 - i * 0.38
        wb = patches.FancyBboxPatch((4.9, y_w - 0.05), 2.1, 0.30, boxstyle='round,pad=0.0',
                                    facecolor='#FFFFFF', edgecolor='#FCD34D', lw=0.8)
        ax.add_patch(wb)
        ax.text(5.95, y_w + 0.10, w, fontsize=7.6, ha='center', va='center', color='#78350F')

    # Arrow 2: To Matrix
    ax.annotate('', xy=(7.7, 2.30), xytext=(7.3, 2.30),
                arrowprops=dict(arrowstyle='->', color='#059669', lw=1.8))
    ax.text(7.5, 2.50, "Codifica\n1-of-D", fontsize=7.2, ha='center', va='bottom', color='#059669', weight='bold')

    # 3. Right Box: Document-Term Matrix
    box_mat = patches.FancyBboxPatch((7.9, 0.95), 4.2, 2.70, boxstyle='round,pad=0.0',
                                     facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.2)
    ax.add_patch(box_mat)
    ax.text(10.0, 3.35, "3. MATRICE DOCUMENTO-TERMINE " + r"$\mathbf{X} \in \{0, 1\}^{N \times D}$",
            fontsize=8.0, weight='bold', ha='center', color='#065F46')

    # Matrix Table Headers
    cols = ["cane", "divano", "gatto", "salta"]
    col_x = [8.8, 9.5, 10.2, 10.9]
    for cx, cname in zip(col_x, cols):
        ax.text(cx, 2.95, cname, fontsize=7.4, weight='bold', ha='center', color='#334155')

    # Row 1 (Doc 1)
    ax.text(8.2, 2.45, r"$\mathbf{x}^{(1)}:$", fontsize=7.8, weight='bold', color='#1E293B')
    row1 = [0, 1, 1, 1]
    for cx, val in zip(col_x, row1):
        bg = '#D1FAE5' if val == 1 else '#F1F5F9'
        cell = patches.Rectangle((cx - 0.28, 2.25), 0.56, 0.38, facecolor=bg, edgecolor='#94A3B8', lw=0.8)
        ax.add_patch(cell)
        ax.text(cx, 2.44, str(val), fontsize=8.2, weight='bold' if val == 1 else 'normal',
                ha='center', va='center', color='#065F46' if val == 1 else '#94A3B8')

    # Row 2 (Doc 2)
    ax.text(8.2, 1.85, r"$\mathbf{x}^{(2)}:$", fontsize=7.8, weight='bold', color='#1E293B')
    row2 = [1, 0, 1, 0]
    for cx, val in zip(col_x, row2):
        bg = '#D1FAE5' if val == 1 else '#F1F5F9'
        cell = patches.Rectangle((cx - 0.28, 1.65), 0.56, 0.38, facecolor=bg, edgecolor='#94A3B8', lw=0.8)
        ax.add_patch(cell)
        ax.text(cx, 1.84, str(val), fontsize=8.2, weight='bold' if val == 1 else 'normal',
                ha='center', va='center', color='#065F46' if val == 1 else '#94A3B8')

    # Summary note
    ax.text(10.0, 1.25, r"Vettore numerico a dimensione fissa $\mathbf{x} \in \mathbb{R}^D$" + "\n" + r"$\to$ Classificabile con Naive Bayes o Logistic Reg",
            fontsize=7.4, ha='center', va='center', color='#334155')

    # Bottom Banner
    bot_box = patches.FancyBboxPatch((0.6, 0.20), 11.5, 0.55, boxstyle='round,pad=0.0',
                                    facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.0)
    ax.add_patch(bot_box)
    ax.text(6.35, 0.47,
            r"$\mathbf{Takeaway\;d'Esame:}$ Il modello BoW scarta l'ordine sintattico preservando solo la presenza/frequenza dei lemmi;" + "\n" +
            r"l'espansione a TF-IDF penalizza le parole comuni introducendo la frequenza inversa nei documenti.",
            fontsize=7.6, ha='center', va='center', color='#1E3A8A')

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_fig_7_3('Anno 1/Machine Learning/immagini/fig_7_3_bag_of_words_vocabolario.svg')
