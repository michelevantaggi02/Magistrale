r"""
===============================================================================
FILTRO AD ISTOGRAMMA PER ROBOT 1D - VERSIONE v10 (Flag Distinti di Attivazione)
Data: 13 Ottobre 2026
Versione: v10.0

DETTAGLI DEL MODELLO:

1) MODELLO DI MOTO:
   - Modello cinematico 1D discreto: x_k = x_{k-1} + u_k + nu_k
   - Moto Deterministico: x_{det, k} = x_{det, k-1} + u_k
   - Moto Stocastico (Reale): x_{sto, k} = x_{sto, k-1} + u_k + nu_k, con nu_k ~ N(0, sigma_x_sim^2)
   - Matrice di Transizione P(x_t | x_{t-1}, u_t): costruita discretizzando lo spazio in bin
     e applicando il modello di moto gaussiano centrato su (x_{t-1} + u_t)
     con varianza di localizzazione sigma_x_loc^2.

2) MODELLO DI MISURA:
   - Modello Diretto (Generazione misure nel Simulatore):
     z_{i, k} = |x_{sto, k} - m_i| + w_{i, k}, con w_{i, k} ~ N(0, sigma_z_sim^2)
   - Modello Inverso / Verosimiglianza P(z | x) (Nel Filtro):
     Aspettativa di misura z_{exp, i}(x) = |x - m_i|
     Verosimiglianza del singolo beacon: L_i(x) = N(z_{i, k}; z_{exp, i}(x), sigma_z_loc^2)
     Verosimiglianza congiunta: L_{joint}(x) = PROD_i L_i(x)

3) DESCRIZIONE DEL FILTRO AD ISTOGRAMMA E FUNZIONALITÀ:
   - Discretizzazione Mappa: Bin fissi definiti tramite la loro ampiezza (bin_size),
     con n_bins = ceil(L / bin_size).
   - Inizializzazione Belief p(x_0): Uniforme o Gaussiana (selezionabile).
   - Doppia Stima dello Stato:
     * Valore Atteso (Media): \hat{x}_mean = SUM_i (bin_center_i * bel_i)
     * Moda (MAP): \hat{x}_mode = bin_center_{argmax(bel)}
   - Controllo Separato delle Funzionalità Grafiche (FI):
     * ATTIVA_VISUALIZZAZIONE_FI: abilita/disabilita la resa grafica a schermo passo-passo.
     * ATTIVA_SALVATAGGIO_FI: abilita/disabilita l'esportazione su file PNG dei grafici.
   - Modularità a Classi Distinte:
     * SimulatoreRobot1D: gestisce unicamente la simulazione fisica e cinematica.
     * FiltroIstogramma1D: implementa l'algoritmo Bayesiano e calcola i due stimatori.
     * VisualizzatoreLocalizzazione1D: gestisce grafici, salvataggi e avanzamento da tastiera.
     * EsperimentoLocalizzazione: coordina la simulazione ed il filtro.
===============================================================================
"""

import math
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 1. CLASSE SIMULATORE (Mondo Reale e Generazione Dati)
# =============================================================================
class SimulatoreRobot1D:
    """
    Simula la fisica e la cinematica del robot e dei sensori (Ground Truth).
    """

    def __init__(
        self,
        L: float = 100.0,
        x0: float = 0.0,
        T_finale: int = 80,
        u_x: float = 0.8,
        landmarks: list = None,
        sigma_x_sim: float = 0.5,
        sigma_z_sim: float = 1.5,
        seed: int = 42,  # Passare None per disattivare il seed deterministico
    ):
        if seed is not None:
            np.random.seed(seed)

        self.L = L
        self.x0 = x0
        self.T_finale = T_finale
        self.u_x = u_x
        self.landmarks = list(landmarks) if landmarks is not None else [30.0, 70.0]
        self.sigma_x_sim = sigma_x_sim
        self.sigma_z_sim = sigma_z_sim

    def modello_moto(self, x_prev: float, u: float, stocastico: bool = True) -> float:
        """Modello di moto cinematico 1D esplicito."""
        rumore = np.random.normal(0, self.sigma_x_sim) if stocastico else 0.0
        return x_prev + u + rumore

    def modello_misura_diretto(self, x: float, stocastico: bool = True) -> np.ndarray:
        """Modello di misura diretto esplicito per tutti i landmark."""
        misure = []
        for m in self.landmarks:
            z_aspettata = abs(x - m)
            rumore = np.random.normal(0, self.sigma_z_sim) if stocastico else 0.0
            misure.append(z_aspettata + rumore)
        return np.array(misure)

    def genera_traiettoria(self):
        """Genera l'intera traiettoria reale/deterministica e le relative misure."""
        num_lm = len(self.landmarks)
        x_det = np.zeros(self.T_finale + 1)
        x_sto = np.zeros(self.T_finale + 1)
        z_sto = np.zeros((self.T_finale + 1, num_lm))

        x_det[0] = self.x0
        x_sto[0] = self.x0
        z_sto[0] = self.modello_misura_diretto(x_sto[0], stocastico=True)

        for k in range(1, self.T_finale + 1):
            x_det[k] = self.modello_moto(x_det[k - 1], self.u_x, stocastico=False)
            x_sto[k] = self.modello_moto(x_sto[k - 1], self.u_x, stocastico=True)
            z_sto[k] = self.modello_misura_diretto(x_sto[k], stocastico=True)

        return x_det, x_sto, z_sto


