"""Concept figures for the Umbrella Sampling / geometric route ternary-complex post.

Hand-drawn schematics. The only numbers taken from the paper are scalar values
that are also quoted in the post text. Run with:
    /c/ProgramData/miniconda3/python.exe -I _scripts/make_us_ternary_figs.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyArrowPatch, Ellipse, Circle,
                                FancyBboxPatch, Arc)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "images", "blog", "us-ternary-geometric-route")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.linewidth": 0.8,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

C_TARGET = "#4C86C6"
C_E3 = "#E08A3C"
C_GLUE = "#49A078"
C_BAD = "#C0392B"
C_GOOD = "#2E7D5B"
C_GREY = "#8A8A8A"


def protein(ax, xy, w, h, color, label, angle=0, alpha=0.85, fs=10):
    e = Ellipse(xy, w, h, angle=angle, facecolor=color, edgecolor="black",
                lw=0.8, alpha=alpha, zorder=2)
    ax.add_patch(e)
    if label:
        ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=fs,
                color="white", fontweight="bold", zorder=3)
    return e


def arrow(ax, p0, p1, color="black", lw=1.4, style="-|>", ls="-", alpha=1.0,
          mutation=14, zorder=4):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, color=color, lw=lw,
                        linestyle=ls, alpha=alpha, mutation_scale=mutation,
                        shrinkA=0, shrinkB=0, zorder=zorder)
    ax.add_patch(a)
    return a


# ---------------------------------------------------------------- figure 1
def fig1_path_problem():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.2))
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 11)
        ax.axis("off")

    ax = axes[0]
    ax.set_title("The problem: a physical path is not unique",
                 fontsize=11.5, fontweight="bold", pad=10)
    protein(ax, (2.0, 4.6), 3.0, 2.2, C_E3, "E3 ligase")
    protein(ax, (3.6, 6.1), 0.8, 0.8, C_GLUE, "")
    ax.text(3.6, 6.1, "glue", ha="center", va="center", fontsize=7,
            color="white", fontweight="bold", zorder=4)

    # the bound-state target, sitting on the glue-created interface
    bound = (4.9, 6.9)
    protein(ax, bound, 2.3, 1.7, C_TARGET, "target", angle=-10)
    ax.text(bound[0], bound[1] - 1.25, "bound pose", ha="center", fontsize=8,
            color=C_TARGET, fontweight="bold")

    # each escape route ends in its own faded copy of the target
    routes = [((6.6, 9.6), -22, 0.30), ((8.2, 7.6), 12, 0.38),
              ((8.0, 4.9), 30, 0.30)]
    for (pos, ang, al) in routes:
        protein(ax, pos, 2.2, 1.6, C_TARGET, "target", angle=ang, alpha=al)
    for (pos, _, _), rad in zip(routes, (0.32, 0.0, -0.3)):
        a = FancyArrowPatch(bound, pos, arrowstyle="-|>", color=C_GREY,
                            lw=1.4, mutation_scale=15, shrinkA=22, shrinkB=24,
                            connectionstyle="arc3,rad=%.2f" % rad, zorder=4)
        ax.add_patch(a)
    ax.text(5.0, 2.1,
            "slide / rock / rotate / peel\n"
            "orientation + conformation wander freely",
            ha="center", va="center", fontsize=9.5, color=C_BAD)
    ax.text(5.0, 0.8,
            r"$\Rightarrow$ the PMF depends on which tunnel you carved",
            ha="center", va="center", fontsize=9.5, color=C_BAD,
            fontweight="bold")

    ax = axes[1]
    ax.set_title("The fix: restrain until one path remains",
                 fontsize=11.5, fontweight="bold", pad=10)
    protein(ax, (2.0, 5.2), 3.0, 2.2, C_E3, "E3 ligase")
    protein(ax, (3.55, 6.5), 0.8, 0.8, C_GLUE, "")
    ax.text(3.55, 6.5, "glue", ha="center", va="center", fontsize=7,
            color="white", fontweight="bold", zorder=4)
    protein(ax, (7.8, 7.3), 2.4, 1.8, C_TARGET, "target")

    ax.plot([4.1, 7.0], [7.5, 8.2], color=C_GOOD, lw=1.0, ls="--")
    ax.plot([4.1, 7.0], [5.5, 6.2], color=C_GOOD, lw=1.0, ls="--")
    ax.fill_between([4.1, 7.0], [5.5, 6.2], [7.5, 8.2],
                    color=C_GOOD, alpha=0.12, zorder=1)
    arrow(ax, (4.3, 6.6), (6.7, 7.15), color=C_GOOD, lw=2.0)
    ax.text(5.4, 9.1, r"$r$ : the only free CV", ha="center", va="center",
            fontsize=10, color=C_GOOD, fontweight="bold")

    ax.text(5.0, 2.6,
            "RMSD restraints freeze conformation\n"
            "Boresch restraints freeze relative orientation",
            ha="center", va="center", fontsize=9.5, color=C_GOOD)
    ax.text(5.0, 1.3,
            r"$\Rightarrow$ every restraint's free energy is refunded",
            ha="center", va="center", fontsize=9.5, color=C_GOOD,
            fontweight="bold")
    ax.text(5.0, 0.4, "ambiguity is not sampled away, it is accounted for",
            ha="center", va="center", fontsize=9.5, style="italic")

    fig.savefig(os.path.join(OUT, "fig1_path_completeness.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 2
def fig2_thermo_cycle():
    fig, ax = plt.subplots(figsize=(10.0, 6.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis("off")

    boxes = [
        (1.25, 5.3, "Bound ternary\ncomplex", "#EAF1F9"),
        (1.25, 3.6, "+ RMSD restraints\n(conformation frozen)", "#EAF1F9"),
        (1.25, 1.9, "+ Boresch restraints\n(orientation frozen)", "#EAF1F9"),
        (5.6, 1.9, "Separated,\nstill restrained", "#FBEFE3"),
        (8.6, 1.9, "Orientation\nreleased", "#FBEFE3"),
        (8.6, 5.3, "Free proteins\nat standard state", "#E8F3ED"),
    ]
    for (x, y, t, c) in boxes:
        ax.add_patch(FancyBboxPatch((x - 1.05, y - 0.42), 2.1, 0.84,
                                    boxstyle="round,pad=0.06,rounding_size=0.12",
                                    facecolor=c, edgecolor="black", lw=0.8))
        ax.text(x, y, t, ha="center", va="center", fontsize=9)

    def step(p0, p1, label, sub, color="black", at=None, ha="center"):
        arrow(ax, p0, p1, color=color, lw=1.6)
        mx, my = at
        ax.text(mx, my, label, ha=ha, va="center", fontsize=10,
                color=color, fontweight="bold")
        ax.text(mx, my - 0.32, sub, ha=ha, va="center", fontsize=8.2,
                color=color)

    step((1.25, 4.86), (1.25, 4.06), r"(1) $\Delta G_{c,bound}$",
         r"US on $C\alpha$ RMSD", at=(2.55, 4.58), ha="left")
    step((1.25, 3.16), (1.25, 2.36), r"(2) $\Delta G_{o,bound}$",
         "US on 2 angles + 3 dihedrals", at=(2.55, 2.88), ha="left")
    step((2.35, 1.9), (4.5, 1.9), r"(3) $\Delta G_{sep}$",
         r"US along $r$: 9 $\rightarrow$ 30 $\AA$", at=(3.42, 1.25))
    step((6.7, 1.9), (7.5, 1.9), r"(4) $\Delta G_{corr}$",
         "analytic", at=(7.1, 3.0))
    step((8.6, 2.36), (8.6, 4.86), r"(5) $\Delta G_{c,bulk}$",
         "US, bulk state", at=(7.35, 4.1), ha="right")

    arrow(ax, (2.35, 5.45), (7.5, 5.45), color=C_GOOD, lw=2.0)
    ax.text(4.9, 5.8, r"$\Delta G_{bind}$  (what we want)", ha="center",
            fontsize=11, color=C_GOOD, fontweight="bold")

    ax.text(5.0, 0.52,
            r"$\Delta G_{bind} = \Delta G_{sep} + \Delta G_{c,bulk} - "
            r"\Delta G_{c,bound} - \Delta G_{o,bound} + \Delta G_{corr}$",
            ha="center", va="center", fontsize=13)
    ax.text(5.0, 0.1,
            "step (4) is a closed-form integral: the forbidden angular volume "
            "is refunded exactly, not simulated",
            ha="center", va="center", fontsize=8.6, style="italic",
            color=C_GREY)

    fig.savefig(os.path.join(OUT, "fig2_thermodynamic_cycle.png"))
    plt.close(fig)


def _ang(P, Q):
    """Direction of P->Q in degrees."""
    return np.degrees(np.arctan2(Q[1] - P[1], Q[0] - P[0]))


def draw_angle(ax, vertex, p1, p2, radius, label, color):
    """Arc marking the angle p1-vertex-p2, labelled on its bisector."""
    a1, a2 = _ang(vertex, p1), _ang(vertex, p2)
    sweep = (a2 - a1) % 360
    if sweep > 180:
        a1, a2 = a2, a1
        sweep = 360 - sweep
    ax.add_patch(Arc(vertex, 2 * radius, 2 * radius, theta1=a1, theta2=a2,
                     color=color, lw=1.8, zorder=6))
    mid = np.radians(a1 + sweep / 2.0)
    lr = radius + 0.34
    ax.text(vertex[0] + lr * np.cos(mid), vertex[1] + lr * np.sin(mid),
            label, ha="center", va="center", fontsize=11.5, color=color,
            fontweight="bold", zorder=7)


def draw_torsion(ax, P, Q, t, label, color, w=0.44, h=1.15, gap=38,
                 lab_side=1.0):
    """Rotation ring around the P-Q bond, marking a dihedral about it."""
    P, Q = np.array(P, float), np.array(Q, float)
    d = Q - P
    ang = np.degrees(np.arctan2(d[1], d[0]))
    c = P + t * d
    ax.add_patch(Arc(c, w, h, angle=ang, theta1=gap, theta2=360 - gap,
                     color=color, lw=1.6, zorder=6))

    ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))

    def rot(x, y):
        return np.array([ca * x - sa * y, sa * x + ca * y])

    th = np.radians(360 - gap)
    tip = c + rot((w / 2) * np.cos(th), (h / 2) * np.sin(th))
    tan = rot(-(w / 2) * np.sin(th), (h / 2) * np.cos(th))
    tan = tan / np.hypot(*tan) * 0.14
    ax.add_patch(FancyArrowPatch(tip - tan, tip, arrowstyle="-|>",
                                 mutation_scale=13, color=color, lw=1.6,
                                 shrinkA=0, shrinkB=0, zorder=7))

    perp = np.array([-d[1], d[0]])
    perp = perp / np.hypot(*perp) * (h / 2 + 0.3) * lab_side
    ax.text(c[0] + perp[0], c[1] + perp[1], label, ha="center", va="center",
            fontsize=11.5, color=color, fontweight="bold", zorder=7)


# ---------------------------------------------------------------- figure 3
def fig3_boresch():
    fig, ax = plt.subplots(figsize=(9.8, 5.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.set_title("Boresch-style orientational restraints: six anchors fix the "
                 "relative orientation", fontsize=11.5, fontweight="bold",
                 pad=12)

    protein(ax, (2.3, 3.5), 3.6, 3.2, C_E3, "", alpha=0.22)
    ax.text(1.25, 5.42, "glue-bound receptor", fontsize=9, color=C_E3,
            fontweight="bold")
    protein(ax, (7.7, 3.5), 3.6, 3.2, C_TARGET, "", alpha=0.22)
    ax.text(6.95, 5.42, "ligand protein", fontsize=9, color=C_TARGET,
            fontweight="bold")

    pts = {"c": (1.30, 2.25), "b": (1.75, 4.25), "a": (3.65, 3.50),
           "A": (6.35, 3.50), "B": (8.30, 4.30), "C": (8.75, 2.25)}
    lab_off = {"c": (-0.08, -0.42), "b": (-0.30, 0.26), "a": (-0.26, 0.30),
               "A": (0.26, 0.30), "B": (0.30, 0.26), "C": (0.12, -0.42)}
    for name, (x, y) in pts.items():
        col = C_E3 if name.islower() else C_TARGET
        ax.add_patch(Circle((x, y), 0.17, facecolor=col, edgecolor="black",
                            lw=0.8, zorder=5))
        dx, dy = lab_off[name]
        ax.text(x + dx, y + dy, name, ha="center", va="center", fontsize=11,
                fontweight="bold", zorder=6)

    for p, q in [("c", "b"), ("b", "a"), ("A", "B"), ("B", "C")]:
        ax.plot([pts[p][0], pts[q][0]], [pts[p][1], pts[q][1]],
                color="black", lw=1.1, zorder=4)

    # the single sampled coordinate
    arrow(ax, (pts["a"][0] + 0.24, pts["a"][1]),
          (pts["A"][0] - 0.24, pts["A"][1]),
          color=C_GOOD, lw=2.0, style="<|-|>", mutation=16)
    ax.text(5.62, 3.22, r"$r$", ha="center", va="top", fontsize=13,
            color=C_GOOD, fontweight="bold")

    # the two restrained angles, at their actual vertices
    C_ANG = "#8E44AD"
    draw_angle(ax, pts["a"], pts["b"], pts["A"], 0.62, r"$\theta_A$", C_ANG)
    draw_angle(ax, pts["A"], pts["a"], pts["B"], 0.62, r"$\theta_B$", C_ANG)

    # the three restrained dihedrals, as rotations about their central bonds
    C_DIH = "#D35400"
    draw_torsion(ax, pts["b"], pts["a"], 0.52, r"$\phi_A$", C_DIH,
                 lab_side=-1.0)
    draw_torsion(ax, pts["a"], pts["A"], 0.34, r"$\phi_B$", C_DIH,
                 lab_side=1.0)
    draw_torsion(ax, pts["A"], pts["B"], 0.52, r"$\phi_C$", C_DIH,
                 lab_side=-1.0)

    ax.text(5.0, 1.28,
            r"angles  $\theta_A$ = b–a–A,   $\theta_B$ = a–A–B",
            ha="center", fontsize=10, color=C_ANG, fontweight="bold")
    ax.text(5.0, 0.86,
            r"dihedrals  $\phi_A$ = c–b–a–A,   $\phi_B$ = b–a–A–B,   "
            r"$\phi_C$ = a–A–B–C",
            ha="center", fontsize=10, color=C_DIH, fontweight="bold")
    ax.text(5.0, 0.40,
            "all five are restrained, leaving $r$ (the interface CoM "
            "separation) as the only sampled CV",
            ha="center", fontsize=9, color=C_GOOD)
    ax.text(5.0, 0.04,
            r"anchors a/A = interface centres of mass;  b, c, B, C = low-RMSF, "
            r"non-collinear $C\alpha$ atoms",
            ha="center", fontsize=8.6, color=C_GREY, style="italic")

    fig.savefig(os.path.join(OUT, "fig3_boresch_anchors.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 4
def fig4_cv_splitting():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.3), sharey=True)
    x = np.linspace(0, 9, 400)

    ax = axes[0]
    y = -2.0 * np.log(x + 0.5) - 0.2 * x + 0.16 * np.sin(2.1 * x)
    y = y - y.min() + 0.3
    ax.plot(x, y, color=C_BAD, lw=2.0)
    ax.set_xlim(0, 9)
    ax.set_title("One CV for BD1 + BD2\n(PMF never reaches a minimum)",
                 fontsize=10.5, color=C_BAD, fontweight="bold")
    ax.annotate("still falling at 8 " + r"$\AA$" + "\n= 820 ns per replicate",
                xy=(8.2, y[np.argmin(np.abs(x - 8.2))] + 0.25),
                xytext=(3.9, 3.4), fontsize=9, color=C_BAD,
                arrowprops=dict(arrowstyle="->", color=C_BAD, lw=1.1))
    ax.text(4.6, 6.4, 'one bromodomain "spins" around the other',
            ha="center", fontsize=9, style="italic", color=C_GREY)
    ax.text(0.3, 0.9, "SE 0.9 kcal/mol\n(and unconverged)", fontsize=9,
            color=C_BAD, va="bottom")

    ax = axes[1]
    for shift, col, lab in [(1.2, "#2E7D5B", "BD1 alone"),
                            (2.0, "#4C86C6", "BD2 alone")]:
        y2 = 2.2 * (x - shift) ** 2 / (1 + 0.25 * (x - shift) ** 2)
        ax.plot(x, y2, color=col, lw=2.0, label=lab)
        ax.plot([shift], [0], marker="v", color=col, ms=8)
    ax.set_xlim(0, 9)
    ax.set_title("Split CVs: BD1 and BD2 restrained separately\n"
                 "(well-defined minima below 3 " + r"$\AA$" + ")",
                 fontsize=10.5, color=C_GOOD, fontweight="bold")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.text(4.3, 1.3, "SE 0.2 kcal/mol\n(converged)", fontsize=9,
            color=C_GOOD, va="bottom")

    for ax in axes:
        ax.set_xlabel(r"RMSD CV / $\AA$")
        ax.set_ylim(-0.4, 7.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_yticks([])
    axes[0].set_ylabel("PMF (schematic)")

    fig.suptitle("Fixing an unconvergeable collective variable by decomposing "
                 "it, not by sampling harder",
                 fontsize=11.5, fontweight="bold", y=1.04)
    fig.savefig(os.path.join(OUT, "fig4_cv_splitting.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 5
def fig5_results():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.3))

    ax = axes[0]
    methods = ["Geometric\nroute (US)", "HADDOCK\nscore", "MM/GBSA"]
    r2 = [0.95, 0.78, 0.62]
    bars = ax.bar(methods, r2, color=[C_GOOD, C_GREY, C_GREY], width=0.55,
                  edgecolor="black", lw=0.7)
    for b, v in zip(bars, r2):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, "%.2f" % v,
                ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel(r"$R^2$ vs TR-FRET affinities")
    ax.set_title(r"(A) CK1$\alpha$-lenalidomide-CRBN set (6 systems)",
                 fontsize=10.5, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    labels = ["BRD4\nG386E", "BRD3\nE344G"]
    vals = [5.0, -14.3]
    cols = [C_BAD, C_GOOD]
    bars = ax.barh(labels, vals, color=cols, height=0.45, edgecolor="black",
                   lw=0.7)
    for b, v, c in zip(bars, vals, cols):
        ax.text(v + (0.7 if v > 0 else -0.7), b.get_y() + b.get_height() / 2,
                "%+.1f" % v, va="center", ha="left" if v > 0 else "right",
                fontsize=10, fontweight="bold", color=c)
    ax.axvline(0, color="black", lw=0.9)
    ax.set_xlim(-18, 10)
    ax.set_ylim(-0.6, 1.75)
    ax.set_xlabel(r"$\Delta\Delta G_{calc}$ / kcal mol$^{-1}$")
    ax.set_title("(B) A single interfacial residue flips degradation\n"
                 "(MM/GBSA and docking are both blind to it)",
                 fontsize=10.5, fontweight="bold")
    ax.text(-17.5, 1.42, "degradation restored", fontsize=9, color=C_GOOD)
    ax.text(-17.5, 0.45, "degradation abolished", fontsize=9, color=C_BAD)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig5_results.png"))
    plt.close(fig)


if __name__ == "__main__":
    fig1_path_problem()
    fig2_thermo_cycle()
    fig3_boresch()
    fig4_cv_splitting()
    fig5_results()
    print("wrote:", sorted(os.listdir(OUT)))
