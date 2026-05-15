# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**KRM** is the corrections and research repository for the Cologne digitization of the *Kṛdantarūpamālā* (a comprehensive list of Sanskrit verbal derivatives / kṛdanta forms). The canonical source lives in `csl-orig/v02/krm/krm.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `verbs01/` | Root correspondence: maps KRM headwords (which are all roots) to MW root spellings; also maps Sayana's Mādhavīya Dhātuvṛtti to MW |

### Verb root pipeline (`verbs01/`)

KRM entries are verbal roots (dhātu), so `verbs01/` establishes systematic correspondence with MW roots:
- [KRM issue #1](https://github.com/sanskrit-lexicon/KRM/issues/1): KRM headword → MW root mapping
- [KRM issue #2](https://github.com/sanskrit-lexicon/KRM/issues/2): Sayana's Mādhavīya Dhātuvṛtti → MW root mapping

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/KRM/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh krm ../../KRMScan/2020
sh xmlchk_xampp.sh krm
```

## Dependencies

- **Python 3**
- **krm.txt** — in `$BASE/cologne/csl-orig/v02/krm/krm.txt`