# =============================================================================
# 2. CLASSE FILTRO AD ISTOGRAMMA (Algoritmo di Localizzazione con 2 Stimatori)
# =============================================================================
class FiltroIstogramma1D:
    """
    Implementa l'algoritmo di stima Bayesiana Discreta (Filtro ad Istogramma).
    """

    def __init__(
        self,
        L: float,
        u_x: float,
        landmarks: list,
        bin_size: float = 0.5,
        sigma_x_loc: float = 0.5,
        sigma_z_loc: float = 1.5,
        tipo_prior: str = "gaussiana",
        sigma_prior: float = 1.0,
        x0_prior: float = 0.0,
    ):
        self.L = L
        self.u_x = u_x
        self.landmarks = landmarks
        self.bin_size = bin_size
        self.n_bins = int(np.ceil(self.L / self.bin_size))
        self.bin_edges = np.linspace(0, self.L, self.n_bins + 1)
        self.bin_centers = (self.bin_edges[:-1] + self.bin_edges[1:]) / 2.0

        self.sigma_x_loc = sigma_x_loc
        self.sigma_z_loc = sigma_z_loc
        self.tipo_prior = tipo_prior.lower()
        self.sigma_prior = sigma_prior
        self.x0_prior = x0_prior

        self._costruisci_matrice_transizione()
        self.belief = self.inizializza_belief()

    def inizializza_belief(self) -> np.ndarray:
        """Crea la belief iniziale uniforme o gaussiana."""
        if self.tipo_prior == "uniforme":
            b = np.ones(self.n_bins) / self.n_bins
        elif self.tipo_prior == "gaussiana":
            b = np.exp(
                -0.5 * ((self.bin_centers - self.x0_prior) / self.sigma_prior) ** 2
            )
            b /= np.sum(b)
        else:
            raise ValueError("tipo_prior deve essere 'gaussiana' o 'uniforme'")
        return b

    def _costruisci_matrice_transizione(self):
        """Costruisce la matrice di transizione di stato P(x_t | x_{t-1}, u_t)."""
        grid_i, grid_j = np.meshgrid(self.bin_centers, self.bin_centers, indexing="ij")
        delta_x = grid_i - (grid_j + self.u_x)
        self.transition_matrix = np.exp(-0.5 * (delta_x / self.sigma_x_loc) ** 2) / (
            self.sigma_x_loc * np.sqrt(2 * np.pi)
        )
        self.transition_matrix /= np.sum(self.transition_matrix, axis=0, keepdims=True)

    def modello_misura_inverso(self, z_misure: np.ndarray):
        """Calcola la Likelihood delle singole misure e la Likelihood congiunta."""
        like_singole = []
        like_joint = np.ones(self.n_bins)

        for i, m in enumerate(self.landmarks):
            z_exp = np.abs(self.bin_centers - m)
            like_i = np.exp(-0.5 * ((z_misure[i] - z_exp) / self.sigma_z_loc) ** 2)
            like_singole.append(like_i)
            like_joint *= like_i

        return like_singole, like_joint

    def passo_predizione(self, belief_attuale: np.ndarray) -> np.ndarray:
        """Passo di predizione (Prior t)."""
        return self.transition_matrix @ belief_attuale

    def passo_correzione(self, belief_pred: np.ndarray, z_misure: np.ndarray):
        """Passo di aggiornamento Bayesiano (Posterior t)."""
        like_singole, like_joint = self.modello_misura_inverso(z_misure)
        belief_updated = belief_pred * like_joint
        sum_b = np.sum(belief_updated)

        belief_post = belief_updated / sum_b if sum_b > 0 else belief_pred
        return belief_post, like_singole, like_joint

    def calcola_stima_media(self, belief: np.ndarray) -> float:
        """Calcola la stima della posa come Valore Atteso (Media)."""
        return float(np.sum(self.bin_centers * belief))

    def calcola_stima_moda(self, belief: np.ndarray) -> float:
        """Calcola la stima della posa come Moda (Maximum A Posteriori - MAP)."""
        idx_max = np.argmax(belief)
        return float(self.bin_centers[idx_max])


