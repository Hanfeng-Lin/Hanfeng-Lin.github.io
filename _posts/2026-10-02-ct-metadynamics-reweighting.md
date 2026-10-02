---
title: 'Learning Notes: c(t) in Well-Tempered Metadynamics — Theory, Reweighting and Implementation'
date: 2026-10-02
permalink: /posts/2026/10/ct-metadynamics-reweighting/
tags:
  - Metadynamics
  - Enhanced Sampling
  - Molecular Dynamics
  - Free Energy
  - Drug Discovery
  - PLUMED
  - Computational Chemistry
---

> Study notes on the **time-dependent bias offset c(t)** in well-tempered metadynamics and how it is used to reweight simulations. Core reference: **Tiwary & Parrinello, "A Time-Independent Free Energy Estimator for Metadynamics", *J. Phys. Chem. B* 2015, 119, 736–742.** All figures below come from a small toy simulation I wrote for this post ([script](/images/blog/ct-metad/ct_metad_toy.py), numpy + matplotlib, about a minute to run).
>
> 本文是关于 well-tempered metadynamics 中**随时间变化的偏置偏移量 c(t)** 及其重加权用法的双语学习笔记。核心文献：**Tiwary & Parrinello, *J. Phys. Chem. B* 2015, 119, 736–742。** 文中所有图都来自我为本文写的一个玩具模型模拟（[脚本](/images/blog/ct-metad/ct_metad_toy.py)，只依赖 numpy + matplotlib，约一分钟跑完）。

---

## 1. The problem: a bias that never stops changing / 问题：一个永远在变的偏置

Metadynamics speeds up rare events by depositing repulsive Gaussian "hills" along a few collective variables (CVs) $s$. The hills accumulate into a bias $V(s,t)$ that fills free-energy wells and pushes the system over barriers. This is what makes it popular for ligand unbinding, conformational change and binding free energy in drug discovery.

Metadynamics 通过沿几个集体变量（CV）$s$ 不断堆放排斥性的高斯"小山"来加速稀有事件。这些小山累积成偏置势 $V(s,t)$，把自由能阱填平，推着体系越过能垒。正因如此，它在药物发现里常被用来研究配体解离、构象变化和结合自由能。

The catch: **$V(s,t)$ depends on time.** A frame recorded at 10 ns was sampled under a different bias than a frame at 100 ns. To recover unbiased statistics, especially for quantities you *did not* bias (a contact, a distance, a water count), every frame needs a weight, and frames from different times must be placed on a common scale. c(t) is that common scale.

麻烦在于：**$V(s,t)$ 是随时间变化的。** 10 ns 时记录的帧与 100 ns 时记录的帧是在不同偏置下采样的。要恢复无偏统计量，尤其是那些你**没有**加偏置的量（某个接触、某段距离、水分子数），就得给每一帧一个权重，而且不同时刻的帧必须放到同一把"尺子"上比较。c(t) 就是这把尺子。

---

## 2. Well-tempered metadynamics in three equations / 三个公式讲清 WTMetaD

**(1) Hill height decays where bias is already high.** Every $\tau$ steps a Gaussian is added at the current CV value $s(t)$:

**(1) 偏置越高的地方，新山越矮。** 每隔 $\tau$ 步在当前 CV 值 $s(t)$ 处加一个高斯：

$$V(s,t+\tau) = V(s,t) + W_0\, e^{-V(s(t),t)/k_B\Delta T}\, \exp\!\left[-\frac{(s-s(t))^2}{2\sigma^2}\right]$$

**(2) The bias factor.** $\Delta T$ sets how aggressively the bias tempers. It is usually written through the bias factor

**(2) 偏置因子。** $\Delta T$ 决定"回火"的力度，通常用偏置因子来表示：

$$\gamma = \frac{T+\Delta T}{T}$$

**(3) The long-time limit.** Once the bias stops changing shape (the *quasi-stationary* regime), it becomes an inverted, scaled copy of the free energy up to a time-dependent constant:

**(3) 长时间极限。** 当偏置的**形状**不再变化（**准稳态**）后，它就是自由能的倒置、缩放版本，外加一个随时间增长的常数：

