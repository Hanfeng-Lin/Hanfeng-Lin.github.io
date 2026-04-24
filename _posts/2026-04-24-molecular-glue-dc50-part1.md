---
title: 'Understanding Molecular Glue Dose-Response Curves — Part 1: What \(\mathrm{DC50}\) and \(D_{\mathrm{max}}\) Actually Mean'
date: 2026-04-24
permalink: /posts/2026/04/molecular-glue-dc50-part1/
tags:
  - Molecular Glue
  - Targeted Protein Degradation
  - Thermodynamics
  - Drug Discovery
---

Molecular glue SAR is reported in the language of \(\mathrm{DC50}\) and \(D_{\mathrm{max}}\), and the field treats them as orthogonal descriptors — one for potency, one for efficacy. It's a convenient shorthand, but it's mechanistically sloppy. Both parameters are governed by the same underlying binding constants, weighted differently by compound concentration, target abundance, and assay kinetics. Once you unpack the coupling, a lot of confusing SAR patterns — curves that move up without moving right, compounds with matched binary engagement but divergent cellular \(D_{\mathrm{max}}\), pre-organization effects that shouldn't be affecting \(D_{\mathrm{max}}\) but clearly are — resolve into a coherent picture.

This series walks through that picture from the ground up. Part 1 covers the two \(\mathrm{DC50}\) definitions, the ternary complex thermodynamics behind \(\mathrm{DC50}\), and how to read mechanistic information from curve shift direction. [Part 2](/posts/2026/04/molecular-glue-dc50-part2/) covers pre-organization, residence time, and the \([P]\) saturation mechanism that drives most \(D_{\mathrm{max}}\) differences in matched-binary series. [Part 3](/posts/2026/04/molecular-glue-dc50-part3/) covers the cellular kinetic filter, diagnostics, and design implications.

**Notation used throughout this series:** **L** = molecular glue compound; **E** = E3 ligase (CRBN); **P** = neosubstrate (target protein). Binary complex: \(L{\cdot}E\). Ternary complex: \(P{\cdot}L{\cdot}E\).

## What \(\mathrm{DC50}\) actually means

The first confusion is definitional. "\(\mathrm{DC50}\)" gets used for two different quantities that happen to coincide when \(D_{\mathrm{max}}\) = 100% and diverge everywhere else.

Cellular degradation dose-response is typically modeled with a Hill equation:

$$
D([L]) = \frac{D_{\mathrm{max}} \cdot [L]^n}{\mathrm{DC50}^n + [L]^n}
$$

where D is fractional degradation (1 − protein_treated / protein_vehicle), \(D_{\mathrm{max}}\) is the achievable plateau, and n is the Hill coefficient.

The definition most people mean — and what curve-fitting software actually returns — is the half-maximal concentration: the \([L]\) at which D(\([L]\)) = \(D_{\mathrm{max}}\) / 2. This is the midpoint of the Hill curve, the direct analog of EC50 or IC50, and it's always defined regardless of how high or low \(D_{\mathrm{max}}\) sits. The other definition, \(\mathrm{DC50}_{\mathrm{abs}}\), asks instead for the concentration at which D(\([L]\)) = 0.5 — i.e., protein falls to exactly 50% of vehicle. That number only exists when \(D_{\mathrm{max}}\) ≥ 0.5. If a compound maxes out at 40% degradation, no concentration ever achieves 50% and this "\(\mathrm{DC50}\)" is simply undefined.

Solving the Hill equation at D = 0.5 gives the relationship between them (with n = 1):

$$
[L]_{50\%\,\mathrm{abs}} = \mathrm{DC50}_{\mathrm{half\text{-}max}} \cdot \frac{0.5}{D_{\mathrm{max}} - 0.5}
$$

At \(D_{\mathrm{max}}\) = 0.6, the two differ by 5×. Below \(D_{\mathrm{max}}\) = 0.5, \(\mathrm{DC50}_{\mathrm{abs}}\) disappears entirely while \(\mathrm{DC50}_{\mathrm{half\text{-}max}}\) remains a perfectly finite, meaningful number.

The practical consequence is that ranking compounds by "\(\mathrm{DC50}\)" is treacherous when \(D_{\mathrm{max}}\) varies across a series. A partial degrader with genuinely sub-nM ternary binding can look worse than a weaker but fully-efficacious glue under the absolute definition, because efficacy gets smuggled into what should be a pure potency number. Throughout this series, \(\mathrm{DC50}\) means half-maximal, consistent with how curve-fitting software reports it.

