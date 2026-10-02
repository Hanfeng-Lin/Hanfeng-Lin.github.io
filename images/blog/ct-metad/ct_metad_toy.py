"""
Toy well-tempered metadynamics + c(t) reweighting (Tiwary & Parrinello, JPCB 2015).

Model: overdamped Langevin on U(x, y) = 5 (x^2 - 1)^2 + 0.8 x + 3 (y - x)^2, in kT units.
  - bias is applied on x only (the "CV");
  - y is NOT biased; we recover its free energy F(y) by reweighting.
Because the y-term is Gaussian around x, the exact F(x) = 5 (x^2 - 1)^2 + 0.8 x + const.

Run:  python ct_metad_toy.py      (numpy + matplotlib, ~1 min)
Outputs: fig1_bias_snapshots.png, fig2_ct.png, fig3_reweight.png, fig4_deltaF.png
"""
import math
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)

# ---------------- model ----------------
A, TILT, KY = 5.0, 0.8, 3.0


def F_exact_x(x):
    return A * (x**2 - 1) ** 2 + TILT * x


def grad_U(x, y):
    dx = 4 * A * x * (x * x - 1) + TILT - 2 * KY * (y - x)
    dy = 2 * KY * (y - x)
    return dx, dy


# ---------------- WTMetaD parameters ----------------
BETA = 1.0          # 1/kT
GAMMA = 8.0         # bias factor
W0 = 0.4            # initial hill height (kT)
SIGMA = 0.12        # hill width
PACE = 250          # steps between hills
DT = 1e-3
NSTEPS = 3_000_000
STRIDE = 50         # output stride (like COLVAR STRIDE)

grid = np.linspace(-2.5, 2.5, 1001)
dg = grid[1] - grid[0]
V = np.zeros_like(grid)
dV = np.zeros_like(grid)


def ct_from_bias(Vg):
    """Tiwary-Parrinello c(t), with F(s) = -gamma/(gamma-1) V(s,t):
    c(t) = 1/beta * ln[ int e^{gamma beta V/(gamma-1)} ds / int e^{beta V/(gamma-1)} ds ]"""
    a = GAMMA * BETA * Vg / (GAMMA - 1)
    b = BETA * Vg / (GAMMA - 1)
    lse = lambda z: z.max() + math.log(np.exp(z - z.max()).sum())
    return (lse(a) - lse(b)) / BETA


# ---------------- simulation ----------------
x, y = -1.0, -1.0
noise = math.sqrt(2 * DT / BETA)
c_now = 0.0
rec_t, rec_x, rec_y, rec_V, rec_c = [], [], [], [], []
hill_t, hill_c, hill_h = [], [], []
snapshots = {}
snap_hills = {200, 1500, 12000}

