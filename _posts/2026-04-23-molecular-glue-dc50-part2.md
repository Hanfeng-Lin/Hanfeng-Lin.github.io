---
title: 'Understanding Molecular Glue Dose-Response Curves — Part 2: Why Pre-organization Moves Both $\mathrm{DC50}$ and $D_{\mathrm{max}}$'
date: 2026-04-23
permalink: /posts/2026/04/molecular-glue-dc50-part2/
tags:
  - Molecular Glue
  - Targeted Protein Degradation
  - VAV1
  - Pre-organization
  - Drug Discovery
---

*This is Part 2 of a three-part series. [Part 3](/posts/2026/04/molecular-glue-dc50-part3/) covers the cellular kinetic filter, diagnostics, and design implications.*

**Notation:** **L** = molecular glue; **E** = CRBN (E3 ligase); **P** = neosubstrate. Binary complex: $L{\cdot}E$. Ternary complex: $P{\cdot}L{\cdot}E$.

**Recap from [Part 1](/posts/2026/04/molecular-glue-dc50-part1/).** $\mathrm{DC50}$ always means the half-maximal concentration (midpoint of the Hill curve), not the concentration achieving 50% absolute degradation — those two definitions diverge whenever $D_{\mathrm{max}}$ < 100%, and conflating them corrupts potency rankings across a series. Thermodynamically, $\mathrm{DC50}$ is set by a single expression: $\mathrm{DC50}$ ≈ $K_{d,\mathrm{CRBN}}$ · $K_{d,\mathrm{ternary}}$ / ($K_{d,\mathrm{ternary}}$ + $[P]$), with the achievable plateau fixed at $f_{\mathrm{PLE}}$ = $\beta/(1+\beta)$ where $\beta$ = $[P]$/$K_{d,\mathrm{ternary}}$. Reading curve shifts: a $D_{\mathrm{max}}$ drop at unchanged $\mathrm{DC50}$ points to a downstream problem (geometry, resistant subpopulation, UPS saturation); a $\mathrm{DC50}$ rightward shift at unchanged $D_{\mathrm{max}}$ points to a binding or exposure problem (weaker $K_d$, efflux, metabolic instability).

## Opening puzzle: Compound 11 vs Compound 17