![Figure 1 — Two \(\mathrm{DC50}\) definitions on the same Hill curve (\(D_{\mathrm{max}}\) = 60%). \(\mathrm{DC50}_{\mathrm{abs}}\) is 5× higher than \(\mathrm{DC50}_{\mathrm{half\text{-}max}}\); below \(D_{\mathrm{max}}\) = 50% it is undefined entirely.](/images/blog/molecular-glue-dc50/fig1_dc50_definitions.png)

## \(\mathrm{DC50}\) in terms of ternary complex thermodynamics

At its core, \(\mathrm{DC50}\) is the concentration at which the cellular steady-state pool of productive ternary complex reaches half of its achievable maximum. The rate of neosubstrate ubiquitination is proportional to \([P{\cdot}L{\cdot}E]\), so the steady-state target level tracks ternary complex occupancy, and \(\mathrm{DC50}\) marks the point at which half of the productive CRBN pool is engaged with the neosubstrate.

For a pure glue with no intrinsic neosubstrate affinity, the binding plays out in two steps:

$$
L + E \rightleftharpoons L{\cdot}E \qquad K_{d,\,\mathrm{CRBN}}
$$

$$
L{\cdot}E + P \rightleftharpoons P{\cdot}L{\cdot}E \qquad K_{d,\,\mathrm{ternary}}
$$

With \([P]\) held constant, the fraction of CRBN in ternary complex is hyperbolic in \([L]\):

$$
\frac{[\mathrm{PLE}]}{[E]_T} = \frac{\beta}{1+\beta} \cdot \frac{[L]}{K_{d,\,\mathrm{CRBN}}\,/\,(1+\beta)\;+\;[L]} \qquad \beta \equiv \frac{[P]}{K_{d,\,\mathrm{ternary}}}
$$

From the two equilibria, express each CRBN pool in terms of free \([E]\):

$$
[\text{L·E}] = \frac{[\text{L}][\text{E}]}{K_{d,\text{CRBN}}}, \qquad [\text{P·L·E}] = \frac{[\text{L}][\text{E}][\text{P}]}{K_{d,\text{CRBN}} \cdot K_{d,\text{ternary}}}
$$

Total CRBN is conserved:

$$
[\text{E}]_\text{total} = [\text{E}]\left(1 + \frac{[\text{L}]}{K_{d,\text{CRBN}}} + \frac{[\text{L}][\text{P}]}{K_{d,\text{CRBN}} \cdot K_{d,\text{ternary}}}\right)
$$

Dividing \([\text{PLE}]\) by \([E]_\text{total}\) — i.e., computing \(f_\text{PLE}\), the fraction of CRBN in ternary complex — and factoring out \([L]/K_{d,\text{CRBN}}\) from numerator and denominator:

$$
f_\text{PLE} = \frac{[\text{PLE}]}{[E]_\text{total}} = \frac{[\text{L}] \cdot \beta/(1+\beta)}{[\text{L}] + K_{d,\text{CRBN}}/(1+\beta)}
$$

where \(\beta\) = \([P]\)/\(K_{d,\mathrm{ternary}}\). This is a standard hyperbola in \([L]\):

