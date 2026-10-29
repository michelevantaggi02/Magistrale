r"""
===============================================================================
BENCHMARK FILTRI DI LOCALIZZAZIONE ROBOTICA 1D: HF vs PF vs EKF
Codice per Autonomous Robotics, a.a. 2026/2027
Università di Perugia, Dipartimento di Ingegneria

Riferimenti:
- S. Thrun, W. Burgard, D. Fox, "Probabilistic Robotics", MIT Press (Cap. 3, 7 e 8).
- Slide di Lezione Prof. Paolo Valigi:
  * "Mobile Robot Localization - Kalman Filter for Localization" (26.10.2026)
  * "Mobile Robot Localization - Particle Filter" e "Histogram Filter"

ARCHITETTURA DEI MODELLI E FILTRI IMPLEMENTATI:

1) MODELLO DI MOTO (Cinematica 1D con rumore gaussiano additivo):
   - Modello di stato: x_k = x_{k-1} + u_k + nu_k, con nu_k ~ N(0, sigma_x^2)
   - Moto Deterministico di riferimento: x_{det, k} = x_{det, k-1} + u_k
   - Moto Stocastico Reale (Ground Truth): x_{sto, k} = x_{sto, k-1} + u_k + nu_k

2) MODELLO DI MISURA (Sensore Range-Only da beacon puntiformi noti m_j):
   - Misure generate dal simulatore: z_{j, k} = |x_{sto, k} - m_j| + w_{j, k}, con w_{j, k} ~ N(0, sigma_z^2)
   - Modello non-lineare atteso: h(x, m_j) = |x - m_j|

3) FILTRI DI LOCALIZZAZIONE A CONFRONTO:
   - Filtro ad Istogramma (HF - Griglia discreta non parametrica):
     Discretizzazione dello spazio di stato in bin, convoluzione per predizione e
     aggiornamento puntuale Bayesiano. Gestisce distribuzioni arbitrarie e multimodali.
   - Filtro a Particelle (PF - Sequential Monte Carlo):
     Rappresentazione campionaria non parametrica con Importance Sampling e Resampling.
     Pesi calcolati ad ogni passo come verosimiglianza congiunta dei beacon.
   - Filtro di Kalman Esteso (EKF - Gaussiano / Parametrico):
     Linearizzazione analitica al primo ordine tramite sviluppo di Taylor:
     * Jacobiano di moto: F_x = 1.0, F_u = 1.0
     * Jacobiano di misura: H_x^j = sgn(x_hat - m_j) = (x_hat - m_j) / |x_hat - m_j|
     * Innovazione: y_tilde = z - z_hat
     * Guadagno di Kalman vettoriale K e aggiornamento simmetrico di Joseph per P.
     * Calcolo delle distanze quadratiche di Mahalanobis mu_j.

4) VISUALIZZAZIONE DETTAGLIATA A 5 SUBPLOT (HF, PF ed EKF):
   - Plot 1: Posteriori t-1 (Belief HF + Particelle PF + Densità Gaussiana EKF).
   - Plot 2: Prior t (Belief HF preditto + Particelle PF predette + Gaussiana EKF preditta).
   - Plot 3: Verosimiglianza dei beacon (Curva HF + Barre PF + Punto di linearizzazione EKF).
   - Plot 4: Posteriori t (Belief HF aggiornato + Particelle ri-campionate + Gaussiana EKF aggiornata).
   - Plot 5: Traiettoria nel tempo (Posa Reale, Deterministica, Stime HF, PF ed EKF con inviluppo 2-sigma).
===============================================================================
"""

import math
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 1. CLASSE SIMULATORE (Mondo Reale e Generazione Dati Sincrona)
# =============================================================================
class SimulatoreRobot1D:
    """
    Simula la fisica e la cinematica del robot e dei sensori in tempo reale.
    """

    def __init__(
        self,
        L: float = 100.0,
        x0: float = 0.0,
        u_x: float = 0.8,
        landmarks: list = None,
        sigma_x_sim: float = 0.5,
        sigma_z_sim: float = 1.5,
        seed: int = 42,
    ):
        if seed is not None:
            np.random.seed(seed)

        self.L = L
        self.x0 = x0
        self.u_x = u_x
        self.landmarks = list(landmarks) if landmarks is not None else [30.0, 70.0]
        self.sigma_x_sim = sigma_x_sim
        self.sigma_z_sim = sigma_z_sim

        self.x_det_k = x0
        self.x_sto_k = x0

    def passo_simulazione(self) -> tuple:
        """
        Esegue un singolo passo di simulazione (moto + generazione misure).
        Restituisce: (x_det, x_sto, z_sto)
        """
        self.x_det_k += self.u_x

        rumore_moto = np.random.normal(0, self.sigma_x_sim)
        self.x_sto_k += self.u_x + rumore_moto

        z_sto = []
        for m in self.landmarks:
            z_aspettata = abs(self.x_sto_k - m)
            rumore_misura = np.random.normal(0, self.sigma_z_sim)
            z_sto.append(z_aspettata + rumore_misura)

        return self.x_det_k, self.x_sto_k, np.array(z_sto)


# =============================================================================
# 2. CLASSE FILTRO AD ISTOGRAMMA (Bayesian Discrete Filter)
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
        grid_i, grid_j = np.meshgrid(self.bin_centers, self.bin_centers, indexing="ij")
        delta_x = grid_i - (grid_j + self.u_x)
        self.transition_matrix = np.exp(-0.5 * (delta_x / self.sigma_x_loc) ** 2) / (
            self.sigma_x_loc * np.sqrt(2 * np.pi)
        )
        self.transition_matrix /= np.sum(self.transition_matrix, axis=0, keepdims=True)

    def modello_misura_inverso(self, z_misure: np.ndarray):
        like_singole = []
        like_joint = np.ones(self.n_bins)

        for i, m in enumerate(self.landmarks):
            z_exp = np.abs(self.bin_centers - m)
            like_i = np.exp(-0.5 * ((z_misure[i] - z_exp) / self.sigma_z_loc) ** 2)
            like_singole.append(like_i)
            like_joint *= like_i

        return like_singole, like_joint

    def passo_predizione(self) -> np.ndarray:
        self.belief = self.transition_matrix @ self.belief
        return self.belief.copy()

    def passo_correzione(self, z_misure: np.ndarray):
        like_singole, like_joint = self.modello_misura_inverso(z_misure)
        belief_updated = self.belief * like_joint
        sum_b = np.sum(belief_updated)

        self.belief = belief_updated / sum_b if sum_b > 0 else self.belief
        return self.belief.copy(), like_singole, like_joint

    def calcola_stima_media(self) -> float:
        return float(np.sum(self.bin_centers * self.belief))

    def calcola_stima_moda(self) -> float:
        idx_max = np.argmax(self.belief)
        return float(self.bin_centers[idx_max])


