---
title: 'Learning Notes: ML-Guided AQFEP — Machine-Learning-Guided Absolute Free Energy Perturbation for Virtual Screening'
date: 2026-07-06
permalink: /posts/2026/07/aqfep-ml-guided-virtual-screening/
tags:
  - Free Energy
  - Molecular Dynamics
  - Drug Discovery
  - Computational Chemistry
  - Machine Learning
  - Virtual Screening
  - AQFEP
  - FEP
---

> Study notes on **"Machine Learning Guided AQFEP: A Fast and Efficient Absolute Free Energy Perturbation Solution for Virtual Screening"** (Crivelli-Decker et al., *J. Chem. Theory Comput.* 2024, 20(16), 7188–7198, SandboxAQ + MIT/Toronto/Vector). Open-access full text on [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11360131/) · [JCTC](https://pubs.acs.org/doi/10.1021/acs.jctc.4c00399).
>
> 本文是对上述论文的双语学习笔记。每一节先给英文，再给中文，方便对照。

---

## 1. The problem this paper attacks / 这篇文章要解决的问题

**EN.** In drug discovery we want to know how tightly a small molecule binds a protein target (binding affinity). Two dominant tools each have a fatal flaw:

**中文.** 在药物发现中，我们想知道小分子和蛋白靶点结合得有多紧（结合亲和力）。目前两类主流工具各有致命短板：

| Method / 方法 | Speed / 速度 | Accuracy / 准确性 |
|---|---|---|
| Docking / 分子对接 | Very fast / 极快 | Poor — empirical scoring / 差，经验打分 |
| FEP / 自由能微扰 | Very slow / 极慢 | High — rigorous statistical mechanics / 高，严格统计力学 |

**EN.** FEP is the gold standard because it rests on real statistical mechanics, but **absolute FEP (AFEP) takes ~1 week per ligand on one GPU** — hopeless for virtual screening of thousands-to-millions of compounds. The paper's goal: **get FEP-quality rankings at near-screening speed.**

**中文.** FEP 是"金标准"，因为它有真正的统计力学基础，但**绝对 FEP（AFEP）每个分子要一块 GPU 算约一周** —— 面对成千上万乃至上百万候选分子完全不现实。文章目标：**在接近筛选的速度下，拿到 FEP 级别的排序。**

---

## 2. Two key ideas / 两个关键创新

**EN.** The system has a **physics engine (AQFEP)** that scores accurately, and an **ML brain (active learning)** that decides where to spend that expensive physics. They are mutually enabling: without a fast AQFEP you cannot produce enough training labels; without ML you would have to score the whole library.

**中文.** 整套系统由一个**物理引擎（AQFEP）**负责"算得准"，和一个**机器学习大脑（主动学习）**负责"算得省"、决定把昂贵的物理计算花在哪里。二者互为前提：没有快速的 AQFEP 就产不出足够训练标签；没有 ML 就得把整个库都算一遍。

---

## 3. AQFEP vs "standard" FEP / AQFEP 与"普通"FEP 的区别

**EN.** "Standard FEP" is ambiguous — there are two families, and AQFEP belongs to the *absolute* branch.

**中文.** "普通 FEP"其实有歧义——它有两支，而 AQFEP 属于**绝对**这一支。

| | **Relative FEP (RFEP)**<br>e.g. FEP+ | **Traditional Absolute FEP (AFEP)** | **AQFEP (this paper)** |
|---|---|---|---|
| Computes / 算什么 | ΔΔG between two similar ligands / 两相似配体之差 | absolute ΔG of one ligand / 单分子绝对值 | absolute ΔG of one ligand / 单分子绝对值 |
| Transformation / 变换 | morph A → B | double decoupling / 双解耦 | double decoupling / 双解耦 |
| Speed / 速度 | fast(ish) / 较快 | ~1 week/ligand / 约一周 | **1–2 h/ligand (T4 GPU)** |
| Best for / 适合 | lead optimization / 先导优化 | too slow to use / 太慢没法用 | **large-scale screening / 大规模筛选** |

### vs Relative FEP (FEP+) / 与相对 FEP 的本质区别

**EN.** RFEP only computes a *difference* between two structurally similar ligands and requires a perturbation map connecting them. A screening library is chemically diverse with no shared scaffold, so RFEP cannot connect the compounds. AQFEP gives each molecule an **absolute** score independently — no similarity, no map required.

**中文.** RFEP 只能算两个高度相似配体之间的**差值**，且需要构建把它们连起来的微扰网络。而筛选库分子五花八门、没有共同母核，RFEP 根本连不起来。AQFEP 对每个分子独立给出**绝对**分数——不需要相似性，也不需要网络。

### vs Traditional AFEP / 与传统绝对 FEP 的区别（提速的取舍）

**EN.** Same theory (double decoupling), but AQFEP trades rigor for speed by: (1) **much shorter simulation windows**; (2) **sampling only states close to the input docking pose** rather than exploring full conformational space; (3) **convergence filtering** (MBAR, 1 kcal/mol uncertainty cutoff) that discards unreliable calculations. Result: **1–2 h/ligand, ~10× faster than RFEP, 40–70× faster than AFEP.**

**中文.** 理论相同（双解耦），但 AQFEP 用严谨换速度：(1) **每个 λ 窗口模拟时间大幅缩短**；(2) **只采样贴近输入对接姿势的构象**，不去穷举整个构象空间；(3) 用 **MBAR 收敛过滤**（1 kcal/mol 不确定度阈值）丢弃不可靠计算。结果：**1–2 小时/分子，比 RFEP 快约 10 倍，比 AFEP 快 40–70 倍。**

> ⚠️ **Counter-intuitive point / 反直觉的一点:** running AQFEP *longer* actually hurts — the ligand drifts into conformations unlike the target pose and adds noise. So AQFEP is **extremely pose-dependent**: a bad pose → a bad score. / AQFEP **跑得越久反而越差**——分子会漂到与目标姿势不像的构象、只增加噪声。所以它**极度依赖姿势质量**：姿势错，结果就废。

---

## 4. Double decoupling explained / 双解耦详解

**EN.** We want the free energy of this process, but MD can never actually sample a ligand swimming from bulk water into the pocket (too slow, huge barriers):

**中文.** 我们想要下面这个过程的自由能，但 MD 根本采样不到"配体从水里游进口袋"（太慢、能垒太高）：

```
Ligand(water) + Protein  ──ΔG_bind──►  Ligand·Protein complex
配体(水)     + 蛋白                     配体·蛋白复合物
```

**EN.** Trick: free energy is a **state function** (path-independent), so we take an "alchemical" path the computer *can* evaluate. **Decoupling** means using a coupling parameter **λ** to gradually switch off the ligand's interactions (electrostatics + van der Waals): at λ=1 the ligand is real; at λ=0 it is a "ghost" that neither attracts nor repels its surroundings.

**中文.** 技巧：自由能是**状态函数**（与路径无关），所以我们走一条计算机能算的"炼金术"路径。**解耦**就是用耦合参数 **λ** 逐渐关掉配体与环境的相互作用（静电 + 范德华）：λ=1 时配体真实存在；λ=0 时它变成"幽灵"，对周围既不吸引也不排斥。

**EN. Why "double"?** A solvated ligand interacts with two environments — water and the pocket — so we decouple twice, forming a thermodynamic cycle:

**中文. 为什么是"双"？** 溶剂化配体的相互作用来自两个环境——水和口袋——所以要解耦两次，构成一个热力学循环：

```
            ΔG_bind  (want this; can't compute directly / 想要，但直接算不了)
   L(water) + P  ─────────────────►  L·P complex
      │                                   │
      │ ΔG_solv                           │ ΔG_site
      │ turn ligand into ghost            │ turn ligand into ghost
      │ in pure water / 水中解耦           │ in the pocket / 口袋中解耦
      ▼                                   ▼
   ghost(water) + P ───ΔG = 0───►  ghost·P
   幽灵(水)                          口袋里的幽灵
```

**EN.** The bottom edge is **ΔG = 0**: a ghost interacts with nothing, so it costs nothing to move it from water to pocket. Closing the cycle gives:

**中文.** 底边 **ΔG = 0**：幽灵对环境无作用，从水移到口袋不耗能。循环闭合即得：

$$\Delta G_{bind} = \Delta G_{solv} - \Delta G_{site}$$

**EN. Intuition:** binding strength = "how hard it is to make the ligand vanish *inside the pocket*" minus "how hard it is to make it vanish *in water*." Harder to remove from the pocket → the pocket grips tightly → strong binding.

**中文. 直观理解：** 结合强度 = "在**口袋里**把配体变没有多难" 减去 "在**水里**把它变没有多难"。口袋里更难拔 → 口袋抓得紧 → 结合强。

**EN. A necessary technical detail — restraints.** When the pocket-bound ligand becomes a ghost, nothing holds it and it drifts across the whole box, wrecking sampling. So we add an artificial **restraint** (Boresch-type distance/angle/dihedral springs) tethering the ghost near the pocket, then **analytically subtract** that restraint's free energy (it has a closed form):

**中文. 一个必须处理的技术细节——限制势。** 口袋里的配体变成幽灵后不再被束缚，会在整个盒子里乱飘，破坏采样。于是加一个人为的**限制势**（Boresch 型的距离/角度/二面角弹簧）把幽灵拴在口袋附近，再把这个限制势对应的自由能**解析地扣掉**（它有闭式解）：

$$\Delta G_{bind} = \Delta G_{solv} - \Delta G_{site} - \Delta G_{restraint}$$

**EN.** AQFEP uses exactly this framework, but keeps the ligand anchored near the given pose with short simulations — which is *why* it is fast and *why* it lives or dies by pose quality.

**中文.** AQFEP 用的正是这套框架，只是把配体牢牢锚定在给定姿势附近、用很短的模拟——这正是它**快**、也**极度依赖姿势**的原因。

---

## 5. What the ML actually does / 机器学习到底起什么作用

**EN.** Even at 1–2 h/ligand, a million-compound library is unaffordable. Core idea: **don't run AQFEP on everything — only on the compounds most likely to be good.** ML never touches the physics; its only job is to decide *which molecules AQFEP should evaluate next.* It plays two roles.

**中文.** 即便 1–2 小时一个分子，百万级库仍然算不起。核心思路：**别对所有分子都跑 AQFEP，只对最可能好的那一小批跑。** ML 完全不碰物理，它唯一的任务是决定**AQFEP 下一批该算谁**。它扮演两个角色。

**Role 1 — Surrogate model (a cheap stand-in for AQFEP) / 角色 1——代理模型（AQFEP 的廉价替身）**

**EN.** Train a model to predict the **AQFEP score** (not experimental activity!) in milliseconds, so it can rank the whole library instantly. Its training labels are AQFEP's own outputs — a fast model mimicking the slow physics engine.

**中文.** 训练一个模型去预测 **AQFEP 分数**（注意：不是实验活性！），毫秒级即可，能瞬间给全库排序。它的训练标签就是 AQFEP 自己的输出——用快模型模仿慢物理引擎。

**Role 2 — Active learning / Bayesian optimization (decide the next batch) / 角色 2——主动学习/贝叶斯优化（决定下一批）**

```
① Seed batch (random / docking) ──► run real AQFEP ──► (molecule, AQFEP score) labels
   种子批次(随机/对接)              跑真实 AQFEP        得到 (分子, 分数) 训练样本
        │
        ▼
② Train / update the surrogate model  训练/更新代理模型
        │
        ▼
③ Surrogate predicts the whole library instantly  代理模型瞬间给全库打分
        │
        ▼
④ Acquisition function picks the next most valuable batch  采集函数挑下一批最值得算的
        │
        ▼
⑤ Run real AQFEP on that batch ──► new labels ──► back to ②  跑真实 AQFEP → 新样本 → 回到②
```

**EN.** The **acquisition function** balances **exploitation** (highest predicted score — greedy) against **exploration** (uncertain molecules that might surprise — UCB / EI / PI). The paper compares greedy, UCB, EI, PI.

**中文.** **采集函数**在**利用**（预测分最高，greedy）和**探索**（模型不确定、可能藏惊喜，UCB/EI/PI）之间权衡。文章比较了 greedy、UCB、EI、PI。

---

## 6. The three surrogate models / 三种代理模型

**EN.** The three models differ mainly in **how the molecule is presented to the model**, from 2D to 3D.

**中文.** 三种模型的差异，本质上是**分子以什么方式呈现给模型**，从 2D 到 3D 递增。

**Model 1 — Random Forest + Morgan fingerprint (2D, simplest) / 随机森林 + Morgan 指纹（2D，最简单）**

**EN.** Morgan/ECFP fingerprint = a fixed 0/1 bit vector recording which local substructures (atom + neighborhood up to radius r) the molecule contains. A random forest of decision trees then votes. Fast, stable, works on small data — but the representation is **hand-fixed**, so it cannot learn new task-specific features, and it is purely 2D (no shape).

**中文.** Morgan/ECFP 指纹 = 一串固定长度的 0/1 向量，记录分子含有哪些局部子结构（原子及其半径 r 内的环境）。再用一堆决策树投票。快、稳、小数据可用——但表示是**人为写死的**，学不出新的任务专属特征，且纯 2D（不含三维形状）。

**Model 2 — D-MPNN (2D graph neural net, medium) / D-MPNN（2D 图神经网络，中等）**

**EN.** Treats the molecule as a **graph** (atoms = nodes, bonds = edges) and lets the model learn its own features via **directed message passing**: each bond passes messages to neighbors over several rounds ("directed" avoids info bouncing straight back), then a readout pools everything into a molecule vector fed to an MLP. Unlike fingerprints, the representation is **learned end-to-end** for the AQFEP-score task (this is the Chemprop architecture). Stronger than fingerprints, still 2D-only — it cannot see 3D shape.

**中文.** 把分子当成**图**（原子=节点，键=边），通过**有向消息传递**让模型自学特征：每条键分几轮把信息传给邻居（"有向"避免信息原路反弹），再汇总成整分子向量喂给 MLP。与指纹不同，它的表示是**端到端学出来的**、针对"预测 AQFEP 分数"这个任务（即 Chemprop 架构）。比指纹强，但仍是纯 2D，看不到三维形状。

**Model 3 — GraphDock (3D E(n)-equivariant GNN, most complex) / GraphDock（3D 等变图神经网络，最复杂）**

**EN.** A qualitative leap: it takes the **3D protein–ligand complex** (atomic coordinates included), not just the ligand. "**E(n)-equivariant**" guarantees the physically correct symmetry — translating/rotating the complex must not change the predicted energy; the network operates on relative distances/directions so the scalar output stays invariant under rotation. It genuinely "sees" 3D complementarity (which group fits the pocket, where there is steric clash). Best-performing in the paper — but heaviest, most data-hungry, and it **needs an input 3D pose**, so it inherits pose sensitivity.

**中文.** 质的飞跃：输入是**蛋白-配体三维复合物**（含原子坐标），而非仅配体。"**E(n)-等变**"保证了物理上正确的对称性——平移/旋转复合物不应改变预测能量；网络作用于相对距离/方向，故标量输出对旋转保持不变。它能真正"看见"三维互补性（哪个基团卡进口袋、哪里有位阻）。文中表现最好——但最重、最吃数据，且**需要输入三维姿势**，因而继承了姿势敏感性。

| | Sees / 看到 | Learned repr.? / 表示可学? | Cost/data / 成本·数据 | Fit to AQFEP physics / 与AQFEP物理契合 |
|---|---|---|---|---|
| RF + Morgan | 2D fragment list / 2D片段清单 | No / 否 | Low / 低 | Low / 低 |
| D-MPNN | 2D graph / 2D图 | Yes / 是 | Medium / 中 | Medium / 中 |
| GraphDock | 3D complex / 3D复合物 | Yes (+geometry) / 是(含几何) | High / 高 | **High / 高** |

**EN. Key insight:** GraphDock wins because it shares AQFEP's worldview — **both are pose-centric.** An AQFEP score is computed around a specific pose, so a 3D model that can *see* that pose is best positioned to imitate it.

**中文. 关键洞察：** GraphDock 之所以最好，是因为它和 AQFEP 共享同一个"世界观"——**都以姿势为中心**。AQFEP 分数本就是围绕某个姿势算出来的，那么一个**能看见姿势的 3D 模型**自然最能模仿它。

---

## 7. GraphDock is a *trained model*, not a deterministic embedding tool / GraphDock 是"一整套训练出来的模型"，不是确定性的 embedding 工具

**EN.** Yes, GraphDock internally produces an **embedding** (the GNN backbone compresses the complex into a vector). But two clarifications:

**中文.** 是的，GraphDock 内部确实产生一个 **embedding**（GNN 主干把复合物压缩成向量）。但要澄清两点：

1. **EN.** It embeds the **protein–ligand complex**, not an isolated small molecule — change the pose or the pocket and the embedding changes. **中文.** 它 embed 的是**蛋白-配体复合物**，而非孤立小分子——换姿势或换口袋，embedding 就变。
2. **EN.** The embedding is a **means, not the goal**: GraphDock is an end-to-end **supervised regressor** trained specifically to predict the AQFEP score; the embedding is just an intermediate product shaped by that task. **中文.** embedding 是**手段而非目的**：GraphDock 是端到端的**监督回归模型**，专门训练来预测 AQFEP 分数；embedding 只是被这个任务"塑形"出来的中间产物。

**EN.** So it is a **trained model**, not a deterministic mapping like a Morgan fingerprint:

**中文.** 所以它是**训练出来的模型**，而不是像 Morgan 指纹那样的确定性映射：

| | Deterministic tool (Morgan) / 确定性工具 | Trained model (GraphDock) / 训练出来的模型 |
|---|---|---|
| How the vector arises / 向量怎么来 | fixed algorithm / 固定算法 | learned weights / 学出来的权重 |
| Needs training? / 需要训练? | No / 否 | Yes, fit on AQFEP data / 是，靠AQFEP数据 |
| Task-dependent? / 依赖任务? | No / 否 | Yes — biased toward AQFEP-correlated features / 是，偏向与AQFEP相关的特征 |

**EN.** Because it is trained, its representation is **biased toward whatever correlates with the AQFEP score** — Morgan is objective (task-agnostic); GraphDock is goal-directed. You *could* extract its middle-layer vector for transfer learning, but it was never trained as a general-purpose encoder, so results are not guaranteed.

**中文.** 正因为它是训练出来的，它的表示**偏向那些与 AQFEP 分数相关的特征**——Morgan 是客观的（与任务无关），GraphDock 是目标导向的。原则上你可以抽它的中间层向量做迁移学习，但它从未被训练成通用编码器，效果不一定好。

---

## 8. No pretrained model — you train iteratively per system / 没有预训练模型——需针对自己的体系迭代训练

**EN.** A crucial practical point: the ML part is a **method/workflow, not a downloadable set of weights.** There is **no** off-the-shelf pretrained model. Because the ML target is "AQFEP's score for *this specific protein*," and that target changes per target, you must **train from scratch for each system.** GraphDock literally takes *this* pocket as input.

**中文.** 一个关键的实践要点：ML 部分是一套**方法/流程，而非可下载的成品权重**。**没有**开箱即用的预训练模型。因为 ML 的目标是"AQFEP 对**这个特定蛋白**的打分"，而这个目标随靶点而变，所以必须**对每个体系从零训练**。GraphDock 直接把**这个**口袋当输入。

**EN.** The training data is **self-produced**: AQFEP generates the labels on the fly (step ① above). Every active-learning round **retrains/updates** the surrogate as more AQFEP data accumulates — the model actively chooses which data to acquire next, then trains itself better on it. What you need to run this yourself:

**中文.** 训练数据是**自产自销**的：AQFEP 现场产生标签（上面步骤①）。每一轮主动学习都会随着 AQFEP 数据积累而**重新训练/更新**代理模型——模型主动决定下一批要什么数据，再用这些数据把自己训得更准。要自己跑这套，你需要：

- **EN.** an AQFEP-capable physics engine to produce labels (this part is **SandboxAQ-proprietary; the paper does not release it**); / **中文.** 一个能跑 AQFEP 的物理引擎来产标签（这部分是 **SandboxAQ 专有的，论文没公开**）；
- **EN.** for **your** target, run a seed batch, then run the active-learning loop, retraining as you go; / **中文.** 对**你自己的**靶点跑种子批次，再跑主动学习循环，边筛边重训；
- **EN.** switch target → start the whole thing over. / **中文.** 换靶点 → 整套重来。

> **Why speed and ML are mutually enabling / 为什么提速和 ML 互为前提:** if AQFEP were as slow as classic AFEP (a week per ligand) you could not even produce the seed batch, and active learning could never start. Fast AQFEP → affordable labels; ML → no need to score the whole library. / 如果 AQFEP 慢如传统 AFEP（一周一个），你连种子批次都跑不出来，主动学习根本启动不了。快 AQFEP → 产得起标签；ML → 不必全库暴算。

---

## 9. Key results & limitations / 主要结果与局限

**Results / 结果**

- **EN. cMet (270k library):** found all 5 known actives in the top 50; Kendall-τ ≈ 0.48 (vs FEP+ ≈ 0.60), far above docking/MMGBSA. / **中文. cMet（27万库）:** 前50名找全5个已知活性；Kendall-τ≈0.48（FEP+≈0.60），远超对接/MMGBSA。
- **EN. GLP1R retrospective (12,720):** GraphDock+UCB recovered **322 ± 7 of the top-500** AQFEP compounds while screening only ~12% of the library; random search and docking found **zero** known actives. / **中文. GLP1R 回顾性（12,720）:** GraphDock+UCB 只筛约12%的库就找回 AQFEP 前500名中的 **322±7 个**；随机搜索和对接找到**零**个已知活性。
- **EN. Prospective screen (1.17M library):** 30,108 AQFEP simulations (claimed largest reported free-energy screen); experimental **hit rate ≈ 2.88%** (41 actives ≤50 µM out of 1,424 tested), far above docking-based selection. / **中文. 前瞻性筛选（117万库）:** 30,108 次 AQFEP 模拟（号称当时最大规模）；实验**命中率≈2.88%**（1,424测试分子中41个≤50µM活性），远高于基于对接的选择。

**Limitations / 局限**

- **EN. Pose dependence is the Achilles' heel** — one GLP1R active with a wrong predicted pose fell to rank ~1100–1700 of 12,720. / **中文. 姿势依赖是致命弱点**——GLP1R 一个姿势预测错的活性分子掉到 12,720 里的 ~1100–1700 名。
- **EN.** MBAR uncertainty estimates **underestimate** true error; fuller λ-overlap analysis would help. / **中文.** MBAR 不确定度**低估**真实误差；更完整的 λ-overlap 分析会更好。
- **EN.** The **AQFEP engine is proprietary** — only the ML/Bayesian-optimization parts are fully disclosed and reproducible. / **中文.** **AQFEP 引擎是专有的**——只有 ML/贝叶斯优化部分完整公开、可复现。
- **EN.** Still needs substantial GPU resources for ultra-large libraries. / **中文.** 对超大库仍需可观的 GPU 资源。

---

## One-line takeaway / 一句话总结

**EN.** The contribution is not a new free-energy theory but an **engineering + ML system**: a speed-tuned *absolute* FEP (AQFEP), steered by active-learning surrogates, brings physics-based binding prediction to million-compound screening — with the whole thing hinging on pose quality, and requiring per-target, from-scratch iterative training rather than any pretrained model.

**中文.** 本文的贡献不是新的自由能理论，而是一套**工程 + 机器学习系统**：用速度调优过的**绝对** FEP（AQFEP），配上主动学习代理模型的引导，把基于物理的结合预测带到百万级筛选——而这一切都系于姿势质量，并且需要针对每个靶点从零迭代训练，而非任何预训练模型。

---

*Notes distilled from a study conversation, 2026-07-06. Corrections welcome. / 笔记整理自一次学习对话，2026-07-06，欢迎指正。*
