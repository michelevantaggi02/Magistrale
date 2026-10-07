#!/usr/bin/env python3
"""
Autonomous Robotics - Simulazione Histogram Filter 1D
======================================================

Specifiche del problema:
  - Mappa monodimensionale: segmento di lunghezza L, x in [0, L]
  - Discretizzazione spaziale: K celle di larghezza delta_x
  - Robot puntiforme: posa vera x_t (scalare continuo)
  - Orizzonte temporale: simulazione da t = 0 a T_finale con passo dt
  - Modello di moto:
        x_t = x_{t-1} + u_x + nu,    nu ~ N(0, sigma_s^2)
  - Modello di misura da beacon:
        z_t = |x_t - m_1| + mu,      mu ~ N(0, sigma_z^2)
  - Histogram Filter (Markov Localization discreta):
        Predizione: bel_bar(x_k) = sum_i p(x_k | x_i, u_x) * bel(x_i)
        Correzione: bel(x_k)     = eta * p(z_t | x_k, m_1) * bel_bar(x_k)
  - Output grafico: plottato interattivamente a video con plt.show() (nessun salvataggio su file)

Struttura del file:
  1. Modelli probabilistici e funzioni di densità gaussiana
  2. Modelli fisici del mondo reale (ground truth e sensore corrotto da rumore)
  3. Implementazione della classe HistogramFilter1D
  4. Ciclo di simulazione su orizzonte temporale T_finale
  5. Funzioni di visualizzazione e plotting (plt.show)
  6. Esecuzione principale (main)
"""

import random
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 0. GESTIONE SEED CASUALE (RIPRODUCIBILITÀ)
# =============================================================================
def set_random_seed(seed: int | None = None):
    """
    Imposta il seed per la generazione di numeri pseudo-casuali (numpy e random standard).
    Se seed è None, il generatore utilizzerà una sorgente di casualità del sistema operativo.
    """
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)


# =============================================================================
# 1. FUNZIONI PROBABILISTICHE DI BASE
# =============================================================================
def prob_normal(error: np.ndarray, variance: float) -> np.ndarray:
    """
    Calcola la densità di probabilità normale N(0, variance) per l'errore assegnato.
    Corrisponde alla 'distribution computation' discussa negli appunti di teoria.
    """
    std = np.sqrt(variance)
    return (1.0 / (np.sqrt(2.0 * np.pi) * std)) * np.exp(-0.5 * (error ** 2) / variance)


# =============================================================================
# 2. MODELLI FISICI DEL SISTEMA REALE (GROUND TRUTH)
# =============================================================================
def true_motion_step(x_prev: float, u_x: float, sigma_s: float, L: float) -> float:
    """
    Simula l'avanzamento reale del robot puntiforme secondo il modello:
        x_t = x_{t-1} + u_x + nu,   nu ~ N(0, sigma_s^2)
    Con saturazione sui bordi del segmento [0, L].
    """
    noise = np.random.normal(0.0, sigma_s)
    x_new = x_prev + u_x + noise
    return float(np.clip(x_new, 0.0, L))


def true_measurement_step(x_true: float, m1: float, sigma_z: float) -> float:
    """
    Simula la lettura esteriorocettiva del sensore di distanza rispetto al beacon m1:
        z_t = |x_t - m_1| + mu,     mu ~ N(0, sigma_z^2)
    """
    actual_distance = abs(x_true - m1)
    noise = np.random.normal(0.0, sigma_z)
    z = actual_distance + noise
    return float(max(0.0, z))  # La distanza scalare misurata è non-negativa