$$V(s,t) \;\to\; -\left(1-\frac{1}{\gamma}\right)F(s) + \text{const}(t) \quad\Longleftrightarrow\quad F(s) = -\frac{\gamma}{\gamma-1}V(s,t) + \text{const}$$

That ever-growing constant is where c(t) comes from: the bias keeps rising everywhere even after its shape has converged.

正是这个不断增长的常数引出了 c(t)：偏置的形状收敛之后，它仍在整体上不停抬高。

![True free energy and bias snapshots with c(t)](/images/blog/ct-metad/fig1_bias_snapshots.png)

*Figure 1. Left: the true $F(s)$ of the toy model (deep well at $s=-1$, shallower well at $s=+1$). Right: the bias at three times. Its shape converges to an inverted copy of $F(s)$, but the whole curve keeps rising, and c(t) (dashed) rises with it.*

*图 1. 左：玩具模型真实的 $F(s)$（$s=-1$ 处为深阱，$s=+1$ 处为浅阱）。右：三个时刻的偏置。形状逐渐收敛为 $F(s)$ 的倒影，但整条曲线持续上移，c(t)（虚线）也随之上升。*

---

## 3. What c(t) is / c(t) 到底是什么

Assume the bias changes slowly compared with how fast the system relaxes (the *adiabatic* assumption). Then, at time $t$, the system is in equilibrium with the frozen bias $V(s,t)$:

假设偏置的变化远慢于体系的弛豫（**绝热假设**）。那么在时刻 $t$，体系就处于"冻结的" $V(s,t)$ 下的平衡态：

$$P_t(\mathbf{R}) = \frac{e^{-\beta[U(\mathbf{R}) + V(s(\mathbf{R}),t)]}}{Z_t}, \qquad P_0(\mathbf{R}) = \frac{e^{-\beta U(\mathbf{R})}}{Z_0}$$

The ratio between the unbiased and biased distributions is then

于是无偏分布与有偏分布之比为

$$\frac{P_0(\mathbf{R})}{P_t(\mathbf{R})} = e^{\beta\,[V(s,t)-c(t)]}, \qquad c(t) = -\frac{1}{\beta}\ln\frac{Z_t}{Z_0} = -\frac{1}{\beta}\ln\big\langle e^{-\beta V(s,t)}\big\rangle_0$$

Three ways to read this:

三种理解方式：

- **c(t) is a free-energy difference.** It is the reversible work of switching the current bias on, written as a Zwanzig exponential average. Readers of my [FEP vs NEQ post](/posts/2026/05/fep-vs-neq/) will recognize the formula. / **c(t) 是一个自由能差。** 它是"把当前偏置打开"的可逆功，形式就是 Zwanzig 指数平均。看过我那篇 [FEP vs NEQ](/posts/2026/05/fep-vs-neq/) 的读者应该很眼熟。
- **c(t) is roughly the "water level" of the bias in the most populated basin.** The unbiased system lives mostly in the deep well, so the average is dominated by the bias there. By Jensen's inequality $c(t) \le \langle V\rangle\_0$. In Figure 1, at t = 3000, the bias at $s=-1$ is about 32 kT and c(t) = 30.7 kT. / **c(t) 大致是最主要盆地里偏置的"水位"。** 无偏体系主要待在深阱里，所以平均值由那里的偏置主导。由 Jensen 不等式 $c(t) \le \langle V\rangle\_0$。图 1 中 t = 3000 时，$s=-1$ 处偏置约 32 kT，而 c(t) = 30.7 kT。
- **Its time derivative is the average rate of bias growth.** Differentiating gives $\dot c(t) = \langle \partial\_t V(s,t) \rangle\_{t}$, the bias growth rate averaged over the *biased* ensemble. / **它对时间的导数是偏置的平均增长速率。** 求导得 $\dot c(t) = \langle \partial\_t V(s,t) \rangle\_{t}$，即偏置增长速率在**有偏**系综上的平均。

**The Tiwary–Parrinello closed form.** $Z\_0$ and $Z\_t$ are unknown, but in WTMetaD we can substitute $F(s) = -\frac{\gamma}{\gamma-1}V(s,t)$ from Section 2. Everything then reduces to integrals over the CV grid:

