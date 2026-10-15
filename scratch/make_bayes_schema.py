import matplotlib.pyplot as plt
import numpy as np

# Set figure size and dpi
fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=300)

w = np.linspace(-3, 5, 500)

# Prior: Gaussian centered at 0 with precision alpha (std = 1.3)
mu_prior = 0.0
sigma_prior = 1.3
prior = np.exp(-0.5 * ((w - mu_prior) / sigma_prior)**2) / (sigma_prior * np.sqrt(2 * np.pi))

# Likelihood: driven by data, peaked at w_ML = 2.4 (std = 0.75)
mu_lik = 2.4
sigma_lik = 0.75
likelihood = np.exp(-0.5 * ((w - mu_lik) / sigma_lik)**2) / (sigma_lik * np.sqrt(2 * np.pi))

# Posterior: product of prior and likelihood -> Gaussian with intermediate mean
prec_prior = 1.0 / (sigma_prior**2)
prec_lik = 1.0 / (sigma_lik**2)
prec_post = prec_prior + prec_lik
sigma_post = np.sqrt(1.0 / prec_post)
mu_post = (mu_prior * prec_prior + mu_lik * prec_lik) / prec_post

posterior = np.exp(-0.5 * ((w - mu_post) / sigma_post)**2) / (sigma_post * np.sqrt(2 * np.pi))

# Plot curves
ax.plot(w, prior, color='#E53E3E', linestyle='--', linewidth=2, label=r'Prior $p(\mathbf{w}|\alpha) \sim \mathcal{N}(0, \alpha^{-1}\mathbf{I})$')
ax.plot(w, likelihood, color='#3182CE', linestyle=':', linewidth=2, label=r'Likelihood $p(\mathbf{t}|\mathbf{X}, \mathbf{w}, \beta)$')
ax.plot(w, posterior, color='#2B6CB0', linewidth=2.5, label=r'Posterior $p(\mathbf{w}|\mathbf{X}, \mathbf{t}) \propto \mathrm{Likelihood} \times \mathrm{Prior}$')

# Highlight peaks
ax.axvline(mu_lik, color='#3182CE', linestyle=':', alpha=0.7)
ax.text(mu_lik, 0.56, r'$w_{\mathrm{ML}}$ (Data fit)', color='#2B6CB0', weight='bold', ha='center', fontsize=9.5)

ax.axvline(mu_post, color='#2B6CB0', linestyle='-', alpha=0.8)
ax.text(mu_post - 0.1, 0.65, r'$w_{\mathrm{MAP}}$ (Trade-off)', color='#1A365D', weight='bold', ha='right', fontsize=10)

ax.axvline(0, color='#E53E3E', linestyle='--', alpha=0.5)
ax.text(0, 0.33, r'Zero ($L_2$ Shrinkage)', color='#C53030', style='italic', ha='center', fontsize=9)

# Labels & title
ax.set_title(r'Interpretazione Bayesiana: da MLE a MAP e Regolarizzazione $L_2$ ($\lambda = \alpha / \beta$)', fontsize=11.5, weight='bold', pad=12, color='#1A202C')
ax.set_xlabel(r'Spazio dei Parametri $\mathbf{w}$', fontsize=10.5, labelpad=8)
ax.set_ylabel('Densita di Probabilita', fontsize=10.5, labelpad=8)
ax.legend(frameon=True, facecolor='#F7FAFC', edgecolor='#CBD5E0', fontsize=9, loc='upper left')

ax.set_xlim(-2.5, 4.5)
ax.set_ylim(0, 0.72)
ax.grid(True, linestyle='-', alpha=0.25, color='#CBD5E0')

# Annotation box
ax.text(3.0, 0.28,
        'Equivalenza Fondamentale:\n' +
        r'• $\mathrm{MLE} \Leftrightarrow$ Min. Errore Quadratico' + '\n' +
        r'• $\mathrm{MAP} \Leftrightarrow$ Regolarizzazione $L_2$ (Ridge)' + '\n' +
        r'• $\lambda = \frac{\alpha}{\beta} = \frac{\mathrm{precisione\ prior}}{\mathrm{precisione\ rumore}}$',
        fontsize=8.5, color='#2D3748',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1.2))

plt.savefig('Anno 1/Machine Learning/immagini/fig_ex_2_mle_vs_map.png', dpi=300, bbox_inches='tight', facecolor='white')
print('OK')
