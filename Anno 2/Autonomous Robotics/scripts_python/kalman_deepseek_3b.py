import numpy as np
from math import sqrt

class ExtendedKalmanFilter1D:
    def __init__(self, L=100.0, u_x=0.8, landmarks=[30.0, 70.0], sigma_x_loc=0.5, sigma_z_loc=1.5,
                 tipo_prior="gaussiana", sigma_prior=1.0, x0_prior=0.0, x0=None, P0=None):
        self.L = L
        self.u_x = u_x
        self.landmarks = landmarks
        self.sigma_x_loc = sigma_x_loc
        self.sigma_z_loc = sigma_z_loc
        self.tipo_prior = tipo_prior
        self.sigma_prior = sigma_prior
        self.x0_prior = x0_prior
        self.x0 = x0
        self.P0 = P0
        self.inizializza_stato()

    def inizializza_stato(self):
        if self.x0 is not None and self.P0 is not None:
            self.x = self.x0
            self.P = self.P0
        elif self.tipo_prior == "gaussiana":
            self.x = self.x0_prior
            self.P = self.sigma_prior ** 2
        else:  # tipo_prior == "uniforme"
            self.x = self.L / 2
            self.P = self.L ** 2 / 12

    def passo_predizione(self, u=None):
        u = self.u_x if u is None else u
        self.x += u
        self.P += self.sigma_x_loc ** 2
        return self.x, self.P

    def passo_correzione(self, z_misure):
        self.H = np.array([[1 if (self.x - m) >= 0 else -1 for m in self.landmarks]])
        self.R = np.eye(len(self.landmarks)) * self.sigma_z_loc ** 2
        self.P = self.sigma_x_loc ** 2
        self.P = self.P * self.H @ self.H.T + self.R
        y = np.array([z - self.calcola_innovazione_misura(j) for j, z in enumerate(z_misure)])
        K = self.P @ (self.H.T @ np.linalg.inv(self.P @ self.H.T + self.R))
        self.x = np.clip(self.x + K @ y.item(), 0, self.L)
        self.P = (1 - K @ self.H) ** 2 * self.P + K @ self.R @ K.T
        return self.x, self.P, y, K, self.P @ self.H @ self.H.T + self.R, np.array([sqrt(si) for si in np.diag(self.P @ self.H @ self.H.T + self.R)])

    def calcola_innovazione_misura(self, j):
        return abs(self.x - self.landmarks[j])

    def calcola_stima_media(self):
        return self.x

    def calcola_stima_moda(self):
        return self.x

    def calcola_deviazione_standard(self):
        return sqrt(self.P)

    def valuta_pdf_gaussiana(self, x_grid, mu=None, P=None, come_massa_bin=True):
        if mu is None:
            mu = self.x
        if P is None:
            P = self.P
        if len(x_grid) == 1 and come_massa_bin:
            return np.array([[np.exp(-(x_grid[0] - mu) ** 2 / (2 * P))]])
        else:
            return np.exp(-(x_grid - mu) ** 2 / (2 * P)) / sqrt(2 * np.pi * P)
