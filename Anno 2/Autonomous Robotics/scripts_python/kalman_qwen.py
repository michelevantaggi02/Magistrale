import numpy as np
import math

class ExtendedKalmanFilter1D:
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
        self.L = L
        self.u_x = u_x
        self.landmarks = landmarks if landmarks is not None else [30.0, 70.0]
        self.sigma_x_loc = sigma_x_loc
        self.sigma_z_loc = sigma_z_loc
        self.tipo_prior = tipo_prior.lower()
        self.sigma_prior = sigma_prior
        self.x0_prior = x0_prior
        self.x0_custom = x0
        self.P0_custom = P0
        self.Q = sigma_x_loc ** 2
        self.R_val = sigma_z_loc ** 2
        self.x = 0.0
        self.P = 1.0
        self.inizializza_stato()

    def inizializza_stato(self) -> None:
        if self.x0_custom is not None and self.P0_custom is not None:
            self.x = self.x0_custom
            self.P = self.P0_custom
        elif self.tipo_prior == "gaussiana":
            self.x = self.x0_prior
            self.P = self.sigma_prior ** 2
        elif self.tipo_prior == "uniforme":
            self.x = self.L / 2.0
            self.P = (self.L ** 2) / 12.0
        else:
            raise ValueError(f"Unsupported tipo_prior: '{self.tipo_prior}'")

    def passo_predizione(self, u: float = None) -> tuple:
        u_val = u if u is not None else self.u_x
        self.x += u_val
        self.P += self.Q
        return (self.x, self.P)

    def passo_correzione(self, z_misure: np.ndarray) -> tuple:
        M = len(self.landmarks)
        z = np.asarray(z_misure, dtype=float).reshape(-1, 1)
        z_hat = np.zeros((M, 1), dtype=float)
        H = np.zeros((M, 1), dtype=float)

        for j in range(M):
            m_j = self.landmarks[j]
            diff = self.x - m_j
            z_hat[j, 0] = abs(diff)

            if abs(diff) < 1e-6:
                H[j, 0] = 1.0
            elif diff > 0.0:
                H[j, 0] = 1.0
            else:
                H[j, 0] = -1.0

        y_tilde = z - z_hat
        R = np.eye(M, dtype=float) * self.R_val
        # Nota: self.P è uno scalare (varianza 1D), per cui si usa la moltiplicazione '*'
        # anziché il prodotto matriciale '@' (che richiede operandi almeno 1D).
        S = self.P * (H @ H.T) + R
        S_inv = np.linalg.inv(S)
        K = self.P * (H.T @ S_inv)

        delta_x = (K @ y_tilde).item()
        x_post = self.x + delta_x

        KH = (K @ H).item()
        I_KH = 1.0 - KH
        P_post = (I_KH ** 2) * self.P + (K @ R @ K.T).item()

        self.x = float(np.clip(x_post, 0.0, self.L))
        self.P = float(max(P_post, 1e-9))

        mahalanobis = []
        for j in range(M):
            s_jj = S[j, j]
            mu_j = (y_tilde[j, 0] ** 2) / s_jj if s_jj > 0.0 else 0.0
            mahalanobis.append(mu_j)

        return (
            self.x,
            self.P,
            z_hat.flatten(),
            y_tilde.flatten(),
            K.flatten(),
            S,
            np.array(mahalanobis, dtype=float),
        )

    def calcola_stima_media(self) -> float:
        return self.x

    def calcola_stima_moda(self) -> float:
        return self.x

    def calcola_deviazione_standard(self) -> float:
        return math.sqrt(self.P)

    def valuta_pdf_gaussiana(
        self,
        x_grid: np.ndarray,
        mu: float = None,
        P: float = None,
        come_massa_bin: bool = True,
    ) -> np.ndarray:
        mu_val = self.x if mu is None else float(mu)
        P_val = self.P if P is None else float(P)
        P_val = max(P_val, 1e-12)

        pdf = (1.0 / math.sqrt(2.0 * math.pi * P_val)) * np.exp(
            -0.5 * ((x_grid - mu_val) ** 2) / P_val
        )

        if come_massa_bin and len(x_grid) > 1:
            dx = float(x_grid[1] - x_grid[0])
            return pdf * dx
        else:
            return pdf