# =============================================================================
# 3. CLASSE FILTRO A PARTICELLE (Sequential Monte Carlo Base)
# =============================================================================
class ParticleFilter1D:
    """
    Implementazione del Particle Filter BASE:
    - Pesi calcolati ad ogni passo esclusivamente come la Likelihood al passo corrente.
    - Resampling eseguito ad ogni passo k.
    """

    def __init__(
        self,
        N_particles: int = 500,
        L: float = 100.0,
        u_x: float = 0.8,
        landmarks: list = None,
        sigma_x_loc: float = 0.5,
        sigma_z_loc: float = 1.5,
        tipo_prior: str = "gaussiana",
        sigma_prior: float = 1.0,
        x0_prior: float = 0.0,
        metodo_resampling: str = "importance",
    ):
        self.N = N_particles
        self.L = L
        self.u_x = u_x
        self.landmarks = landmarks if landmarks is not None else [30.0, 70.0]
        self.sigma_x_loc = sigma_x_loc
        self.sigma_z_loc = sigma_z_loc
        self.tipo_prior = tipo_prior.lower()
        self.sigma_prior = sigma_prior
        self.x0_prior = x0_prior
        self.metodo_resampling = metodo_resampling.lower()

        self.particles = np.zeros(self.N)
        self.weights = np.ones(self.N) / self.N
        self.inizializza_particelle()

    def inizializza_particelle(self):
        if self.tipo_prior == "uniforme":
            self.particles = np.random.uniform(0.0, self.L, self.N)
        elif self.tipo_prior == "gaussiana":
            self.particles = np.random.normal(self.x0_prior, self.sigma_prior, self.N)
            self.particles = np.clip(self.particles, 0.0, self.L)
        else:
            raise ValueError("tipo_prior deve essere 'gaussiana' o 'uniforme'")

        self.weights = np.ones(self.N) / self.N

    def passo_predizione(self, u: float = None) -> tuple:
        """
        Passo di predizione (Prior t): applica la cinematica di moto.
        I pesi a priori per le nuove particelle sono uniformi (1/N) a causa del resampling a t-1.
        """
        u_val = u if u is not None else self.u_x
        rumore = np.random.normal(0.0, self.sigma_x_loc, size=self.N)

        self.particles = self.particles + u_val + rumore
        self.particles = np.clip(self.particles, 0.0, self.L)

        self.weights = np.ones(self.N) / self.N
        return self.particles.copy(), self.weights.copy()

    def passo_correzione(self, z_misure: np.ndarray) -> tuple:
        """
        Passo di correzione BASE:
        1. I pesi sono ricalcolati esclusivamente come la verosimiglianza Likelihood al passo corrente.
        2. Viene ESEGUITO SEMPRE il resampling ad ogni passo k.
        """
        like_singole = []
        like_joint = np.ones(self.N)

        for i, m in enumerate(self.landmarks):
            z_exp = np.abs(self.particles - m)
            like_i = np.exp(-0.5 * ((z_misure[i] - z_exp) / self.sigma_z_loc) ** 2)
            like_singole.append(like_i)
            like_joint *= like_i

        weights_current_like = like_joint.copy()
        sum_w = np.sum(weights_current_like)

        if sum_w > 0:
            weights_current_like /= sum_w
        else:
            weights_current_like = np.ones(self.N) / self.N

        self.weights = weights_current_like.copy()

        # Resampling ad ogni passo k
        if self.metodo_resampling == "importance":
            self.resample_importance_sampling()
        elif self.metodo_resampling == "low_variance":
            self.resample_low_variance()

        return (
            like_singole,
            like_joint,
            weights_current_like,
            self.particles.copy(),
            self.weights.copy(),
        )

    def resample_importance_sampling(self):
        indices = np.random.choice(self.N, size=self.N, replace=True, p=self.weights)
        self.particles = self.particles[indices]
        self.weights = np.ones(self.N) / self.N

    def resample_low_variance(self):
        new_particles = np.zeros(self.N)
        cumulative_sum = np.cumsum(self.weights)
        step = 1.0 / self.N
        r = np.random.uniform(0.0, step)

        i = 0
        for j in range(self.N):
            u = r + j * step
            while u > cumulative_sum[i] and i < self.N - 1:
                i += 1
            new_particles[j] = self.particles[i]

        self.particles = new_particles
        self.weights = np.ones(self.N) / self.N

    def calcola_stima_media(self) -> float:
        return float(np.sum(self.particles * self.weights))

    def calcola_stima_moda(self, n_bins: int = 50) -> float:
        counts, bin_edges = np.histogram(
            self.particles, bins=n_bins, range=(0.0, self.L), weights=self.weights
        )
        max_idx = np.argmax(counts)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        return float(bin_centers[max_idx])