$$
f_{\mathrm{PLE}}([L]) = \textcolor{#2166ac}{\frac{\beta}{1+\beta}} \cdot \frac{[L]}{[L] + \textcolor{#d6604d}{K_{d,\,\mathrm{CRBN}}/(1+\beta)}}
$$

with plateau \(\textcolor{#2166ac}{\beta/(1+\beta)}\) and half-max \(\textcolor{#d6604d}{K_{d,\,\mathrm{CRBN}}/(1+\beta)}\). The simplification relies on \([P]\) being held constant — valid when \([P]\) is in large excess over \([L{\cdot}E]\), or when analyzing E occupancy with \([P]\) as a fixed parameter. If ternary complex formation meaningfully depletes \([P]\), the expression becomes non-hyperbolic.

Two parameters fall out cleanly. The plateau is \(\beta/(1+\beta)\). The half-max of \(f_{\mathrm{PLE}}\) — the concentration at which ternary occupancy reaches half its ceiling — is exactly:

$$
[L]_{1/2}^{f_{\mathrm{PLE}}} = \frac{K_{d,\,\mathrm{CRBN}}}{1+\beta} = \frac{K_{d,\,\mathrm{CRBN}} \cdot K_{d,\,\mathrm{ternary}}}{K_{d,\,\mathrm{ternary}} + [P]}
$$

This is not the same as the cellular \(\mathrm{DC50}\). The cellular \(\mathrm{DC50}\) is the half-max of D(\([L]\)), which passes through the \(\gamma\)-filter (Part 3). Working through that filter gives \(\mathrm{DC50}_{\mathrm{cellular}}\) = \(K_{d,\mathrm{CRBN}}\) / (1 + \(\beta(1+\gamma)\)), shifted further left than the thermodynamic half-max by a \(\gamma\beta\) term in the denominator. The formula above is therefore an approximation to cellular \(\mathrm{DC50}\) — exact when \(\gamma\) is small or \(\beta\) is small, increasingly optimistic as the degradation machinery becomes more efficient. With that caveat in mind:

$$
\mathrm{DC50} \approx \frac{K_{d,\,\mathrm{CRBN}} \cdot K_{d,\,\mathrm{ternary}}}{K_{d,\,\mathrm{ternary}} + [P]}
$$

The two limiting regimes tell the story. When the target is abundant and the ternary is tight (\([P]\) ≫ \(K_{d,\mathrm{ternary}}\)), \(\mathrm{DC50}\) is pushed well below \(K_{d,\mathrm{CRBN}}\) — this is the "cooperativity for free" that glues exploit, where the neosubstrate surface stabilizes what would otherwise be a weak CRBN engagement. In the opposite limit, when ternary recruitment is poor (\([P]\) ≪ \(K_{d,\mathrm{ternary}}\)), \(\mathrm{DC50}\) collapses back toward \(K_{d,\mathrm{CRBN}}\) and \(D_{\mathrm{max}}\) scales with \([P]\)/\(K_{d,\mathrm{ternary}}\). The compound then titrates CRBN on its own merits, and ternary complex never reaches meaningful occupancy.

This is the thermodynamic backbone. Everything else is embellishment on top.

![Figure 2 — Two-step binding equilibrium. L and E associate with \(K_{d,\mathrm{CRBN}}\) to form the binary complex; recruitment of neosubstrate P (governed by \(K_{d,\mathrm{ternary}}\) and cooperativity \(\alpha\)) forms the productive ternary complex; ubiquitin transfer (\(k_{\mathrm{ub}}\) · P(transfer)) drives target degradation.](/images/blog/molecular-glue-dc50/fig2_ternary_equilibrium.png)

## Reading dose-response shifts: up vs right

When two compounds' dose-response curves differ, the direction of the shift encodes mechanistic information — and it's worth reading carefully before reaching for an explanation.

If the curve moves up (\(D_{\mathrm{max}}\) drops, \(\mathrm{DC50}\) unchanged), you have the same apparent potency but a lower achievable plateau. Something is rate-limiting downstream of ternary complex formation, or capping the degradable pool. The most common culprits are compromised ubiquitination geometry — \(k_{\mathrm{ub}}\) drops even though \([P{\cdot}L{\cdot}E]\) saturates normally — a degradation-resistant subpopulation of target that is compartmentalized or sequestered in a complex, target resynthesis outpacing the degradation rate, UPS saturation at high compound doses, or non-productive ternary engagement that forms complex but fails to position lysines correctly. Up-shift diagnostics focus on geometry and accessibility; in vitro ubiquitination assays can separate \(k_{\mathrm{ub}}\) from occupancy cleanly.

If the curve moves right (\(\mathrm{DC50}\) rises, \(D_{\mathrm{max}}\) unchanged), the plateau is preserved but more compound is needed to reach it. Something is shifting the binding side: weaker \(K_{d,\mathrm{CRBN}}\), weaker \(K_{d,\mathrm{ternary}}\) or lower cooperativity \(\alpha\), reduced intracellular exposure through permeability or efflux (P-gp is a classic SAR trap), metabolic instability within the assay window, or off-target compound sequestration. Right-shift diagnostics focus on biochemistry versus exposure, and a matched biochemical TR-FRET assay will quickly distinguish a thermodynamic cause from a pharmacokinetic one.

Is this clean separation really true? — Can a binding change ever drop \(D_{\mathrm{max}}\) without moving \(\mathrm{DC50}\)? Hold that question for Part 2.

![Figure 3 — Shift direction diagnoses mechanism. Left: \(D_{\mathrm{max}}\) drops while \(\mathrm{DC50}\) is unchanged — a downstream problem (geometry, resistant subpopulation, UPS saturation). Right: \(\mathrm{DC50}\) rises while \(D_{\mathrm{max}}\) is unchanged — a binding or exposure problem (weaker Kd, efflux, metabolic instability).](/images/blog/molecular-glue-dc50/fig3_shift_up_right.png)

---

*Part 2 covers the matched-binary case, residence time, pre-organization, and why \([P]\) saturation is the single most important variable for understanding \(D_{\mathrm{max}}\) differences:* [*Part 2 →*](/posts/2026/04/molecular-glue-dc50-part2/)
