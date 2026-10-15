r"""
===============================================================================
PARTICLE FILTER PER ROBOT 1D (Monte Carlo Localization - MCL) - VERSIONE v1.0
Corso: Autonomous Robotics - Prof. Paolo Valigi
Data: 14 Ottobre 2026
Autore: Pair Programming Assistant (Antigravity) & Studente

DETTAGLI DEL MODELLO E SPECIFICHE DIDATTICHE:

1) MODELLO DI MOTO (Cinematica 1D Stocastica):
   - Equazione reale/stocastica del robot:
     x_{sto, k} = x_{sto, k-1} + u_k + nu_k,   con nu_k ~ N(0, sigma_x_sim^2)
   - Moto deterministico di riferimento (odometria ideale priva di rumore):
     x_{det, k} = x_{det, k-1} + u_k
   - Generazione di campioni nel filtro (Sample Motion Model / Proposal Distribution):
     x_t^[m] ~ p(x_t | x_{t-1}^[m], u_t)
     x_t^[m] = x_{t-1}^[m] + u_k + nu_{loc}^[m],  con nu_{loc}^[m] ~ N(0, sigma_x_loc^2)
   - Motivazione ingegneristica: a differenza del Filtro ad Istogramma (che richiede
     di calcolare la matrice di transizione discreta completa P(x_t | x_{t-1}, u_t)
     con costo O(K^2)), il Particle Filter richiede unicamente un modello *generativo*,
     estraendo campioni numerici in O(M).

2) MODELLO DI MISURA (Sensore Range da Beacon Noti):
   - Modello Diretto nel Simulatore (Ground Truth):
     z_{i, k} = |x_{sto, k} - m_i| + w_{i, k},  con w_{i, k} ~ N(0, sigma_z_sim^2)
   - Modello di Verosimiglianza nel Filtro (Measurement Model / Likelihood):
     Misura attesa per la particella m-esima: z_{exp, i}(x_t^[m]) = |x_t^[m] - m_i|
     Verosimiglianza del singolo beacon:
       L_i(x_t^[m]) = (1 / sqrt(2*pi*sigma_z_loc^2)) * exp( - (z_{i,k} - z_{exp, i})^2 / (2*sigma_z_loc^2) )
     Verosimiglianza congiunta (Fattore di Importanza non normalizzato):
       w_t^[m] = PROD_i L_i(x_t^[m])

3) IMPORTANCE SAMPLING E RICAMPIONAMENTO (SIR - Sampling Importance Resampling):
   - Self-Normalized Importance Sampling (SNIS):
     Poiché la target f(x) = bel(x_t) è nota solo a meno della costante eta = 1/p(z_t),
     calcoliamo i pesi grezzi w_t^[m] = p(z_t | x_t^[m]) e li normalizziamo:
       \tilde{w}_t^[m] = w_t^[m] / SUM_j(w_t^[j])
   - Numero Effettivo di Particelle (Diagnostica di Degenerazione):
     N_eff = 1 / SUM_m (\tilde{w}_t^[m])^2   in [1, M]
   - Algoritmi di Ricampionamento implementati:
     a) Low-Variance Resampling (Campionamento Sistematico di Thrun, O(M)):
        Pettine a passo fisso 1/M con singolo offset casuale r in [0, 1/M).
        Minimizza la varianza di campionamento ed è lo standard in ROS/AMCL.
     b) Roulette Wheel (Multinomial Resampling, O(M log M)):
        Campionamento indipendente con ricerca dicotomica su CDF discreta.

4) STIME DELLA POSA E CONFRONTO:
   - Stima Media (Valore Atteso Pesato): \hat{x}_mean = SUM_m (\tilde{w}_t^[m] * x_t^[m])
   - Stima Moda (Maximum A Posteriori - MAP): posa della particella con peso massimo
   - Benchmark integrato con Filtro ad Istogramma (v10) per confronto contestuale.
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
    Simula la fisica, la cinematica del robot e le osservazioni dei sensori (Ground Truth).
    Mantiene la perfetta compatibilità e parità di condizioni rispetto al file v10.
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
        seed: int = 42,  # Impostare a None per disattivare la riproducibilità deterministica
    ):
        """
        Inizializza l'ambiente di simulazione reale.

        Scelta progettuale del seed: fissare il seed consente di generare esattamente
        la stessa traiettoria reale e le stesse misure rumorose, rendendo possibile un
        confronto equo, oggettivo e ripetibile tra Histogram Filter e Particle Filter.
        """
        if seed is not None:
            np.random.seed(seed)

        self.L = float(L)
        self.x0 = float(x0)
        self.T_finale = int(T_finale)
        self.u_x = float(u_x)
        self.landmarks = list(landmarks) if landmarks is not None else [25.0]
        self.sigma_x_sim = float(sigma_x_sim)
        self.sigma_z_sim = float(sigma_z_sim)

    def modello_moto(self, x_prev: float, u: float, stocastico: bool = True) -> float:
        """
        Simula il moto fisico 1D del veicolo.
        x_k = x_{k-1} + u + nu_k, con nu_k ~ N(0, sigma_x_sim^2)
        """
        rumore = np.random.normal(0.0, self.sigma_x_sim) if stocastico else 0.0
        return x_prev + u + rumore

    def modello_misura_diretto(self, x: float, stocastico: bool = True) -> np.ndarray:
        """
        Simula la lettura sensoriale di distanza (range) rispetto a tutti i beacon noti.
        z_{i, k} = |x - m_i| + w_{i, k}, con w_{i, k} ~ N(0, sigma_z_sim^2)
        """
        misure = []
        for m in self.landmarks:
            z_aspettata = abs(x - m)
            rumore = np.random.normal(0.0, self.sigma_z_sim) if stocastico else 0.0
            misure.append(z_aspettata + rumore)
        return np.array(misure, dtype=float)

    def genera_traiettoria(self):
        """
        Genera a priori l'intera sequenza temporale di stati reali e misure rumorose.
        Ritorna:
            x_det: traiettoria puramente deterministica (senza rumore)
            x_sto: traiettoria reale del robot (Ground Truth stocastica)
            z_sto: matrice delle misure (T_finale + 1, num_landmarks)
        """
        num_lm = len(self.landmarks)
        x_det = np.zeros(self.T_finale + 1, dtype=float)
        x_sto = np.zeros(self.T_finale + 1, dtype=float)
        z_sto = np.zeros((self.T_finale + 1, num_lm), dtype=float)

        x_det[0] = self.x0
        x_sto[0] = self.x0
        z_sto[0] = self.modello_misura_diretto(x_sto[0], stocastico=True)

        for k in range(1, self.T_finale + 1):
            x_det[k] = self.modello_moto(x_det[k - 1], self.u_x, stocastico=False)
            x_sto[k] = self.modello_moto(x_sto[k - 1], self.u_x, stocastico=True)
            z_sto[k] = self.modello_misura_diretto(x_sto[k], stocastico=True)

        return x_det, x_sto, z_sto


# =============================================================================
# 2. CLASSE FILTRO A PARTICELLE (Monte Carlo Localization - 1D MCL)
# =============================================================================
class FiltroParticelle1D:
    """
    Implementa l'algoritmo di stima stocastica non-parametrica tramite Particle Filter (MCL).
    Rappresenta la distribuzione di probabilità continua tramite un set di M particelle pesate.
    """

    def __init__(
        self,
        L: float,
        u_x: float,
        landmarks: list,
        M: int = 1000,
        sigma_x_loc: float = 0.5,
        sigma_z_loc: float = 1.5,
        tipo_prior: str = "gaussiana",
        sigma_prior: float = 1.0,
        x0_prior: float = 0.0,
        metodo_resampling: str = "low_variance",
        gestione_bordi: str = "clip",
    ):
        """
        Inizializza il Particle Filter.

        Parametri:
            L: estensione dello spazio continuo [0, L]
            u_x: comando di controllo di traslazione nominale
            landmarks: posizioni note dei beacon
            M: numero di particelle (campioni stocastici)
            sigma_x_loc: deviazione standard del modello di moto ipotizzato dal filtro
            sigma_z_loc: deviazione standard del modello di misura ipotizzato dal filtro
            tipo_prior: 'gaussiana' (tracking) o 'uniforme' (global localization)
            sigma_prior: deviazione standard dell'incertezza iniziale se gaussiana
            x0_prior: valore medio della posa iniziale ipotizzata se gaussiana
            metodo_resampling: 'low_variance' (predefinito) o 'roulette_wheel'
            gestione_bordi: 'clip' (satura in [0, L]) o 'free' (lascia particelle libere)
        """
        self.L = float(L)
        self.u_x = float(u_x)
        self.landmarks = list(landmarks)
        self.M = int(M)
        self.sigma_x_loc = float(sigma_x_loc)
        self.sigma_z_loc = float(sigma_z_loc)
        self.tipo_prior = tipo_prior.lower()
        self.sigma_prior = float(sigma_prior)
        self.x0_prior = float(x0_prior)
        self.metodo_resampling = metodo_resampling.lower()
        self.gestione_bordi = gestione_bordi.lower()

        # Inizializzazione della popolazione di particelle e dei pesi
        self.particelle = self.inizializza_particelle()
        self.pesi = np.ones(self.M, dtype=float) / float(self.M)
        self.pesi_non_normalizzati = self.pesi.copy()

    def inizializza_particelle(self) -> np.ndarray:
        """
        Genera la popolazione iniziale delle M particelle nello spazio di stato continuo.

        Scelta algoritmica:
        - 'uniforme': campiona M punti casuali da U(0, L). Modella la 'Global Localization',
          in cui non abbiamo alcuna conoscenza pregressa sulla posizione iniziale.
        - 'gaussiana': campiona da N(x0_prior, sigma_prior^2). Modella il 'Position Tracking',
          in cui disponiamo di una stima a priori con incertezza limitata attorno a x0.
        """
        if self.tipo_prior == "uniforme":
            p = np.random.uniform(0.0, self.L, size=self.M)
        elif self.tipo_prior == "gaussiana":
            p = np.random.normal(self.x0_prior, self.sigma_prior, size=self.M)
            if self.gestione_bordi == "clip":
                p = np.clip(p, 0.0, self.L)
        else:
            raise ValueError("tipo_prior deve essere 'gaussiana' oppure 'uniforme'")
        return p

    def applica_vincolo_bordi(self, particelle: np.ndarray) -> np.ndarray:
        """
        Mantiene le particelle all'interno del dominio fisico della mappa [0, L].
        Scelta di saturazione (clipping): impedisce a particelle rumorose di evadere
        dall'arena nota durante il campionamento della predizione.
        """
        if self.gestione_bordi == "clip":
            return np.clip(particelle, 0.0, self.L)
        return particelle

    def passo_predizione(self, particelle_attuali: np.ndarray) -> np.ndarray:
        """
        Passo di Predizione (Motion Model / Proposal Distribution g(x)):
        Per ciascuna particella m, propaga lo stato secondo il comando u_x
        aggiungendo rumore stocastico gaussiano indipendente:
            x_t^[m] = x_{t-1}^[m] + u_x + nu^[m],  nu^[m] ~ N(0, sigma_x_loc^2)

        Motivazione teorica: ogni particella sperimenta una realizzazione stocastica
        indipendente del rumore di attuazione. Questo garantisce che la nube si disperda
        in modo realistico in assenza di misure correttive.
        """
        rumore_moto = np.random.normal(0.0, self.sigma_x_loc, size=self.M)
        particelle_predette = particelle_attuali + self.u_x + rumore_moto
        return self.applica_vincolo_bordi(particelle_predette)

    def calcola_pesi_misura(
        self, particelle: np.ndarray, z_misure: np.ndarray
    ) -> tuple:
        """
        Passo di Correzione (Measurement Model / Likelihood Weighting):
        Valuta la verosimiglianza delle misure osservate z_misure rispetto a ciascuna
        ipotesi di posa x_t^[m].

        Per prevenire l'underflow numerico nel prodotto di molteplici esponenziali,
        il calcolo della verosimiglianza congiunta viene eseguito nel dominio logaritmico
        tramite il 'Log-Sum-Exp trick' prima della normalizzazione.

        Ritorna:
            pesi_normalizzati: \tilde{w}_t^[m] tale che SUM \tilde{w}_t^[m] = 1.0
            pesi_grezzi: verosimiglianza congiunta non normalizzata w_t^[m]
            like_singole_per_particella: lista delle likelihood per singolo beacon
        """
        log_like_joint = np.zeros(self.M, dtype=float)
        like_singole = []

        costante_norm = 1.0 / (self.sigma_z_loc * math.sqrt(2.0 * math.pi))

        for idx, m in enumerate(self.landmarks):
            z_exp = np.abs(particelle - m)
            errore_misura = z_misure[idx] - z_exp
            log_l_i = -0.5 * (errore_misura / self.sigma_z_loc) ** 2

            # Likelihood del singolo beacon per ogni particella
            l_i = costante_norm * np.exp(log_l_i)
            like_singole.append(l_i)

            # Accumulo dei logaritmi per il prodotto congiunto (indipendenza condizionata)
            log_like_joint += log_l_i

        # Calcolo stabile dei pesi congiunti (sottrazione del massimo per evitare underflow)
        max_log = np.max(log_like_joint)
        pesi_grezzi = np.exp(log_like_joint - max_log)

        somma_pesi = np.sum(pesi_grezzi)
        if somma_pesi > 0.0 and not np.isnan(somma_pesi):
            pesi_normalizzati = pesi_grezzi / somma_pesi
        else:
            # Fallback di sicurezza: se tutte le particelle sono degeneri, assegna pesi uniformi
            pesi_normalizzati = np.ones(self.M, dtype=float) / float(self.M)

        return pesi_normalizzati, pesi_grezzi, like_singole

    def calcola_neff(self, pesi_norm: np.ndarray) -> float:
        """
        Calcola il numero effettivo di particelle (Effective Sample Size - N_eff):
            N_eff = 1.0 / SUM_m (\tilde{w}_t^[m]^2)

        Significato fisico:
        - N_eff = M: tutti i pesi sono identici (1/M), massima varianza campionaria.
        - N_eff -> 1: una singola particella domina la popolazione, collasso statistico
          (particle depletion / degeneracy).
        """
        somma_quadrati = np.sum(pesi_norm**2)
        if somma_quadrati > 0.0:
            return float(1.0 / somma_quadrati)
        return 1.0

    def ricampionamento(
        self, particelle: np.ndarray, pesi_norm: np.ndarray
    ) -> np.ndarray:
        """
        Passo di Ricampionamento (Resampling with replacement):
        Estrae M nuove particelle equiprobabili selezionando quelle con peso maggiore
        ed eliminando quelle con peso trascurabile.

        Implementa due strategie selezionabili:
        1. 'low_variance' (Campionamento Sistematico / Pettine di Thrun):
           Estrae un singolo offset casuale r in [0, 1/M) e scorre la CDF con passo
           costante 1/M. Vantaggi: complessità deterministica O(M), azzera la varianza
           di campionamento tra campioni e assicura che qualsiasi particella con
           peso >= 1/M venga inclusa con certezza.
        2. 'roulette_wheel' (Campionamento Multinomiale Indipendente):
           Estrae M numeri casuali indipendenti in [0, 1) e usa la ricerca binaria O(M log M).
        """
        if self.metodo_resampling == "low_variance":
            nuove_particelle = np.empty(self.M, dtype=float)
            r = np.random.uniform(0.0, 1.0 / float(self.M))
            c = pesi_norm[0]
            i = 0

            for m in range(self.M):
                u = r + float(m) / float(self.M)
                while u > c and i < self.M - 1:
                    i += 1
                    c += pesi_norm[i]
                nuove_particelle[m] = particelle[i]

            return nuove_particelle

        elif self.metodo_resampling == "roulette_wheel":
            indici = np.random.choice(
                self.M, size=self.M, replace=True, p=pesi_norm
            )
            return particelle[indici].copy()

        else:
            raise ValueError(
                f"Metodo di ricampionamento non valido: '{self.metodo_resampling}'"
            )

    def calcola_stima_media(
        self, particelle: np.ndarray, pesi_norm: np.ndarray
    ) -> float:
        r"""
        Calcola la stima della posa come Valore Atteso Pesato (Media Empirica):
            \hat{x}_mean = SUM_m (\tilde{w}_t^[m] * x_t^[m])
        """
        return float(np.sum(particelle * pesi_norm))

    def calcola_stima_moda(
        self, particelle: np.ndarray, pesi_norm: np.ndarray
    ) -> float:
        """
        Calcola la stima della posa come Moda (Maximum A Posteriori - MAP):
        Identifica la particella che possiede il peso di verosimiglianza massimo
        all'istante corrente prima del ricampionamento.
        """
        idx_max = np.argmax(pesi_norm)
        return float(particelle[idx_max])

    def calcola_dispersione(
        self, particelle: np.ndarray, stima_media: float, pesi_norm: np.ndarray
    ) -> float:
        """
        Calcola la deviazione standard pesata della nube di particelle (misura di incertezza).
        """
        varianza = np.sum(pesi_norm * (particelle - stima_media) ** 2)
        return float(np.sqrt(max(0.0, varianza)))


# =============================================================================
# 3. CLASSE FILTRO AD ISTOGRAMMA (Per Benchmark e Confronto Diretto)
# =============================================================================
class FiltroIstogramma1D:
    """
    Filtro ad Istogramma discreto (Markov Localization su Griglia) conforme a v10.
    Incluso per consentire il confronto analitico e grafico richiesto dall'assignment.
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
        self.L = float(L)
        self.u_x = float(u_x)
        self.landmarks = list(landmarks)
        self.bin_size = float(bin_size)
        self.n_bins = int(np.ceil(self.L / self.bin_size))
        self.bin_edges = np.linspace(0.0, self.L, self.n_bins + 1)
        self.bin_centers = (self.bin_edges[:-1] + self.bin_edges[1:]) / 2.0

        self.sigma_x_loc = float(sigma_x_loc)
        self.sigma_z_loc = float(sigma_z_loc)
        self.tipo_prior = tipo_prior.lower()
        self.sigma_prior = float(sigma_prior)
        self.x0_prior = float(x0_prior)

        self._costruisci_matrice_transizione()
        self.belief = self.inizializza_belief()

    def inizializza_belief(self) -> np.ndarray:
        if self.tipo_prior == "uniforme":
            b = np.ones(self.n_bins, dtype=float) / float(self.n_bins)
        elif self.tipo_prior == "gaussiana":
            b = np.exp(
                -0.5 * ((self.bin_centers - self.x0_prior) / self.sigma_prior) ** 2
            )
            somma = np.sum(b)
            b = b / somma if somma > 0 else np.ones(self.n_bins) / self.n_bins
        else:
            raise ValueError("tipo_prior deve essere 'gaussiana' o 'uniforme'")
        return b

    def _costruisci_matrice_transizione(self):
        grid_i, grid_j = np.meshgrid(self.bin_centers, self.bin_centers, indexing="ij")
        delta_x = grid_i - (grid_j + self.u_x)
        self.transition_matrix = np.exp(-0.5 * (delta_x / self.sigma_x_loc) ** 2) / (
            self.sigma_x_loc * math.sqrt(2.0 * math.pi)
        )
        self.transition_matrix /= np.sum(self.transition_matrix, axis=0, keepdims=True)

    def modello_misura_inverso(self, z_misure: np.ndarray):
        like_singole = []
        like_joint = np.ones(self.n_bins, dtype=float)
        for i, m in enumerate(self.landmarks):
            z_exp = np.abs(self.bin_centers - m)
            like_i = np.exp(-0.5 * ((z_misure[i] - z_exp) / self.sigma_z_loc) ** 2)
            like_singole.append(like_i)
            like_joint *= like_i
        return like_singole, like_joint

    def passo_predizione(self, belief_attuale: np.ndarray) -> np.ndarray:
        return self.transition_matrix @ belief_attuale

    def passo_correzione(self, belief_pred: np.ndarray, z_misure: np.ndarray):
        like_singole, like_joint = self.modello_misura_inverso(z_misure)
        belief_updated = belief_pred * like_joint
        sum_b = np.sum(belief_updated)
        belief_post = belief_updated / sum_b if sum_b > 0 else belief_pred
        return belief_post, like_singole, like_joint

    def calcola_stima_media(self, belief: np.ndarray) -> float:
        return float(np.sum(self.bin_centers * belief))

    def calcola_stima_moda(self, belief: np.ndarray) -> float:
        idx_max = np.argmax(belief)
        return float(self.bin_centers[idx_max])