nh = 0
for chunk in range(NSTEPS // 100_000):
    xi = rng.standard_normal((100_000, 2))
    for k in range(100_000):
        step = chunk * 100_000 + k
        i = int((x - grid[0]) / dg + 0.5)
        i = min(max(i, 0), grid.size - 1)
        if step % STRIDE == 0:
            rec_t.append(step * DT); rec_x.append(x); rec_y.append(y)
            rec_V.append(V[i]); rec_c.append(c_now)
        if step % PACE == 0:
            # well-tempered hill height: W0 * exp(-V(s)/(kB dT)), dT = (gamma-1) T
            h = W0 * math.exp(-BETA * V[i] / (GAMMA - 1))
            g = h * np.exp(-0.5 * ((grid - x) / SIGMA) ** 2)
            V += g
            dV += g * (-(grid - x) / SIGMA**2)
            nh += 1
            c_now = ct_from_bias(V)
            hill_t.append(step * DT); hill_c.append(c_now); hill_h.append((x, h))
            if nh in snap_hills:
                snapshots[nh] = (step * DT, V.copy(), c_now)
        gx, gy = grad_U(x, y)
        gx += dV[i]
        x += -gx * DT + noise * xi[k, 0]
        y += -gy * DT + noise * xi[k, 1]

t = np.array(rec_t); xs = np.array(rec_x); ys = np.array(rec_y)
Vt = np.array(rec_V); ct = np.array(rec_c)
hill_t = np.array(hill_t); hill_c = np.array(hill_c)

# ---------------- exact references ----------------
yy = np.linspace(-2.5, 2.5, 501)
X, Y = np.meshgrid(grid, yy, indexing="ij")
U2 = A * (X**2 - 1) ** 2 + TILT * X + KY * (Y - X) ** 2
Fy_exact = -np.log(np.exp(-BETA * U2).sum(axis=0)) / BETA
Fy_exact -= Fy_exact.min()
Fx_exact = F_exact_x(grid) - F_exact_x(grid).min()
px = np.exp(-BETA * F_exact_x(grid))
dF_exact = -math.log(px[grid > 0].sum() / px[grid < 0].sum()) / BETA

# ---------------- reweighting ----------------
burn = t > 0.1 * t[-1]  # drop the initial transient (before quasi-stationarity)


def fes_1d(vals, logw, edges):
    w = np.exp(logw - logw.max())
    hist, _ = np.histogram(vals, bins=edges, weights=w)
    with np.errstate(divide="ignore"):
        f = -np.log(hist) / BETA
    return f - np.nanmin(f[np.isfinite(f)])


def kish_ess(logw):
    w = np.exp(logw - logw.max())
    return w.sum() ** 2 / (w**2).sum() / w.size


edges = np.linspace(-2.2, 2.2, 89)
centers = 0.5 * (edges[1:] + edges[:-1])
logw_ct = BETA * (Vt - ct)          # correct: rbias = V - c(t)
logw_naive = BETA * Vt              # wrong: forgets c(t)
Fy_ct = fes_1d(ys[burn], logw_ct[burn], edges)
Fy_naive = fes_1d(ys[burn], logw_naive[burn], edges)
ess_ct, ess_naive = kish_ess(logw_ct[burn]), kish_ess(logw_naive[burn])


def dF_reweight(xv, logw):
    w = np.exp(logw - logw.max())
    return -math.log(w[xv > 0].sum() / w[xv < 0].sum()) / BETA


# running estimates of Delta F = F(right) - F(left)
checkpoints = np.linspace(0.12, 1.0, 40) * t[-1]
dF_rw, dF_bias = [], []
for tc in checkpoints:
    m = burn & (t <= tc)
    dF_rw.append(dF_reweight(xs[m], logw_ct[m]))
# bias-based estimate needs V(s,t) at each checkpoint: rebuild it from the hill history
Vb = np.zeros_like(grid)
k = 0
for tc in checkpoints:
    while k < len(hill_t) and hill_t[k] <= tc:
        hx, h = hill_h[k]
        Vb += h * np.exp(-0.5 * ((grid - hx) / SIGMA) ** 2)
        k += 1
    Fb = -GAMMA / (GAMMA - 1) * Vb
    pb = np.exp(-BETA * (Fb - Fb.min()))
    dF_bias.append(-math.log(pb[grid > 0].sum() / pb[grid < 0].sum()) / BETA)

print(f"hills={nh}  final c(t)={hill_c[-1]:.2f} kT")
print(f"exact dF={dF_exact:.3f}  reweighted={dF_rw[-1]:.3f}  bias={dF_bias[-1]:.3f}")
print(f"Kish ESS fraction: with c(t)={ess_ct:.3f}  naive={ess_naive:.4f}")

# ---------------- plotting ----------------
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({
    "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "legend.frameon": False, "lines.linewidth": 2,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, name), dpi=160)
    plt.close(fig)


# Fig 1: bias snapshots + c(t) levels
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
a1.plot(grid, Fx_exact, color=INK, lw=2)
a1.set_xlim(-2, 2); a1.set_ylim(-0.5, 12)
a1.set_xlabel("CV  s = x"); a1.set_ylabel("F(s)  [kT]")
a1.set_title("True free energy F(s)", loc="left", fontsize=10)
for (nhk, (tk, Vk, ck)), col in zip(sorted(snapshots.items()), (S1, S2, S3)):
    a2.plot(grid, Vk, color=col, label=f"t = {tk:.0f}  ({nhk} hills)")
    a2.axhline(ck, color=col, lw=1, ls="--")
    a2.text(0, ck + 0.3, f"c(t) = {ck:.1f}", color=INK2, ha="center", va="bottom", fontsize=8.5)
a2.set_xlim(-2, 2); a2.set_ylim(-1, 44)
a2.set_xlabel("CV  s = x"); a2.set_ylabel("V(s, t)  [kT]")
a2.set_title("Bias V(s,t); dashed = c(t)", loc="left", fontsize=10)
a2.legend(loc="upper left", fontsize=8.5)
save(fig, "fig1_bias_snapshots.png")

# Fig 2: c(t) and the bias felt by the system
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.plot(t, Vt, color=AXIS, lw=0.6, label="V(s(t), t)  instantaneous bias")
ax.plot(hill_t, hill_c, color=S1, lw=2, label="c(t)")
ax.axvline(0.1 * t[-1], color=MUTED, lw=1, ls=":")
ax.text(0.1 * t[-1], ax.get_ylim()[1] * 0.92, "  transient discarded", color=INK2, fontsize=8.5)
ax.set_xlabel("time  [reduced units]"); ax.set_ylabel("[kT]")
ax.legend(loc="lower right", fontsize=8.5)
save(fig, "fig2_ct.png")

# Fig 3: reweighting an unbiased CV (y)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4), gridspec_kw={"width_ratios": [2.2, 1]})
a1.plot(yy, Fy_exact, color=INK, lw=2, label="exact")
a1.plot(centers, Fy_ct, color=S1, marker="o", ms=4, lw=0, label="reweighted, w = e^{β(V − c(t))}")
a1.plot(centers, Fy_naive, color=S2, marker="s", ms=4, lw=0, label="reweighted, w = e^{βV}  (no c(t))")
a1.set_xlim(-2.2, 2.2); a1.set_ylim(-0.5, 10)
a1.set_xlabel("unbiased variable  y"); a1.set_ylabel("F(y)  [kT]")
a1.legend(loc="upper center", fontsize=8.5)
bars = a2.bar([0, 1], [ess_ct * 100, ess_naive * 100], color=[S1, S2], width=0.55)
a2.set_xticks([0, 1], ["with c(t)", "no c(t)"])
a2.set_ylabel("effective sample size  [%]")
for b, v in zip(bars, (ess_ct, ess_naive)):
    a2.text(b.get_x() + b.get_width() / 2, v * 100, f"{v*100:.1f}%", ha="center", va="bottom", color=INK, fontsize=9)
a2.grid(axis="x", visible=False)
save(fig, "fig3_reweight.png")

# Fig 4: Delta F convergence
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.axhline(dF_exact, color=INK, lw=1.2, ls="--", label=f"exact  ΔF = {dF_exact:.2f} kT")
ax.plot(checkpoints, dF_rw, color=S1, label="c(t) reweighting (time-independent)")
ax.plot(checkpoints, dF_bias, color=S3, label="from current bias  −γ/(γ−1)·V(s,t)")
ax.set_xlabel("simulation time  [reduced units]"); ax.set_ylabel("ΔF (right − left)  [kT]")
ax.legend(loc="lower right", fontsize=8.5)
save(fig, "fig4_deltaF.png")
