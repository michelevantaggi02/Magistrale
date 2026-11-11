import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_figure(output_path):
    fig_w, fig_h = 16, 8.4
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8.4)
    ax.axis('off')

    # Title & Subtitle
    ax.text(8.0, 7.95, "Tassonomia dei Tre Approcci Fondamentali alla Classificazione",
            fontsize=16, weight='bold', ha='center', va='center', color='#0F172A')
    ax.text(8.0, 7.55, "Inquadramento concettuale dei paradigmi di inferenza supervisionata (ML_Notes, Sez. 5.4)",
            fontsize=10.5, ha='center', va='center', color='#475569')

    # 3 Columns
    card_w = 4.6
    card_h = 5.8
    y_card = 1.30
    xs = [0.8, 5.7, 10.6]

    configs = [
        {
            "title": "1. MODELLI GENERATIVI",
            "subtitle": r"Modellazione congiunta $p(\mathbf{x}, \mathcal{C}_k)$",
            "theme_border": "#2563EB",
            "theme_header": "#DBEAFE",
            "theme_text": "#1E3A8A",
            "pill_bg": "#EFF6FF",
            "formula": r"$p(\mathcal{C}_k|\mathbf{x}) = \frac{p(\mathbf{x}|\mathcal{C}_k)P(\mathcal{C}_k)}{p(\mathbf{x})}$",
            "formula_desc": r"Stima $p(\mathbf{x}|\mathcal{C}_k)$ e $P(\mathcal{C}_k)$ $\to$ Bayes",
            "models": [
                "• Gaussian LDA & QDA",
                "• Naive Bayes (Bernoulliano)",
                "• Modelli a Mistura di Gaussiane (GMM)"
            ],
            "traits": [
                ("Densità p(x)", "Modellata (outlier detection)"),
                ("Incertezza", r"Probabilistica $p(\mathcal{C}_k|\mathbf{x})$"),
                ("Soglia", "Regolabile a posteriori"),
                ("Sintesi dati", "Campioni sintetici generabili")
            ]
        },
        {
            "title": "2. DISCRIMINATIVI PROBABILISTICI",
            "subtitle": r"Modellazione a posteriori $p(\mathcal{C}_k \mid \mathbf{x})$",
            "theme_border": "#059669",
            "theme_header": "#D1FAE5",
            "theme_text": "#065F46",
            "pill_bg": "#ECFDF5",
            "formula": r"$p(\mathcal{C}_1|\mathbf{x}) = \sigma(\mathbf{w}^T\boldsymbol{\phi}(\mathbf{x})) \quad\text{o}\quad \frac{k_k}{K}$",
            "formula_desc": r"Modella $p(\mathcal{C}_k|\mathbf{x})$ senza stimare $p(\mathbf{x})$",
            "models": [
                "• Regressione Logistica",
                "• K-Nearest Neighbors (K-NN)",
                "• Softmax Multi-classe & Reti Neurali"
            ],
            "traits": [
                ("Densità p(x)", "Non modellata (basso costo)"),
                ("Incertezza", r"Probabilistica $p(\mathcal{C}_k|\mathbf{x})$"),
                ("Soglia", "Regolabile a posteriori"),
                ("Sintesi dati", "Non generabili dal modello")
            ]
        },
        {
            "title": "3. FUNZIONI DISCRIMINANTI",
            "subtitle": r"Mappatura diretta $\mathbf{x} \mapsto \hat{t} \in \{-1, +1\}$",
            "theme_border": "#D97706",
            "theme_header": "#FEF3C7",
            "theme_text": "#92400E",
            "pill_bg": "#FFFBEB",
            "formula": r"$\hat{t} = f(\mathbf{x}) = \mathrm{sign}\left(\mathbf{w}^T\boldsymbol{\phi}(\mathbf{x}) + b\right)$",
            "formula_desc": r"Superficie di decisione geometrica",
            "models": [
                "• Percettrone di Rosenblatt",
                "• Support Vector Machines (SVM)",
                "• Kernel SVM (frontiere non lineari)"
            ],
            "traits": [
                ("Densità p(x)", "Non modellata (massima efficienza)"),
                ("Incertezza", "Assente (decisione deterministica)"),
                ("Soglia", "Fissa (richiede riaddestramento)"),
                ("Sintesi dati", "Non generabili dal modello")
            ]
        }
    ]

    for x, cfg in zip(xs, configs):
        # 1. Outer Card Box
        rect = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle='round,pad=0.0',
                                      facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5)
        ax.add_patch(rect)
        
        # 2. Header Box
        h_h = 0.95
        h_rect = patches.FancyBboxPatch((x, y_card + card_h - h_h), card_w, h_h, boxstyle='round,pad=0.0',
                                        facecolor=cfg["theme_header"], edgecolor=cfg["theme_border"], linewidth=1.8)
        ax.add_patch(h_rect)
        ax.text(x + card_w/2, y_card + card_h - 0.32, cfg["title"],
                fontsize=11.5, weight='bold', ha='center', va='center', color=cfg["theme_text"])
        ax.text(x + card_w/2, y_card + card_h - 0.68, cfg["subtitle"],
                fontsize=8.8, ha='center', va='center', color='#334155')

        # 3. Block 1: Formulazione Matematica
        y_b1 = y_card + card_h - 1.25
        ax.text(x + 0.35, y_b1, "FORMULAZIONE MATEMATICA", fontsize=8.2, weight='bold', color='#64748B')
        ax.text(x + 0.35, y_b1 - 0.30, cfg["formula_desc"], fontsize=8.4, color='#1E293B')
        
        # Formula box
        f_box = patches.FancyBboxPatch((x + 0.3, y_b1 - 1.10), card_w - 0.6, 0.65, boxstyle='round,pad=0.0',
                                      facecolor=cfg["pill_bg"], edgecolor=cfg["theme_border"], linewidth=1.0)
        ax.add_patch(f_box)
        ax.text(x + card_w/2, y_b1 - 0.77, cfg["formula"], fontsize=9.2, ha='center', va='center', color=cfg["theme_text"])

        # 4. Block 2: Modelli Tipici del Corso
        y_b2 = y_b1 - 1.48
        ax.text(x + 0.35, y_b2, "MODELLI TIPICI DEL CORSO", fontsize=8.2, weight='bold', color='#64748B')
        for i, m in enumerate(cfg["models"]):
            ax.text(x + 0.45, y_b2 - 0.32 - i*0.28, m, fontsize=8.6, weight='bold', color='#0F172A')

        # 5. Block 3: Proprietà e Caratteristiche
        y_b3 = y_b2 - 1.48
        ax.text(x + 0.35, y_b3, "PROPRIETÀ E CARATTERISTICHE", fontsize=8.2, weight='bold', color='#64748B')
        for i, (label, val) in enumerate(cfg["traits"]):
            y_line = y_b3 - 0.30 - i*0.28
            ax.text(x + 0.45, y_line, f"• {label}:", fontsize=8.2, weight='bold', color='#1E293B')
            ax.text(x + 1.75, y_line, val, fontsize=8.1, color='#475569')

    # Bottom Banner
    bot_y = 0.30
    bot_h = 0.75
    banner = patches.FancyBboxPatch((0.8, bot_y), 14.4, bot_h, boxstyle='round,pad=0.0',
                                    facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.2)
    ax.add_patch(banner)
    
    line1 = r"$\mathbf{Regola\;Metodologica\;d'Esame:}$ se l'obiettivo è la sola decisione secca, la funzione discriminante è la più efficiente;"
    line2 = r"se occorre calibrare l'incertezza o gestire costi asimmetrici, è indispensabile un approccio probabilistico."
    ax.text(8.0, bot_y + 0.48, line1, fontsize=8.6, ha='center', va='center', color='#0F172A')
    ax.text(8.0, bot_y + 0.22, line2, fontsize=8.6, ha='center', va='center', color='#334155')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path} successfully.")

if __name__ == '__main__':
    generate_figure('scratch/test_schema.png')