# =============================================================================
# 4. CLASSE VISUALIZZATORE (5 Pannelli per Particle Filter e Confronto)
# =============================================================================
class VisualizzatoreLocalizzazione1D:
    """
    Gestisce la visualizzazione a 5 pannelli specifica per il Particle Filter,
    mantenendo la piena aderenza visiva al layout della lezione del professore.
    """

    def __init__(
        self,
        L: float,
        landmarks: list,
        visualizza: bool = True,
        salva: bool = False,
        confronta_histogram: bool = True,
        metodo_resampling: str = "low_variance",
    ):
        self.L = float(L)
        self.landmarks = list(landmarks)
        self.visualizza = visualizza
        self.salva = salva
        self.confronta_histogram = confronta_histogram
        self.metodo_resampling = str(metodo_resampling)

    def mostra_passo_dettagliato(
        self,
        k: int,
        N_iniziali: int,
        particelle_prev: np.ndarray,
        particelle_pred: np.ndarray,
        particelle_post: np.ndarray,
        pesi_norm: np.ndarray,
        z_k: np.ndarray,
        sigma_z: float,
        x_sto_k: float,
        t_hist: np.ndarray,
        x_det_hist: np.ndarray,
        x_sto_hist: np.ndarray,
        x_pf_mean_hist: np.ndarray,
        x_pf_mode_hist: np.ndarray,
        x_fi_mean_hist: np.ndarray = None,
        x_fi_mode_hist: np.ndarray = None,
        tipo_prior: str = "gaussiana",
        neff_k: float = 0.0,
        M: int = 1000,
        metodo_resampling: str = None,
    ):
        """
        Genera il grafico a 5 pannelli del Particle Filter:
        1) Posterior t-1: distribuzione empirica delle particelle al passo k-1
        2) Prior t: particelle propagate dal moto (proposal g) al passo k
        3) Verosimiglianza Sensoriale p(z | x): curva analitica valutata su griglia densa
        4) Posterior t: particelle ricampionate (target f) con istogramma di densità
        5) Traiettorie Temporali: confronto stime PF (e FI se attivo) vs Posa Reale
        """
        if not (self.visualizza or self.salva):
            return

        fig, axes = plt.subplots(
            5,
            1,
            figsize=(11, 10.5),
            sharex=True,
            gridspec_kw={"height_ratios": [1, 1, 1.2, 1, 1.3]},
        )
        (ax1, ax2, ax3, ax4, ax_bot) = axes

        # Funzione ausiliaria per linee verticali di riferimento (posa reale e beacon)
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

        # Griglia per istogrammi di densità delle particelle
        n_bins_vis = 100
        bins_vis = np.linspace(0.0, self.L, n_bins_vis + 1)

        # ---------------------------------------------------------------------
        # 1) Posteriori t-1 (k-1)
        # ---------------------------------------------------------------------
        ax1.hist(
            particelle_prev,
            bins=bins_vis,
            density=True,
            color="gray",
            alpha=0.45,
            edgecolor="none",
            label=f"Densità Particelle t-1 (k={k - 1})",
        )
        # Rug plot (campioni singoli alla base)
        ax1.plot(
            particelle_prev,
            np.zeros_like(particelle_prev),
            "|",
            color="dimgray",
            markersize=8,
            alpha=0.6,
        )
        evidenzia_riferimenti(ax1)
        ax1.set_ylabel("Posteriori t-1")
        ax1.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 2) Prior t (k) - Dopo il comando di moto
        # ---------------------------------------------------------------------
        ax2.hist(
            particelle_pred,
            bins=bins_vis,
            density=True,
            color="orange",
            alpha=0.45,
            edgecolor="none",
            label=f"Densità Prior t (k={k}) [Proposal]",
        )
        ax2.plot(
            particelle_pred,
            np.zeros_like(particelle_pred),
            "|",
            color="darkorange",
            markersize=8,
            alpha=0.6,
        )
        evidenzia_riferimenti(ax2)
        ax2.set_ylabel("Prior t")
        ax2.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 3) Likelihood Singole e Congiunta nello spazio continuo
        # ---------------------------------------------------------------------
        x_dense = np.linspace(0.0, self.L, 500)
        like_joint_dense = np.ones_like(x_dense)
        colors_like = ["deepskyblue", "darkorchid", "mediumseagreen", "chocolate"]

        costante_norm = 1.0 / (sigma_z * math.sqrt(2.0 * math.pi))
        for idx, m in enumerate(self.landmarks):
            z_exp_dense = np.abs(x_dense - m)
            l_i = costante_norm * np.exp(
                -0.5 * ((z_k[idx] - z_exp_dense) / sigma_z) ** 2
            )
            # Normalizzazione per resa visiva
            l_norm = l_i / np.max(l_i) if np.max(l_i) > 0 else l_i
            ax3.plot(
                x_dense,
                l_norm,
                color=colors_like[idx % len(colors_like)],
                linestyle=":",
                linewidth=1.5,
                label=f"Likelihood Beacon {idx + 1} (z={z_k[idx]:.2f})",
            )
            like_joint_dense *= l_i

        lj_norm = (
            like_joint_dense / np.max(like_joint_dense)
            if np.max(like_joint_dense) > 0
            else like_joint_dense
        )
        ax3.plot(
            x_dense,
            lj_norm,
            "green",
            linestyle="--",
            linewidth=2.2,
            label="Likelihood Congiunta w(x)",
        )
        evidenzia_riferimenti(ax3)
        ax3.set_ylabel("Verosimiglianza")
        ax3.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 4) Posteriori t (k) - Dopo pesatura e ricampionamento
        # ---------------------------------------------------------------------
        ax4.hist(
            particelle_post,
            bins=bins_vis,
            density=True,
            color="red",
            alpha=0.45,
            edgecolor="none",
            label=f"Posteriori t Ricampionata (k={k}, N_eff={neff_k:.1f}/{M})",
        )
        ax4.plot(
            particelle_post,
            np.zeros_like(particelle_post),
            "|",
            color="crimson",
            markersize=8,
            alpha=0.6,
        )
        evidenzia_riferimenti(ax4)
        ax4.set_ylabel("Posteriori t")
        ax4.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 5) Pannello Inferiore: Traiettorie e Stime Temporali
        # ---------------------------------------------------------------------
        ax_bot.plot(t_hist, x_det_hist, "k--", label="Posa Det.", alpha=0.7)
        ax_bot.plot(
            t_hist, x_sto_hist, "g-o", markersize=4, label="Posa Reale", linewidth=1.5
        )

        # Stime del Particle Filter
        ax_bot.plot(
            t_hist,
            x_pf_mean_hist,
            "r-s",
            markersize=4,
            label=r"Posa Stim. Media (PF) $\hat{x}_{\mathrm{media}}$",
            linewidth=2.0,
        )
        ax_bot.plot(
            t_hist,
            x_pf_mode_hist,
            color="darkorange",
            linestyle="-",
            markersize=4,
            label=r"Posa Stim. MAP/Moda (PF) $\hat{x}_{\mathrm{moda}}$",
            linewidth=1.8,
        )

        # Benchmark congiunto con Filtro ad Istogramma se attivo
        if self.confronta_histogram and x_fi_mean_hist is not None:
            ax_bot.plot(
                t_hist,
                x_fi_mean_hist,
                color="blue",
                linestyle="--",
                label="Posa Stim. Media (FI v10)",
                linewidth=1.5,
                alpha=0.8,
            )

        for idx, m in enumerate(self.landmarks):
            ax_bot.axhline(
                y=m, linestyle=":", alpha=0.6, label=f"Beacon m_{idx + 1}={m}"
            )

        ax_bot.set_xlim(0.0, self.L)
        ax_bot.set_xlabel("Posizione x / Dominio Mappa [0, L]")
        ax_bot.set_ylabel("Traiettoria")
        ax_bot.grid(True, linestyle=":", alpha=0.6)
        ax_bot.legend(loc="upper left", fontsize=7.0)

        nome_resampling = (
            metodo_resampling
            if metodo_resampling is not None
            else getattr(self, "metodo_resampling", "low_variance")
        )
        resampling_title = str(nome_resampling).replace("_", " ").title()

        fig.suptitle(
            f"Particle Filter 1D - Passo k = {k} / {N_iniziali} - Prior: {tipo_prior.capitalize()} "
            f"- Resampling: {resampling_title}",
            fontsize=11,
            fontweight="bold",
        )
        plt.tight_layout()

        # Salvataggio facoltativo su disco
        if self.salva:
            filename = f"particle_filter_{tipo_prior}_passo_{k}.png"
            fig.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"[INFO] Grafico salvato: '{filename}'")

        # Visualizzazione interattiva passo-passo
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
# 5. CLASSE ESPERIMENTO (Orchestratore e Confronto Diretto PF vs FI)
# =============================================================================
class EsperimentoLocalizzazionePF:
    """
    Coordina la simulazione reale, l'esecuzione del Particle Filter e
    il benchmark facoltativo con l'Histogram Filter sulla medesima traiettoria.
    """

    def __init__(
        self,
        simulatore: SimulatoreRobot1D,
        filtro_pf: FiltroParticelle1D,
        visualizzatore: VisualizzatoreLocalizzazione1D,
        filtro_fi: FiltroIstogramma1D = None,
        N_iniziali: int = 4,
    ):
        self.sim = simulatore
        self.pf = filtro_pf
        self.vis = visualizzatore
        self.fi = filtro_fi
        self.N_iniziali = int(N_iniziali)

    def esegui(self):
        # 1. Genera traiettoria reale e misure del simulatore
        x_det, x_sto, z_sto = self.sim.genera_traiettoria()

        T = self.sim.T_finale
        # Strutture dati per le stime del Particle Filter
        x_pf_mean = np.zeros(T + 1, dtype=float)
        x_pf_mode = np.zeros(T + 1, dtype=float)
        sigma_pf = np.zeros(T + 1, dtype=float)
        neff_pf = np.zeros(T + 1, dtype=float)

        # Strutture dati per il Filtro ad Istogramma (se abilitato)
        x_fi_mean = np.zeros(T + 1, dtype=float) if self.fi is not None else None
        x_fi_mode = np.zeros(T + 1, dtype=float) if self.fi is not None else None

        # Stime iniziali al passo t = 0
        particelle_curr = self.pf.particelle.copy()
        pesi_curr = self.pf.pesi.copy()

        x_pf_mean[0] = self.pf.calcola_stima_media(particelle_curr, pesi_curr)
        x_pf_mode[0] = self.pf.calcola_stima_moda(particelle_curr, pesi_curr)
        sigma_pf[0] = self.pf.calcola_dispersione(particelle_curr, x_pf_mean[0], pesi_curr)
        neff_pf[0] = self.pf.calcola_neff(pesi_curr)

        if self.fi is not None:
            b_fi_curr = self.fi.belief.copy()
            x_fi_mean[0] = self.fi.calcola_stima_media(b_fi_curr)
            x_fi_mode[0] = self.fi.calcola_stima_moda(b_fi_curr)

        # 2. Ciclo temporale di stima bayesiana
        for k in range(1, T + 1):
            particelle_prev = particelle_curr.copy()

            # --- PARTICLE FILTER: CICLO PREDIZIONE - CORREZIONE - RICAMPIONAMENTO ---
            # a) Predizione: campiona dal modello di moto (Proposal g)
            particelle_pred = self.pf.passo_predizione(particelle_prev)

            # b) Correzione: calcola i pesi di importanza tramite verosimiglianza di misura
            pesi_norm, pesi_grezzi, like_singole = self.pf.calcola_pesi_misura(
                particelle_pred, z_sto[k]
            )

            # c) Diagnostica di degenerazione
            neff_k = self.pf.calcola_neff(pesi_norm)
            neff_pf[k] = neff_k

            # d) Calcolo stime di posa prima o durante il ricampionamento
            x_pf_mean[k] = self.pf.calcola_stima_media(particelle_pred, pesi_norm)
            x_pf_mode[k] = self.pf.calcola_stima_moda(particelle_pred, pesi_norm)
            sigma_pf[k] = self.pf.calcola_dispersione(
                particelle_pred, x_pf_mean[k], pesi_norm
            )

            # e) Ricampionamento con rimpiazzo (Target f)
            particelle_post = self.pf.ricampionamento(particelle_pred, pesi_norm)
            particelle_curr = particelle_post.copy()

            # --- FILTRO AD ISTOGRAMMA (BENCHMARK CONGIUNTO) ---
            if self.fi is not None:
                b_fi_pred = self.fi.passo_predizione(b_fi_curr)
                b_fi_curr, _, _ = self.fi.passo_correzione(b_fi_pred, z_sto[k])
                x_fi_mean[k] = self.fi.calcola_stima_media(b_fi_curr)
                x_fi_mode[k] = self.fi.calcola_stima_moda(b_fi_curr)

            # --- VISUALIZZAZIONE PASSO-PASSO DEI PRIMI PASSI ---
            if k <= self.N_iniziali:
                self.vis.mostra_passo_dettagliato(
                    k=k,
                    N_iniziali=self.N_iniziali,
                    particelle_prev=particelle_prev,
                    particelle_pred=particelle_pred,
                    particelle_post=particelle_post,
                    pesi_norm=pesi_norm,
                    z_k=z_sto[k],
                    sigma_z=self.pf.sigma_z_loc,
                    x_sto_k=x_sto[k],
                    t_hist=np.arange(k + 1),
                    x_det_hist=x_det[: k + 1],
                    x_sto_hist=x_sto[: k + 1],
                    x_pf_mean_hist=x_pf_mean[: k + 1],
                    x_pf_mode_hist=x_pf_mode[: k + 1],
                    x_fi_mean_hist=x_fi_mean[: k + 1] if self.fi is not None else None,
                    x_fi_mode_hist=x_fi_mode[: k + 1] if self.fi is not None else None,
                    tipo_prior=self.pf.tipo_prior,
                    neff_k=neff_k,
                    M=self.pf.M,
                    metodo_resampling=self.pf.metodo_resampling,
                )

        t_axis = np.arange(T + 1)
        risultati = {
            "t": t_axis,
            "x_det": x_det,
            "x_sto": x_sto,
            "z_sto": z_sto,
            "x_pf_mean": x_pf_mean,
            "x_pf_mode": x_pf_mode,
            "sigma_pf": sigma_pf,
            "neff_pf": neff_pf,
            "x_fi_mean": x_fi_mean,
            "x_fi_mode": x_fi_mode,
        }
        return risultati


