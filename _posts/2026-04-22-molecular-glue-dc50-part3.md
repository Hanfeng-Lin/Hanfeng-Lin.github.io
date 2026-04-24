---
title: 'Understanding Molecular Glue Dose-Response Curves — Part 3: From Biochemistry to the Cell'
date: 2026-04-22
permalink: /posts/2026/04/molecular-glue-dc50-part3/
tags:
  - Molecular Glue
  - Targeted Protein Degradation
  - Kinetics
  - Drug Discovery
---

*This is Part 3 of a three-part series.*

**Notation:** **L** = molecular glue; **E** = CRBN (E3 ligase); **P** = neosubstrate. Binary complex: \(L{\cdot}E\). Ternary complex: \(P{\cdot}L{\cdot}E\).

**Recap from [Part 1](/posts/2026/04/molecular-glue-dc50-part1/) and [Part 2](/posts/2026/04/molecular-glue-dc50-part2/).** \(\mathrm{DC50}\) is the half-max Hill midpoint; the achievable plateau is \(f_{\mathrm{PLE}}\) = \(\beta/(1+\beta)\) with \(\beta\) = \([P]\)/\(K_{d,\mathrm{ternary}}\). Curve shift direction encodes mechanism: \(D_{\mathrm{max}}\) drop → downstream problem; \(\mathrm{DC50}\) rightward shift → binding or exposure problem — though Part 2 showed that this separation breaks down in the \([P]\)-subsaturating regime, where \(K_{d,\mathrm{ternary}}\) changes \(D_{\mathrm{max}}\) strongly while barely moving \(\mathrm{DC50}\). Pre-organization tightens \(K_{d,\mathrm{ternary}}\) without changing \(K_{d,\mathrm{CRBN}}\), improving both \(\mathrm{DC50}\) and \(D_{\mathrm{max}}\) on the same lever. The NGT-201 halogen series on VAV1 illustrates this: compound 17 (Cl) wins on \(D_{\mathrm{max}}\) (15% → 90%) and \(\mathrm{DC50}\) (~30×) relative to compound 11 (H) despite slightly worse CRBN binary engagement — pre-organization pays off on both axes when the compound moves along the Langmuir curve from \(\beta \ll 1\) toward \(\beta \gg 1\).

But there is one more layer. So far, everything has been about ternary complex thermodynamics — how much of CRBN ends up bound to the neosubstrate at a given compound concentration. A cellular dose-response doesn't actually measure that. It measures target protein remaining at the assay endpoint, which is the *result* of ternary occupancy running against the target's own synthesis-degradation machinery. This layer is what Part 3 unpacks — and it's where the compound 11 vs 17 story gets its final reality check.

## \(f_{\mathrm{PLE}}\) is not the dose-response curve

Target protein levels follow a synthesis-degradation balance:

$$\frac{d[T]}{dt} = k_{\mathrm{syn}} - k_{\mathrm{deg}}\cdot[T] \qquad k_{\mathrm{deg}} = k_{\mathrm{basal}} + k_{\mathrm{induced}}$$

The glue-driven degradation rate \(k_{\mathrm{induced}}\) is proportional to ternary complex concentration: \(k_{\mathrm{induced}} \propto k_{\mathrm{ub}} \cdot P(\text{transfer}) \cdot [P{\cdot}L{\cdot}E]\). At steady state, this gives:

$$\frac{[T]_{ss}}{[T]_0} = \frac{k_{\mathrm{basal}}}{k_{\mathrm{basal}}+k_{\mathrm{induced}}} = \frac{1}{1+\gamma\cdot f_{\mathrm{PLE}}([L])}$$

where **\(\gamma\) = \(k_{\mathrm{induced, max}}\) / \(k_{\mathrm{basal}}\) is a dimensionless degradation efficiency — a ratio comparing how fast glue-driven degradation can run against the target's natural turnover rate.** At saturating compound, \(D_{\mathrm{max}}\) takes the form:

$$D_{\mathrm{max}} = \frac{\gamma\beta}{1+\beta+\gamma\beta}$$

