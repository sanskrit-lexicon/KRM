# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**KRM** is the development and correction repository for the **_Kṛdantarūpamālā_** (attributed to Bhaṭṭoji Dīkṣita), a Sanskrit grammatical handbook of *kṛdanta* (primary derivative / participial) verb forms, within the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL).

- **Canonical source text**: [`csl-orig/v02/krm/krm.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/krm/krm.txt) (2,061 entries) — corrections are applied there, not stored here.
- This repository holds **verb-identification** work mapping KRM roots to MW and Mādhavīya-Dhātuvṛtti (MDP) headwords.

## Architecture

| Path | Purpose |
|---|---|
| `verbs01/` | Verb-identification: KRM root ↔ MW / MDP headword mapping |
| `DATA_DICTIONARY.md` | Markup tag reference |
| `CITATION.cff` | Citation metadata |
| `LICENSE` | Creative Commons Attribution-ShareAlike 4.0 International |

## Key commands

Corrections follow the CDSL `updateByLine.py` pattern, applied against the csl-orig source:

```sh
python updateByLine.py <input> <changefile> <output>
```

Change-file format (paired lines; `;`-prefixed comments): `new` (replace), `ins` (insert after), `del` (delete). All files UTF-8 (no BOM).

## Data format

Kṛdantarūpamālā entries use standard CDSL markup with Sanskrit in SLP1. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for the tag reference.

| Tag | Role | Example |
|---|---|---|
| `<L>NNNN` | Entry begin, with `<pc>` print page ref | `<L>1<pc>0003` |
| `<k1>`, `<k2>` | Primary / secondary headword (SLP1) | `<k1>aka<k2>aka` |
| `<LEND>` | Entry end | |
| `<s>…</s>` | Sanskrit text (SLP1) | `<s>I-BvAdiH</s>` |
| `{@…@}` | Bold display | `{@…@}` |
| `{%…%}` | Italic display | |

Annotated example — the first entry of `krm.txt`:
```
<L>1<pc>0003<k1>aka<k2>aka         # entry 1; print page 0003; headword "aka"
(1) {@<s>"aka kuwilAyAM gatO"</s>@}¦ (<s>I-BvAdiH</s>-792 ...)   # root + grammatical analysis
<LEND>                              # entry end
```

## Dependencies

- Python 3 (correction and verb-identification scripts).
- No build step in this repo; XML and web display are generated centrally from `csl-orig` via `csl-pywork`.

## Licensing note

The repository `LICENSE` and `CITATION.cff` both declare **CC BY-SA 4.0** for this dataset, matching the CDSL dictionary-data standard.

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.