**Tiwary–Parrinello 闭式表达。** $Z\_0$ 和 $Z\_t$ 都未知，但在 WTMetaD 中可以代入第 2 节的 $F(s) = -\frac{\gamma}{\gamma-1}V(s,t)$，于是一切都化为 CV 格点上的积分：

$$\boxed{\,c(t) = \frac{1}{\beta}\ln\frac{\displaystyle\int ds\; e^{\frac{\gamma}{\gamma-1}\beta V(s,t)}}{\displaystyle\int ds\; e^{\frac{1}{\gamma-1}\beta V(s,t)}}\,}$$

This is cheap: it needs only the current bias grid, no trajectory. It is what PLUMED evaluates when you turn on `CALC_RCT`.

计算代价很低：只需要当前的偏置格点，不需要轨迹。PLUMED 打开 `CALC_RCT` 时算的就是它。

![c(t) and the instantaneous bias over time](/images/blog/ct-metad/fig2_ct.png)

*Figure 2. The bias felt by the system $V(s(t),t)$ (gray) fluctuates as it moves between wells; c(t) (blue) is a smooth, monotonically increasing reference. Their difference, $V - c(t)$, stays bounded, and that is what makes it usable as a log-weight.*

*图 2. 体系感受到的偏置 $V(s(t),t)$（灰）随其在阱间穿梭而剧烈波动；c(t)（蓝）是一条平滑、单调上升的参考线。二者之差 $V - c(t)$ 始终有界，正因如此才能拿来当对数权重。*

---

## 4. Reweighting with c(t) / 用 c(t) 做重加权

Each frame $i$ recorded at time $t\_i$ gets the weight

在时刻 $t\_i$ 记录的第 $i$ 帧，其权重为

$$w_i = e^{\beta\,[V(s_i,t_i) - c(t_i)]}, \qquad \langle O\rangle_0 \approx \frac{\sum_i w_i\, O_i}{\sum_i w_i}$$

PLUMED calls $V - c(t)$ the **`rbias`** ("reweighted bias"). Any observable can then be reweighted: a histogram of an unbiased CV, a population ratio, a contact probability.

PLUMED 把 $V - c(t)$ 称为 **`rbias`**（"重加权偏置"）。之后任何可观测量都可以重加权：未加偏置 CV 的直方图、布居比、接触概率等。

**Why not just use $e^{\beta V}$?** Within a single frozen bias, a global constant cancels on normalization. But c(t) is not constant: it grew from 0 to about 31 kT in the toy run. Leaving it out makes late frames exponentially heavier than early ones for no physical reason. Most of the trajectory gets almost zero weight, and frames from different "bias epochs" are mixed on inconsistent scales.

**为什么不直接用 $e^{\beta V}$？** 在同一个冻结的偏置下，全局常数会在归一化时消掉。但 c(t) 不是常数：在玩具模拟中它从 0 涨到约 31 kT。不扣掉它，后期帧的权重会毫无物理理由地比早期帧大几个数量级。大部分轨迹的权重几乎为零，而且不同"偏置时期"的帧被放在不一致的尺度上混在一起。

![Reweighted free energy of an unbiased variable](/images/blog/ct-metad/fig3_reweight.png)

*Figure 3. Toy model: the bias acts only on $x$, and we recover the free energy of the **unbiased** variable $y$. With c(t) (blue) the result follows the exact curve, and the Kish effective sample size $n\_\text{eff} = (\sum w)^2/\sum w^2$ is 37.9% of the frames. Without c(t) (orange) only 9.9% of the data effectively contributes and the curve is visibly noisier, especially in the tails.*

*图 3. 玩具模型：偏置只加在 $x$ 上，我们要恢复**未加偏置**的变量 $y$ 的自由能。用 c(t)（蓝）时结果贴合精确曲线，Kish 有效样本量 $n\_\text{eff} = (\sum w)^2/\sum w^2$ 为总帧数的 37.9%。不用 c(t)（橙）时只有 9.9% 的数据真正起作用，曲线明显更噪，尤其在尾部。*

