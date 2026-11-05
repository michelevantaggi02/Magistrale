import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 4.4), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.5)
ax.axis('off')

# Colors
c_hlp = '#EBF8FF'
c_hlp_border = '#3182CE'
c_out = '#FEFCBF'
c_out_border = '#D69E2E'
c_hif = '#FED7D7'
c_hif_border = '#E53E3E'
c_reg = '#F0FFF4'
c_reg_border = '#38A169'

# Title
ax.text(5.5, 5.1, 'Tassonomia dei Punti nei Modelli di Regressione Lineare', fontsize=12.5, weight='bold', ha='center', color='#1A202C')

# Box 1: Punti Regolari
rect1 = patches.FancyBboxPatch((0.5, 1.2), 2.2, 3.4, boxstyle='round,pad=0.06',
                               facecolor=c_reg, edgecolor=c_reg_border, linewidth=1.8)
ax.add_patch(rect1)
ax.text(1.6, 4.25, 'Punto Regolare', fontsize=11, weight='bold', ha='center', color='#276749')
ax.text(1.6, 3.8, r'• $h_{ii} \leq 3D/N$' + '\n' + r'• $|d_{\mathrm{ESR}}| \leq 3$', fontsize=9.5, ha='center', color='#2F855A')
ax.text(1.6, 3.0, 'Caratteristiche:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(1.6, 2.1, 'Valore delle feature\nvicino alla media;\nresiduo contenuto\ne compatibile con\nil rumore di misura.', fontsize=8.8, ha='center', color='#2D3748')

# Box 2: Outlier Semplice
rect2 = patches.FancyBboxPatch((3.0, 1.2), 2.3, 3.4, boxstyle='round,pad=0.06',
                               facecolor=c_out, edgecolor=c_out_border, linewidth=1.8)
ax.add_patch(rect2)
ax.text(4.15, 4.25, 'Outlier Semplice', fontsize=11, weight='bold', ha='center', color='#B7791F')
ax.text(4.15, 3.8, r'• $h_{ii} \leq 3D/N$' + '\n' + r'• $|d_{\mathrm{ESR}}| > 3$', fontsize=9.5, ha='center', color='#B7791F')
ax.text(4.15, 3.0, 'Impatto Stima:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(4.15, 2.1, r'Feature tipiche,' + '\n' + r'ma target $t$ anomalo.' + '\n' + r'Altera la stima di $\sigma_\epsilon^2$' + '\n' + r'e gonfia i SE,' + '\n' + r'ma non sposta la retta.', fontsize=8.8, ha='center', color='#2D3748')

# Box 3: High-Leverage Point (HLP)
rect3 = patches.FancyBboxPatch((5.6, 1.2), 2.4, 3.4, boxstyle='round,pad=0.06',
                               facecolor=c_hlp, edgecolor=c_hlp_border, linewidth=1.8)
ax.add_patch(rect3)
ax.text(6.8, 4.25, 'High-Leverage (HLP)', fontsize=11, weight='bold', ha='center', color='#2B6CB0')
ax.text(6.8, 3.8, r'• $h_{ii} > 3D/N$' + '\n' + r'• $|d_{\mathrm{ESR}}| \leq 3$', fontsize=9.5, ha='center', color='#2B6CB0')
ax.text(6.8, 3.0, 'Impatto Stima:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(6.8, 2.1, r'Feature estreme/isolate' + '\n' + r'nello spazio $\mathbf{x}$,' + '\n' + r'ma coerenti con la retta.' + '\n' + r'Riduce i SE sui pesi,' + '\n' + r'nessun danno al modello.', fontsize=8.8, ha='center', color='#2D3748')

# Box 4: High Influential Point (HIF)
rect4 = patches.FancyBboxPatch((8.3, 1.2), 2.3, 3.4, boxstyle='round,pad=0.06',
                               facecolor=c_hif, edgecolor=c_hif_border, linewidth=2.2)
ax.add_patch(rect4)
ax.text(9.45, 4.25, 'Influente (HIF)', fontsize=11, weight='bold', ha='center', color='#C53030')
ax.text(9.45, 3.8, r'• HLP + Outlier' + '\n' + r'• $|\mathrm{DFFITS}| > 2\sqrt{\frac{D}{N-D}}$', fontsize=9.2, ha='center', color='#C53030')
ax.text(9.45, 3.0, 'Massimo Pericolo:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(9.45, 2.1, r'Leva elevata e residuo' + '\n' + r'estremo. Sposta la retta' + '\n' + r'verso di se alterando' + '\n' + r'completamente i pesi $\mathbf{w}$.' + '\n' + r'Candidato all\'esclusione.', fontsize=8.8, ha='center', color='#742A2A')

# Bottom rule box
ax.text(5.5, 0.45, 'Regola Diagnostica: un punto e dannoso (HIF) solo se possiede simultaneamente elevato Leverage $h_{ii}$ ed elevato Residuo $|d_{\mathrm{ESR}}|$',
        fontsize=9, weight='bold', ha='center', color='#C53030',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFF5F5', edgecolor='#FEB2B2', lw=1.2))

plt.savefig('Anno 1/Machine Learning/immagini/fig_ex_3_tassonomia_outlier_hlp.png', dpi=300, bbox_inches='tight', facecolor='white')
print('OK')
