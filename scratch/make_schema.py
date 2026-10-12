import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.5)
ax.axis('off')

# Colors
c_matrix = '#EBF8FF'
c_matrix_border = '#3182CE'
c_sample_hl = '#FED7D7'
c_sample_border = '#E53E3E'
c_target = '#F0FFF4'
c_target_border = '#38A169'
c_target_hl = '#FEEBC8'
c_target_hl_border = '#DD6B20'

# Draw X matrix (N x D)
rect_x = patches.FancyBboxPatch((0.9, 1.1), 4.7, 3.5, boxstyle='round,pad=0.08',
                                facecolor=c_matrix, edgecolor=c_matrix_border, linewidth=2)
ax.add_patch(rect_x)

# Highlight row i (sample i)
rect_row_i = patches.FancyBboxPatch((1.0, 2.45), 4.5, 0.55, boxstyle='round,pad=0.04',
                                    facecolor=c_sample_hl, edgecolor=c_sample_border, linewidth=1.5, linestyle='--')
ax.add_patch(rect_row_i)

# Labels on X
ax.text(3.25, 4.95, r'$\mathbf{X} \in \mathbb{R}^{N \times D}$ (Matrice delle Feature)', fontsize=12, weight='bold', ha='center', color='#2B6CB0')
ax.text(3.25, 4.35, r'$D$ colonne (Feature $0, \dots, D-1$)', fontsize=9.5, ha='center', style='italic', color='#4A5568')
ax.text(0.4, 2.85, 'N righe\n(campioni)', fontsize=9.5, ha='center', va='center', style='italic', color='#4A5568')

# Content inside X
ax.text(3.25, 3.85, r'$\mathbf{x}^{(0)T} = [\, x_{0,0} \quad x_{0,1} \quad \cdots \quad x_{0,D-1} \,]$', fontsize=9, ha='center', color='#2D3748')
ax.text(3.25, 3.3, r'$\vdots$', fontsize=11, ha='center', color='#718096')
ax.text(3.25, 2.7, r'$\mathbf{x}^{(i)T} = [\, x_{i,0} \quad x_{i,1} \quad \cdots \quad x_{i,D-1} \,]$', fontsize=9.2, weight='bold', ha='center', color='#9B2C2C')
ax.text(3.25, 2.05, r'$\vdots$', fontsize=11, ha='center', color='#718096')
ax.text(3.25, 1.5, r'$\mathbf{x}^{(N-1)T} = [\, x_{N-1,0} \quad \cdots \quad x_{N-1,D-1} \,]$', fontsize=9, ha='center', color='#2D3748')

# Pairing symbol
ax.text(6.05, 2.7, r'$\longleftrightarrow$', fontsize=20, ha='center', va='center', color='#4A5568')

# Draw y target vector (N x 1)
rect_y = patches.FancyBboxPatch((6.6, 1.1), 2.2, 3.5, boxstyle='round,pad=0.08',
                                facecolor=c_target, edgecolor=c_target_border, linewidth=2)
ax.add_patch(rect_y)

# Highlight element i in y
rect_y_i = patches.FancyBboxPatch((6.7, 2.45), 2.0, 0.55, boxstyle='round,pad=0.04',
                                  facecolor=c_target_hl, edgecolor=c_target_hl_border, linewidth=1.5, linestyle='--')
ax.add_patch(rect_y_i)

# Labels on y
ax.text(7.7, 4.95, r'$\mathbf{y} \in \mathbb{R}^{N \times 1}$ (Target/Label)', fontsize=12, weight='bold', ha='center', color='#276749')
ax.text(7.7, 4.35, r'$1$ colonna', fontsize=9.5, ha='center', style='italic', color='#4A5568')

# Content inside y
ax.text(7.7, 3.85, r'$y^{(0)}$', fontsize=9.5, ha='center', color='#2D3748')
ax.text(7.7, 3.3, r'$\vdots$', fontsize=11, ha='center', color='#718096')
ax.text(7.7, 2.7, r'$y^{(i)}$', fontsize=10, weight='bold', ha='center', color='#C05621')
ax.text(7.7, 2.05, r'$\vdots$', fontsize=11, ha='center', color='#718096')
ax.text(7.7, 1.5, r'$y^{(N-1)}$', fontsize=9.5, ha='center', color='#2D3748')

# Bottom annotation
ax.text(5.5, 0.45, r'Singolo campione supervisionato: coppia $(\mathbf{x}^{(i)}, y^{(i)})$ con $\mathbf{x}^{(i)} \in \mathbb{R}^{D \times 1}$ e $y^{(i)} \in \mathbb{R}$',
        fontsize=9.5, weight='bold', ha='center', color='#2B6CB0',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1.2))

plt.tight_layout()
plt.savefig('Anno 1/Machine Learning/immagini/fig_ex_0_struttura_dataset_matrice.png', dpi=300, bbox_inches='tight', facecolor='white')
print('OK')