The two limiting cases reveal the range of behavior. When \(\gamma\) is large — efficient induced degradation against a slowly-turning-over target — \(D_{\mathrm{max}}\) approaches 1 and the target is driven near zero even at modest \(f_{\mathrm{PLE}}\). Resynthesis simply cannot keep up. When \(\gamma\) is small — the induced rate barely exceeds basal — \(D_{\mathrm{max}}\) tracks \(f_{\mathrm{PLE}}\) linearly and deep degradation is hard to achieve regardless of compound potency.

### Does this change the compound 11 vs 17 story?

It's worth stress-testing Part 2's explanation against the γ-filter. In Part 2 we matched compound 11's 15% \(D_{\mathrm{max}}\) and compound 17's 90% \(D_{\mathrm{max}}\) to putative \(f_{\mathrm{PLE}}\) plateaus of ~14% and ~83% with \(\beta \approx 0.17\) and \(\beta \approx 5\)–10 — a pure Langmuir story, with γ not even mentioned. That fit the data, but it's also consistent with other γ/β combinations. What does \(D_{\mathrm{max}} = \gamma\beta/(1+\beta+\gamma\beta)\) actually say?

At modest \(\gamma\) (say \(\gamma\) = 1 — induced rate comparable to basal), compound 11's \(\beta = 0.17\) would give \(D_{\mathrm{max}} = 0.17/(1 + 0.17 + 0.17) \approx 13\%\) and compound 17's \(\beta = 5\) gives \(5/(1 + 5 + 5) \approx 45\%\) — the gap shows up, but 17 falls short of 90%. Push \(\gamma\) higher — say \(\gamma = 10\) — and compound 17 rises to \(50/61 \approx 82\%\), while compound 11 rises to \(1.7/2.87 \approx 59\%\), shrinking the gap. Push \(\gamma\) above ~30, and compound 11 alone would be driven to \(\sim 84\%\) \(D_{\mathrm{max}}\) purely by the filter — making the observed 15% incompatible with the data.

The observed 15% / 90% pair boxes VAV1's γ into a specific regime: high enough that compound 17 (with \(\beta \gg 1\)) can reach near-100% \(D_{\mathrm{max}}\), but not so high that compound 11 (with \(\beta \ll 1\)) gets rescued by the filter. In other words, VAV1 behaves like a moderately-turnover target where the Langmuir ceiling in \([P{\cdot}L{\cdot}E]\) really is the binding constraint. The Part 2 explanation survives — but only because γ sits in the right window to let it dominate. On a much faster-turnover target (MYC, c-Jun, short-half-life TFs), the same compound 17 might underperform and compound 11 might look roughly similar, because γ would not be high enough to amplify compound 17's ternary-occupancy advantage.

Several practical consequences follow from this. **Fast-turnover targets are intrinsically harder to degrade deeply**: a target with a 30-minute basal half-life demands a far higher \(\gamma\) than a 24-hour target to achieve the same \(D_{\mathrm{max}}\). This is why stable targets often show impressive \(D_{\mathrm{max}}\) with mediocre compounds, while unstable targets ruthlessly punish every thermodynamic weakness in the series. **At high \(\gamma\), \(D_{\mathrm{max}}\) and \(f_{\mathrm{PLE}}\) decouple** — small fractions of actively-engaged CRBN can overwhelm resynthesis, and improving \(f_{\mathrm{PLE}}\) from 0.3 to 0.9 changes little. **Time-dependence matters**: steady-state requires the assay to run long enough to equilibrate. A 4-hour \(D_{\mathrm{max}}\) and a 24-hour \(D_{\mathrm{max}}\) can differ substantially for stable targets, and published \(\mathrm{DC50}\)/\(D_{\mathrm{max}}\) pairs are window-specific — not cleanly comparable across protocols. Finally, the 1/(1+\(\gamma\)·\(f_{\mathrm{PLE}}\)) transformation is nonlinear in a way that compresses near the plateau and steepens near the midpoint, which is why cellular Hill slopes typically exceed 1 and fitted Hill coefficients absorb this without illuminating the mechanism.

### Biochemical vs cellular readouts measure different things

