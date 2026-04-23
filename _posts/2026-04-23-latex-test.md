---
title: 'LaTeX Rendering Test'
date: 2026-04-23
permalink: /posts/2026/04/latex-test/
tags:
  - Test
---

This post tests MathJax LaTeX rendering.

## Inline Math

The energy-mass equivalence $E = mc^2$ and the quadratic formula $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ should render inline.

## Display Math

The Gaussian integral:

$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

Euler's identity:

$$e^{i\pi} + 1 = 0$$

A matrix:

$$\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \quad \det(\mathbf{A}) = ad - bc$$

The Schrödinger equation:

$$i\hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat{H}\Psi(\mathbf{r},t)$$

If all of the above render correctly, LaTeX support is working.