# =============================================================================
# 4. CLASSE FILTRO DI KALMAN ESTESO 1D (Extended Kalman Filter - EKF)
# =============================================================================
class ExtendedKalmanFilter1D:
    r"""
    Filtro di Kalman Esteso (EKF) per la localizzazione unidimensionale (1D).

    Riferimenti Teorici:
    - Slide Lezione Prof. Paolo Valigi:
      'Mobile Robot Localization - Kalman Filter for Localization' (26.10.2026).
    - Probabilistic Robotics (S. Thrun, W. Burgard, D. Fox), Cap. 3 e Cap. 7.

    MOTIVAZIONE DELL'EKF RISPETTO AL KALMAN FILTER LINEARE STANDARD (KF):
    Nel problema di localizzazione 1D con sensore range-only (misura di distanza
    da beacon noti), il modello di misura:
        h(x, m_j) = |x - m_j|
    presenta una non-linearità fondamentale dovuta al modulo (valore assoluto).
    Poiché le equazioni di misura non sono lineari nella variabile di stato x,
    il KF standard non è applicabile e si ricorre all'EKF, che linearizza
    il modello di misura calcolando lo Jacobiano H_x al primo ordine (sviluppo di Taylor)
    attorno alla migliore stima a priori corrente x_hat_{t|t-1}.

    MODELLO DI STATO E MOTO (Slide 4 e Slide 9):
        x_t = f(x_{t-1}, u_t + w_t) = x_{t-1} + u_t + w_t
        w_t ~ N(0, Q_t), con Q_t = sigma_x_loc^2

        Jacobiani analitici del moto:
            F_x = df/dx = 1.0
            F_u = df/du = 1.0

        Fase di Predizione A Priori (Slide 4):
            x_hat_{t|t-1} = x_hat_{t-1|t-1} + u_t
            P_{t|t-1} = F_x * P_{t-1|t-1} * F_x^T + F_u * Q_t * F_u^T
                      = P_{t-1|t-1} + Q_t

    MODELLO DI MISURA E CORREZIONE A POSTERIORI (Slide 5, Slide 7 e Slide 9):
        Vettore di misure dai beacon puntiformi noti m_j (j = 1, ..., M):
            z_t^j = h(x_t, m_j) + v_t^j = |x_t - m_j| + v_t^j
            v_t^j ~ N(0, R_t), con R_t = sigma_z_loc^2

        Misura attesa (predizione di misura):
            z_hat_t^j = h(x_hat_{t|t-1}, m_j) = |x_hat_{t|t-1} - m_j|

        Jacobiano analitico del modello di misura (Slide 9):
            H_x^j = dh/dx|_{x_hat} = sgn(x_hat_{t|t-1} - m_j) = (x_hat - m_j) / |x_hat - m_j|
            (Nel punto singolare x_hat == m_j si adotta la convenzione di subgradiente +1.0).

        Innovazione di misura (Slide 5 e Slide 7):
            y_tilde_t^j = z_t^j - z_hat_t^j

        Formulazione Vettoriale per Misure Multiple Simultanee (Slide 7):
            S_t = H * P_{t|t-1} * H^T + R_mat    [Matrice di covarianza dell'innovazione]
            K_t = P_{t|t-1} * H^T * S_t^(-1)     [Matrice / Vettore del Guadagno di Kalman]
            x_hat_{t|t} = x_hat_{t|t-1} + K_t * y_tilde_t   [Aggiornamento dello stato]
            P_{t|t} = (I - K_t * H) * P_{t|t-1}             [Aggiornamento della covarianza]
            (Implementato tramite forma simmetrica di Joseph per garantire la stabilità numerica).

        Distanza di Mahalanobis per Data Association (Slide 7 riga 7):
            mu_j = (y_tilde_j)^2 / S_{jj}
    """

    def __init__(
        self,
        L: float = 100.0,
        u_x: float = 0.8,
        landmarks: list = None,
        sigma_x_loc: float = 0.5,
        sigma_z_loc: float = 1.5,
        tipo_prior: str = "gaussiana",
        sigma_prior: float = 1.0,
        x0_prior: float = 0.0,
        x0: float = None,
        P0: float = None,
    ):
        self.L = float(L)
        self.u_x = float(u_x)
        self.landmarks = list(landmarks) if landmarks is not None else [30.0, 70.0]
        self.sigma_x_loc = float(sigma_x_loc)
        self.sigma_z_loc = float(sigma_z_loc)
        self.tipo_prior = tipo_prior.lower()
        self.sigma_prior = float(sigma_prior)
        self.x0_prior = float(x0_prior)

        # Matrici/scalari di rumore di processo (Q) e di misura (R)
        self.Q = float(self.sigma_x_loc ** 2)
        self.R_val = float(self.sigma_z_loc ** 2)

        self.x0_custom = x0
        self.P0_custom = P0

        # Stato stocastico: media stimata x_hat e varianza dell'errore P
        self.x = 0.0
        self.P = 1.0
        self.inizializza_stato()

    def inizializza_stato(self):
        """
        Inizializza la stima dello stato e la covarianza iniziale (Slide 5):
            x_0 ~ N(x_bar_0, P_0) => x_hat_0 = x_bar_0, P_{0|0} = P_0
        """
        if self.x0_custom is not None and self.P0_custom is not None:
            self.x = float(self.x0_custom)
            self.P = float(self.P0_custom)
        elif self.tipo_prior == "gaussiana":
            self.x = float(self.x0_prior)
            self.P = float(self.sigma_prior ** 2)
        elif self.tipo_prior == "uniforme":
            # Approssimazione Gaussiana di una distribuzione uniforme U(0, L):
            # media = L / 2, varianza = L^2 / 12
            self.x = float(self.L / 2.0)
            self.P = float((self.L ** 2) / 12.0)
        else:
            raise ValueError(f"tipo_prior non valido: '{self.tipo_prior}'")

    def passo_predizione(self, u: float = None) -> tuple:
        """
        Fase di Predizione A Priori (Prior t) - Slide 4 e Slide 7:
            x_hat_{t|t-1} = x_hat_{t-1|t-1} + u_t
            P_{t|t-1} = P_{t-1|t-1} + Q_t
        Restituisce: (x_pred, P_pred)
        """
        u_val = float(u) if u is not None else self.u_x

        # Applicazione cinematica di traslazione 1D
        self.x = self.x + u_val
        # Propagazione dell'incertezza con il rumore di processo Q
        self.P = self.P + self.Q

        return self.x, self.P

    def passo_correzione(self, z_misure: np.ndarray) -> tuple:
        r"""
        Fase di Correzione A Posteriori (Posteriori t) - Slide 5 e Slide 7:
        Implementa l'aggiornamento vettoriale simultaneo per tutti i beacon osservati.

        Restituisce:
            (x_post, P_post, z_hat, y_innov, K, S, distanze_mahalanobis)
        """
        m = len(self.landmarks)
        z = np.asarray(z_misure, dtype=float).reshape(-1, 1)

        # 1. Calcolo delle misure attese z_hat e del vettore Jacobiano H (Slide 7 riga 5-6)
        z_hat = np.zeros((m, 1), dtype=float)
        H = np.zeros((m, 1), dtype=float)

        for j, landmark_pos in enumerate(self.landmarks):
            diff = self.x - landmark_pos
            z_hat[j, 0] = abs(diff)

            # Derivata della distanza assoluta d|x - m|/dx = sgn(x - m) (Slide 9)
            if abs(diff) < 1e-6:
                # Singolarità nel punto di inversione (convenzione subgradiente)
                H[j, 0] = 1.0
            else:
                H[j, 0] = 1.0 if diff > 0.0 else -1.0

        # 2. Vettore di Innovazione (Slide 5 e Slide 7 riga 8): y_tilde = z - z_hat
        y_tilde = z - z_hat

        # 3. Matrice di Covarianza del rumore di misura R (diag(sigma_z^2))
        R = np.eye(m, dtype=float) * self.R_val

        # 4. Matrice di Covarianza dell'Innovazione S (Slide 5 e Slide 7 riga 10):
        # S = H * P * H^T + R  (dimensione M x M)
        S = self.P * (H @ H.T) + R

        # 5. Guadagno di Kalman K (Slide 5 e Slide 7 riga 11):
        # K = P * H^T * S^(-1)  (dimensione 1 x M)
        S_inv = np.linalg.inv(S)
        K = self.P * (H.T @ S_inv)

        # 6. Aggiornamento dello Stato (Slide 5 e Slide 7 riga 12):
        # x_hat_{t|t} = x_hat_{t|t-1} + K * y_tilde
        delta_x = float((K @ y_tilde).item())
        x_post = self.x + delta_x

        # 7. Aggiornamento della Covarianza dell'errore (Slide 5 e Slide 7 riga 13):
        # Utilizzo della Forma Simmetrica di Joseph:
        # P_{t|t} = (I - K*H) * P * (I - K*H)^T + K * R * K^T
        # che garantisce analiticamente simmetria e semi-definita positività numerica.
        KH = float((K @ H).item())
        I_KH = 1.0 - KH
        P_post = (I_KH ** 2) * self.P + float((K @ R @ K.T).item())

        # Vincoli fisici di consistenza: mappa limitata [0, L] e varianza minima
        self.x = float(np.clip(x_post, 0.0, self.L))
        self.P = float(max(P_post, 1e-9))

        # 8. Calcolo delle Distanze di Mahalanobis per ciascun beacon (Slide 7 riga 7):
        # mu_j = (y_tilde_j)^2 / S_{jj}
        mahalanobis = []
        for j in range(m):
            s_jj = S[j, j]
            mu_j = float((y_tilde[j, 0] ** 2) / s_jj) if s_jj > 0.0 else 0.0
            mahalanobis.append(mu_j)

        return (
            self.x,
            self.P,
            z_hat.flatten(),
            y_tilde.flatten(),
            K.flatten(),
            S,
            np.array(mahalanobis),
        )

    def calcola_stima_media(self) -> float:
        """Nei filtri gaussiani (EKF), la stima a posteriori coincide con la media."""
        return float(self.x)

    def calcola_stima_moda(self) -> float:
        """Per la densità gaussiana simmetrica unimodale, moda == media."""
        return float(self.x)

    def calcola_deviazione_standard(self) -> float:
        """Restituisce la deviazione standard corrente sigma = sqrt(P)."""
        return float(np.sqrt(self.P))

    def valuta_pdf_gaussiana(
        self,
        x_grid: np.ndarray,
        mu: float = None,
        P: float = None,
        come_massa_bin: bool = True,
    ) -> np.ndarray:
        r"""
        Calcola la distribuzione normale N(mu, P) sui punti di x_grid.
        Se come_massa_bin=True e x_grid è equispaziata, restituisce la massa di
        probabilità per intervallo (PDF * dx), rendendola direttamente sommabile a 1
        e confrontabile sulla stessa scala dell'istogramma (HF).
        """
        mu_val = self.x if mu is None else float(mu)
        P_val = self.P if P is None else float(P)
        P_val = max(P_val, 1e-12)

        pdf = (1.0 / np.sqrt(2.0 * np.pi * P_val)) * np.exp(
            -0.5 * ((x_grid - mu_val) ** 2) / P_val
        )
        if come_massa_bin and len(x_grid) > 1:
            dx = float(x_grid[1] - x_grid[0])
            return pdf * dx
        return pdf


