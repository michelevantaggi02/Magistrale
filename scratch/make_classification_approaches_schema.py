import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10.5, 4.6), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 5.5)
ax.axis('off')

# Title
ax.text(5.5, 5.15, 'Tassonomia dei Tre Approcci Fondamentali alla Classificazione', fontsize=12.5, weight='bold', ha='center', color='#1A202C')

# Box 1: Modelli Generativi
c1_bg, c1_b = '#EBF8FF', '#3182CE'
rect1 = patches.FancyBboxPatch((0.4, 0.8), 3.1, 4.0, boxstyle='round,pad=0.08', facecolor=c1_bg, edgecolor=c1_b, linewidth=1.8)
ax.add_patch(rect1)
ax.text(1.95, 4.45, '1. Modelli Generativi', fontsize=11, weight='bold', ha='center', color='#2B6CB0')
ax.text(1.95, 4.05, r'Stima $p(\mathbf{x}|\mathcal{C}_k)$ e $P(\mathcal{C}_k)$' + '\n' + r'$\Downarrow$ Bayes' + '\n' + r'$p(\mathcal{C}_k|\mathbf{x}) = \frac{p(\mathbf{x}|\mathcal{C}_k)P(\mathcal{C}_k)}{p(\mathbf{x})}$', fontsize=8.8, ha='center', color='#2C5282')
ax.text(1.95, 2.75, 'Modelli Tipici:', fontsize=9.2, weight='bold', ha='center', color='#2D3748')
ax.text(1.95, 2.35, '• Gaussian LDA / QDA\n• Naive Bayes\n• Mixture di Gaussiane (GMM)', fontsize=8.4, ha='center', color='#2D3748')
ax.text(1.95, 1.45, 'Caratteristiche:\n(+) Outlier/Novelty detection\n(+) Permette sintesi dati\n(-) Elevato costo parametri\n(-) Modella la densita di input', fontsize=8.2, ha='center', color='#2C5282')

# Box 2: Modelli Discriminativi Probabilistici
c2_bg, c2_b = '#F0FFF4', '#38A169'
rect2 = patches.FancyBboxPatch((3.9, 0.8), 3.2, 4.0, boxstyle='round,pad=0.08', facecolor=c2_bg, edgecolor=c2_b, linewidth=1.8)
ax.add_patch(rect2)
ax.text(5.5, 4.45, '2. Discriminativi Probabilistici', fontsize=10.5, weight='bold', ha='center', color='#276749')
ax.text(5.5, 4.05, r'Modellano direttamente' + '\n' + r'la probabilita a posteriori:' + '\n' + r'$p(\mathcal{C}_k|\mathbf{x}) = \sigma(\mathbf{w}^T\boldsymbol{\phi}(\mathbf{x}))$', fontsize=8.8, ha='center', color='#22543D')
ax.text(5.5, 2.75, 'Modelli Tipici:', fontsize=9.2, weight='bold', ha='center', color='#2D3748')
ax.text(5.5, 2.35, '• Regressione Logistica\n• Softmax per Multiclasse\n• Reti Neurali con BCE/CE', fontsize=8.4, ha='center', color='#2D3748')
ax.text(5.5, 1.45, 'Caratteristiche:\n(+) Nessun costo per $p(\mathbf{x})$\n(+) Calibrazione probabilita\n(+) Scelta flessibile della soglia\n(-) Non genera nuovi campioni', fontsize=8.2, ha='center', color='#22543D')

# Box 3: Funzioni Discriminanti Dirette
c3_bg, c3_b = '#FEFCBF', '#D69E2E'
rect3 = patches.FancyBboxPatch((7.5, 0.8), 3.1, 4.0, boxstyle='round,pad=0.08', facecolor=c3_bg, edgecolor=c3_b, linewidth=1.8)
ax.add_patch(rect3)
ax.text(9.05, 4.45, '3. Funzioni Discriminanti', fontsize=10.5, weight='bold', ha='center', color='#B7791F')
ax.text(9.05, 4.05, r'Mappatura diretta input $\to$ classe' + '\n' + r'senza calcolo probabilistico:' + '\n' + r'$y = f(\mathbf{w}^T\boldsymbol{\phi}(\mathbf{x})) \in \{-1, +1\}$', fontsize=8.8, ha='center', color='#744210')
ax.text(9.05, 2.75, 'Modelli Tipici:', fontsize=9.2, weight='bold', ha='center', color='#2D3748')
ax.text(9.05, 2.35, '• Perceptron di Rosenblatt\n• Support Vector Machines (SVM)\n• K-Nearest Neighbors (K-NN)', fontsize=8.4, ha='center', color='#2D3748')
ax.text(9.05, 1.45, 'Caratteristiche:\n(+) Approccio diretto ed essenziale\n(+) Efficienza computazionale\n(-) Output deterministico secco\n(-) Nessuna misura di incertezza', fontsize=8.2, ha='center', color='#744210')

# Bottom rule box
ax.text(5.5, 0.35, r'Regola Metodologica: se l\'obiettivo e solo la decisione, la funzione discriminante e sufficiente; se serve quantificare l\'incertezza o gestire costi asimmetrici, e indispensabile un modello probabilistico',
        fontsize=8.4, weight='bold', ha='center', color='#1A202C',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.2))

plt.savefig('Anno 1/Machine Learning/immagini/fig_ex_4_tassonomia_approcci_classificazione.png', dpi=300, bbox_inches='tight', facecolor='white')
print('OK: Classification approaches schema generated')