The gap between thermodynamic occupancy and cellular dose-response is large enough that it is worth stating explicitly. Biochemical ternary TR-FRET gives \(f_{\mathrm{PLE}}([L])\) directly — the plateau really is \(\beta/(1+\beta)\), a thermodynamic observable. Cellular dose-response gives \(D([L])\), which is \(f_{\mathrm{PLE}}\) filtered through \(\gamma\) and assay kinetics. As a result, cellular \(\mathrm{DC50}\) and biochemical \(K_{d,\mathrm{ternary}}\) can differ by orders of magnitude, and cellular \(D_{\mathrm{max}}\) is not the \(f_{\mathrm{PLE}}\) plateau but rather that plateau passed through a nonlinear \(1/(1+\gamma x)\) filter.

This is why biochemical-to-cellular translation in the glue field is so noisy. At least four target-dependent parameters — \(\gamma\), \(k_{\mathrm{cat}}\), \([P]\), and basal turnover — sit between the biochemical measurement and the cellular readout, and most labs don't measure them explicitly. The apparent \(\mathrm{DC50}\) and \(D_{\mathrm{max}}\) absorb all of these terms simultaneously. For compound 11 vs 17 this means the biochemical TR-FRET ceiling would read cleanly (something like 14% vs 83%), while the cellular read gets pushed further apart by the γ filter — but only on a target like VAV1 where γ is big enough to do the amplification.

![Figure 5 — Biochemical TR-FRET measures thermodynamic occupancy (\(f_{\mathrm{PLE}}\) plateau) directly; the cellular assay reads that occupancy after passage through a multi-parameter filter. Apparent \(\mathrm{DC50}\) and \(D_{\mathrm{max}}\) absorb all filter terms, making cross-assay comparisons unreliable without accounting for \(\gamma\), resynthesis, window, and exposure.](/images/blog/molecular-glue-dc50/fig5_biochemical_cellular_filter.png)

## Diagnostics and design implications

With that framework in hand, the diagnostic logic becomes more concrete. Take the compound 11/17 case as the reference: what would it actually take to confirm the Langmuir-dominated story we've been telling?

**First, measure \(K_{d,\mathrm{ternary}}\) directly.** Biochemical ternary TR-FRET at fixed CRBN, fixed \([P]\), titrated against compound, extracts \(K_{d,\mathrm{ternary}}\) without relying on the cellular filter at all. If compound 11 really sits at \(K_{d,\mathrm{ternary}} \approx 300\) nM and compound 17 at ~10 nM (as the cellular numbers suggest), the TR-FRET plateaus should read ~14% and ~83% directly when [P] is held at the cellular range (~50 nM). A clean match between biochemical plateau and cellular \(D_{\mathrm{max}}\) would say γ is small on this target; a large gap (biochemical ceiling low, cellular \(D_{\mathrm{max}}\) high) would say γ is doing the amplification. Either way, the experiment cleanly separates the two hypotheses.

**Second, titrate \([P]\) in a single cellular background.** Neosubstrate overexpression should preferentially rescue the weak compound (compound 11), because it pushes β from sub-saturation up toward saturation. Conversely, knockdown should widen the gap, because compound 11 stays deeply sub-saturating while compound 17 moves closer to the \(\beta = 1\) transition where the Langmuir is steepest. The titration has to be done in one cell line — comparing across cell lines confounds \([P]\) with \([E]\) (CRBN levels vary too) and with γ, so any cross-line "abundance panel" mixes the variables we're trying to separate. If overexpression/knockdown in a fixed background doesn't move the \(D_{\mathrm{max}}\) gap the way the Langmuir predicts, the story is not pure saturation and something else (residence time, γ differences, geometry) is in play.

**Residence time is a real lever but a secondary one.** Separating it from \(K_{d,\mathrm{ternary}}\) requires jump-dilution or competitive-chase kinetics on ternary complex dissociation. For the NGT-201 series, the chlorine's pre-organization effect should show up primarily in \(K_{d,\mathrm{ternary}}\) (equilibrium) rather than specifically in \(k_{\mathrm{off}}\), but chase experiments would confirm this cleanly. Worth building into the assay stack as a tier-2 readout once the primary \(K_{d,\mathrm{ternary}}\) ranking is established.

