# LaTeX rendering rules for this Jekyll + kramdown + MathJax site

Hard-earned from a long debugging session. Apply these when authoring posts or pages with math.

## Setup (already in place)

- **Markdown processor**: kramdown with `input: GFM` ([_config.yml](../_config.yml))
- **Math renderer**: MathJax 3 loaded from CDN with the `color` package ([_includes/scripts.html](../_includes/scripts.html))
- **Delimiters configured**: `$...$` and `\(...\)` for inline; `$$...$$` and `\[...\]` for display

## The inline math problem

kramdown is called **before** MathJax on the built page. kramdown treats math delimiters as plain text and processes the body as markdown — which mangles LaTeX in two ways that are not obvious:

1. **`\(` is stripped to `(`**: kramdown treats `\` as an escape character and `(` is an escapable character. So `\(foo\)` in markdown becomes `(foo)` in HTML, and MathJax never sees its delimiters. Single-backslash `\(...\)` inline math **does not work** on this site.

2. **Underscores inside `$...$` become emphasis markers**: for patterns like `$\mathrm{DC50}_{\mathrm{abs}}$`, the `_` between `}` and `{` satisfies GFM's left-flanking rule (both sides are punctuation) so it *can* open emphasis. If another `_` later in the paragraph can close it, kramdown wraps the content between them in `<em>` tags and **consumes both underscores**. MathJax then sees `$\mathrm{DC50}{\mathrm{abs}}$` (no subscript) or, worse, the whole span including the `$` signs absorbed into italic text.

The count and flanking of underscores matters:
- A single formula with one `_` on a line → works.
- Two formulas with one `_` each, where one `_` sits in a `}_{` position → **breaks** (the `}_{` `_` opens, the next `_` closes).
- Dense chain of formulas with only `_{` (underscore-before-brace after a letter) can work because those `_` can only close, not open.

## The rule

**Inline math**: use `$...$` and **escape every underscore as `\_`** inside math.

```markdown
$D\_{\mathrm{max}}$ and $\mathrm{DC50}\_{\mathrm{abs}}$
```

kramdown converts `\_` back to a literal `_` in HTML, MathJax reads `_` as subscript, and no emphasis matching can touch it.

**Display math**: `$$...$$` on its own lines (blank line before and after). kramdown recognizes it as a math block and does not process markdown inside — underscores are safe, escaping not needed.

```markdown
$$
\mathrm{DC50} \approx \frac{K_{d,\mathrm{CRBN}} \cdot K_{d,\mathrm{ternary}}}{K_{d,\mathrm{ternary}} + [P]}
$$
```

**Also wrap `\mathrm{...}` arguments in braces on subscripts**: `_{\mathrm{abs}}` not `_\mathrm{abs}`. Both work inside `$$...$$`, but inside `$...$` the unbraced form tends to tangle with kramdown's escape handling.

**Color**: the `color` MathJax package is loaded, so `\textcolor{#hexcode}{...}` works in both inline and display math.

## What does NOT work (do not retry)

| Attempt | Why it fails |
|---|---|
| `\(...\)` (single backslash) inline | kramdown strips `\(` → `(` |
| `\\(...\\)` (double backslash) inline | Delimiter survives but content still gets mangled: kramdown pairs underscores across expressions as emphasis, consuming `_` before MathJax can see them |
| `$...$` with multiple `_`-containing formulas in one paragraph (unescaped) | `_` in `}_{` positions opens emphasis, pairs with the next `_`, kramdown italicizes everything in between |
| Wrapping math in `<span>...</span>` | kramdown still processes markdown inside |

## What also works (if you prefer, but uglier)

- `{::nomarkdown}$foo${:/nomarkdown}` — disables markdown parsing per-formula.
- `<p markdown="0">...</p>` — disables kramdown for an entire paragraph.

Neither is necessary if you just use `\_` escaping.

## Quick mental checklist when adding math

1. Display math (own line)? → use `$$...$$`, no escaping needed.
2. Inline math in a sentence? → use `$...$` and escape every `_` as `\_`.
3. Need color? → `\textcolor{#hex}{...}` works (color package is loaded).
4. Need to use `\mathrm`/`\text` in a subscript? → brace the argument: `_{\mathrm{abs}}`.

## Reference: the test post

[_posts/2026-04-24-math-rendering-test.md](../_posts/2026-04-24-math-rendering-test.md) exercises every delimiter/content combo documented here. If the rendering rules need to be re-verified (e.g. after a kramdown/MathJax upgrade), rebuild and look at that page.
