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

## 7. Notes on what should work

- All **Section 4** (display block) should render since kramdown recognizes `$$...$$` as a math block and leaves it alone.
- **Section 2 vs 3** is the key test: whether kramdown escapes `\(` to `(` (in which case Section 2 fails and Section 3 succeeds) or passes it through.
- **Section 1** tests kramdown's handling of `$...$` — any underscore-bearing content is suspect.