# =============================================================================
# 3. CLASSE HISTOGRAM FILTER 1D
# =============================================================================
class HistogramFilter1D:
    def __init__(self, L: float, delta_x: float):
        """
        Inizializza la griglia discreta di tassellazione per un segmento [0, L].
        
        Parametri:
        - L: lunghezza complessiva del segmento (in metri)
        - delta_x: risoluzione spaziale / dimensione della singola cella (in metri)
        """
        self.L = L
        self.delta_x = delta_x
        # I centri delle celle rappresentano le ipotesi di stato discrete x_k
        self.cells = np.arange(delta_x / 2.0, L, delta_x)
        self.num_cells = len(self.cells)
        # Inizializzazione predefinita: belief uniforme su tutto il dominio [0, L] (localizzazione globale)
        self.bel = np.ones(self.num_cells) / self.num_cells

    def set_uniform_belief(self):
        """Inizializza il belief come uniforme (massima incertezza / global localization)."""
        self.bel = np.ones(self.num_cells) / self.num_cells

    def set_gaussian_belief(self, mean: float, std: float):
        """Inizializza il belief come gaussiana centrata attorno a una posa di partenza (tracking)."""
        raw = prob_normal(self.cells - mean, std ** 2)
        self.bel = raw / np.sum(raw)

    def predict(self, u_x: float, sigma_s: float) -> np.ndarray:
        """
        Passo di Predizione (Total Probability Theorem):
            bel_bar(x_k) = sum_i p(x_k | x_i, u_x) * bel_{t-1}(x_i)
        
        dove per ogni coppia (x_k, x_i) l'errore di moto è:
            nu = x_k - (x_i + u_x)
        e la probabilità di transizione è N(nu; 0, sigma_s^2).
        """
        bel_bar = np.zeros(self.num_cells)
        variance_s = sigma_s ** 2

        # Convoluzione discreta su tutte le celle di destinazione x_k
        for k, x_k in enumerate(self.cells):
            # Vettore delle discrepanze cinematiche rispetto a tutte le celle di partenza
            nu = x_k - (self.cells + u_x)
            transition_probs = prob_normal(nu, variance_s)
            bel_bar[k] = np.sum(transition_probs * self.bel)

        # Normalizzazione numerica conservativa
        total_mass = np.sum(bel_bar)
        if total_mass > 0:
            bel_bar /= total_mass
        self.bel = bel_bar
        return self.bel

    def correct(self, z_t: float, m1: float, sigma_z: float) -> np.ndarray:
        """
        Passo di Correzione (Regola di Bayes):
            bel(x_k) = eta * p(z_t | x_k, m_1) * bel_bar(x_k)
            
        con likelihood gaussiana sull'errore residuo di misura:
            mu = z_t - |x_k - m_1|
            p(z_t | x_k, m_1) = N(mu; 0, sigma_z^2)
        """
        variance_z = sigma_z ** 2
        # Distanza teorica attesa per ciascuna ipotesi di cella x_k
        expected_distance = np.abs(self.cells - m1)
        residual = z_t - expected_distance
        likelihood = prob_normal(residual, variance_z)

        # Aggiornamento puntuale e normalizzazione eta
        unnormalized = likelihood * self.bel
        eta_inv = np.sum(unnormalized)
        if eta_inv > 0:
            self.bel = unnormalized / eta_inv
        else:
            # Fallback in caso di deperimento numerico
            self.bel = np.ones(self.num_cells) / self.num_cells
        return self.bel

    def get_estimate_mean(self) -> float:
        """Calcola la media pesata del belief (stima attesa)."""
        return float(np.sum(self.cells * self.bel))

    def get_estimate_map(self) -> float:
        """Calcola la posa di Massimo a Posteriori (MAP)."""
        idx_max = np.argmax(self.bel)
        return float(self.cells[idx_max])

    def get_estimate_std(self) -> float:
        """Calcola la deviazione standard del belief (indice di incertezza)."""
        mean = self.get_estimate_mean()
        var = np.sum(((self.cells - mean) ** 2) * self.bel)
        return float(np.sqrt(max(0.0, var)))