Here is the observation that motivates everything in this post. Two VAV1 molecular glues from the NGT-201 series — data and figures throughout this case study are from our [bioRxiv preprint (Wang et al., 2025)](https://www.biorxiv.org/content/10.1101/2025.06.08.658535v2) — differing by a single atom at one position on the phenyl-glutarimide scaffold:

- **Compound 11** (X = H): CRBN NanoBRET IC50 = 100 nM. VAV1 $\mathrm{DC50}$: unfittable (curve barely rises). $D_{\mathrm{max}}$ at 1 μM = **15%**.
- **Compound 17** (X = Cl): CRBN NanoBRET IC50 = 297 nM. $\log\mathrm{DC50}$ = −7.80 (≈ 16 nM). $D_{\mathrm{max}}$ at 1 μM = **90%**.

The chloride doesn't help CRBN binary engagement — if anything, compound 17 binds CRBN ~3× weaker than the parent. Yet $D_{\mathrm{max}}$ jumps from 15% to 90%, and the $\mathrm{DC50}$ improves by something like 30× (compound 11 barely shows any degradation at all). The textbook story says pre-organization tightens $K_{d,\mathrm{ternary}}$ and shifts $\mathrm{DC50}$ without moving $D_{\mathrm{max}}$ — the opposite of what happened here.

The companion analogs in the series sharpen the puzzle further. Fluorine (**compound 15**) and hydrogen (**compound 11**) have indistinguishable CRBN NanoBRET binary engagement (both 100 nM); fluorine delivers $D_{\mathrm{max}}$ = 67% with a fittable $\mathrm{DC50}$. Methyl (**compound 13**) breaks CRBN binary down to 883 nM — and that compound is the only one whose $\mathrm{DC50}$ takes a visible hit. So across the halogen series, **$\mathrm{DC50}$ tracks primarily with $K_{d,\mathrm{CRBN}}$, while $D_{\mathrm{max}}$ is scattered across 15%–90% driven by something else**.

![Figure — NGT-201 halogen series on VAV1: dose-response curves (A) and chemical structures with $\log\mathrm{DC50}$ (red bar, more negative = more potent) and $D_{\mathrm{max}}$ at 1 μM (green bar, higher = more efficacious) for the phenyl series (top, compound 11/13/15/17) and indole series (bottom, compounds 12/14/16/18). Chloride substitution delivers the largest gain on both axes, but the pattern across 11/15/17 is "matched CRBN binary, similar $\mathrm{DC50}$, dramatically different $D_{\mathrm{max}}$." Data from Figure 4A,B of [Lin et al., 2025](https://www.biorxiv.org/content/10.1101/2025.06.08.658535v2).](/images/blog/molecular-glue-dc50/vav1_fig4ab_halogen_sar.png)

| Compound | Substituent X | CRBN NanoBRET IC50 | $\log\mathrm{DC50}$ (VAV1) | $D_{\mathrm{max}}$ at 1 μM |
|---|---|---|---|---|
| compound 11 | H | 100 nM | — (unfittable) | 15% |
| compound 13 | Me | **883 nM** | −6.53 | 54% |
| compound 15 | F | 100 nM | −7.56 | 67% |
| compound 17 | Cl | 297 nM | **−7.80** | **90%** |

What is the chloride doing that produces this specific signature — $D_{\mathrm{max}}$ far more sensitive than $\mathrm{DC50}$ to the substitution? And what is the methyl doing differently that breaks the pattern?

## Why chloride: DFT evidence for pre-organization

Before getting to the thermodynamic explanation, it's worth seeing what the Cl is actually doing at the atomic level. Density functional theory calculations on the free molecules show the answer directly. The phenyl-glutarimide scaffold has a single rotatable bond connecting the glutarimide-bearing phenyl ring to the distal aryl ring that contacts VAV1. Scanning the dihedral around that bond gives a 1D potential energy profile — a map of which conformations are accessible in free solution.

![Figure — DFT dihedral scans for compound 11 (H, red) and compound 17 (Cl, blue). Panel F: 1D potential energy profile along the rotatable bond between the two aryl rings — compound 17 shows substantially deeper energy wells and higher rotational barriers, meaning it spends more of its time in a smaller set of conformations. Panels G, H: 2D potential energy surfaces (both rotatable bonds scanned simultaneously) — the compound 11 landscape is broad and shallow, with many near-degenerate conformations; compound 17 collapses into narrow wells. This is pre-organization visualized. Figure 4E–H of [Lin et al., 2025](https://www.biorxiv.org/content/10.1101/2025.06.08.658535v2).](/images/blog/molecular-glue-dc50/vav1_fig4efgh_dft.png)

The 1D dihedral scan (Panel F) tells the story compactly: compound 11 has a shallow profile — most dihedral angles are energetically accessible, so the free molecule samples a wide distribution of conformations. Compound 17 has substantially deeper wells and higher barriers — the chlorine sterically impedes rotation, trapping the molecule in a narrow conformational ensemble. The 2D scans (Panels G, H) confirm this over both rotatable bonds simultaneously: the compound 11 potential energy surface is a broad basin; the compound 17 surface is a set of sharp wells. Molecular dynamics simulations of each compound bound to CRBN show the same pattern — compound 17 samples a narrower dihedral distribution.

This is pre-organization made concrete. The chlorine doesn't participate in any specific contact with CRBN or VAV1; it simply restricts the free-solution ensemble to conformations more likely to be productive for ternary assembly. So why does that restriction translate specifically into $D_{\mathrm{max}}$ gain with barely any $\mathrm{DC50}$ gain? The rest of this post builds the framework to answer that.

## What can still move $D_{\mathrm{max}}$ when the geometry is matched

Take two compounds in the same cellular system with a matched ternary complex model — same productive geometry, same lysines presented to the E2. The geometric explanations for $D_{\mathrm{max}}$ differences (broken ubiquitination orientation, degradation-resistant target subpopulation, etc.) fall away. What is left?

**The first possibility is that the plateau $\beta/(1+\beta)$ genuinely differs** between the two compounds, even when their DC50s look similar. Recall from Part 1 that

$$\mathrm{DC50} \approx \frac{K_{d,\mathrm{CRBN}} \cdot K_{d,\mathrm{ternary}}}{K_{d,\mathrm{ternary}} + [P]}$$

— it depends on the product of the two $K_d$ values. That means two compounds can hit the same $\mathrm{DC50}$ through opposite changes: one can have a weaker $K_{d,\mathrm{ternary}}$ paired with a correspondingly tighter $K_{d,\mathrm{CRBN}}$, and the other can have the reverse. The DC50s match, but the plateau $\beta/(1+\beta)$ depends only on $K_{d,\mathrm{ternary}}$ versus $[P]$, so the compound with weaker $K_{d,\mathrm{ternary}}$ will reach a lower $f_{\mathrm{PLE}}$ ceiling.

**A second possibility is that intracellular exposure caps out** before the dose-response reaches saturation. Every cellular assay has a highest testable dose, set by solubility, DMSO tolerance, or off-target toxicity. If that ceiling falls below where $f_{\mathrm{PLE}}$ would plateau, the "$D_{\mathrm{max}}$" you read off the curve isn't the true plateau at all — it's the point where you ran out of compound.

**A third possibility is residence time** — the compound's $k_{\mathrm{off}}$ on the ternary complex. Two compounds can have matched equilibrium $K_{d,\mathrm{ternary}}$ but very different $k_{\mathrm{off}}$ values (with $k_{\mathrm{on}}$ adjusting in compensation). Residence time controls how long each ternary encounter survives, which in turn controls whether ubiquitin transfer has time to fire.

<details markdown="1">
<summary>Why residence time is a separate lever from K_d (math detour)</summary>

At equilibrium, $K_d = k_{\mathrm{off}}/k_{\mathrm{on}}$. You cannot vary $k_{\mathrm{off}}$ independently while holding $K_d$ fixed — $k_{\mathrm{on}}$ has to move in compensation. "Same $K_{d,\mathrm{ternary}}$, different residence time" specifically means $k_{\mathrm{off}}$ and $k_{\mathrm{on}}$ scale together.

Residence time depends only on $k_{\mathrm{off}}$:

$$\tau = 1 / k_{\mathrm{off}}$$

There is no dependence on $K_d$ or $k_{\mathrm{on}}$. Two compounds with matched $K_{d,\mathrm{ternary}}$ but different $k_{\mathrm{off}}$ values have different residence times, full stop.

Ubiquitin transfer is a catalytic event with its own timescale. What determines productive degradation is whether the ternary complex survives long enough for Ub transfer to occur:

$$P(\text{productive transfer per binding event}) = \frac{k_{\mathrm{cat}}}{k_{\mathrm{cat}} + k_{\mathrm{off}}}$$

When $k_{\mathrm{off}}$ is much slower than $k_{\mathrm{cat}}$, nearly every binding event produces a Ub transfer, and further slowing $k_{\mathrm{off}}$ returns almost nothing. When $k_{\mathrm{off}}$ is much faster than $k_{\mathrm{cat}}$, most events dissociate before transfer happens and slowing $k_{\mathrm{off}}$ directly improves the yield per encounter. The degradation flux is $k_{\mathrm{on}} \cdot [L{\cdot}E] \cdot [P] \cdot P(\text{transfer})$. At fixed $K_{d,\mathrm{ternary}}$, the product $k_{\mathrm{on}} \cdot P(\text{transfer})$ increases as $k_{\mathrm{off}}$ slows, so matched $K_d$ with slower $k_{\mathrm{off}}$ gives higher degradation flux — provided you are not already in the saturating regime.

**Summary:** $K_{d,\mathrm{ternary}}$ sets the equilibrium occupancy of the ternary complex at any given $[L]$, while $k_{\mathrm{off}}$ sets the catalytic efficiency per occupied complex through $P(\text{transfer})$. Same $K_d$ with slower $k_{\mathrm{off}}$ wins on $D_{\mathrm{max}}$. Same $k_{\mathrm{off}}$ with tighter $K_d$ wins on $\mathrm{DC50}$.

</details>

Beyond these three core possibilities, several artefacts can masquerade as $D_{\mathrm{max}}$ differences.

**CRBN auto-degradation**: some glues destabilize CRBN itself, shrinking the ligase pool available to form ternary complex and lowering the observed ceiling (well documented for IMiD-class compounds).

**Off-target sequestration**: the compound binds to unrelated proteins, or compound-induced depletion of other pathway components (E2s, ubiquitin pool, proteasome capacity) caps $D_{\mathrm{max}}$ from the side rather than through the direct binding model.

**Solubility/aggregation**: compound precipitation at the top of the dose-response breaks the assumption that nominal and free concentrations match.

**Cytotoxicity**: at truly high doses, cell-death or stress responses confound the readout entirely.

For compound 11 vs compound 17, most of these are quickly ruled out: same scaffold, same cellular system, exposure and solubility don't differ meaningfully, and there's no evidence of selective CRBN auto-degradation between them. That leaves the first possibility — the plateau $\beta/(1+\beta)$ itself differs — as the working hypothesis. To see why, we need to know where pre-organization lives thermodynamically.

## Pre-organization and where it lives

Pre-organization means the compound's free-solution conformational ensemble is already enriched in the productive pose — exactly what the DFT scans showed for compound 17 above. To see why this translates into thermodynamics, decompose the free energy of ternary formation into two pieces:

$$\Delta G_{\mathrm{ternary}} \;=\; \underbrace{\Delta G_{\mathrm{conf}}}_{\text{free} \,\to\, \text{bound pose}} \;+\; \underbrace{\Delta G_{\mathrm{bind}}}_{\text{bound-pose ligand} \,\to\, \text{ternary complex}}$$

A pre-organized compound pays a small $\Delta G_{\mathrm{conf}}$ because it spends most of its time near the productive geometry. An unconstrained analog pays more. If the ternary complex pose is genuinely identical between them — same CRBN contacts, same neosubstrate interface — then $\Delta G_{\mathrm{bind}}$ is matched, and the entire thermodynamic difference lives in $\Delta G_{\mathrm{conf}}$.

Binary TE in the NanoBRET assay measures L + E ⇌ $L{\cdot}E$ and averages over whatever binary poses CRBN accepts. It does not require the productive ternary-competent pose. So matched binary $K_d$ can coexist with very different propensities to access the ternary pose in solution. The chlorine in compound 17 pays off specifically at the ternary assembly step — smaller $\Delta G_{\mathrm{conf}}$ on the path to the productive state — and should show up as tighter $K_{d,\mathrm{ternary}}$ with barely any change (or even slight loss) in $K_{d,\mathrm{CRBN}}$. Same binary affinity, different cooperativity $\alpha$ = $K_{d,\mathrm{CRBN}}(\mathrm{alone})$ / $K_{d,\mathrm{CRBN}}(\mathrm{in\ ternary})$.

In the clean idealization, the consequence looks simple: $K_{d,\mathrm{ternary}}$ differs, and $\mathrm{DC50}$ shifts proportionally via the $K_{d,\mathrm{ternary}}$ term in the $\mathrm{DC50}$ formula. $D_{\mathrm{max}}$ is *supposedly* unaffected in the saturating regime — at saturating compound, both compounds drive $f_{\mathrm{PLE}}$ toward $\beta/(1+\beta)$, and if $[P]$ ≫ $K_{d,\mathrm{ternary}}$ for both, both plateau near 1 and $D_{\mathrm{max}}$ matches.

That last claim — $D_{\mathrm{max}}$ unaffected — is where the textbook prediction breaks. The opening puzzle (big $D_{\mathrm{max}}$ swing, modest $\mathrm{DC50}$ swing) is the exact inversion of it. Which brings us to the single most important section of this post.

## $[P]$ saturation: the single most important thing to understand about $D_{\mathrm{max}}$

Imagine the compound is at saturation — essentially all CRBN is in the $L{\cdot}E$ binary complex. What fraction of that pool ends up in ternary complex?

$$L{\cdot}E + P \rightleftharpoons P{\cdot}L{\cdot}E \qquad K_{d,\,\mathrm{ternary}}$$

$$f_{\mathrm{PLE}} = \frac{[P]}{K_{d,\,\mathrm{ternary}}+[P]} = \frac{\beta}{1+\beta} \qquad \beta = \frac{[P]}{K_{d,\,\mathrm{ternary}}}$$

This is a Langmuir isotherm in $[P]$ with $K_{d,\mathrm{ternary}}$ as the midpoint. It is the plateau of the Hill curve in $[L]$ — what you reach at saturating compound — and it depends entirely on $\beta$ = $[P]$/$K_{d,\mathrm{ternary}}$. The numbers are unforgiving:

| $\beta$ = $[P]$/$K_{d,\mathrm{ternary}}$ | $f_{\mathrm{PLE}}$ plateau | Ceiling on $D_{\mathrm{max}}$ from occupancy alone |
|---|---|---|
| 10 (saturating) | 0.91 | 91% |
| 3.3 | 0.77 | 77% |
| 1 (at $K_d$) | 0.50 | 50% |
| 0.33 | 0.25 | 25% |
| 0.1 (sub-saturating) | 0.09 | 9% |

These are ceilings from ternary occupancy alone. Actual cellular $D_{\mathrm{max}}$ will be lower still, because resynthesis, incomplete ubiquitination, and inaccessible target pools all multiply down from this starting number.

![Figure 4 — Langmuir isotherm: $f_{\mathrm{PLE}}$ = $\beta/(1+\beta)$. With $[P]$ held constant, a compound whose $K_{d,\mathrm{ternary}}$ sits far above $[P]$ ($\beta \ll 1$) is structurally capped at low $D_{\mathrm{max}}$; a compound with $K_{d,\mathrm{ternary}}$ comparable to or below $[P]$ plateaus high. A modest $K_{d,\mathrm{ternary}}$ improvement in this regime translates into a large $D_{\mathrm{max}}$ gain without a proportional $\mathrm{DC50}$ shift.](/images/blog/molecular-glue-dc50/fig4_langmuir_isotherm.png)

Apply this to compound 11 vs compound 17. We don't have direct ternary TR-FRET $K_d$ values, but the observed cellular numbers are consistent with compound 11 sitting deep in the sub-saturating regime and compound 17 sitting close to or above saturation. Take a concrete illustration: cellular VAV1 $[P]$ ≈ 50 nM, compound 11 $K_{d,\mathrm{ternary}}$ ≈ 300 nM ($\beta$ ≈ 0.17, $f_{\mathrm{PLE}}$ plateau ≈ 14%), compound 17 $K_{d,\mathrm{ternary}}$ ≈ 5–10 nM ($\beta$ ≈ 5–10, $f_{\mathrm{PLE}}$ plateau = 83–91%). Those numbers reproduce the observed $D_{\mathrm{max}}$ almost exactly, and they require nothing beyond the Langmuir shape — no $k_{\mathrm{cat}}$ differences, no residence time, no downstream magic.

What makes this regime so diagnostically distinctive is that DC50s can still look broadly similar across compounds, even when their $K_{d,\mathrm{ternary}}$ values differ by an order of magnitude. The reason is in the $\mathrm{DC50}$ formula:

$$\mathrm{DC50} \approx \frac{K_{d,\,\mathrm{CRBN}}\cdot K_{d,\,\mathrm{ternary}}}{K_{d,\,\mathrm{ternary}} + [P]}$$

When $K_{d,\mathrm{ternary}}$ ≫ $[P]$ (sub-saturating), the ratio $K_{d,\mathrm{ternary}}$/($K_{d,\mathrm{ternary}}$ + $[P]$) approaches 1, so $\mathrm{DC50}$ ≈ $K_{d,\mathrm{CRBN}}$ — **completely insensitive to $K_{d,\mathrm{ternary}}$**.

When $K_{d,\mathrm{ternary}}$ drops to the $[P]$ range, the ratio falls to ~0.5 and $\mathrm{DC50}$ ≈ $K_{d,\mathrm{CRBN}}$/2. When $K_{d,\mathrm{ternary}}$ ≪ $[P]$, the ratio is $K_{d,\mathrm{ternary}}$/$[P]$, and $\mathrm{DC50}$ = $K_{d,\mathrm{CRBN}}$ · $K_{d,\mathrm{ternary}}$/$[P]$ starts dropping with $K_{d,\mathrm{ternary}}$.

So between "very weak $K_{d,\mathrm{ternary}}$" and "moderate $K_{d,\mathrm{ternary}}$," $\mathrm{DC50}$ barely moves; only when $K_{d,\mathrm{ternary}}$ becomes comparable to or tighter than $[P]$ does $\mathrm{DC50}$ start to pick up substantial gains. The $D_{\mathrm{max}}$ plateau, meanwhile, moves monotonically from 0% toward 100% the entire time. **This is why the halogen series shows "similar $\mathrm{DC50}$, different $D_{\mathrm{max}}$" across 11, 15, 17**: all three are navigating the sub-to-near-saturating $K_{d,\mathrm{ternary}}$ regime, where $K_{d,\mathrm{ternary}}$ changes $D_{\mathrm{max}}$ strongly and $\mathrm{DC50}$ weakly.

This also resolves the question left open at the end of Part 1: yes, a binding change can drop $D_{\mathrm{max}}$ without moving $\mathrm{DC50}$ much. It happens whenever $K_{d,\mathrm{ternary}}$ is weak enough that $[P]$ is sub-saturating. A $D_{\mathrm{max}}$ drop with $\mathrm{DC50}$ nearly unchanged is *not* a reliable fingerprint of a downstream problem; it can equally be a thermodynamic one.

### Why the saturating regime assumption silently fails

People assume $[P]$ is high because a target looks abundant on a Western or shows up confidently in proteomics. That is the wrong comparison. The relevant question is whether $[P]$ ≫ $K_{d,\mathrm{ternary}}$ for this specific compound, and in practice the answer is often no.

Cellular concentrations of CRBN neosubstrates are typically 10–300 nM. Transcription factors, translation factors, splicing factors — the classic neosubstrate classes — all live in this window. Back-calculating, 10,000 copies per HEK293 cell in a ~2 pL volume gives roughly 8 nM. $K_{d,\mathrm{ternary}}$ for non-optimized glues commonly falls in the 50 nM–1 µM range, putting $\beta$ in the range 0.1–2 for early-series compounds — precisely where $D_{\mathrm{max}}$ is structurally capped. On top of this, protein-protein complexes, DNA and RNA binding, and subcellular compartmentalization all reduce free $[P]$ below total $[P]$, and endogenous CRBN interactors compete by effectively reducing the available CRBN pool.

This reframes how pre-organization delivers its effect. The same thermodynamic parameter — $K_{d,\mathrm{ternary}}$ — governs both $\mathrm{DC50}$ and $D_{\mathrm{max}}$ when $[P]$ is finite. Pre-organization tightens $K_{d,\mathrm{ternary}}$, sliding the compound along $\beta$, and the ratio of how much that helps $D_{\mathrm{max}}$ versus $\mathrm{DC50}$ depends on where $\beta$ sits. Deep in the sub-saturating regime ($\beta \ll 1$), $D_{\mathrm{max}}$ rises steeply while $\mathrm{DC50}$ barely moves. Once $\beta$ crosses into the near-saturating regime, $\mathrm{DC50}$ starts to improve too. You do not need two separate mechanisms for the two axes.

## The methyl counterexample: Compound 13

Everything above is the signature of a $K_{d,\mathrm{ternary}}$ change — and that signature fits compound 11, compound 15, and compound 17 cleanly. **Compound 13 breaks the pattern**, and in a way that confirms the framework rather than undermining it.

Methyl at the same position should, in principle, do what fluorine and chlorine do — sterically impede rotation, pre-organize the molecule. But the methyl group is large enough to clash with CRBN's binding pocket. Binary NanoBRET IC50 degrades from 100 nM to 883 nM — $K_{d,\mathrm{CRBN}}$ got roughly 10× worse. On the $\mathrm{DC50}$ formula, the $K_{d,\mathrm{CRBN}}$ term lives outside the $K_{d,\mathrm{ternary}}$-sensitive ratio, so it translates directly into $\mathrm{DC50}$: compound 13's $\log\mathrm{DC50}$ is −6.53 (≈ 300 nM), about 20× worse than compound 15 and compound 17. This is the right-shift case from Part 1, where the binding side broke.

But crucially, compound 13 still has its Cl-like rigidification helping $K_{d,\mathrm{ternary}}$, so its $D_{\mathrm{max}}$ is respectable (54%) — not as high as compound 17 but well above compound 11. The $D_{\mathrm{max}}$ benefit came through; the $K_{d,\mathrm{CRBN}}$ price tag just shifted the $\mathrm{DC50}$ rightward. Pre-organization and binary engagement aren't independent levers; a single substituent can tune both, and compound 13 is the case where the rigidifying group was too big to fit the CRBN pocket.

The indole-series compounds (compounds 12/14/16/18) retell the same story on a stronger baseline — each chlorinated analog again outperforms its non-halogenated precursor — reinforcing that the effect is driven by conformational restriction rather than by idiosyncratic pocket interactions. From a design standpoint this is the cleanest kind of SAR lever: a single-atom substitution on the periphery of the molecule that reshapes the conformational ensemble enough to slide the compound along the Langmuir curve, without needing to redesign either binding interface. The only caution — as compound 13 demonstrates — is that the rigidifying group still has to fit where the molecule actually binds.

---

*Part 3 covers the cellular kinetic filter that converts ternary occupancy into observed $D_{\mathrm{max}}$, plus diagnostics and design implications: [Part 3 →](/posts/2026/04/molecular-glue-dc50-part3/)*