# =============================================================================
# 3. CLASSE VISUALIZZATORE (Grafici e Esportazione)
# =============================================================================
class VisualizzatoreLocalizzazione1D:
    """
    Gestisce la rappresentazione grafica, il salvataggio ed il controllo da tastiera.
    """

    def __init__(
        self, L: float, landmarks: list, visualizza: bool = True, salva: bool = True
    ):
        self.L = L
        self.landmarks = landmarks
        self.visualizza = visualizza
        self.salva = salva

    def mostra_passo_dettagliato(
        self,
        k: int,
        N_iniziali: int,
        bin_centers: np.ndarray,
        belief_prev: np.ndarray,
        belief_pred: np.ndarray,
        like_singole: list,
        like_joint: np.ndarray,
        belief_post: np.ndarray,
        x_sto_k: float,
        x_det_hist: np.ndarray,
        x_sto_hist: np.ndarray,
        x_est_mean_hist: np.ndarray,
        x_est_mode_hist: np.ndarray,
        tipo_prior: str,
    ):
        if not (self.visualizza or self.salva):
            return

        fig, axes = plt.subplots(
            5,
            1,
            figsize=(11, 10),
            sharex=True,
            gridspec_kw={"height_ratios": [1, 1, 1.2, 1, 1.3]},
        )
        (ax1, ax2, ax3, ax4, ax_bot) = axes

        def evidenzia_riferimenti(ax):
            ax.axvline(
                x=x_sto_k,
                color="black",
                linestyle="-.",
                linewidth=1.5,
                label=f"Posa Reale x_k={x_sto_k:.2f}",
            )
            colors = ["blue", "purple", "darkgreen", "crimson", "orange"]
            for idx, m in enumerate(self.landmarks):
                c = colors[idx % len(colors)]
                ax.axvline(
                    x=m,
                    color=c,
                    linestyle=":",
                    linewidth=1.5,
                    label=f"Beacon m_{idx + 1}={m}",
                )
            ax.grid(True, linestyle=":", alpha=0.6)

        # 1) Posteriori t-1
        ax1.plot(
            bin_centers,
            belief_prev,
            "gray",
            linestyle="--",
            linewidth=1.8,
            label=f"Posteriori t-1 (k={k - 1})",
        )
        evidenzia_riferimenti(ax1)
        ax1.set_ylabel("Posteriori t-1")
        ax1.legend(loc="upper right", fontsize=7.5)

        # 2) Prior t
        ax2.plot(
            bin_centers,
            belief_pred,
            "orange",
            linestyle="-",
            linewidth=2,
            label=f"Prior t (k={k})",
        )
        evidenzia_riferimenti(ax2)
        ax2.set_ylabel("Prior t")
        ax2.legend(loc="upper right", fontsize=7.5)

        # 3) Likelihood Singole e Congiunta
        max_p = max(np.max(belief_post), np.max(belief_pred), np.max(belief_prev))
        colors_like = ["deepskyblue", "darkorchid", "mediumseagreen", "chocolate"]
        for idx, l_i in enumerate(like_singole):
            l_norm = (l_i / np.max(l_i)) * max_p if np.max(l_i) > 0 else l_i
            ax3.plot(
                bin_centers,
                l_norm,
                color=colors_like[idx % len(colors_like)],
                linestyle=":",
                linewidth=1.5,
                label=f"Likelihood Beacon {idx + 1}",
            )

        lj_norm = (
            (like_joint / np.max(like_joint)) * max_p
            if np.max(like_joint) > 0
            else like_joint
        )
        ax3.plot(
            bin_centers,
            lj_norm,
            "green",
            linestyle="--",
            linewidth=2.2,
            label="Likelihood Congiunta",
        )
        evidenzia_riferimenti(ax3)
        ax3.set_ylabel("Verosimiglianza")
        ax3.legend(loc="upper right", fontsize=7.5)

        # 4) Posteriori t
        ax4.plot(
            bin_centers,
            belief_post,
            "red",
            linestyle="-",
            linewidth=2.5,
            label=f"Posteriori t (k={k})",
        )
        evidenzia_riferimenti(ax4)
        ax4.set_ylabel("Posteriori t")
        ax4.legend(loc="upper right", fontsize=7.5)

        # 5) Pose (Descrizioni Brevi con "FI")
        t_hist = np.arange(len(x_det_hist))
        ax_bot.plot(t_hist, x_det_hist, "k--", label="Posa Det.", alpha=0.7)
        ax_bot.plot(
            t_hist, x_sto_hist, "g-o", markersize=4, label="Posa Reale", linewidth=1.5
        )
        ax_bot.plot(
            t_hist,
            x_est_mean_hist,
            "r-.s",
            markersize=4,
            label="Posa Stim. Media (FI)",
            linewidth=2,
        )
        ax_bot.plot(
            t_hist,
            x_est_mode_hist,
            color="darkorange",
            linestyle="-.",
            marker="^",
            markersize=4,
            label="Posa Stim. Moda (FI)",
            linewidth=1.8,
        )

        for idx, m in enumerate(self.landmarks):
            ax_bot.axhline(
                y=m, linestyle=":", alpha=0.6, label=f"Beacon m_{idx + 1}={m}"
            )

        ax_bot.set_xlim(0, self.L)
        ax_bot.set_xlabel("Posizione x / Dominio Mappa [0, L]")
        ax_bot.set_ylabel("Traiettoria")
        ax_bot.grid(True, linestyle=":", alpha=0.6)
        ax_bot.legend(loc="upper right", fontsize=7.5)

        # Titolo pulito
        fig.suptitle(
            f"Passo k = {k} / {N_iniziali} - Prior Iniziale: {tipo_prior.capitalize()}",
            fontsize=11,
            fontweight="bold",
        )
        plt.tight_layout()

        # Salvataggio su disco (Gestito separatamente tramite self.salva)
        if self.salva:
            filename = f"filtro_istogramma_{tipo_prior}_passo_{k}.png"
            fig.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"[INFO] Grafico salvato: '{filename}'")

        # Visualizzazione e avanzamento interattivo via tastiera (Gestito separatamente tramite self.visualizza)
        if self.visualizza:
            plt.ion()
            plt.show()
            plt.pause(0.1)
            input(
                f">>> [Passo k={k}/{N_iniziali}] Premi INVIO nel terminale per avanzare..."
            )
            plt.close(fig)
            plt.ioff()
        else:
            plt.close(fig)