# =============================================================================
# ESECUZIONE E COMPARAZIONE FINALE (Main Script)
# =============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("AVVIO SIMULAZIONE: 1D PARTICLE FILTER (Monte Carlo Localization)")
    print("Confronto Sperimentale Diretto con Histogram Filter (v10)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # PARAMETRI AMBIENTALI E CONFIGURAZIONE MISSIONE
    # -------------------------------------------------------------------------
    L_MAPPA: float = 100.0  # Lunghezza del segmento 1D [0, L]
    BEACONS: list = [40]  # Posizione del/i beacon noto/i (es. [25.0] o [25.0, 75.0])
    T_FINALE: int = 80  # Orizzonte temporale di simulazione
    U_NOMINALE: float = 0.8  # Comando di avanzamento nominale

    # Parametri di rumore
    SIGMA_X_SIM: float = 0.5  # Deviazione standard rumore di moto reale
    SIGMA_Z_SIM: float = 1.5  # Deviazione standard rumore di misura reale
    SEED_SIMULAZIONE: int = 42  # Seed deterministico per riproducibilità (None per casuale)

    # -------------------------------------------------------------------------
    # FLAG DI CONTROLLO OPERATIVO
    # -------------------------------------------------------------------------
    ATTIVA_VISUALIZZAZIONE_PF: bool = True  # True per animazione grafica passo-passo
    ATTIVA_SALVATAGGIO_PF: bool = False  # True per salvare su file PNG i grafici
    ATTIVA_CONFRONTO_HISTOGRAM: bool = True  # True per eseguire e confrontare anche il FI v10
    PASSI_VISUALIZZAZIONE: int = 4  # Numero di passi iniziali mostrati in dettaglio

    # -------------------------------------------------------------------------
    # PARAMETRI SPECIFICI DEI FILTRI
    # -------------------------------------------------------------------------
    TIPO_PRIOR: str = "gaussiana"  # 'gaussiana' (Position Tracking) o 'uniforme' (Global Localization)
    X0_PRIOR: float = 0.0
    SIGMA_PRIOR: float = 1.0

    # Configurazione Particle Filter
    NUMERO_PARTICELLE_M: int = 1000  # Cardinalità della popolazione M
    METODO_RESAMPLING: str = (
        "low_variance"  # 'low_variance' (consigliato O(M)) o 'roulette_wheel'
    )

    # Configurazione Histogram Filter (Benchmark)
    BIN_SIZE_FI: float = 0.5  # Risoluzione spaziale griglia (200 celle)

    # -------------------------------------------------------------------------
    # 1. Istanziazione del Simulatore
    # -------------------------------------------------------------------------
    simulatore = SimulatoreRobot1D(
        L=L_MAPPA,
        x0=0.0,
        T_finale=T_FINALE,
        u_x=U_NOMINALE,
        landmarks=BEACONS,
        sigma_x_sim=SIGMA_X_SIM,
        sigma_z_sim=SIGMA_Z_SIM,
        seed=SEED_SIMULAZIONE,
    )

    # -------------------------------------------------------------------------
    # 2. Istanziazione del Filtro a Particelle (MCL)
    # -------------------------------------------------------------------------
    filtro_pf = FiltroParticelle1D(
        L=L_MAPPA,
        u_x=U_NOMINALE,
        landmarks=BEACONS,
        M=NUMERO_PARTICELLE_M,
        sigma_x_loc=SIGMA_X_SIM,
        sigma_z_loc=SIGMA_Z_SIM,
        tipo_prior=TIPO_PRIOR,
        sigma_prior=SIGMA_PRIOR,
        x0_prior=X0_PRIOR,
        metodo_resampling=METODO_RESAMPLING,
        gestione_bordi="clip",
    )

    # -------------------------------------------------------------------------
    # 3. Istanziazione del Filtro ad Istogramma (Opzionale per Benchmark)
    # -------------------------------------------------------------------------
    filtro_fi = None
    if ATTIVA_CONFRONTO_HISTOGRAM:
        filtro_fi = FiltroIstogramma1D(
            L=L_MAPPA,
            u_x=U_NOMINALE,
            landmarks=BEACONS,
            bin_size=BIN_SIZE_FI,
            sigma_x_loc=SIGMA_X_SIM,
            sigma_z_loc=SIGMA_Z_SIM,
            tipo_prior=TIPO_PRIOR,
            sigma_prior=SIGMA_PRIOR,
            x0_prior=X0_PRIOR,
        )

    # -------------------------------------------------------------------------
    # 4. Istanziazione del Visualizzatore
    # -------------------------------------------------------------------------
    visualizzatore = VisualizzatoreLocalizzazione1D(
        L=L_MAPPA,
        landmarks=BEACONS,
        visualizza=ATTIVA_VISUALIZZAZIONE_PF,
        salva=ATTIVA_SALVATAGGIO_PF,
        confronta_histogram=ATTIVA_CONFRONTO_HISTOGRAM,
        metodo_resampling=METODO_RESAMPLING,
    )

    # -------------------------------------------------------------------------
    # 5. Esecuzione dell'Esperimento
    # -------------------------------------------------------------------------
    esperimento = EsperimentoLocalizzazionePF(
        simulatore=simulatore,
        filtro_pf=filtro_pf,
        visualizzatore=visualizzatore,
        filtro_fi=filtro_fi,
        N_iniziali=PASSI_VISUALIZZAZIONE,
    )

    res = esperimento.esegui()

    t = res["t"]
    x_det = res["x_det"]
    x_sto = res["x_sto"]
    x_pf_mean = res["x_pf_mean"]
    x_pf_mode = res["x_pf_mode"]
    sigma_pf = res["sigma_pf"]
    neff_pf = res["neff_pf"]

    # Calcolo metriche prestazionali (Errore Assoluto Medio e RMSE)
    err_pf_mean = np.abs(x_sto - x_pf_mean)
    err_pf_mode = np.abs(x_sto - x_pf_mode)
    mae_pf_mean = np.mean(err_pf_mean)
    rmse_pf_mean = np.sqrt(np.mean((x_sto - x_pf_mean) ** 2))

    print("\n" + "=" * 50)
    print("METRICHE PRESTAZIONALI - PARTICLE FILTER (MCL):")
    print(f"  * MAE Media Pesata:   {mae_pf_mean:.3f} m")
    print(f"  * RMSE Media Pesata:  {rmse_pf_mean:.3f} m")
    print(f"  * MAE Moda/MAP:       {np.mean(err_pf_mode):.3f} m")
    print(f"  * N_eff Medio:        {np.mean(neff_pf):.1f} / {NUMERO_PARTICELLE_M}")
    print("=" * 50)

    if ATTIVA_CONFRONTO_HISTOGRAM:
        x_fi_mean = res["x_fi_mean"]
        x_fi_mode = res["x_fi_mode"]
        err_fi_mean = np.abs(x_sto - x_fi_mean)
        mae_fi_mean = np.mean(err_fi_mean)
        rmse_fi_mean = np.sqrt(np.mean((x_sto - x_fi_mean) ** 2))
        print("METRICHE PRESTAZIONALI - HISTOGRAM FILTER (v10):")
        print(f"  * MAE Media Discreta: {mae_fi_mean:.3f} m")
        print(f"  * RMSE Media:         {rmse_fi_mean:.3f} m")
        print(f"  * MAE Moda/MAP:       {np.mean(np.abs(x_sto - x_fi_mode)):.3f} m")
        print("=" * 50 + "\n")

    # -------------------------------------------------------------------------
    # 6. GRAFICO FINALE RIASSUNTIVO (3 Subplot di Analisi)
    # -------------------------------------------------------------------------
    fig_final, (ax1, ax2, ax3) = plt.subplots(
        3, 1, figsize=(11, 9.5), sharex=True, gridspec_kw={"height_ratios": [1.2, 1, 0.8]}
    )

    # Subplot 1: Traiettorie a confronto
    ax1.plot(t, x_det, "k--", label="Posa Deterministica", alpha=0.5)
    ax1.plot(t, x_sto, "g-", label="Posa Reale (Ground Truth)", linewidth=1.8)
    ax1.plot(
        t,
        x_pf_mean,
        "r-.",
        label=r"Stima Media PF $\hat{x}_{\mathrm{media}}$",
        linewidth=2.0,
    )
    ax1.plot(
        t,
        x_pf_mode,
        color="darkorange",
        linestyle=":",
        label=r"Stima Moda/MAP PF $\hat{x}_{\mathrm{moda}}$",
        linewidth=1.8,
    )
    if ATTIVA_CONFRONTO_HISTOGRAM:
        ax1.plot(
            t,
            x_fi_mean,
            color="blue",
            linestyle="--",
            label="Stima Media FI (v10)",
            linewidth=1.4,
            alpha=0.85,
        )
    for idx, m in enumerate(BEACONS):
        ax1.axhline(y=m, linestyle=":", color="purple", alpha=0.7, label=f"Beacon m_{idx + 1}={m}")
    ax1.set_ylabel("Posizione x [m]")
    ax1.set_title(
        f"Confronto Finale Localizzazione 1D (Prior: {TIPO_PRIOR.capitalize()}, "
        f"Particelle M={NUMERO_PARTICELLE_M}, Resampling: {METODO_RESAMPLING})",
        fontweight="bold",
    )
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=8)

    # Subplot 2: Errori Assoluti nel Tempo
    ax2.plot(
        t,
        err_pf_mean,
        "r-",
        label=f"Errore PF Media (MAE: {mae_pf_mean:.2f} m)",
        linewidth=1.8,
    )
    ax2.plot(
        t,
        err_pf_mode,
        color="darkorange",
        linestyle=":",
        label=f"Errore PF MAP (MAE: {np.mean(err_pf_mode):.2f} m)",
        linewidth=1.5,
    )
    if ATTIVA_CONFRONTO_HISTOGRAM:
        ax2.plot(
            t,
            err_fi_mean,
            "b--",
            label=f"Errore FI Media (MAE: {mae_fi_mean:.2f} m)",
            linewidth=1.4,
            alpha=0.85,
        )
    ax2.set_ylabel("Errore Assoluto [m]")
    ax2.set_title("Confronto Errore di Stima nel Tempo (|Posa Reale - Stima|)")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=8)

    # Subplot 3: Diagnostica dell'Incertezza (Dispersione particelle e N_eff)
    ax3_twin = ax3.twinx()
    p1 = ax3.plot(
        t,
        sigma_pf,
        color="magenta",
        linestyle="-",
        label=r"Dispersione Nube $\sigma_{\mathrm{PF}}$ [m]",
        linewidth=1.6,
    )
    p2 = ax3_twin.plot(
        t,
        neff_pf,
        color="teal",
        linestyle="-.",
        label=r"Dimensione Efficace $N_{\mathrm{eff}}$",
        linewidth=1.6,
    )
    ax3.set_xlabel("Passo Temporale k")
    ax3.set_ylabel(r"Incertezza $\sigma_{\mathrm{PF}}$ [m]", color="magenta")
    ax3_twin.set_ylabel(r"$N_{\mathrm{eff}}$ [campioni]", color="teal")
    ax3.grid(True, linestyle=":", alpha=0.6)

    # Unione legende su asse twin
    lines = p1 + p2
    labels = [l.get_label() for l in lines]
    ax3.legend(lines, labels, loc="upper right", fontsize=8)
    ax3.set_title("Diagnostica di Convergenza e Degenerazione del Particle Filter")

    plt.tight_layout()
    plt.show()