# =============================================================================
# 5. VISUALIZZATORE (Grafica a 5 Subplot con HF, PF ed EKF)
# =============================================================================
class VisualizzatoreLocalizzazione1D:
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
        esegui_hf: bool,
        esegui_pf: bool,
        esegui_ekf: bool = False,
        bin_centers: np.ndarray = None,
        hf_post_prev: np.ndarray = None,
        hf_pred: np.ndarray = None,
        hf_like_joint: np.ndarray = None,
        hf_post: np.ndarray = None,
        particles_prev: np.ndarray = None,
        particles_pred: np.ndarray = None,
        pf_like_joint: np.ndarray = None,
        particles_post: np.ndarray = None,
        ekf_post_prev: tuple = None,
        ekf_pred: tuple = None,
        ekf_post: tuple = None,
        x_sto_k: float = 0.0,
        x_det_hist: np.ndarray = None,
        x_sto_hist: np.ndarray = None,
        hf_mean_hist: np.ndarray = None,
        pf_mean_hist: np.ndarray = None,
        pf_mode_hist: np.ndarray = None,
        ekf_mean_hist: np.ndarray = None,
        ekf_std_hist: np.ndarray = None,
        metodo_resampling: str = "",
    ):
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

        # Griglia spaziale comune per plottare le PDF analitiche dell'EKF
        x_grid = bin_centers if bin_centers is not None else np.linspace(0.0, self.L, 1000)
        dx = float(x_grid[1] - x_grid[0]) if len(x_grid) > 1 else 0.1

        def evidenzia_riferimenti(ax):
            ax.axvline(
                x=x_sto_k,
                color="black",
                linestyle="-.",
                linewidth=1.5,
                label=f"Posa Reale x_k={x_sto_k:.2f}",
            )
            colors = ["purple", "darkgreen", "crimson", "orange"]
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

        # ---------------------------------------------------------------------
        # 1) Posteriori t-1
        # ---------------------------------------------------------------------
        if esegui_hf and hf_post_prev is not None:
            ax1.plot(
                bin_centers,
                hf_post_prev,
                "r-",
                linewidth=1.5,
                label="HF Belief (t-1)",
            )

        if esegui_pf and particles_prev is not None:
            h_const_prev = (
                (1.0 / 3.0) * np.max(hf_post_prev)
                if (esegui_hf and hf_post_prev is not None and np.max(hf_post_prev) > 0)
                else 0.33
            )

            ax1.vlines(
                x=particles_prev,
                ymin=0,
                ymax=h_const_prev,
                colors="gray",
                linewidth=1.2,
                alpha=0.5,
                label="PF Particelle t-1",
            )
            ax1.plot(
                particles_prev,
                np.zeros_like(particles_prev),
                "o",
                color="gray",
                markersize=2.5,
            )

        if esegui_ekf and ekf_post_prev is not None:
            mu_prev, P_prev = ekf_post_prev
            pdf_prev = (1.0 / np.sqrt(2.0 * np.pi * max(P_prev, 1e-12))) * np.exp(
                -0.5 * ((x_grid - mu_prev) ** 2) / max(P_prev, 1e-12)
            )
            curva_ekf_prev = (
                pdf_prev * dx
                if (esegui_hf and hf_post_prev is not None)
                else (pdf_prev / np.max(pdf_prev) if np.max(pdf_prev) > 0 else pdf_prev)
            )
            ax1.plot(
                x_grid,
                curva_ekf_prev,
                color="darkviolet",
                linestyle="-",
                linewidth=2.0,
                label=f"EKF Post. t-1 (μ={mu_prev:.2f}, σ={np.sqrt(P_prev):.2f})",
            )

        evidenzia_riferimenti(ax1)
        ax1.set_ylabel("Posteriori t-1")
        ax1.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 2) Prior t
        # ---------------------------------------------------------------------
        if esegui_hf and hf_pred is not None:
            ax2.plot(bin_centers, hf_pred, "r--", linewidth=1.5, label="HF Prior t")

        if esegui_pf and particles_pred is not None:
            h_const_pred = (
                (1.0 / 3.0) * np.max(hf_pred)
                if (esegui_hf and hf_pred is not None and np.max(hf_pred) > 0)
                else 0.33
            )

            ax2.vlines(
                x=particles_pred,
                ymin=0,
                ymax=h_const_pred,
                colors="orange",
                linewidth=1.0,
                alpha=0.4,
                label="PF Prior t (particelle dopo il moto)",
            )
            ax2.plot(
                particles_pred,
                np.zeros_like(particles_pred),
                "o",
                color="orange",
                markersize=2.5,
            )

        if esegui_ekf and ekf_pred is not None:
            mu_pred, P_pred = ekf_pred
            pdf_pred = (1.0 / np.sqrt(2.0 * np.pi * max(P_pred, 1e-12))) * np.exp(
                -0.5 * ((x_grid - mu_pred) ** 2) / max(P_pred, 1e-12)
            )
            curva_ekf_pred = (
                pdf_pred * dx
                if (esegui_hf and hf_pred is not None)
                else (pdf_pred / np.max(pdf_pred) if np.max(pdf_pred) > 0 else pdf_pred)
            )
            ax2.plot(
                x_grid,
                curva_ekf_pred,
                color="darkviolet",
                linestyle="--",
                linewidth=2.0,
                label=f"EKF Prior t (μ={mu_pred:.2f}, σ={np.sqrt(P_pred):.2f})",
            )

        evidenzia_riferimenti(ax2)
        ax2.set_ylabel("Prior t")
        ax2.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 3) Verosimiglianza Congiunta
        # ---------------------------------------------------------------------
        if esegui_hf and hf_like_joint is not None:
            max_hf_like = np.max(hf_like_joint)
            norm_hf_like = (
                hf_like_joint / max_hf_like if max_hf_like > 0 else hf_like_joint
            )
            ax3.plot(
                bin_centers,
                norm_hf_like,
                "m-",
                linewidth=1.5,
                label="Likelihood Congiunta (HF)",
            )
        if esegui_pf and particles_pred is not None and pf_like_joint is not None:
            max_pf_like = np.max(pf_like_joint)
            norm_pf_like = (
                pf_like_joint / max_pf_like if max_pf_like > 0 else pf_like_joint
            )

            ax3.vlines(
                x=particles_pred,
                ymin=0,
                ymax=norm_pf_like,
                colors="darkgreen",
                linewidth=1.2,
                alpha=0.6,
                label="Likelihood Congiunta (PF - barre = L(z|x_i))",
            )
            ax3.plot(
                particles_pred,
                np.zeros_like(particles_pred),
                "k.",
                markersize=2,
            )

        if esegui_ekf and ekf_pred is not None:
            mu_pred, _ = ekf_pred
            ax3.axvline(
                x=mu_pred,
                color="darkviolet",
                linestyle=":",
                linewidth=1.8,
                label=f"Linearizzazione EKF (x̂={mu_pred:.2f})",
            )

        evidenzia_riferimenti(ax3)
        ax3.set_ylabel("Verosimiglianza")
        ax3.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 4) Posteriori t (Frequenza/Conteggio esatto delle copie ri-campionate)
        # ---------------------------------------------------------------------
        target_scale_post = (
            np.max(hf_post)
            if (esegui_hf and hf_post is not None and np.max(hf_post) > 0)
            else 1.0
        )

        if esegui_hf and hf_post is not None:
            ax4.plot(bin_centers, hf_post, "r-", linewidth=1.8, label="HF Posteriori t")

        if esegui_pf and particles_post is not None:
            unique_part, counts = np.unique(particles_post, return_counts=True)
            counts_norm = (counts / np.max(counts)) * target_scale_post

            ax4.vlines(
                x=unique_part,
                ymin=0,
                ymax=counts_norm,
                colors="blue",
                linewidth=1.8,
                alpha=0.7,
                label="PF Posteriori t (Molteplicità copie)",
            )
            ax4.plot(
                unique_part,
                np.zeros_like(unique_part),
                "bo",
                markersize=3,
            )

        if esegui_ekf and ekf_post is not None:
            mu_post, P_post = ekf_post
            pdf_post = (1.0 / np.sqrt(2.0 * np.pi * max(P_post, 1e-12))) * np.exp(
                -0.5 * ((x_grid - mu_post) ** 2) / max(P_post, 1e-12)
            )
            curva_ekf_post = (
                pdf_post * dx
                if (esegui_hf and hf_post is not None)
                else (pdf_post / np.max(pdf_post) * target_scale_post if np.max(pdf_post) > 0 else pdf_post)
            )
            ax4.plot(
                x_grid,
                curva_ekf_post,
                color="darkviolet",
                linestyle="-",
                linewidth=2.2,
                label=f"EKF Posteriori t (μ={mu_post:.2f}, σ={np.sqrt(P_post):.2f})",
            )

        evidenzia_riferimenti(ax4)
        ax4.set_ylabel("Posteriori t")
        ax4.legend(loc="upper right", fontsize=7.5)

        # ---------------------------------------------------------------------
        # 5) Traiettorie Stimate nel tempo
        # ---------------------------------------------------------------------
        t_hist = np.arange(len(x_det_hist))
        ax_bot.plot(t_hist, x_det_hist, "k--", label="Posa Det.", alpha=0.6)
        ax_bot.plot(
            t_hist, x_sto_hist, "g-o", markersize=3, label="Posa Reale", linewidth=1.5
        )

        if esegui_hf and len(hf_mean_hist) > 0:
            ax_bot.plot(
                t_hist,
                hf_mean_hist,
                "r:",
                markersize=3,
                label="Stima HF (Media)",
                linewidth=2,
            )
        if esegui_pf and len(pf_mean_hist) > 0:
            ax_bot.plot(
                t_hist,
                pf_mean_hist,
                "b-.s",
                markersize=3,
                label="Stima PF (Media)",
                linewidth=1.8,
            )
            ax_bot.plot(
                t_hist,
                pf_mode_hist,
                color="cyan",
                linestyle="-.",
                marker="^",
                markersize=3,
                label="Stima PF (Moda)",
                linewidth=1.5,
            )
        if esegui_ekf and ekf_mean_hist is not None and len(ekf_mean_hist) > 0:
            ax_bot.plot(
                t_hist,
                ekf_mean_hist,
                color="darkviolet",
                linestyle="-.",
                marker="x",
                markersize=3,
                label="Stima EKF (Media)",
                linewidth=1.8,
            )
            if ekf_std_hist is not None and len(ekf_std_hist) > 0:
                ekf_m = np.asarray(ekf_mean_hist)
                ekf_s = np.asarray(ekf_std_hist)
                ax_bot.fill_between(
                    t_hist,
                    ekf_m - 2.0 * ekf_s,
                    ekf_m + 2.0 * ekf_s,
                    color="darkviolet",
                    alpha=0.15,
                    label=r"Intervallo Conf. EKF ($\pm 2\sigma$)",
                )

        for idx, m in enumerate(self.landmarks):
            ax_bot.axhline(
                y=m, linestyle=":", alpha=0.6, label=f"Beacon m_{idx + 1}={m}"
            )

        ax_bot.set_xlim(0, max(len(x_det_hist), 10))
        ax_bot.set_xlabel("Passo Temporale k")
        ax_bot.set_ylabel("Posizione x")
        ax_bot.grid(True, linestyle=":", alpha=0.6)
        ax_bot.legend(loc="upper right", fontsize=7.5)

        titolo_filtri = []
        if esegui_hf:
            titolo_filtri.append("HF")
        if esegui_pf:
            titolo_filtri.append(
                f"PF ({metodo_resampling.capitalize()})"
            )
        if esegui_ekf:
            titolo_filtri.append("EKF")

        fig.suptitle(
            f"Simulazione Localizzazione 1D (Passo k = {k}) - Filtri attivi: {' + '.join(titolo_filtri)}",
            fontsize=11,
            fontweight="bold",
        )
        plt.tight_layout()

        if self.salva:
            filename = f"simulazione_passo_{k}.png"
            fig.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"[INFO] Grafico salvato: '{filename}'")

        if self.visualizza:
            plt.ion()
            plt.show()
            plt.pause(0.1)
            try:
                input(f">>> [Passo k={k}] Premi INVIO per avanzare al passo successivo...")
            except (EOFError, OSError):
                pass
            plt.close(fig)
            plt.ioff()
        else:
            plt.close(fig)