# =============================================================================
# 4. CLASSE ESPERIMENTO (Orchestratore e Coordinatore)
# =============================================================================
class EsperimentoLocalizzazione:
    """
    Collega il simulatore reale con il filtro di localizzazione.
    """

    def __init__(
        self,
        simulatore: SimulatoreRobot1D,
        filtro: FiltroIstogramma1D,
        visualizzatore: VisualizzatoreLocalizzazione1D,
        N_iniziali: int = 4,
    ):
        self.sim = simulatore
        self.filtro = filtro
        self.vis = visualizzatore
        self.N_iniziali = N_iniziali

    def esegui(self):
        # 1. Genera ambiente e traiettoria reale nel simulatore
        x_det, x_sto, z_sto = self.sim.genera_traiettoria()

        # 2. Prepara strutture dati per i due stimatori del filtro
        x_est_mean = np.zeros(self.sim.T_finale + 1)
        x_est_mode = np.zeros(self.sim.T_finale + 1)

        belief_curr = self.filtro.belief.copy()
        x_est_mean[0] = self.filtro.calcola_stima_media(belief_curr)
        x_est_mode[0] = self.filtro.calcola_stima_moda(belief_curr)

        # 3. Loop temporale di stima
        for k in range(1, self.sim.T_finale + 1):
            belief_prev = belief_curr.copy()

            # Predizione e Correzione Bayesiana
            belief_pred = self.filtro.passo_predizione(belief_prev)
            belief_curr, like_singole, like_joint = self.filtro.passo_correzione(
                belief_pred, z_sto[k]
            )

            # Calcolo di entrambi gli stimatori di posa
            x_est_mean[k] = self.filtro.calcola_stima_media(belief_curr)
            x_est_mode[k] = self.filtro.calcola_stima_moda(belief_curr)

            # Grafici interattivi e salvataggi
            if k <= self.N_iniziali:
                self.vis.mostra_passo_dettagliato(
                    k=k,
                    N_iniziali=self.N_iniziali,
                    bin_centers=self.filtro.bin_centers,
                    belief_prev=belief_prev,
                    belief_pred=belief_pred,
                    like_singole=like_singole,
                    like_joint=like_joint,
                    belief_post=belief_curr,
                    x_sto_k=x_sto[k],
                    x_det_hist=x_det[: k + 1],
                    x_sto_hist=x_sto[: k + 1],
                    x_est_mean_hist=x_est_mean[: k + 1],
                    x_est_mode_hist=x_est_mode[: k + 1],
                    tipo_prior=self.filtro.tipo_prior,
                )

        return np.arange(self.sim.T_finale + 1), x_det, x_sto, x_est_mean, x_est_mode