> Honest caveat / 坦白说明: in this simple, well-converged toy model the no-c(t) curve is noisy rather than badly wrong. In real systems with long transients and hidden slow modes, the inconsistency across bias epochs also shifts relative populations. / 在这个简单且收敛良好的玩具模型里，不扣 c(t) 的结果主要是"噪"而不是"错得离谱"。但在真实体系中，若有长过渡期和隐藏慢变量，不同偏置时期间的不一致还会让相对布居发生偏移。

**A time-independent estimator.** Because every frame is placed on the same scale, the reweighted estimate *accumulates* information as the run continues, instead of just reporting the latest bias. Figure 4 compares two ways of computing $\Delta F$ between the wells.

**一个与时间无关的估计量。** 因为每一帧都被放到同一尺度上，重加权估计会随模拟进行而**累积**信息，而不只是反映最新的偏置。图 4 比较了计算两阱间 $\Delta F$ 的两种方法。

![Convergence of Delta F](/images/blog/ct-metad/fig4_deltaF.png)

*Figure 4. $\Delta F$ (right well minus left well). Estimating it from the current bias alone (green) keeps oscillating, because each hill reshapes the bias. The c(t)-reweighted estimate (blue) averages over the whole post-transient trajectory and settles near the exact 1.52 kT (final value 1.55 kT, versus 1.65 kT from the bias alone).*

*图 4. $\Delta F$（右阱减左阱）。只用当前偏置估计（绿）会一直振荡，因为每座新山都在改变偏置的形状。c(t) 重加权估计（蓝）对整段过渡期之后的轨迹求平均，稳定在精确值 1.52 kT 附近（最终 1.55 kT，只用偏置估计为 1.65 kT）。*

---

## 5. Implementation / 实现方法

### 5.1 The core loop in ~20 lines / 20 行左右的核心循环

Stripped down from the toy script (units of kT, so β = 1). The only addition to plain WTMetaD is the `ct_from_bias` call after each hill:

从玩具脚本中精简而来（以 kT 为单位，β = 1）。与普通 WTMetaD 相比，唯一多出来的就是每加一座山后调用一次 `ct_from_bias`：

```python
def ct_from_bias(V, gamma, beta=1.0):
    """Tiwary-Parrinello c(t) from the bias on a CV grid (log-sum-exp for stability)."""
    a = gamma * beta * V / (gamma - 1)
    b = beta * V / (gamma - 1)
    lse = lambda z: z.max() + np.log(np.exp(z - z.max()).sum())
    return (lse(a) - lse(b)) / beta

for step in range(nsteps):
    i = grid_index(x)                       # nearest grid point of the CV
    if step % STRIDE == 0:                  # "COLVAR": store CVs, V and c(t)
        frames.append((x, y, V[i], c_now))
    if step % PACE == 0:                    # deposit a well-tempered hill
        h = W0 * np.exp(-beta * V[i] / (gamma - 1))
        g = h * np.exp(-0.5 * ((grid - x) / sigma) ** 2)
        V += g
        dV += g * (-(grid - x) / sigma**2)
        c_now = ct_from_bias(V, gamma)      # <-- the c(t) update
    gx, gy = grad_U(x, y)
    gx += dV[i]                             # bias force acts on the CV only
    x += -gx * dt + np.sqrt(2 * dt / beta) * rng.standard_normal()
    y += -gy * dt + np.sqrt(2 * dt / beta) * rng.standard_normal()

# afterwards: log-weights for reweighting
logw = beta * (V_frames - c_frames)
```

Two details matter. First, the grid integrals in `ct_from_bias` must use log-sum-exp: $\frac{\gamma}{\gamma-1}\beta V$ reaches tens of kT and plain `exp` overflows. Second, each frame stores the c(t) that was current *when it was sampled*. Recomputing c from the final bias for every frame is a different (and wrong) estimator.

两个细节很重要。第一，`ct_from_bias` 里的格点积分必须用 log-sum-exp：$\frac{\gamma}{\gamma-1}\beta V$ 能到几十 kT，直接 `exp` 会溢出。第二，每一帧存的是**它被采样时**的 c(t)。对每一帧都用最终偏置重新算 c，是另一种（错误的）估计量。

### 5.2 In PLUMED / 在 PLUMED 中

