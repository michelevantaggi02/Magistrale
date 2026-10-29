import numpy as np
import math

class ExtendedKalmanFilter1D:
    def __init__(self, L=100.0, u_x=0.8, landmarks=[30.0, 70.0], sigma_x_loc=0.5, sigma_z_loc=1.5, tipo_prior="gaussiana", sigma_prior=1.0,x0_prior=0.0, x0=None, P0=None):
        self.L = L
        self.u_x = u_x
        self.landmarks = landmarks
        self.sigma_x_loc = sigma_x_loc
        self.sigma_z_loc = sigma_z_loc
        self.tipo_prior = tipo_prior
        self.sigma_prior = sigma_prior
        self.x0_prior = x0_prior
        self.x0 = x0 if x0 is not None else (x0_prior, sigma_prior**2)[tipo_prior == "gaussiana"]
        self.P0 = P0 if P0 is not None else L**2 / 12 if tipo_prior == "uniforme" else sigma_prior**2
        self.x = self.x0
        self.P = self.P0

    def inizializza_stato(self):
        self.x = self.x0
        self.P = self.P0

    def passo_predizione(self, u=None):
        if u is None:
            u = self.u_x
        self.x = np.clip(self.x + u, 0.0, self.L)
        self.P += self.sigma_x_loc**2
        return self.x, self.P

    def passo_correzione(self, z_misure):
        z_hat = np.zeros(len(self.landmarks))
        y = np.zeros(len(self.landmarks))
        K = np.zeros(len(self.landmarks))
        S = np.zeros(len(self.landmarks))
        mahalanobis = np.zeros(len(self.landmarks))
        for j, m_j in enumerate(self.landmarks):
            z_hat[j] = abs(self.x - m_j)
            y[j] = z_misure[j] - z_hat[j]
            H_j = 1.0 if (self.x - m_j) >= 0 else -1.0
            S[j] = self.P * H_j**2 + self.sigma_z_loc**2
            K[j] = self.P * H_j * np.linalg.inv(S[j])
            self.x += K[j] * y[j]
            self.P = (1 - K[j] * H_j) * self.P + K[j] * self.sigma_z_loc**2 * K[j].T
            mahalanobis[j] = y[j]**2 / S[j]
        return self.x, self.P, z_hat, y, K, S, mahalanobis

    def calcola_stima_media(self):
        return self.x

    def calcola_stima_moda(self):
        return self.x

    def calcola_deviazione_standard(self):
        return math.sqrt(self.P)

    def valuta_pdf_gaussiana(self, x_grid, mu=None, P=None, come_massa_bin=True):
        if mu is None:
            mu = self.x
        if P is None:
            P = self.P
        if come_massa_bin and len(x_grid) > 1:
            dx = x_grid[1] - x_grid[0]
            pdf = np.zeros_like(x_grid)
            for i, x in enumerate(x_grid):
                pdf[i] = (1 / (math.sqrt(2 * math.pi) * math.sqrt(P))) * math.exp(-((x - mu) ** 2) / (2 * P)) * dx
            return pdf
        else:
            return (1 / (math.sqrt(2 * math.pi) * math.sqrt(P))) * math.exp(-((x_grid - mu) ** 2) / (2 * P))