# =============================================================================
# ESECUZIONE SIMULAZIONE V10
# =============================================================================
if __name__ == "__main__":
    # Parametri Mappa e Landmark
    L_MAPPA = 100.0
    BEACONS = [25.0]  # , 50.0, 75.0]  # Esempio con 3 Landmark

    # -------------------------------------------------------------------------
    # VARIABILI DI ATTIVAZIONE SPECIFICHE PER IL FILTRO AD ISTOGRAMMA (FI)
    # -------------------------------------------------------------------------
    # Assegnazione di valori effettivi per attivare/disattivare separatamente le funzioni:
    ATTIVA_VISUALIZZAZIONE_FI: bool = (
        True  # True per mostrare le figure passo-passo a schermo
    )
    ATTIVA_SALVATAGGIO_FI: bool = (
        True  # True per salvare i file PNG delle figure su disco
    )

    # 1. Istanziazione del Simulatore
    simulatore = SimulatoreRobot1D(
        L=L_MAPPA,
        x0=0.0,
        T_finale=80,
        u_x=0.8,
        landmarks=BEACONS,
        sigma_x_sim=0.5,
        sigma_z_sim=1.5,
        seed=42,  # Impostare a None per disattivare il seed deterministico
    )

    # 2. Istanziazione del Filtro ad Istogramma
    filtro = FiltroIstogramma1D(
        L=L_MAPPA,
        u_x=0.8,
        landmarks=BEACONS,
        bin_size=0.5,  # Bin fissi di ampiezza 0.5 (n_bins = 200)
        sigma_x_loc=0.5,
        sigma_z_loc=1.5,
        tipo_prior="gaussiana",  # "gaussiana" o "uniforme"
        sigma_prior=1.0,
        x0_prior=0.0,
    )

    # 3. Istanziazione del Visualizzatore configurato con le due variabili distinte
    visualizzatore = VisualizzatoreLocalizzazione1D(
        L=L_MAPPA,
        landmarks=BEACONS,
        visualizza=ATTIVA_VISUALIZZAZIONE_FI,
        salva=ATTIVA_SALVATAGGIO_FI,
    )

    # 4. Esecuzione Esperimento
    esperimento = EsperimentoLocalizzazione(
        simulatore, filtro, visualizzatore, N_iniziali=4
    )
    t, x_det, x_sto, x_est_mean, x_est_mode = esperimento.esegui()

    # --- Plot finale riassuntivo ---
    fig_final, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7.5), sharex=True)

    # Subplot 1: Traiettorie
    ax1.plot(t, x_det, "k--", label="Posa Det.", alpha=0.6)
    ax1.plot(t, x_sto, "g-", label="Posa Reale", linewidth=1.5)
    ax1.plot(
        t,
        x_est_mean,
        "r-.",
        label=r"Posa Stim. Media (FI) $\hat{x}_{\mathrm{media}}$",
        linewidth=2,
    )
    ax1.plot(
        t,
        x_est_mode,
        color="darkorange",
        linestyle="-.",
        label=r"Posa Stim. Moda (FI) $\hat{x}_{\mathrm{moda}}$",
        linewidth=1.8,
    )
    for idx, m in enumerate(BEACONS):
        ax1.axhline(y=m, linestyle=":", label=f"Beacon $m_{idx + 1}$={m}")
    ax1.set_ylabel("Posizione $x$")
    ax1.set_title(f"Localizzazione Finale - Filtro v10 (Prior: {filtro.tipo_prior})")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=8)

    # Subplot 2: Errore di Localizzazione con descrizioni sintetiche e sigla "FI"
    err_mean = np.abs(x_sto - x_est_mean)
    err_mode = np.abs(x_sto - x_est_mode)

    ax2.plot(
        t,
        err_mean,
        "r-.",
        label=r"Err. Media (FI) $|x_{\mathrm{reale}} - \hat{x}_{\mathrm{media}}|$",
        linewidth=1.8,
    )
    ax2.plot(
        t,
        err_mode,
        color="darkorange",
        linestyle="-.",
        label=r"Err. Moda (FI) $|x_{\mathrm{reale}} - \hat{x}_{\mathrm{moda}}|$",
        linewidth=1.8,
    )
    ax2.set_xlabel("Tempo $t$")
    ax2.set_ylabel("Errore Assoluto")
    ax2.set_title("Confronto Errore Assoluto di Localizzazione (FI: Media vs Moda)")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=8)

    plt.tight_layout()
    plt.show()