PLUMED implements this inside `METAD`. Add `CALC_RCT` (this **requires a grid**), and optionally `RCT_USTRIDE` to update c(t) only every N hills. PLUMED then exposes `metad.rct` (c(t)) and `metad.rbias` (= `metad.bias − metad.rct`).

PLUMED 在 `METAD` 内部实现了这一点。加上 `CALC_RCT`（**必须使用格点**），并可用 `RCT_USTRIDE` 设置每 N 座山才更新一次 c(t)。之后 PLUMED 会提供 `metad.rct`（即 c(t)）和 `metad.rbias`（= `metad.bias − metad.rct`）。

```
# plumed.dat — production run (example: ligand–pocket distance as the CV)
# atom indices are placeholders; take them from your own topology
lig:    GROUP ATOMS=2601-2640
pocket: GROUP ATOMS=410,415,422,980,986,1203
lcom:   COM ATOMS=lig
pcom:   COM ATOMS=pocket

d:     DISTANCE ATOMS=lcom,pcom                          # biased CV
coord: COORDINATION GROUPA=lig GROUPB=pocket R_0=0.45   # NOT biased; reweighted later

metad: METAD ...
   ARG=d SIGMA=0.05 HEIGHT=1.2 PACE=500
   BIASFACTOR=10 TEMP=300
   GRID_MIN=0.0 GRID_MAX=4.0 GRID_BIN=800
   CALC_RCT RCT_USTRIDE=10
   FILE=HILLS
...

PRINT ARG=d,coord,metad.bias,metad.rct,metad.rbias STRIDE=500 FILE=COLVAR
```

You can also build the reweighted histogram on the fly, by feeding `metad.rbias` to `REWEIGHT_BIAS` and using its output as log-weights:

也可以在模拟过程中直接构建重加权直方图：把 `metad.rbias` 交给 `REWEIGHT_BIAS`，再把它的输出当作对数权重：

```
rw:    REWEIGHT_BIAS TEMP=300 ARG=metad.rbias
hc:    HISTOGRAM ARG=coord GRID_MIN=0 GRID_MAX=20 GRID_BIN=200 BANDWIDTH=0.2 LOGWEIGHTS=rw
fc:    CONVERT_TO_FES GRID=hc TEMP=300
DUMPGRID GRID=fc FILE=fes_coord.dat STRIDE=100000
```

Or post-process `COLVAR` yourself, which makes it easy to discard the transient and run block analysis:

或者自己后处理 `COLVAR`，这样更方便丢弃过渡期并做分块分析：

```python
import numpy as np

kT = 0.0083144626 * 300               # kJ/mol, PLUMED default units
with open("COLVAR") as f:
    fields = f.readline().split()[2:]  # "#! FIELDS time d coord ..."
data = np.loadtxt("COLVAR", comments="#")
col = {name: data[:, k] for k, name in enumerate(fields)}

keep = col["time"] > 0.1 * col["time"][-1]          # drop the initial transient
logw = col["metad.rbias"][keep] / kT
w = np.exp(logw - logw.max())

hist, edges = np.histogram(col["coord"][keep], bins=100, weights=w)
fes = -kT * np.log(hist)
fes -= np.nanmin(fes[np.isfinite(fes)])
n_eff = w.sum() ** 2 / (w ** 2).sum()                # Kish effective sample size
```

### 5.3 Practical checklist / 实践检查清单

| Item / 项目 | What to do / 怎么做 |
|---|---|
| Transient / 过渡期 | Plot c(t). Discard the early part where it rises steeply and the bias is still reshaping (here, the first 10%). / 画出 c(t)，丢掉它陡升、偏置还在大幅变形的早期部分（本例为前 10%）。 |
| Grid range / 格点范围 | The grid must cover everywhere the CV goes, or the integrals in c(t) are truncated. / 格点必须覆盖 CV 到过的所有区域，否则 c(t) 的积分会被截断。 |
| Adiabaticity / 绝热性 | Hills too tall or too frequent break the quasi-equilibrium assumption. Keep PACE × (hill height) modest relative to the system's relaxation time. / 山太高或太密会破坏准平衡假设。相对体系弛豫时间，PACE 与山高要适中。 |
| CV quality / CV 质量 | A slow mode missing from the CVs (e.g. a side-chain flip or a water entering the pocket) is the real failure mode. The weights are then formally correct only for the slice of phase space actually sampled. / CV 里漏掉的慢变量（如侧链翻转、水分子进入口袋）才是真正的失败来源。此时权重只对实际采样到的那部分相空间形式上正确。 |
| Static restraints / 静态限制势 | Walls you want removed go into `REWEIGHT_BIAS ARG=` together with `metad.rbias`. A funnel restraint (funnel metaD) is kept and corrected analytically through the standard-state volume term instead. / 想去掉的墙势要和 `metad.rbias` 一起放进 `REWEIGHT_BIAS ARG=`。漏斗限制势（funnel metaD）则保留，并通过标准态体积项解析校正。 |
| Error bars / 误差 | Use block averaging on the weighted data and report $n\_\text{eff}$, not the raw frame count. / 对加权数据做分块平均，并报告 $n\_\text{eff}$ 而非原始帧数。 |