# =============================================================================
# 4. CICLO DI SIMULAZIONE
# =============================================================================
def run_simulation(
    L: float = 20.0,
    delta_x: float = 0.1,
    T_finale: float = 25.0,
    dt: float = 1.0,
    x0_true: float = 2.0,
    u_x: float = 0.6,
    sigma_s: float = 0.25,
    m1: float = 10.0,
    sigma_z: float = 0.3,
    initial_mode: str = "uniform",  # "uniform" per global localization, "gaussian" per tracking
    seed: int | None = None          # Seed per riproducibilità stocastica (es. intero o None per casuale)
):
    """
    Esegue la simulazione dell'ambiente e del filtro sull'orizzonte temporale [0, T_finale].
    """
    # Impostazione del seed pseudo-casuale per riproducibilità numerica
    set_random_seed(seed)

    time_steps = np.arange(0.0, T_finale + dt, dt)
    num_steps = len(time_steps)

    # Inizializzazione filtro
    hf = HistogramFilter1D(L=L, delta_x=delta_x)
    if initial_mode == "uniform":
        hf.set_uniform_belief()
    else:
        hf.set_gaussian_belief(mean=x0_true, std=0.5)

    # Vettori di log per analisi storica
    history_x_true = np.zeros(num_steps)
    history_x_est_mean = np.zeros(num_steps)
    history_x_est_map = np.zeros(num_steps)
    history_est_std = np.zeros(num_steps)
    history_measurements = np.zeros(num_steps)
    history_belief_map = np.zeros((num_steps, hf.num_cells))

    # Stato iniziale
    current_x_true = x0_true
    history_x_true[0] = current_x_true
    history_x_est_mean[0] = hf.get_estimate_mean()
    history_x_est_map[0] = hf.get_estimate_map()
    history_est_std[0] = hf.get_estimate_std()
    history_belief_map[0, :] = hf.bel.copy()

    # Ciclo temporale
    for t_idx in range(1, num_steps):
        # 1. Avanzamento del robot reale (Ground Truth)
        current_x_true = true_motion_step(current_x_true, u_x, sigma_s, L)
        history_x_true[t_idx] = current_x_true

        # 2. Passo di Predizione del Filtro
        hf.predict(u_x=u_x, sigma_s=sigma_s)

        # 3. Misura sensoriale corrotta da rumore
        z_t = true_measurement_step(current_x_true, m1, sigma_z)
        history_measurements[t_idx] = z_t

        # 4. Passo di Correzione Bayesiana del Filtro
        hf.correct(z_t=z_t, m1=m1, sigma_z=sigma_z)

        # Registrazione delle stime
        history_x_est_mean[t_idx] = hf.get_estimate_mean()
        history_x_est_map[t_idx] = hf.get_estimate_map()
        history_est_std[t_idx] = hf.get_estimate_std()
        history_belief_map[t_idx, :] = hf.bel.copy()

    return {
        "time": time_steps,
        "x_true": history_x_true,
        "x_mean": history_x_est_mean,
        "x_map": history_x_est_map,
        "std": history_est_std,
        "measurements": history_measurements,
        "belief_matrix": history_belief_map,
        "cells": hf.cells,
        "L": L,
        "m1": m1
    }


