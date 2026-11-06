import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)

x = np.linspace(-4, 8, 1000)

# Parametri delle due classi
mu1, s1, p1 = 0.5, 1.2, 0.45
mu2, s2, p2 = 4.0, 1.4, 0.55

# Joint distributions p(x, Ck) = p(x|Ck) * p(Ck)
p_x_c1 = p1 * (1.0 / (s1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu1) / s1) ** 2)
p_x_c2 = p2 * (1.0 / (s2 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu2) / s2) ** 2)

# Trova intersezione (soglia ottima x*)
diff = np.abs(p_x_c1 - p_x_c2)
idx_opt = np.argmin(diff[200:700]) + 200
x_star = x[idx_opt]

# Plot curve
ax.plot(x, p_x_c1, color='#2B6CB0', lw=2.4, label=r'$p(\mathbf{x}, \mathcal{C}_1) = p(\mathbf{x}|\mathcal{C}_1)P(\mathcal{C}_1)$')
ax.plot(x, p_x_c2, color='#C53030', lw=2.4, label=r'$p(\mathbf{x}, \mathcal{C}_2) = p(\mathbf{x}|\mathcal{C}_2)P(\mathcal{C}_2)$')

# Fill error regions
# Errore 1: vero C1 ma predetto C2 (x > x_star)
ax.fill_between(x[x >= x_star], 0, p_x_c1[x >= x_star], color='#3182CE', alpha=0.35, hatch='//',
                label=r'Errore Classe $\mathcal{C}_1$ (predetta $\mathcal{C}_2$)')
# Errore 2: vero C2 ma predetto C1 (x < x_star)
ax.fill_between(x[x <= x_star], 0, p_x_c2[x <= x_star], color='#E53E3E', alpha=0.35, hatch='\\\\',
                label=r'Errore Classe $\mathcal{C}_2$ (predetta $\mathcal{C}_1$)')

# Vertical line soglia ottima
ax.axvline(x_star, color='#2D3748', ls='--', lw=2.0)
ax.text(x_star, 0.17, r' Soglia Ottima $x^*$' + '\n' + r' $p(\mathbf{x}, \mathcal{C}_1) = p(\mathbf{x}, \mathcal{C}_2)$',
        fontsize=9.5, weight='bold', color='#1A202C', ha='left',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1.2))

# Regioni di decisione
ax.text(-0.5, 0.015, r'Regione $\mathcal{R}_1$' + '\n' + r'Decidi $\mathcal{C}_1$',
        fontsize=10.5, weight='bold', color='#2B6CB0', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#EBF8FF', edgecolor='#bee3f8', lw=1.0))
ax.text(5.5, 0.015, r'Regione $\mathcal{R}_2$' + '\n' + r'Decidi $\mathcal{C}_2$',
        fontsize=10.5, weight='bold', color='#C53030', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5F5', edgecolor='#fed7d7', lw=1.0))

# Decorazione
ax.set_title('Bayesian Error Rate: Limite Inferiore Teorico dell\'Errore di Classificazione', fontsize=11.5, weight='bold', pad=12, color='#1A202C')
ax.set_xlabel('Spazio delle Feature $x$', fontsize=10.5, weight='bold')
ax.set_ylabel('Densita Congiunta $p(x, \mathcal{C}_k)$', fontsize=10.5, weight='bold')
ax.legend(loc='upper right', fontsize=8.8, framealpha=0.95)
ax.grid(True, ls=':', color='#CBD5E0', alpha=0.6)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('Anno 1/Machine Learning/immagini/fig_ex_4_bayesian_error_rate.png', dpi=300, facecolor='white')
print('OK: Bayesian Error Rate schema generated')