---

## 6. c(t) is not the acceleration factor / c(t) 不等于加速因子

Both quantities are exponentials of the bias, and both come from Tiwary & Parrinello, so they are easy to confuse:

两者都是偏置的指数形式，又都出自 Tiwary & Parrinello，很容易混淆：

| | **c(t) reweighting** | **Acceleration factor (infrequent metaD)** |
|---|---|---|
| Goal / 目标 | Thermodynamics: populations, FES, ΔG / 热力学：布居、FES、ΔG | Kinetics: rates, residence time / 动力学：速率、停留时间 |
| Formula / 公式 | $w = e^{\beta(V-c(t))}$, per frame / 逐帧 | $\alpha = \langle e^{\beta V(s,t)}\rangle\_t$, $t\_\text{real} = \alpha\, t\_\text{MD}$ |
| Bias regime / 偏置方式 | Keep depositing until converged / 持续加山直至收敛 | Rare, gentle hills; bias must stay off the transition state / 稀疏、轻柔的山，偏置不能碰到过渡态 |
| PLUMED / PLUMED | `CALC_RCT` → `metad.rbias` | `ACCELERATION` → `metad.acc` |

Infrequent metaD (Tiwary & Parrinello, *PRL* 2013; applied to protein–ligand unbinding in Tiwary et al., *PNAS* 2015) is the route to drug **residence times**. c(t) reweighting is the route to **affinities and mechanisms**.

Infrequent metaD（Tiwary & Parrinello, *PRL* 2013；Tiwary 等人 *PNAS* 2015 将其用于蛋白-配体解离）是求药物**停留时间**的方法。c(t) 重加权则是求**亲和力和机制**的方法。

---

## 7. Where it sits in drug discovery and recent literature / 在药物发现与近期文献中的位置

**Typical use / 典型用法.** In funnel metadynamics (Limongelli, Bonomi & Parrinello, *PNAS* 2013; protocol in Raniolo & Limongelli, *Nat. Protoc.* 2020), the bias acts on one or two funnel CVs (depth along the funnel axis, distance from the axis). Reweighting then projects the binding free energy surface onto variables that were never biased: key hydrogen bonds, pocket hydration, ligand torsions. Those projections are what tell a medicinal chemist *why* a modification helps. A recent example is Troussicot et al. (*ACS Omega* 2026), who used funnel metaD to design a peroxiredoxin-5 inhibitor and reweighted along unbiased CVs (they used the Bonomi et al. scheme, the older alternative to c(t)). The predicted gain in affinity was confirmed by NMR.

在 funnel metadynamics（Limongelli, Bonomi & Parrinello, *PNAS* 2013；操作流程见 Raniolo & Limongelli, *Nat. Protoc.* 2020）中，偏置加在一两个漏斗 CV 上（沿漏斗轴的深度、离轴距离）。然后通过重加权把结合自由能面投影到从未加偏置的变量上：关键氢键、口袋水合、配体扭转角。正是这些投影告诉药化人员某个修饰**为什么**有效。近期的例子是 Troussicot 等人（*ACS Omega* 2026）：他们用 funnel metaD 设计过氧化物还原酶 5 的抑制剂，并沿未加偏置的 CV 做重加权（用的是 Bonomi 等人的方案，即 c(t) 之前的较早替代方法），预测的亲和力提升得到了 NMR 证实。