# =============================================================================
# 5. VISUALIZZAZIONE E PLOTTING
# =============================================================================
def plot_results(data: dict):
    """
    Visualizza i risultati della simulazione su pannelli informativi dedicati.
    Tutti i grafici vengono mostrati a video con plt.show().
    """
    t = data["time"]
    x_true = data["x_true"]
    x_map = data["x_map"]
    x_mean = data["x_mean"]
    std = data["std"]
    cells = data["cells"]
    belief_matrix = data["belief_matrix"]
    L = data["L"]
    m1 = data["m1"]

    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.2, 1.2, 1.0], hspace=0.35, wspace=0.25)

    # -------------------------------------------------------------------------
    # Subplot 1: Traiettoria temporale (Ground Truth vs Stima)
    # -------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(t, x_true, 'k-', linewidth=2.5, label='Posa Reale x_true (Ground Truth)')
    ax1.plot(t, x_map, 'b--', linewidth=2.0, label='Stima MAP (Cella a massima probabilità)')
    ax1.fill_between(t, x_mean - 2 * std, x_mean + 2 * std, color='blue', alpha=0.15, label=r'Banda di Confidenza $\pm 2\sigma$')
    ax1.axhline(y=m1, color='red', linestyle=':', linewidth=2.0, label=f'Posizione Beacon m1 = {m1} m')
    ax1.set_title("1D Histogram Filter: Traiettoria Reale vs Stima nel Tempo", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Tempo [s]", fontsize=10)
    ax1.set_ylabel("Posizione x [m]", fontsize=10)
    ax1.set_ylim([0, L])
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper left', framealpha=0.9, fontsize=9)

    # -------------------------------------------------------------------------
    # Subplot 2: Heatmap spazio-temporale del Belief bel(x, t)
    # -------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[1, :])
    im = ax2.imshow(
        belief_matrix,
        aspect='auto',
        origin='lower',
        extent=[cells[0], cells[-1], t[0], t[-1]],
        cmap='viridis'
    )
    ax2.plot(x_true, t, 'r--', linewidth=2.0, label='Traiettoria Reale x_true')
    ax2.axvline(x=m1, color='white', linestyle=':', linewidth=1.8, label=f'Beacon m1 = {m1} m')
    cbar = fig.colorbar(im, ax=ax2, pad=0.02)
    cbar.set_label("Probabilità per cella", fontsize=9)
    ax2.set_title(r"Evoluzione Spazio-Temporale del Belief $bel(x, t)$", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Spazio x [m]", fontsize=10)
    ax2.set_ylabel("Tempo [s]", fontsize=10)
    ax2.legend(loc='upper left', framealpha=0.9, fontsize=9)

    # -------------------------------------------------------------------------
    # Subplot 3: Snapshot dei profili di probabilità a istanti chiave
    # -------------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[2, 0])
    # Selezioniamo 3 snapshot: inizio (t=1), metà e fine simulazione
    indices = [1, len(t) // 2, -1]
    colors = ['#f0ad4e', '#0275d8', '#5cb85c']
    for idx, c in zip(indices, colors):
        t_val = t[idx]
        ax3.plot(cells, belief_matrix[idx], label=f't = {t_val:.1f} s', color=c, linewidth=2.0)
        ax3.axvline(x=x_true[idx], color=c, linestyle=':', alpha=0.7)
    ax3.axvline(x=m1, color='red', linestyle='--', alpha=0.8, label='Beacon m1')
    ax3.set_title(r"Snapshot del Profilo di Probabilità $bel(x)$", fontsize=11, fontweight='bold')
    ax3.set_xlabel("Posa x [m]", fontsize=9)
    ax3.set_ylabel("Probabilità", fontsize=9)
    ax3.set_xlim([0, L])
    ax3.grid(True, linestyle='--', alpha=0.5)
    ax3.legend(loc='upper right', fontsize=8)

    # -------------------------------------------------------------------------
    # Subplot 4: Errore di localizzazione nel tempo
    # -------------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[2, 1])
    error_map = np.abs(x_true - x_map)
    ax4.plot(t, error_map, color='#d9534f', linewidth=2.0, label=r'Errore Assoluto $|x_{true} - x_{MAP}|$')
    ax4.axhline(y=np.mean(error_map), color='black', linestyle='--', label=f'Errore Medio = {np.mean(error_map):.3f} m')
    ax4.set_title("Errore di Localizzazione nel Tempo", fontsize=11, fontweight='bold')
    ax4.set_xlabel("Tempo [s]", fontsize=9)
    ax4.set_ylabel("Errore [m]", fontsize=9)
    ax4.grid(True, linestyle='--', alpha=0.5)
    ax4.legend(loc='upper right', fontsize=8)

    # Mostra i grafici a video
    plt.show()


# =============================================================================
# 6. MAIN
# =============================================================================
if __name__ == "__main__":
    # Parametri conformi alle specifiche della richiesta:
    # - Mappa segmento di lunghezza L
    # - Orizzonte temporale T_finale
    # - Passo di moto u_x con rumore sigma_s
    # - Beacon in m1 con rumore di misura sigma_z
    L = 20.0             # Lunghezza mappa [m]
    delta_x = 0.1        # Risoluzione cella [m]
    T_finale = 25.0      # Orizzonte temporale [s]
    dt = 1.0             # Passo discreto di campionamento [s]
    x0_true = 2.0        # Posa iniziale reale del robot puntiforme [m]
    u_x = 0.6            # Comando di spostamento [m/passo]
    sigma_s = 0.25       # Deviazione standard del rumore di moto [m]
    m1 = 10.0            # Posizione del beacon [m]
    sigma_z = 0.3        # Deviazione standard del rumore di misura [m]
    random_seed = 42     # Seed per riproducibilità (es. intero come 42, oppure None per casuale)

    print("==================================================")
    print("AVVIO SIMULAZIONE HISTOGRAM FILTER 1D")
    print(f"Mappa L = {L} m | Risoluzione delta_x = {delta_x} m")
    print(f"Orizzonte T_finale = {T_finale} s | Passo dt = {dt} s")
    print(f"Comando u_x = {u_x} m | Rumore moto sigma_s = {sigma_s} m")
    print(f"Beacon m1 = {m1} m | Rumore misura sigma_z = {sigma_z} m")
    print(f"Seed casuale = {random_seed if random_seed is not None else 'Casuale (None)'}")
    print("==================================================")

    # Esecuzione simulazione
    sim_data = run_simulation(
        L=L,
        delta_x=delta_x,
        T_finale=T_finale,
        dt=dt,
        x0_true=x0_true,
        u_x=u_x,
        sigma_s=sigma_s,
        m1=m1,
        sigma_z=sigma_z,
        initial_mode="uniform",  # Localizzazione globale da zero
        seed=random_seed
    )

    print("\nSimulazione completata con successo. Apertura grafici interattivi...")
    # Plotta i risultati a video (plt.show)
    plot_results(sim_data)
