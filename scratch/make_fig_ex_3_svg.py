import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'path'
matplotlib.rcParams['font.sans-serif'] = 'DejaVu Sans'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def generate_svg(output_path):
    fig_w, fig_h = 13.0, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 5.0)
    ax.axis('off')

    # Titolo Superiore
    ax.text(6.5, 4.68, "Tassonomia dei Punti nei Modelli di Regressione Lineare",
            fontsize=12.5, weight='bold', ha='center', va='center', color='#0F172A')

    # Definizione delle 4 Schede (Cards)
    card_w = 2.75
    card_h = 3.45
    card_y = 0.95
    xs = [0.50, 3.58, 6.66, 9.74]

    configs = [
        {
            'x': xs[0],
            'title': "1. Punto Regolare",
            'subtitle': "Inlier Tipico",
            'color_bg': "#F0FDF4",
            'color_border': "#16A34A",
            'color_title': "#166534",
            'color_badge': "#DCFCE7",
            'criteri': [
                r"$\bullet\ \mathrm{Leva:}\ h_{ii} \leq 3D/N$",
                r"$\bullet\ \mathrm{Residuo:}\ |d_{\mathrm{ESR}}| \leq 3$"
            ],
            'proprieta': [
                r"$\bullet$ Feature $\mathbf{x}$ vicine alla media",
                r"$\bullet$ Target $t$ coerente con la retta",
                r"$\bullet$ Stima OLS ideale e stabile"
            ]
        },
        {
            'x': xs[1],
            'title': "2. Outlier Semplice",
            'subtitle': "Discrepanza sul Target (Y-Outlier)",
            'color_bg': "#FFFBEB",
            'color_border': "#D97706",
            'color_title': "#92400E",
            'color_badge': "#FEF3C7",
            'criteri': [
                r"$\bullet\ \mathrm{Leva:}\ h_{ii} \leq 3D/N$",
                r"$\bullet\ \mathrm{Residuo:}\ |d_{\mathrm{ESR}}| > 3$"
            ],
            'proprieta': [
                r"$\bullet$ Feature $\mathbf{x}$ tipiche (no braccio di leva)",
                r"$\bullet$ Target $t$ anomalo (forte residuo)",
                r"$\bullet$ Gonfia $\sigma_\epsilon^2$ e i SE, non sposta $\mathbf{w}$"
            ]
        },
        {
            'x': xs[2],
            'title': "3. High-Leverage (HLP)",
            'subtitle': "Leva Alta Coerente (X-Outlier)",
            'color_bg': "#EFF6FF",
            'color_border': "#2563EB",
            'color_title': "#1E40AF",
            'color_badge': "#DBEAFE",
            'criteri': [
                r"$\bullet\ \mathrm{Leva:}\ h_{ii} > 3D/N$",
                r"$\bullet\ \mathrm{Residuo:}\ |d_{\mathrm{ESR}}| \leq 3$"
            ],
            'proprieta': [
                r"$\bullet$ Feature $\mathbf{x}$ isolate / estreme",
                r"$\bullet$ Target $t$ perfettamente allineato",
                r"$\bullet$ Riduce i SE sui pesi (benefico)"
            ]
        },
        {
            'x': xs[3],
            'title': "4. Influente (HIF)",
            'subtitle': "Leva Alta e Residuo Estremo",
            'color_bg': "#FEF2F2",
            'color_border': "#DC2626",
            'color_title': "#991B1B",
            'color_badge': "#FEE2E2",
            'criteri': [
                r"$\bullet\ \mathrm{Leva:}\ h_{ii} > 3D/N$",
                r"$\bullet\ \mathrm{Residuo:}\ |d_{\mathrm{ESR}}| > 3$",
                r"$\bullet\ |\mathrm{DFFITS}| > 2\sqrt{D/N}$"
            ],
            'proprieta': [
                r"$\bullet$ Massima criticità architetturale",
                r"$\bullet$ Ruota la retta verso di sé",
                r"$\bullet$ Altera i pesi $\mathbf{w}$ (da escludere)"
            ]
        }
    ]

    for cfg in configs:
        x = cfg['x']
        # Contenitore Principale
        box = FancyBboxPatch((x, card_y), card_w, card_h, boxstyle='round,pad=0.0,rounding_size=0.08',
                             facecolor=cfg['color_bg'], edgecolor=cfg['color_border'], linewidth=1.5)
        ax.add_patch(box)

        # Header Badge
        header_y = card_y + card_h - 0.55
        header_box = FancyBboxPatch((x + 0.08, header_y), card_w - 0.16, 0.48,
                                    boxstyle='round,pad=0.0,rounding_size=0.06',
                                    facecolor=cfg['color_badge'], edgecolor=cfg['color_border'], linewidth=1.0)
        ax.add_patch(header_box)
        ax.text(x + card_w/2, header_y + 0.31, cfg['title'],
                fontsize=9.5, weight='bold', ha='center', va='center', color=cfg['color_title'])
        ax.text(x + card_w/2, header_y + 0.12, cfg['subtitle'],
                fontsize=7.8, ha='center', va='center', color='#475569')

        # Box Criteri Diagnostici
        crit_box_y = card_y + card_h - 1.55
        crit_box_h = 0.90
        crit_box = FancyBboxPatch((x + 0.10, crit_box_y), card_w - 0.20, crit_box_h,
                                  boxstyle='round,pad=0.0,rounding_size=0.05',
                                  facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.0)
        ax.add_patch(crit_box)

        ax.text(x + card_w/2, crit_box_y + crit_box_h - 0.14, "CRITERI ANALITICI",
                fontsize=7.8, weight='bold', ha='center', va='center', color='#64748B')

        if len(cfg['criteri']) == 2:
            ax.text(x + 0.20, crit_box_y + 0.45, cfg['criteri'][0],
                    fontsize=8.5, ha='left', va='center', color='#1E293B')
            ax.text(x + 0.20, crit_box_y + 0.20, cfg['criteri'][1],
                    fontsize=8.5, ha='left', va='center', color='#1E293B')
        else:
            ax.text(x + 0.20, crit_box_y + 0.53, cfg['criteri'][0],
                    fontsize=8.0, ha='left', va='center', color='#1E293B')
            ax.text(x + 0.20, crit_box_y + 0.33, cfg['criteri'][1],
                    fontsize=8.0, ha='left', va='center', color='#1E293B')
            ax.text(x + 0.20, crit_box_y + 0.13, cfg['criteri'][2],
                    fontsize=8.0, ha='left', va='center', color='#991B1B')

        # Sezione Proprietà ed Effetti
        prop_y = crit_box_y - 0.22
        ax.text(x + card_w/2, prop_y, "EFFETTO SULLA STIMA",
                fontsize=8.0, weight='bold', ha='center', va='center', color='#334155')

        # 3 Righe di Proprietà spaziate con rigore (y = 1.85, 1.45, 1.08)
        y_lines = [prop_y - 0.30, prop_y - 0.65, prop_y - 1.02]
        for y_pos, prop_txt in zip(y_lines, cfg['proprieta']):
            color_txt = '#991B1B' if ('altera' in prop_txt.lower() or 'criticità' in prop_txt.lower() or 'ruota' in prop_txt.lower()) else '#1E293B'
            ax.text(x + 0.16, y_pos, prop_txt, fontsize=8.2, ha='left', va='center', color=color_txt)

    # Banner Diagnostico Inferiore
    banner_y = 0.40
    banner_box = FancyBboxPatch((0.50, banner_y - 0.18), 11.99, 0.36,
                                boxstyle='round,pad=0.0,rounding_size=0.06',
                                facecolor='#FEF2F2', edgecolor='#FCA5A5', linewidth=1.2)
    ax.add_patch(banner_box)
    ax.text(6.5, banner_y,
            r"$\mathbf{Regola\ Diagnostica:}$ Un punto è dannoso ($\mathbf{HIF}$) solo se possiede simultaneamente elevata Leva $h_{ii}$ ed elevato Residuo $|d_{\mathrm{ESR}}|$",
            fontsize=8.8, ha='center', va='center', color='#991B1B')

    plt.tight_layout()
    plt.savefig(output_path, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path} successfully.")

if __name__ == '__main__':
    out_svg = "Anno 1/Machine Learning/immagini/fig_ex_3_tassonomia_outlier_hlp.svg"
    generate_svg(out_svg)
