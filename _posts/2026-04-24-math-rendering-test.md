---
title: 'Math Rendering Test — All Delimiter & Escape Variants'
date: 2026-04-24T23:00:00
permalink: /posts/2026/04/math-rendering-test/
tags:
  - Test
---

Each row tests one delimiter style and one content pattern. After viewing the built page, every formula should render as math — any that show as raw source tell us the delimiter/content combo kramdown is breaking.

---

## 1. Inline math — single-dollar delimiters

**1a. Plain, no underscores**: $\alpha + \beta = \gamma$

**1b. Braced subscript**: $D_{\max}$ and $K_{d,\mathrm{ternary}}$

**1c. Unbraced subscript + backslash command**: $\mathrm{DC50}_\mathrm{abs}$ (the historical problem case)

**1d. Braced subscript with backslash command**: $\mathrm{DC50}_{\mathrm{abs}}$

**1e. Two formulas on the same line**: $D_{\max}$ sits above $\mathrm{DC50}_\mathrm{half\text{-}max}$ which is sus.

**1f. Formula next to a literal word with underscore**: $D_{\max}$ and some_var below.

**1g. With color**: $\textcolor{#2166ac}{K_{d,\mathrm{CRBN}}}$

---

## 2. Inline math — MathJax `\(...\)` delimiters (single backslash in source)

**2a. Plain**: \(\alpha + \beta = \gamma\)

**2b. Braced subscript**: \(D_{\max}\) and \(K_{d,\mathrm{ternary}}\)

**2c. Unbraced subscript + backslash command**: \(\mathrm{DC50}_\mathrm{abs}\)

**2d. Braced subscript with backslash command**: \(\mathrm{DC50}_{\mathrm{abs}}\)

**2e. Two on same line**: \(D_{\max}\) and \(\mathrm{DC50}_\mathrm{half\text{-}max}\) together.

**2f. With color**: \(\textcolor{#2166ac}{K_{d,\mathrm{CRBN}}}\)

---

## 3. Inline math — `\(...\)` delimiters (double backslash in source)

**3a. Plain**: \\(\alpha + \beta = \gamma\\)

**3b. Braced subscript**: \\(D_{\max}\\) and \\(K_{d,\mathrm{ternary}}\\)

**3c. Unbraced subscript + backslash command**: \\(\mathrm{DC50}_\mathrm{abs}\\)

**3d. Braced subscript with backslash command**: \\(\mathrm{DC50}_{\mathrm{abs}}\\)

**3e. Two on same line**: \\(D_{\max}\\) and \\(\mathrm{DC50}_\mathrm{half\text{-}max}\\) together.

**3f. With color**: \\(\textcolor{#2166ac}{K_{d,\mathrm{CRBN}}}\\)

---

## 4. Display math — `$$...$$` on own lines

**4a. Plain**:

$$
\alpha + \beta = \gamma
$$

**4b. With subscripts and fractions**:

$$
\mathrm{DC50} \approx \frac{K_{d,\mathrm{CRBN}} \cdot K_{d,\mathrm{ternary}}}{K_{d,\mathrm{ternary}} + [P]}
$$

**4c. With `\textcolor`**:

$$
f_\mathrm{PLE}([L]) = \textcolor{#2166ac}{\frac{\beta}{1+\beta}} \cdot \frac{[L]}{[L] + \textcolor{#d6604d}{K_{d,\mathrm{CRBN}}/(1+\beta)}}
$$

**4d. With underscores + `\text`**:

$$
[L]_{50\%\,\mathrm{abs}} = \mathrm{DC50}_{\mathrm{half\text{-}max}} \cdot \frac{0.5}{D_{\mathrm{max}} - 0.5}
$$

---

## 5. Display math — `$$...$$` on a single line

**5a. Plain**: $$\alpha + \beta = \gamma$$

**5b. Braced subscript**: $$D_{\max}$$

**5c. With `\textcolor`**: $$\textcolor{#2166ac}{K_{d,\mathrm{CRBN}}}$$

---

## 6. Display math — `\[...\]` delimiters

**6a. Single backslash**:

\[
\alpha + \beta = \gamma
\]

**6b. Double backslash**:

\\[
\alpha + \beta = \gamma
\\]

---

## 7. Multi-underscore stress test — paragraphs with many inline formulas

These paragraphs reproduce the real failure condition: **multiple** `$...$` formulas in one paragraph, each containing underscores. kramdown pairs `_` across math expressions as emphasis, so even-count paragraphs tend to break.

### 7a. `$...$` with four braced underscores (even count — historical failure)

The definition most people mean — and what curve-fitting software actually returns — is the half-maximal concentration: the $[L]$ at which D($[L]$) = $D_{\mathrm{max}}$ / 2. This is the midpoint of the Hill curve, the direct analog of EC50 or IC50, and it's always defined regardless of how high or low $D_{\mathrm{max}}$ sits. The other definition, $\mathrm{DC50}_{\mathrm{abs}}$, asks instead for the concentration at which D($[L]$) = 0.5 — i.e., protein falls to exactly 50% of vehicle. That number only exists when $D_{\mathrm{max}}$ ≥ 0.5.

### 7b. `$...$` with eight underscores mixed braced/unbraced

At $D_{\mathrm{max}}$ = 0.6, the two differ by 5×. Below $D_{\mathrm{max}}$ = 0.5, $\mathrm{DC50}_\mathrm{abs}$ disappears entirely while $\mathrm{DC50}_\mathrm{half\text{-}max}$ remains finite. Combining $K_{d,\mathrm{CRBN}}$, $K_{d,\mathrm{ternary}}$, $K_{d,\mathrm{abs}}$, and $K_{d,\mathrm{rel}}$ into one line.

### 7c. `\\(...\\)` (double-backslash) — same content as 7a

The definition most people mean — and what curve-fitting software actually returns — is the half-maximal concentration: the \\([L]\\) at which D(\\([L]\\)) = \\(D_{\mathrm{max}}\\) / 2. This is the midpoint of the Hill curve, the direct analog of EC50 or IC50, and it's always defined regardless of how high or low \\(D_{\mathrm{max}}\\) sits. The other definition, \\(\mathrm{DC50}_{\mathrm{abs}}\\), asks instead for the concentration at which D(\\([L]\\)) = 0.5 — i.e., protein falls to exactly 50% of vehicle. That number only exists when \\(D_{\mathrm{max}}\\) ≥ 0.5.

### 7d. `\\(...\\)` with eight underscores mixed braced/unbraced

At \\(D_{\mathrm{max}}\\) = 0.6, the two differ by 5×. Below \\(D_{\mathrm{max}}\\) = 0.5, \\(\mathrm{DC50}_\mathrm{abs}\\) disappears entirely while \\(\mathrm{DC50}_\mathrm{half\text{-}max}\\) remains finite. Combining \\(K_{d,\mathrm{CRBN}}\\), \\(K_{d,\mathrm{ternary}}\\), \\(K_{d,\mathrm{abs}}\\), and \\(K_{d,\mathrm{rel}}\\) into one line.

### 7e. `$...$` with deliberate odd underscore count

Only $D_{\mathrm{max}}$ here; three underscores across: $K_{a,\mathrm{x}}$, $K_{b,\mathrm{y}}$, $K_{c,\mathrm{z}}$.

### 7f. Nested / complex math content — `$...$`

The $f_\mathrm{PLE}([L]) = \beta/(1+\beta)$ plateau depends on $\beta = [P]/K_{d,\mathrm{ternary}}$, not on $K_{d,\mathrm{CRBN}}$ directly.

### 7g. Nested / complex math content — `\\(...\\)`

The \\(f_\mathrm{PLE}([L]) = \beta/(1+\beta)\\) plateau depends on \\(\beta = [P]/K_{d,\mathrm{ternary}}\\), not on \\(K_{d,\mathrm{CRBN}}\\) directly.

### 7h. Dense chain of formulas — `$...$`

With $K_{d,\mathrm{ternary}}$, $K_{d,\mathrm{CRBN}}$, $K_{d,\mathrm{binary}}$, $K_{d,\mathrm{cell}}$, $K_{d,\mathrm{biochem}}$, and $K_{d,\mathrm{app}}$ all on one line.

### 7i. Dense chain — `\\(...\\)`

With \\(K_{d,\mathrm{ternary}}\\), \\(K_{d,\mathrm{CRBN}}\\), \\(K_{d,\mathrm{binary}}\\), \\(K_{d,\mathrm{cell}}\\), \\(K_{d,\mathrm{biochem}}\\), and \\(K_{d,\mathrm{app}}\\) all on one line.

### 7j. `$...$` + backticks/code + underscores nearby

If `some_var = 1` and `other_thing` sit next to $D_{\mathrm{max}}$ and $K_{d,\mathrm{ternary}}$, does inline code interfere?

### 7k. `$...$` within bold/italic context

**In bold**: $D_{\mathrm{max}}$ = 0.9 and $K_{d,\mathrm{ternary}}$ = 10 nM.

*In italic*: $D_{\mathrm{max}}$ = 0.9 and $K_{d,\mathrm{ternary}}$ = 10 nM.

---

## 8. Escape-underscore strategies — same paragraph, different protection

Same multi-formula paragraph as 7a, tested with different strategies for protecting underscores from kramdown.

### 8a. `$...$` with `\_` escaped underscores

The definition most people mean — is the half-maximal concentration: the $[L]$ at which D($[L]$) = $D\_{\mathrm{max}}$ / 2. Regardless of how high or low $D\_{\mathrm{max}}$ sits. The other definition, $\mathrm{DC50}\_{\mathrm{abs}}$, asks instead for the concentration. That number only exists when $D\_{\mathrm{max}}$ ≥ 0.5.

### 8b. `\\(...\\)` with `\_` escaped underscores

The definition most people mean — is the half-maximal concentration: the \\([L]\\) at which D(\\([L]\\)) = \\(D\_{\mathrm{max}}\\) / 2. Regardless of how high or low \\(D\_{\mathrm{max}}\\) sits. The other definition, \\(\mathrm{DC50}\_{\mathrm{abs}}\\), asks instead for the concentration. That number only exists when \\(D\_{\mathrm{max}}\\) ≥ 0.5.

### 8c. `{::nomarkdown}...{:/nomarkdown}` wrapping each formula

The definition most people mean — is the half-maximal concentration: the {::nomarkdown}$[L]${:/nomarkdown} at which D({::nomarkdown}$[L]${:/nomarkdown}) = {::nomarkdown}$D_{\mathrm{max}}${:/nomarkdown} / 2. Regardless of how high or low {::nomarkdown}$D_{\mathrm{max}}${:/nomarkdown} sits. The other definition, {::nomarkdown}$\mathrm{DC50}_{\mathrm{abs}}${:/nomarkdown}, asks instead. That number only exists when {::nomarkdown}$D_{\mathrm{max}}${:/nomarkdown} ≥ 0.5.

### 8d. HTML `<span>` wrapping each formula — `$...$`

<span>The definition most people mean — is the half-maximal concentration: the $[L]$ at which D($[L]$) = $D_{\mathrm{max}}$ / 2. Regardless of how high or low $D_{\mathrm{max}}$ sits. The other definition, $\mathrm{DC50}_{\mathrm{abs}}$, asks instead. That number only exists when $D_{\mathrm{max}}$ ≥ 0.5.</span>

### 8e. Raw HTML `<p markdown="0">` — `$...$` (kramdown extension)

<p markdown="0">The definition most people mean — is the half-maximal concentration: the $[L]$ at which D($[L]$) = $D_{\mathrm{max}}$ / 2. Regardless of how high or low $D_{\mathrm{max}}$ sits. The other definition, $\mathrm{DC50}_{\mathrm{abs}}$, asks instead. That number only exists when $D_{\mathrm{max}}$ ≥ 0.5.</p>

---

## 9. Notes on what should work

- All **Section 4** (display block) should render since kramdown recognizes `$$...$$` as a math block.
- **Section 2 vs 3** showed: kramdown strips `\(` to `(`, so single-backslash `\(...\)` fails, double-backslash `\\(...\\)` succeeds (delimiter-wise).
- **Section 7** is the real stress test: multi-underscore paragraphs. 7a/7b show that `$...$` breaks here; 7c/7d show whether `\\(...\\)` actually survives the content-mangling (underscores paired across expressions as emphasis).
- **Section 8** tests escape strategies to prevent kramdown from consuming `_`:
  - 8a/8b: escape each `_` with `\_` to survive kramdown emphasis processing.
  - 8c: disable markdown parsing per-formula with kramdown's `{::nomarkdown}` block.
  - 8d: wrap the whole paragraph in an HTML `<span>` — kramdown may still process content.
  - 8e: use `markdown="0"` attribute on HTML element to disable kramdown parsing inside.
