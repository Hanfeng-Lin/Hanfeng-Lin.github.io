---
title: 'Learning Notes: Umbrella Sampling for Ternary Complexes — How the Geometric Route Handles the "Is My Dissociation Path Complete?" Problem'
date: 2026-11-16
permalink: /posts/2026/11/umbrella-sampling-ternary-complex-geometric-route/
tags:
  - Free Energy
  - Molecular Dynamics
  - Umbrella Sampling
  - Targeted Protein Degradation
  - Molecular Glue
  - PROTAC
  - Computational Chemistry
  - Drug Discovery
---

> Study notes on **"Predicting Ternary Complex Stability through Binding Free-Energy Calculations in the Geometric Route"** (Benedict Tan, Alessio Ciulli & Julien Michel, *J. Chem. Theory Comput.* 2026, 22, 11662–11675; Edinburgh + Dundee). [DOI: 10.1021/acs.jctc.6c01541](https://doi.org/10.1021/acs.jctc.6c01541) · code at [michellab/MolecularGluesBFE](https://github.com/michellab/MolecularGluesBFE).
>
> 本文是对上述论文的双语学习笔记，每节先英文、后中文。它接着前两篇笔记往下讲：[从 FEP 到 NEQ](/posts/2026/05/fep-vs-neq/) 和 [ML-guided AQFEP](/posts/2026/07/aqfep-ml-guided-virtual-screening/) 讲的是小分子的**炼金术**路径，这篇讲的是蛋白-蛋白界面的**几何**路径。
>
> *All figures below are my own schematics drawn for these notes, not reproductions of the paper's figures. / 下面所有图都是我为这篇笔记自己画的示意图，不是论文原图。*

---

## 1. Why alchemy runs out of road / 为什么炼金术在这里走不通

In the AQFEP notes, absolute binding free energies came from **double decoupling**: turn the ligand into a "ghost" in the pocket, turn it into a ghost in water, close the cycle. That works because a drug-like ligand is small — a few dozen atoms you can switch off over a manageable number of λ windows.

在 AQFEP 那篇笔记里，绝对结合自由能来自**双解耦**：把配体在口袋里变成"幽灵"，再在水里变成"幽灵"，闭合循环。这条路走得通，是因为类药配体很小——几十个原子，用数量可控的 λ 窗口就能关掉。

A ternary complex is a different animal. In targeted protein degradation (TPD), a molecular glue or PROTAC induces a complex between a **target protein**, the **small molecule**, and an **E3 ligase**. What matters is not "how tightly does the glue bind CRBN" but **how stable is the protein–protein interface the glue creates**. You cannot alchemically annihilate a whole protein: a bromodomain has thousands of atoms, and decoupling it from solvent is hopeless.

三元复合物是另一回事。在靶向蛋白降解（TPD）里，分子胶或 PROTAC 诱导**靶蛋白**、**小分子**和 **E3 连接酶**形成复合物。真正要紧的不是"胶和 CRBN 结合有多紧"，而是**胶造出来的那个蛋白-蛋白界面有多稳**。而你没法用炼金术把一整个蛋白湮灭掉：一个 bromodomain 有几千个原子，把它从溶剂里解耦出来根本不现实。

So you are forced to do the very thing alchemical FEP was invented to avoid: pull the two proteins apart along a **real, physical path**, and compute the free energy as you go. That is **Umbrella Sampling (US)** in the **geometric route**.

于是你被迫去做炼金术 FEP 当初发明出来就是为了避免的事：沿着一条**真实的物理路径**把两个蛋白拉开，并沿途算自由能。这就是**几何路径**下的**伞形采样（Umbrella Sampling, US）**。

---

## 2. The core worry: is one path enough? / 核心疑问：一条路径够吗？

This is the question in the title, and it should bother anyone trained on alchemical methods.

这正是标题要回答的问题，也是任何被炼金术方法训练过的人都该不安的地方。

Free energy is a **state function**, so an alchemical path is allowed to be arbitrary and unphysical. A *physical* dissociation path is different: there is no single correct way for two proteins to come apart. They can slide, rock, rotate, or peel from one edge. Pick one separation coordinate — say the distance between two interface centres of mass — and push along it, and you are sampling **one tunnel through a very high-dimensional space**. The orthogonal degrees of freedom (relative orientation, internal conformation of each protein) are uncontrolled, and two failure modes follow.

自由能是**状态函数**，所以炼金术路径可以任意、可以非物理。但**物理解离路径**不一样：两个蛋白分开没有唯一正确的方式。它们可以滑、可以摇、可以转，也可以从一边"撕"开。你挑一个分离坐标——比如两个界面质心之间的距离——沿着它推，采样的就只是**高维空间里的一条隧道**。正交自由度（相对取向、各自的内部构象）完全不受控，于是有两种失败模式。

![Figure 1 — The path-completeness problem and the geometric route's answer. Left: with only a separation coordinate controlled, the two proteins can slide, rock and rotate as they come apart, so the PMF reflects whichever tunnel the steered MD happened to carve. Right: RMSD restraints freeze each protein's conformation and Boresch restraints freeze their relative orientation, leaving the separation coordinate r as the only free CV — and every restraint's free energy is paid back later in the cycle.](/images/blog/us-ternary-geometric-route/fig1_path_completeness.png)

1. **Under-sampling / 采样不足.** In each separation window the proteins have time to tumble and rearrange; converging over all of that is, in practice, never achieved. / 在每个分离窗口里，两个蛋白都有时间翻滚、重排；要把这些全部采样收敛，实际上做不到。
2. **Path dependence / 路径依赖.** The PMF depends on which tunnel your steered MD carved. A different pull gives a different number, with no internal way to tell which is right. / PMF 取决于你的 steered MD 恰好挖出了哪条隧道。换一次拉伸就得到另一个数，而你没有任何内部判据能说明哪个才对。

The geometric route's answer is almost cheeky in its simplicity: **do not let the orthogonal degrees of freedom move — restrain them, and then pay back the cost of every restraint exactly.**

几何路径的答案简单到近乎取巧：**干脆不让正交自由度动——把它们限制住，再把每个限制的代价精确地还回去。**

---

## 3. The trick: restrain, then refund / 关键技巧：先限制，再把账还清

The intellectual move is the same one that makes absolute FEP work, pushed further. In double decoupling you add a Boresch restraint so the ghost ligand cannot drift, then subtract that restraint's free energy analytically. The geometric route (Woo & Roux 2005, here with the Boresch-style restraint implementation of Notari et al. 2025) applies the same idea to **every** degree of freedom you refuse to sample.

思想动作和绝对 FEP 是同一个，只是推得更远。双解耦里你加一个 Boresch 限制势，让幽灵配体不能乱飘，再把这部分自由能解析地扣掉。几何路径（Woo & Roux 2005；这里用的是 Notari 等 2025 的 Boresch 式实现）把这个想法用到了**每一个你拒绝采样的自由度**上。

![Figure 2 — The five-stage thermodynamic cycle. Stages (1) and (2) add conformational and orientational restraints to the bound complex; stage (3) is the separation umbrella sampling along r; stage (4) releases the orientational restraints analytically at large separation; stage (5) releases the conformational restraints in bulk. The path ambiguity of Figure 1 has been converted into restraint free energies that are computed rather than assumed.](/images/blog/us-ternary-geometric-route/fig2_thermodynamic_cycle.png)

$$\Delta G_{bind} = \Delta G_{sep} + \Delta G_{c,bulk} - \Delta G_{c,bound} - \Delta G_{o,bound} + \Delta G_{corr}$$

**Why this addresses the completeness problem / 为什么这解决了"路径完备性"问题.** During the separation stage the two proteins can neither reorient nor change conformation, because the earlier stages nailed those down. The tunnel is no longer an arbitrary slice of a wide space — it is the *only* thing left to sample. Path ambiguity has been converted into **restraint free energies that are computed, not assumed.** Stage (4) matters most here: once the proteins are far apart, the free energy of releasing the orientational restraints has a **closed form** depending only on the force constants, the equilibrium angle, and the standard-state volume. The angular space the complex was forbidden from exploring is restored **by integration rather than by simulation**.

**为什么这解决了"路径完备性"问题。** 分离阶段里，两个蛋白既不能重新取向也不能改变构象，因为前面两步已经把它们钉死了。那条隧道不再是宽阔空间里随手切的一刀——它是**唯一还剩下要采样的东西**。路径的不确定性被转化成了**算出来、而不是假设掉的限制自由能**。第（4）步最关键：两个蛋白一旦拉得足够远，松开取向限制的自由能有**闭式解**，只依赖力常数、平衡角度和标准态体积。复合物被禁止探索的那片角度空间，是靠**积分而不是模拟**还回来的。

> **One-sentence version / 一句话版本:** you don't make the path complete — you make it **narrow enough to be the only path**, then analytically refund everything you forbade. / 你不是把路径变完备，而是把它**收窄到只剩这一条**，再把禁止掉的东西解析地退还。

---

## 4. The practical machinery / 具体是怎么干的

Three implementation details carry most of the real weight; skipping any of them is where a reimplementation would fail.

有三个实现细节承担了大部分真实工作量，复现时跳过任何一个都会翻车。

![Figure 3 — The Boresch restraint scheme. Six anchor points (three per protein) define two angles and three dihedrals; restraining all five, plus the Cα RMSD of each protein, leaves the interface centre-of-mass separation r as the single sampled coordinate. Anchors b, c, B and C are chosen at local minima of the RMSF plot so that the restrained angles are built on rigid parts of the structure.](/images/blog/us-ternary-geometric-route/fig3_boresch_anchors.png)

**Anchor selection / 锚点选择.** The Boresch scheme needs six anchors: three in the glue-bound receptor, three in the ligand protein. An anchor on a floppy loop makes the restrained angles meaningless. The authors run 100 ns of unrestrained MD in triplicate, compute **RMSF**, and pick anchors at **local minima of the RMSF plot** that are also non-collinear. The two interface centres of mass are the "bonded" pair that defines the separation coordinate. Equilibration is detected automatically with White's marginal standard error rule (the RED package), not by eye.

**锚点选择。** Boresch 方案需要六个锚点：受体（带胶的那一侧）三个，配体蛋白三个。锚点落在柔性 loop 上，被限制的角度就失去意义。作者跑三次独立的 100 ns 无限制 MD，算 **RMSF**，在 **RMSF 的局部极小**处挑锚点，并要求不共线。两个界面质心作为"成键"的一对，定义分离坐标。平衡时刻用 White 的边际标准误准则（RED 包）自动判定，而不是靠眼睛看。

**Sequential application / 限制势逐个施加.** Restraints are not switched on together. US runs for θ_A first (with only RMSD restraints present), then θ_B in the presence of the θ_A restraint, then the three dihedrals one at a time, each with all previously applied restraints in place. Each stage's equilibrium value is read off as the **minimum of the previous stage's PMF**, not taken from the crystal structure. This keeps every PMF one-dimensional and every contribution well defined.

**限制势逐个施加。** 限制不是同时打开的。先对 θ_A 做 US（此时只有 RMSD 限制在场），再在 θ_A 限制下做 θ_B，然后三个二面角逐个来，每个都在前面所有限制就位的条件下进行。每一步的平衡值取自**上一步 PMF 的极小位置**，而不是直接用晶体结构的值。这样每条 PMF 都是一维的，每项贡献都定义清楚。

**Starting structures from steered MD / 用 steered MD 生成起始构型.** Each separation window needs a starting configuration. One steered MD run pulls r out toward 40 Å over 2 ns, saving snapshots every 0.5 Å (out to 21 Å) and every 1.0 Å beyond. Those snapshots seed the US windows. The box carries 15 Å of padding so that widely separated windows never see their own periodic images.

**用 steered MD 生成起始构型。** 每个分离窗口都需要起始构型。作者用一次 steered MD 在 2 ns 内把 r 拉向 40 Å，21 Å 以内每 0.5 Å、之后每 1.0 Å 存一帧，用这些帧作为各 US 窗口的种子。水盒子留 15 Å padding，确保分离很远的窗口不会"看到"自己的周期性镜像。

---

## 5. How they show the answer is trustworthy / 他们怎么证明结果可信

Restraining away the hard degrees of freedom is only legitimate if each contribution is genuinely converged. Four checks, all worth stealing:

把难采样的自由度限制掉，只有在每项贡献确实收敛时才合法。四道检查，都值得照搬：

- **Window overlap / 窗口重叠.** CV histograms of neighbouring windows are inspected for overlap before WHAM is applied — the same logic as λ-overlap in FEP.
- **Forward/reverse convergence / 正反向收敛.** For each stage, a free energy estimate from the first *t* of equilibrated samples is compared with one from the last *t*; agreement within 1 kcal/mol is the pass mark. The separation stage is slowest: only **31 of 42 replicates** pass at 80% sampling time. The authors report this rather than bury it.
- **Integral coverage / 积分覆盖率.** Restraint free energies come from integrating over the CV. Both numerator and denominator integrands must decay below 1% of their maximum, capturing >98% of each contribution — a direct check that the restrained coordinate's accessible range really was covered.
- **Triplicates throughout / 处处三重复.** Every US simulation runs three times; inter-replicate standard error is the reported precision (<1.1 kcal/mol for the CRBN systems).

- **窗口重叠.** 做 WHAM 之前先看相邻窗口 CV 直方图是否重叠，逻辑同 FEP 里的 λ-overlap。
- **正反向收敛.** 每个阶段用"前 t 段平衡样本"和"后 t 段样本"各估一次自由能，差在 1 kcal/mol 以内算通过。分离阶段最慢：42 次重复里只有 **31 次**在 80% 采样时达标——这个数字写在正文里，没有被藏起来。
- **积分覆盖率.** 限制自由能靠对 CV 积分得到，要求分子和分母的被积函数都衰减到最大值的 1% 以下，捕获每项贡献的 >98%，等于直接检查"被限制坐标能到达的范围真的覆盖到了"。
- **处处三重复.** 每个 US 模拟跑三次，用重复间标准误作为精度（CRBN 体系 <1.1 kcal/mol）。

---

## 6. When the recipe breaks: the dual-bromodomain problem / 方子失灵时：双 bromodomain 难题

The most instructive part of the paper is where the protocol fails and has to be redesigned. The BRD4 degrader IBG1 engages **both** bromodomains (BD1 and BD2) of BRD4 at once.

全文最有教益的部分，是协议失灵、被迫重新设计的地方。BRD4 降解剂 IBG1 **同时**抓住 BRD4 的两个 bromodomain（BD1 和 BD2）。

Putting BD1 and BD2 under a **single RMSD collective variable** does not work. In the unbound state the interdomain contacts are weak, so the RMSD PMF spans more than 6 Å without ever reaching a well-defined minimum — in high-RMSD windows the authors watched one bromodomain **spinning around the other**. Even at a CV value of 8 Å, corresponding to 820 ns per replicate, the contribution had not converged.

把 BD1 和 BD2 放进**同一个 RMSD 集合变量**行不通。自由态下两个结构域之间接触很弱，RMSD PMF 铺开超过 6 Å 也到不了明确极小——在高 RMSD 窗口里，作者看到一个 bromodomain 绕着另一个**打转**。哪怕 CV 推到 8 Å（对应每个重复 820 ns），这项贡献仍未收敛。

![Figure 4 — Why the collective variable had to be decomposed. Left: a single RMSD CV covering both bromodomains yields a PMF with no minimum inside the sampled range, so the free energy contribution never converges and the inter-replicate error stays near 0.9 kcal/mol. Right: restraining BD1 and BD2 as separate, sequentially applied CVs confines each to a 0–3 Å range with a clear minimum, and cumulative error drops to about 0.2 kcal/mol. Curves are schematic illustrations of the described behaviour, not digitised data.](/images/blog/us-ternary-geometric-route/fig4_cv_splitting.png)

The fix is to **split the CV**: restrain DCAF16 first, then BD1 in the presence of the DCAF16 restraint, then BD2 with both in place. Each isolated bromodomain needs only a 0–3 Å range. This adds a stage to the cycle but shrinks the sampling range enormously, and precision improves from 0.9 kcal/mol (single CV, still unconverged) to about 0.2 kcal/mol cumulative.

解决办法是**把 CV 拆开**：先限制 DCAF16，再在其限制存在下限制 BD1，最后在前两者都在场时限制 BD2。单个 bromodomain 只需要 0–3 Å 范围。这给循环多加一步，但采样范围大幅收缩，精度从 0.9 kcal/mol（单一 CV，且未收敛）改善到累计约 0.2 kcal/mol。

**The general lesson / 一般性教训:** a conformational-restraint contribution converges satisfactorily only when its PMF reaches a well-defined minimum at a **low RMSD value, typically below 3 Å**. If your CV's PMF has no minimum in range, the cure is not more sampling — it is a better-decomposed CV.

**一般性教训：** 构象限制项只有在 PMF 于**较低 RMSD（通常小于 3 Å）**处出现明确极小时才算收敛得好。如果你的 CV 对应的 PMF 在范围内根本没有极小，解药不是加采样，而是把 CV 拆得更合理。

Two further compromises are worth recording, both flagged by the authors themselves: DCAF16 has no stability-rescuing construct analogous to CRBN^midi, so its DDB1-binding helices are held by a permanent RMSD restraint present in **both** end states, which makes the contribution cancel; and the roughly 180-residue disordered linker between BD1 and BD2 is **omitted entirely**, so the conformational entropy of the truly separated BD1/BD2 pair is never sampled.

还有两处妥协值得记下，都是作者自己标出来的：DCAF16 没有类似 CRBN^midi 的稳定化构建体，所以它结合 DDB1 的螺旋区被一个**在两个端态都存在**的恒定 RMSD 限制拴住，贡献因此相消；而 BD1 与 BD2 之间约 180 个残基的无序 linker 被**整段略去**，真正分开的 BD1/BD2 的构象熵从未被采样。

---

## 7. Results: what the method buys you / 结果：这套方法换来了什么

![Figure 5 — Headline numbers. (A) On the six CRBN-based systems the geometric route tracks TR-FRET affinities far better than trajectory-averaged HADDOCK scoring or MM/GBSA, and it is the only method that ranks all four CK1α single-point mutants correctly. (B) For the DCAF16 systems the calculated effect of swapping a single interfacial residue matches the experimental degradation switch: BRD4 G386E loses degradation, BRD3 E344G regains it. MM/GBSA and docking detect neither.](/images/blog/us-ternary-geometric-route/fig5_results.png)

**CK1α–lenalidomide–CRBN.** Six systems: the bare binary protein–protein interaction plus five lenalidomide-induced ternary complexes (wild-type and four CK1α interface mutants). Correlation with TR-FRET affinities reaches **R² = 0.95**, against 0.78 for trajectory-averaged HADDOCK scoring and 0.62 for MM/GBSA. Only the geometric route ranks all four single-point mutants correctly. Binding of lenalidomide at the interface is worth about **−8.0 kcal/mol**, and the separation stage alone drives almost all of the ranking: ΔG_sep spans −8.9 to −19.4 kcal/mol across systems while everything else varies by only 1–2 kcal/mol.

**CK1α–来那度胺–CRBN。** 六个体系：裸的二元 PPI，加上五个来那度胺诱导的三元复合物（野生型和四个 CK1α 界面突变体）。与 TR-FRET 亲和力相关性 **R² = 0.95**，轨迹平均 HADDOCK 打分 0.78，MM/GBSA 0.62。只有几何路径把四个单点突变体全部排对。来那度胺结合在界面带来约 **−8.0 kcal/mol**，而排序几乎完全由分离阶段决定：各体系 ΔG_sep 从 −8.9 到 −19.4 kcal/mol，其余各项加起来只差 1–2 kcal/mol。

**BRD4–IBG1–DCAF16 selectivity.** IBG1 degrades BRD4 but not BRD3, and the switch is a **single residue**: G386 in BRD4 versus E344 in BRD3. The protocol reproduces it — G386E destabilises by +5.0 kcal/mol, E344G stabilises by −14.3 kcal/mol — while **both MM/GBSA and docking miss it entirely**. That is the paper's headline claim: reduced-sampling methods cannot see a single interfacial glycine. Interestingly, the calculations also indicate BD2 has a stronger intrinsic affinity for DCAF16 than BD1 (−8.7 vs −1.5 kcal/mol), consistent with the experimental observation that disruptive mutations block degradation only when placed in BD2.

**BRD4–IBG1–DCAF16 选择性。** IBG1 降解 BRD4 而不降解 BRD3，开关是**单个残基**：BRD4 的 G386 对 BRD3 的 E344。协议重现了这一点——G386E 去稳定 +5.0 kcal/mol，E344G 稳定 −14.3 kcal/mol——而 **MM/GBSA 和对接都完全看不到**。这是全文的核心卖点：低采样量的方法看不见一个界面甘氨酸。另外计算还显示 BD2 对 DCAF16 的内在亲和力强于 BD1（−8.7 对 −1.5 kcal/mol），这与"破坏性突变只有放在 BD2 才能阻断降解"的实验观察一致。

Three caveats stated plainly in the paper:

论文明确写出的三条警告：

| Caveat / 警告 | Detail / 细节 |
|---|---|
| Absolute values are offset / 绝对值有系统偏移 | Linear fit y = 3.2x + 15.8; only **rankings** are meaningful. Likely from incomplete holo→apo relaxation of the unbound proteins. / 只有**排序**有意义；偏移可能来自自由态蛋白 holo→apo 弛豫采样不足 |
| One result is suspicious / 有一个结果可疑 | BRD3(E344G) came out 7.7 kcal/mol **more** stable than BRD4 with no experimental support — probably because the BRD4 complex was used as the starting structure for both / BRD3(E344G) 比 BRD4 还稳 7.7 kcal/mol，无实验支持，很可能因为两者都用 BRD4 复合物当起始结构 |
| Stability ≠ degradation / 稳定性 ≠ 降解 | Interface stability is necessary but not sufficient; lysine accessibility for ubiquitination is not modelled at all / 界面稳定是必要非充分条件；泛素化所需的赖氨酸可及性完全未建模 |

**Cost / 代价.** One replicate of the full cycle is **~2 μs of simulation**, i.e. weeks on a single GPU at 120–300 ns/day. The windows are embarrassingly parallel, so with enough GPUs it is hours — but this is a late-stage filter, not a screening method. The authors point to Hamiltonian replica exchange inside the US windows as the obvious next accelerator, aimed at the slow separation CV.

**代价。** 完整循环跑一个重复约需 **2 μs 模拟**，按 120–300 ns/天算，单卡要几周。窗口之间完全并行，卡够多就是几小时——但这注定是筛选末端的精筛工具，不是筛选方法本身。作者指出的下一步加速是在 US 窗口里上 Hamiltonian replica exchange，专门针对收敛最慢的分离 CV。

---

## 8. Reading it next to the alchemical notes / 和前两篇笔记放在一起看

| | Alchemical (AQFEP / FEP) / 炼金术 | Geometric route + US / 几何路径 |
|---|---|---|
| Path / 路径 | Unphysical, λ-parametrised / 非物理，λ 参数化 | Physical separation along r / 沿 r 的物理分离 |
| Scales to / 适用规模 | Small molecules / 小分子 | Protein–protein interfaces / 蛋白-蛋白界面 |
| Main risk / 主要风险 | Pose dependence, λ-overlap / 姿势依赖、λ 重叠 | Path completeness, CV choice / 路径完备性、CV 选择 |
| Fix for that risk / 风险怎么治 | More windows, soft-core / 加窗口、软核 | **Restrain orthogonal DoFs, refund analytically** / **限制正交自由度，解析退还** |
| Throughput / 通量 | 1–2 h per ligand (AQFEP) / 1–2 小时每分子 | ~2 μs per replicate, parallelisable / 每重复约 2 μs，可并行 |

The shared intellectual core is the one from the double-decoupling notes: **a restraint is not a cheat as long as you pay its free energy back.** Alchemical AFEP uses one Boresch restraint to hold a ghost ligand in place and subtracts it analytically. The geometric route takes that single trick and scales it to five restrained orientational degrees of freedom plus the RMSD coordinates — turning an intractable sampling problem into a stack of one-dimensional PMFs, each individually convergence-testable.

共同的思想内核和双解耦那篇是同一个：**只要你把限制势的自由能如数还回去，限制就不是作弊。** 炼金术绝对 FEP 用一个 Boresch 限制把幽灵配体按住，再解析扣掉。几何路径把这一招扩展到五个受限取向自由度加上若干 RMSD 坐标——把一个不可解的采样问题，变成一摞一维 PMF，每条都能单独做收敛检验。

---

## One-line takeaway / 一句话总结

Path completeness is not bought by sampling more paths; it is bought by **restraining the system until only one path remains, then analytically refunding every restraint** — which is why a 2 μs umbrella-sampling cycle can resolve a single interfacial glycine that MM/GBSA and docking both miss.

路径完备性不是靠多采几条路径换来的，而是靠**把体系限制到只剩一条路径，再把每个限制解析地退还**——这正是为什么一个 2 μs 的伞形采样循环，能分辨出 MM/GBSA 和对接都看不见的那一个界面甘氨酸。

---

*Notes distilled from a study session, 2026-11-16. Figures drawn for these notes. Corrections welcome. / 笔记整理自一次学习讨论，2026-11-16，配图为自绘，欢迎指正。*