# =============================================================================
# 6. MAIN - ESECUZIONE SINCRONA E BENCHMARK COMPARATIVO (HF vs PF vs EKF)
# =============================================================================
if __name__ == "__main__":
    L_MAPPA = 100.0
    BEACONS = [25.0, 75.0]
    T_FINALE = 80
    N_PASSI_VISUALIZZATI = 4

    # Flag per abilitare/disabilitare ciascun filtro in modo indipendente
    ESEGUI_FILTRO_ISTOGRAMMA: bool = True
    ESEGUI_FILTRO_PARTICELLE: bool = True
    ESEGUI_FILTRO_KALMAN: bool = True

    ATTIVA_VISUALIZZAZIONE: bool = True
    ATTIVA_SALVATAGGIO: bool = False

    simulatore = SimulatoreRobot1D(
        L=L_MAPPA,
        x0=0.0,
        u_x=0.8,
        landmarks=BEACONS,
        sigma_x_sim=0.5,
        sigma_z_sim=1.5,
        seed=42,
    )

    filtro_hf = (
        FiltroIstogramma1D(
            L=L_MAPPA,
            u_x=0.8,
            landmarks=BEACONS,
            bin_size=0.1,
            sigma_x_loc=0.5,
            sigma_z_loc=1.5,
            tipo_prior="gaussiana",
            sigma_prior=1.0,
            x0_prior=0.0,
        )
        if ESEGUI_FILTRO_ISTOGRAMMA
        else None
    )

    filtro_pf = (
        ParticleFilter1D(
            N_particles=500,
            L=L_MAPPA,
            u_x=0.8,
            landmarks=BEACONS,
            sigma_x_loc=0.5,
            sigma_z_loc=1.5,
            tipo_prior="uniforme",
            sigma_prior=1.0,
            x0_prior=0.0,
            metodo_resampling="importance",
        )
        if ESEGUI_FILTRO_PARTICELLE
        else None
    )

    filtro_ekf = (
        ExtendedKalmanFilter1D(
            L=L_MAPPA,
            u_x=0.8,
            landmarks=BEACONS,
            sigma_x_loc=0.5,
            sigma_z_loc=1.5,
            tipo_prior="gaussiana",
            sigma_prior=1.0,
            x0_prior=0.0,
        )
        if ESEGUI_FILTRO_KALMAN
        else None
    )

    visualizzatore = VisualizzatoreLocalizzazione1D(
        L=L_MAPPA,
        landmarks=BEACONS,
        visualizza=ATTIVA_VISUALIZZAZIONE,
        salva=ATTIVA_SALVATAGGIO,
    )

    history = {
        "t": [0],
        "x_det": [simulatore.x_det_k],
        "x_sto": [simulatore.x_sto_k],
        "hf_mean": [filtro_hf.calcola_stima_media()] if filtro_hf else [],
        "hf_mode": [filtro_hf.calcola_stima_moda()] if filtro_hf else [],
        "pf_mean": [filtro_pf.calcola_stima_media()] if filtro_pf else [],
        "pf_mode": [filtro_pf.calcola_stima_moda()] if filtro_pf else [],
        "ekf_mean": [filtro_ekf.calcola_stima_media()] if filtro_ekf else [],
        "ekf_std": [filtro_ekf.calcola_deviazione_standard()] if filtro_ekf else [],
    }

    print("Avvio simulazione e benchmark sincrono in corso (HF vs PF vs EKF)...")

    for k in range(1, T_FINALE + 1):
        x_det_k, x_sto_k, z_sto_k = simulatore.passo_simulazione()

        history["t"].append(k)
        history["x_det"].append(x_det_k)
        history["x_sto"].append(x_sto_k)

        # ---------------------------------------------------------------------
        # 1. Aggiornamento Filtro ad Istogramma (HF)
        # ---------------------------------------------------------------------
        hf_post_prev, hf_pred, hf_like_joint, hf_post = None, None, None, None
        if ESEGUI_FILTRO_ISTOGRAMMA and filtro_hf:
            hf_post_prev = filtro_hf.belief.copy()
            hf_pred = filtro_hf.passo_predizione()
            hf_post, _, hf_like_joint = filtro_hf.passo_correzione(z_sto_k)

            history["hf_mean"].append(filtro_hf.calcola_stima_media())
            history["hf_mode"].append(filtro_hf.calcola_stima_moda())

        # ---------------------------------------------------------------------
        # 2. Aggiornamento Filtro a Particelle (PF)
        # ---------------------------------------------------------------------
        particles_prev = None
        particles_pred, weights_pred = None, None
        pf_like_joint, weights_current_like, particles_post, weights_post = (
            None,
            None,
            None,
            None,
        )

        if ESEGUI_FILTRO_PARTICELLE and filtro_pf:
            particles_prev = filtro_pf.particles.copy()
            particles_pred, weights_pred = filtro_pf.passo_predizione(simulatore.u_x)

            (
                _,
                pf_like_joint,
                weights_current_like,
                particles_post,
                weights_post,
            ) = filtro_pf.passo_correzione(z_sto_k)

            history["pf_mean"].append(filtro_pf.calcola_stima_media())
            history["pf_mode"].append(filtro_pf.calcola_stima_moda())

        # ---------------------------------------------------------------------
        # 3. Aggiornamento Filtro di Kalman Esteso (EKF)
        # ---------------------------------------------------------------------
        ekf_post_prev = None
        ekf_pred_tuple = None
        ekf_post_tuple = None

        if ESEGUI_FILTRO_KALMAN and filtro_ekf:
            ekf_post_prev = (filtro_ekf.x, filtro_ekf.P)
            x_pred_ekf, P_pred_ekf = filtro_ekf.passo_predizione(simulatore.u_x)
            ekf_pred_tuple = (x_pred_ekf, P_pred_ekf)

            x_post_ekf, P_post_ekf, _, _, _, _, _ = filtro_ekf.passo_correzione(z_sto_k)
            ekf_post_tuple = (x_post_ekf, P_post_ekf)

            history["ekf_mean"].append(filtro_ekf.calcola_stima_media())
            history["ekf_std"].append(filtro_ekf.calcola_deviazione_standard())

        # ---------------------------------------------------------------------
        # Visualizzazione grafica passo-passo
        # ---------------------------------------------------------------------
        if k <= N_PASSI_VISUALIZZATI and visualizzatore:
            visualizzatore.mostra_passo_dettagliato(
                k=k,
                esegui_hf=ESEGUI_FILTRO_ISTOGRAMMA,
                esegui_pf=ESEGUI_FILTRO_PARTICELLE,
                esegui_ekf=ESEGUI_FILTRO_KALMAN,
                bin_centers=filtro_hf.bin_centers if filtro_hf else None,
                hf_post_prev=hf_post_prev,
                hf_pred=hf_pred,
                hf_like_joint=hf_like_joint,
                hf_post=hf_post,
                particles_prev=particles_prev,
                particles_pred=particles_pred,
                pf_like_joint=pf_like_joint,
                particles_post=particles_post,
                ekf_post_prev=ekf_post_prev,
                ekf_pred=ekf_pred_tuple,
                ekf_post=ekf_post_tuple,
                x_sto_k=x_sto_k,
                x_det_hist=np.array(history["x_det"]),
                x_sto_hist=np.array(history["x_sto"]),
                hf_mean_hist=np.array(history["hf_mean"]),
                pf_mean_hist=np.array(history["pf_mean"]),
                pf_mode_hist=np.array(history["pf_mode"]),
                ekf_mean_hist=np.array(history["ekf_mean"]),
                ekf_std_hist=np.array(history["ekf_std"]),
                metodo_resampling=filtro_pf.metodo_resampling if filtro_pf else "",
            )

    print("Simulazione completata con successo.")

    # -------------------------------------------------------------------------
    # GRAFICO FINALE COMPARATIVO (Traiettorie, Inviluppi di Incertezza ed Errori)
    # -------------------------------------------------------------------------
    fig_final, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.5, 8), sharex=True)

    ax1.plot(history["t"], history["x_det"], "k--", label="Posa Det.", alpha=0.6)
    ax1.plot(history["t"], history["x_sto"], "g-", label="Posa Reale (Ground Truth)", linewidth=1.5)

    if ESEGUI_FILTRO_ISTOGRAMMA:
        ax1.plot(
            history["t"],
            history["hf_mean"],
            "r:",
            label="Posa Stim. Media (HF)",
            linewidth=2,
        )

    if ESEGUI_FILTRO_PARTICELLE:
        ax1.plot(
            history["t"],
            history["pf_mean"],
            "b-.",
            label="Posa Stim. Media (PF)",
            linewidth=1.8,
        )
        ax1.plot(
            history["t"],
            history["pf_mode"],
            color="cyan",
            linestyle="-.",
            label="Posa Stim. Moda (PF)",
            linewidth=1.5,
        )

    if ESEGUI_FILTRO_KALMAN and len(history["ekf_mean"]) > 0:
        ax1.plot(
            history["t"],
            history["ekf_mean"],
            color="darkviolet",
            linestyle="-",
            label="Posa Stim. Media (EKF)",
            linewidth=1.8,
        )
        ekf_m_arr = np.array(history["ekf_mean"])
        ekf_s_arr = np.array(history["ekf_std"])
        ax1.fill_between(
            history["t"],
            ekf_m_arr - 2.0 * ekf_s_arr,
            ekf_m_arr + 2.0 * ekf_s_arr,
            color="darkviolet",
            alpha=0.18,
            label=r"Intervallo Conf. EKF ($\pm 2\sigma$)",
        )

    for idx, m in enumerate(BEACONS):
        ax1.axhline(y=m, linestyle=":", alpha=0.6, label=f"Beacon $m_{idx + 1}$={m}")

    ax1.set_ylabel("Posizione $x$")
    ax1.set_title("Localizzazione Finale - Confronto Traiettorie e Inviluppi")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=8)

    if ESEGUI_FILTRO_ISTOGRAMMA:
        err_hf_mean = np.abs(np.array(history["x_sto"]) - np.array(history["hf_mean"]))
        ax2.plot(
            history["t"],
            err_hf_mean,
            "r:",
            label=r"Err. Media (HF)",
            linewidth=1.8,
        )

    if ESEGUI_FILTRO_PARTICELLE:
        err_pf_mean = np.abs(np.array(history["x_sto"]) - np.array(history["pf_mean"]))
        ax2.plot(
            history["t"],
            err_pf_mean,
            "b-.",
            label=r"Err. Media (PF)",
            linewidth=1.8,
        )

    if ESEGUI_FILTRO_KALMAN and len(history["ekf_mean"]) > 0:
        err_ekf_mean = np.abs(np.array(history["x_sto"]) - np.array(history["ekf_mean"]))
        ax2.plot(
            history["t"],
            err_ekf_mean,
            color="darkviolet",
            linestyle="-",
            label=r"Err. Media (EKF)",
            linewidth=1.8,
        )
        # Limite teorico 2-sigma dell'errore atteso per consistenza EKF
        ax2.plot(
            history["t"],
            2.0 * np.array(history["ekf_std"]),
            color="darkviolet",
            linestyle=":",
            alpha=0.7,
            label=r"Banda Limite $2\sigma$ EKF",
        )

    ax2.set_xlabel("Tempo $t$")
    ax2.set_ylabel("Errore Assoluto")
    ax2.set_title("Confronto Errore Assoluto di Localizzazione")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=8)

    plt.tight_layout()

    # -------------------------------------------------------------------------
    # RIEPILOGO STATISTICO PRESTAZIONI (RMSE) IN CONSOLE
    # -------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print("RIEPILOGO COMPARATIVO PRESTAZIONI FILTRI (RMSE sui passi temporali):")
    x_sto_arr = np.array(history["x_sto"])

    if ESEGUI_FILTRO_ISTOGRAMMA and len(history["hf_mean"]) > 0:
        rmse_hf = np.sqrt(np.mean((x_sto_arr - np.array(history["hf_mean"])) ** 2))
        print(f" - Filtro ad Istogramma (Media): RMSE = {rmse_hf:.4f} m")

    if ESEGUI_FILTRO_PARTICELLE and len(history["pf_mean"]) > 0:
        rmse_pf_mean = np.sqrt(np.mean((x_sto_arr - np.array(history["pf_mean"])) ** 2))
        rmse_pf_mode = np.sqrt(np.mean((x_sto_arr - np.array(history["pf_mode"])) ** 2))
        print(f" - Filtro a Particelle (Media):   RMSE = {rmse_pf_mean:.4f} m")
        print(f" - Filtro a Particelle (Moda):    RMSE = {rmse_pf_mode:.4f} m")

    if ESEGUI_FILTRO_KALMAN and len(history["ekf_mean"]) > 0:
        rmse_ekf = np.sqrt(np.mean((x_sto_arr - np.array(history["ekf_mean"])) ** 2))
        print(f" - Filtro di Kalman Esteso (EKF): RMSE = {rmse_ekf:.4f} m")
    print("=" * 65 + "\n")

    plt.show()