**Pre-organization is one of the cleanest design levers in glue chemistry** — not least because the NGT-201 halogen series shows it delivering on both axes at once. It operates through \(K_{d,\mathrm{ternary}}\) without touching the CRBN or neosubstrate contact surfaces, is addressable synthetically (ring constraints, conformational locks, intramolecular H-bonds), and pays off on \(\mathrm{DC50}\) and \(D_{\mathrm{max}}\) simultaneously when the compound is sliding through the sub-saturating regime. The single caveat — as compound 13 demonstrated in Part 2 — is that the rigidifying group has to fit wherever the molecule actually binds.

**\(D_{\mathrm{max}}\) reporting should specify the target.** The same compound can appear as a "70% \(D_{\mathrm{max}}\) glue" against a stable, abundant target and as a weak partial degrader against a fast-turnover, low-abundance one — purely because \(\gamma\) and \([P]\) differ. Compound 17's 90% on VAV1 is a VAV1 number; the same molecule on a MYC-like target could easily read 30%. These are not the same compound in any pharmacologically meaningful sense, even if the cellular dose-response curves look superficially similar.

**"Saturating compound" in biochemistry ≠ saturating ternary occupancy.** You can flood CRBN with compound until binary engagement is complete and still only have \(f_{\mathrm{PLE}}\) = 0.1 in ternary complex if \([P]\) falls below \(K_{d,\mathrm{ternary}}\). The plateau of the biochemical TR-FRET titration in \([L]\) reads this out directly — if the signal is flat at 15% of maximum rather than 90%, you are \([P]\)-limited, not compound-limited. For compound 11, that's exactly the diagnosis; for compound 17, the plateau should climb to near saturation.

## The broader point

\(\mathrm{DC50}\) and \(D_{\mathrm{max}}\) are not orthogonal potency/efficacy descriptors. They are coupled readouts of the same underlying thermodynamics — \(K_{d,\mathrm{CRBN}}\), \(K_{d,\mathrm{ternary}}\), \([P]\) — filtered through kinetics (\(k_{\mathrm{off}}\), \(k_{\mathrm{cat}}\)) and cellular physiology (\(\gamma\), resynthesis, assay window). Treating them as independent axes is convenient for SAR tables but leads to systematic misreading: pre-organization effects appearing where they "shouldn't," matched-binary compounds giving divergent cellular profiles, biochemical-to-cellular translation that looks random.

The cleaner mental model is that \(K_{d,\mathrm{ternary}}\) is the master variable. It sets \(\mathrm{DC50}\) through \(\mathrm{DC50} \approx K_{d,\mathrm{CRBN}} \cdot K_{d,\mathrm{ternary}} / (K_{d,\mathrm{ternary}} + [P])\), and it sets the \(f_{\mathrm{PLE}}\) plateau through \(\beta/(1+\beta)\). \(D_{\mathrm{max}}\) is that plateau filtered through the target's \(\gamma\). Improving \(K_{d,\mathrm{ternary}}\) — through cooperativity, pre-organization, or optimized interface contacts — moves both axes simultaneously, in the same direction, for the same reason.

The NGT-201 halogen series is a concrete demonstration of exactly this. Compound 11 to compound 17 is a single-atom swap on the periphery of the molecule — it doesn't touch either binding interface, doesn't improve binary CRBN engagement (if anything it makes it worse), and doesn't invoke residence time or geometric corrections. What it does is reshape the free-solution conformational ensemble, tightening \(K_{d,\mathrm{ternary}}\) enough to slide the compound from deep sub-saturation (\(\beta \ll 1\)) to comfortably past saturation (\(\beta \gg 1\)). Both DC50 and \(D_{\mathrm{max}}\) follow — they have no choice, given the math. Compound 13 (methyl) is the counterexample: same rigidification intent, but the rigidifier clashes in the CRBN pocket, so \(K_{d,\mathrm{CRBN}}\) collapses and the DC50 right-shifts. Every data point in the series fits the framework; none of them require side explanations.

Once you hold that in mind, most of the apparent paradoxes in cellular degradation SAR dissolve into straightforward consequences of a three-body binding equilibrium running against the background of cellular proteostasis. The formulas are not hard; the habit of applying them is.
