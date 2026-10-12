import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.5)
ax.axis('off')

# Colors
c_train = '#EBF8FF'
c_train_border = '#3182CE'
c_val = '#FEFCBF'
c_val_border = '#D69E2E'
c_test = '#FED7D7'
c_test_border = '#E53E3E'

# Entire dataset bar
rect_all = patches.FancyBboxPatch((0.6, 4.1), 9.8, 0.85, boxstyle='round,pad=0.05',
                                  facecolor='#EDF2F7', edgecolor='#4A5568', linewidth=1.8)
ax.add_patch(rect_all)
ax.text(5.5, 4.52, r'Dataset Completo $\mathcal{D}$ ($N$ campioni)', fontsize=12.5, weight='bold', ha='center', color='#1A202C')

# Downward arrows
ax.annotate('', xy=(2.4, 3.45), xytext=(2.4, 4.05), arrowprops=dict(arrowstyle='->', lw=1.6, color='#4A5568'))
ax.annotate('', xy=(5.9, 3.45), xytext=(5.9, 4.05), arrowprops=dict(arrowstyle='->', lw=1.6, color='#4A5568'))
ax.annotate('', xy=(9.0, 3.45), xytext=(9.0, 4.05), arrowprops=dict(arrowstyle='->', lw=1.6, color='#4A5568'))

# Training Set (60%)
rect_tr = patches.FancyBboxPatch((0.6, 1.2), 3.6, 2.2, boxstyle='round,pad=0.06',
                                 facecolor=c_train, edgecolor=c_train_border, linewidth=2)
ax.add_patch(rect_tr)
ax.text(2.4, 3.05, r'Training Set $\mathcal{D}_{\mathrm{train}}$', fontsize=11.5, weight='bold', ha='center', color='#2B6CB0')
ax.text(2.4, 2.7, '(tipicamente ~60-70%)', fontsize=9, style='italic', ha='center', color='#4A5568')
ax.text(2.4, 2.25, 'Ruolo primario:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(2.4, 1.7, 'Ottimizzazione parametri\n' + r'$\mathbf{w}^* = \arg\min_{\mathbf{w}} L(\mathbf{w})$', fontsize=9, ha='center', color='#1A365D')

# Validation Set (20%)
rect_v = patches.FancyBboxPatch((4.5, 1.2), 2.8, 2.2, boxstyle='round,pad=0.06',
                                facecolor=c_val, edgecolor=c_val_border, linewidth=2)
ax.add_patch(rect_v)
ax.text(5.9, 3.05, r'Validation Set $\mathcal{D}_{\mathrm{val}}$', fontsize=11.5, weight='bold', ha='center', color='#B7791F')
ax.text(5.9, 2.7, '(tipicamente ~20%)', fontsize=9, style='italic', ha='center', color='#4A5568')
ax.text(5.9, 2.25, 'Model Selection:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(5.9, 1.7, 'Scelta iperparametri\n' + r'($M^*, \lambda^*$)', fontsize=9, ha='center', color='#744210')

# Test Set (20%)
rect_te = patches.FancyBboxPatch((7.6, 1.2), 2.8, 2.2, boxstyle='round,pad=0.06',
                                 facecolor=c_test, edgecolor=c_test_border, linewidth=2)
ax.add_patch(rect_te)
ax.text(9.0, 3.05, r'Test Set $\mathcal{D}_{\mathrm{test}}$', fontsize=11.5, weight='bold', ha='center', color='#C53030')
ax.text(9.0, 2.7, '(tipicamente ~10-20%)', fontsize=9, style='italic', ha='center', color='#4A5568')
ax.text(9.0, 2.25, 'Model Assessment:', fontsize=9.5, weight='bold', ha='center', color='#2D3748')
ax.text(9.0, 1.7, 'Stima imparziale errore\ngeneralizzazione', fontsize=9, ha='center', color='#742A2A')

# Bottom rule box
ax.text(5.5, 0.45, r'Regola Aurea: i dati di Test NON devono MAI essere usati per scegliere parametri $\mathbf{w}$ o iperparametri ($M, \lambda$)',
        fontsize=9.2, weight='bold', ha='center', color='#C53030',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFF5F5', edgecolor='#FEB2B2', lw=1.2))

plt.savefig('Anno 1/Machine Learning/immagini/fig_ex_1_train_val_test_split.png', dpi=300, bbox_inches='tight', facecolor='white')
print('OK')
