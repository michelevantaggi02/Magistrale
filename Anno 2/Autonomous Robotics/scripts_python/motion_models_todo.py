"""
Autonomous Robotics - Kinematic and motion models: coding
==========================================================

Differential-drive robot (unicycle) - ODE kinematic model:

    x_dot     = v cos(theta)
    y_dot     = v sin(theta)          pose  p = (x, y, theta)
    theta_dot = omega                 input u = (v, omega)

Goal:
  - simulate the deterministic discrete-time motion models
        Euler, Runge-Kutta (midpoint), Velocity (exact arc)
  - compare their accuracy against a reference solution of the ODE (scipy odeint)
  - plot: robot path, robot pose path, trajectory (pose vs time), error

Structure of this file:
  1. Inputs            u(t) = (v(t), omega(t))
  2. Motion models     p_t = f(p_{t-1}, u_t, T)
  3. Simulation        loop of a discrete-time model over the time grid
  4. Reference         ODE + scipy odeint  ("ground truth")
  5. Main              initialisation -> simulation -> accuracy -> plots
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# =============================================================================
# 1. INPUTS
# =============================================================================
def inputs(t):
    """Commands at time t: linear velocity v [m/s], angular velocity w [rad/s]."""
    # return the commands (v, w) as functions of time t.
    #       Use time-varying signals, e.g. sinusoids around a mean value,
    #       with w not always zero so that the robot turns.
    v = 1.0+ 0.5 * np.sin(0.2 * t)
    w = 0.2 + 0.6 * np.sin(0.15 * t)
    return v, w


# =============================================================================
# 2. DISCRETE-TIME MOTION MODELS
#    p = [x, y, theta] at step t-1, (v, w) constant over the step T
#    return p at step t
# =============================================================================
def euler(p, v, w, T):
    """Move along the TANGENT: heading kept at theta_{t-1} for the whole step."""
    x, y, th = p
        
    xn = x + v * T * np.cos(th)
    yn = y + v * T * np.sin(th)
    thn = th + w * T

    pn = np.array([xn, yn,thn])

    return pn


def runge_kutta(p, v, w, T):
    """Move along the CHORD: heading taken at mid-step, theta_{t-1} + w T / 2."""
    x, y, th = p

    mid = th + (w * T) / 2

    xn = x + v * T * np.cos(mid)
    yn = y + v * T * np.sin(mid)
    thn = th + w * T

    return np.array([xn, yn, thn])


#FIXME: sembra avere più errore di eulero, strano
def velocity_model(p, v, w, T, eps=1e-9):
    """Move along the ARC of radius r = v / w (exact if v, w constant over T)."""
    x, y, th = p

    if abs(w) < eps:
        # uso eulero perché con w=0 i modelli collassano sullo stesso
        # significa che runge_kutta e eulero diventano uguali
        return euler(p, v, w, T)

    thn = th + w * T
    r = v / w
    xn = x - r * np.sin(th) + r * np.sin(thn)
    yn = y + r * np.cos(th) - r * np.cos(thn)
    
    return np.array([xn, yn, thn])


# =============================================================================
# 3. SIMULATION OF A DISCRETE-TIME MODEL
# =============================================================================
def simulate(model, p0, t, T):
    """Run `model` over the time grid t. Input sampled at t_{k-1} and held
    constant over [t_{k-1}, t_k) (zero-order hold). Returns P, shape (N, 3)."""
    N = len(t)
    P = np.zeros((N, 3))
    P[0] = p0

    for i in range(1, N):
        v, w = inputs(t[i])
        P[i] = model(P[i-1], v, w, T)


    return P


# =============================================================================
# 4. REFERENCE: CONTINUOUS-TIME ODE + scipy odeint
# =============================================================================
def unicycle_ode(p, t, u):
    """Kinematic model p_dot = f(p, u(t)). `u` is a function of time -> (v, w).
    Signature (state, time, *args) as required by odeint."""
    x, y, th = p
    v, w = u(t)
    return [v * np.cos(th), v * np.sin(th), w]


def reference(p0, t, tol=1e-10):
    """Ground truth sampled on the grid t: the ODE integrated by odeint with the
    inputs v(t), w(t) varying continuously in time."""
    return odeint(unicycle_ode, p0, t, args=(inputs,), rtol=tol, atol=tol)


def wrap(a):
    """Wrap an angle to [-pi, pi)."""
    return (a + np.pi) % (2 * np.pi) - np.pi


# =============================================================================
# 5. MAIN
# =============================================================================
if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # 5.1 Initialisation
    # -------------------------------------------------------------------------
    p0 = np.array([0.0, 0.0, 0.0])     # initial pose (x, y, theta)
    T = 0.5                            # sampling time [s] (large -> visible errors)
    t_end = 40.0                       # simulation length [s]
    t = np.arange(0.0, t_end + 1e-12, T)

    models = {"Euler": euler,
              "Runge-Kutta": runge_kutta,
              "Velocity": velocity_model}

    # -------------------------------------------------------------------------
    # 5.2 Simulation
    # -------------------------------------------------------------------------
    P_ref = reference(p0, t)

    results = {}
    for name, model in models.items():
        results[name] = simulate(model, p0, t, T)

    # position error w.r.t. the reference
    errors = {name: np.linalg.norm(P[:, :2] - P_ref[:, :2], axis=1)
              for name, P in results.items()}

    # -------------------------------------------------------------------------
    # 5.3 Accuracy vs sampling time T
    # -------------------------------------------------------------------------
    print(f"{'T [s]':>6} | {'model':<12} | {'final pos err [m]':>18} | "
          f"{'max pos err [m]':>16} | {'final |th err| [rad]':>20}")
    print("-" * 85)
    for Ts in (1.0, 0.5, 0.1, 0.01):
        ts = np.arange(0.0, t_end + 1e-12, Ts)
        Pr = reference(p0, ts)
        for name, model in models.items():
            P = simulate(model, p0, ts, Ts)
            e = np.linalg.norm(P[:, :2] - Pr[:, :2], axis=1)
            eth = abs(wrap(P[-1, 2] - Pr[-1, 2]))
            print(f"{Ts:>6} | {name:<12} | {e[-1]:>18.3e} | {e.max():>16.3e} | {eth:>20.3e}")
        print("-" * 85)

    # =========================================================================
    # =========================================================================
    #                                 PLOTS
    # =========================================================================
    # =========================================================================
    colors = {"Euler": "#2a78d6", "Runge-Kutta": "#eb6834", "Velocity": "#1baf7a"}
    styles = {"Euler": "-", "Runge-Kutta": "-", "Velocity": "--"}
    ref_kw = dict(color="#52514e", lw=1, ls=":", label="Reference (odeint)")
    tag = f"T = {T} s"

    # ---- 1. Robot path: (x, y) in the plane ---------------------------------
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(P_ref[:, 0], P_ref[:, 1], **ref_kw)
    for name, P in results.items():
        ax.plot(P[:, 0], P[:, 1], styles[name], color=colors[name], lw=2, label=name)
    ax.plot(*p0[:2], "ko", ms=8, label="Start")
    ax.set(title=f"Robot path ({tag})", xlabel="x [m]", ylabel="y [m]")
    ax.axis("equal"); ax.grid(alpha=0.3); ax.legend()

    # ---- 2. Robot pose path: (x, y) + heading theta -------------------------
    fig, ax = plt.subplots(figsize=(7, 6))
    step = 4                           # one arrow every `step` samples
    ax.plot(P_ref[:, 0], P_ref[:, 1], **ref_kw)
    for name, P in results.items():
        ax.plot(P[:, 0], P[:, 1], styles[name], color=colors[name], lw=1, alpha=0.6)
        Q = P[::step]
        ax.quiver(Q[:, 0], Q[:, 1], np.cos(Q[:, 2]), np.sin(Q[:, 2]),
                  color=colors[name], angles="xy", scale=25, width=0.004, label=name)
    ax.set(title=f"Robot pose path: (x, y) + heading θ ({tag})", xlabel="x [m]", ylabel="y [m]")
    ax.axis("equal"); ax.grid(alpha=0.3); ax.legend()

    # ---- 3. Trajectory: pose vs time ----------------------------------------
    fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    labels = ["x [m]", "y [m]", "θ [rad]"]
    for i, a in enumerate(axs):
        a.plot(t, P_ref[:, i], **ref_kw)
        for name, P in results.items():
            a.plot(t, P[:, i], styles[name], color=colors[name], lw=2, label=name)
        a.set_ylabel(labels[i]); a.grid(alpha=0.3)
    axs[0].set_title(f"Trajectory: pose vs time ({tag})")
    axs[0].legend(ncol=4, fontsize=8)
    axs[-1].set_xlabel("t [s]")

    # ---- 4. Position error vs time ------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))
    for name, e in errors.items():
        ax.semilogy(t[1:], e[1:] + 1e-16, color=colors[name], lw=2, label=name)
    ax.set(title=f"Position error w.r.t. reference ({tag})", xlabel="t [s]", ylabel="‖e_xy‖ [m]")
    ax.grid(alpha=0.3, which="both"); ax.legend()

    plt.tight_layout()
    plt.show()