**Methodological context / 方法学背景.**

- **Barducci, Bussi & Parrinello, *PRL* 2008**: well-tempered metadynamics, the $\gamma$ bias factor and the asymptotic $F \leftrightarrow V$ relation. / 提出 well-tempered metadynamics、偏置因子 $\gamma$ 以及 $F \leftrightarrow V$ 渐近关系。
- **Bonomi et al., *J. Comput. Chem.* 2009**: an earlier reweighting scheme for WTMetaD. / 早期的 WTMetaD 重加权方案。
- **Tiwary & Parrinello, *J. Phys. Chem. B* 2015**: the c(t) estimator discussed here. / 本文讨论的 c(t) 估计量。
- **Marinova & Salvalaglio, *J. Chem. Phys.* 2019 (mean force integration, MFI)**: obtains time-independent FES from history-dependent bias *without* computing c(t), by integrating local mean forces. / 通过积分局部平均力，**无需**计算 c(t) 即可从历史相关偏置得到与时间无关的 FES。
- **Schäfer & Settanni, *J. Chem. Theory Comput.* 2020, "Data Reweighting in Metadynamics Simulations"**: a systematic comparison of reweighting schemes, c(t) included. / 系统比较了包括 c(t) 在内的各种重加权方案。
- **Invernizzi & Parrinello, *J. Phys. Chem. Lett.* 2020 (OPES)**: the bias quickly becomes quasi-static, so reweighting reduces to plain $e^{\beta V}$. Much of the field has moved this way, but c(t) remains the standard tool for the large body of existing WTMetaD data and protocols. / OPES 的偏置很快变为准静态，重加权退化为简单的 $e^{\beta V}$。不少人已转向 OPES，但面对大量现有的 WTMetaD 数据和流程，c(t) 仍是标准工具。
- **Ghidini, Serra & Cavalli, *Acc. Chem. Res.* 2025, "On Free Energy Calculations in Drug Discovery"**: reviews semi-automatic metadynamics-based and nonequilibrium protocols for binding free energies. / 综述了基于 metadynamics 与非平衡模拟的半自动结合自由能流程。
- **Mandelli, Ippoliti & Plate, arXiv:2608.04834 (2026)**: on turning simulated bound/unbound *populations*, which are exactly what reweighting produces, into absolute binding affinities with the correct volumetric (standard-state) terms. They report that common single-bin estimators can be off by about 1 kcal/mol. / 讨论如何把模拟得到的结合/解离**布居**（正是重加权的产物）正确转化为绝对结合亲和力（含正确的体积/标准态项）；指出常见的单 bin 估计量可偏差约 1 kcal/mol。
- **Badanin & Rogacheva, arXiv:2609.01934 (2026)**: a mathematical analysis of metadynamics convergence with Gaussian hills. Convergence is proven for periodic 1D CVs; on a bounded interval no proper quasi-stationary state exists. That is a formal reminder of why CV boundaries and walls need care. / 对高斯山 metadynamics 收敛性的数学分析：对周期性一维 CV 证明了收敛，而在有界区间上不存在真正的准稳态。这从理论上提醒我们，CV 边界和墙势需要谨慎处理。

---

## One-line takeaway / 一句话总结

c(t) is the free energy of "switching on" the current metadynamics bias, $-k\_BT\ln\langle e^{-\beta V}\rangle\_0$. Subtracting it puts every frame of a well-tempered run on a single scale, turning a history-dependent simulation into a time-independent estimator of any observable. In practice it is one keyword (`CALC_RCT`) plus a careful look at the transient, the grid and the CVs.

c(t) 是"打开"当前 metadynamics 偏置的自由能，$-k\_BT\ln\langle e^{-\beta V}\rangle\_0$。把它扣掉，就能把 well-tempered 模拟的每一帧放到同一尺度上，从而把一个历史相关的模拟变成任意可观测量的、与时间无关的估计量。实际操作上只是一个关键词（`CALC_RCT`），外加认真检查过渡期、格点范围和 CV。

---

*Notes written 2026-10-02. Figures are from a toy model, not a production system. Corrections welcome. / 笔记写于 2026-10-02，图片来自玩具模型而非真实体系，欢迎指正。*
