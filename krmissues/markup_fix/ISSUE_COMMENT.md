_Created: 22-05-2026 · Last updated: 05-09-2026_

### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `krm.txt`.

I ran the same two-job recipe over `csl-orig/v02/krm/krm.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `krmissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `krm.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<s> word </s>` | `<s>word</s>` |
| `<sup> word </sup>` | `<sup>word</sup>` |
| `<F> word </F>` | `<F>word</F>` |

Whitespace trimming applies to all 4 paired tag(s) in `krm.txt`: `<s>`, `<sup>`, `<F>`, `<Poem>`. The original file is never modified — output goes to `krm_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). 5 line(s) changed.

### Closing-tag inventory in current `krm.txt`

| Tag | Count |
|---|---:|
| `</s>` | 74 |
| `</816)>` | ? |
| `</sup>` | 9 |
| `</327)>` | ? |
| `</F>` | 9 |
| `</293)>` | ? |
| `</Poem>` | 2 |

### What it found in current `krm.txt`

- 5 whitespace trims applied: trailing spaces in `<s>` (5) and `<F>` (3) tags.
- 0 adjacent `</ab> <ab>` — no `<ab>` tag in krm.txt.
- 0 `<ab n="…">` attributes.
- 2 correction records present.

### Usage

```
cd krmissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/krm/krm.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `krm_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

No <ab> or <ls>; <s> and <F> are primary paired tags.

### Severity

`minor`

_Dr. Mārcis Gasūns_
