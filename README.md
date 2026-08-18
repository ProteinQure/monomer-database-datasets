# Monomer database datasets
[![Release](https://img.shields.io/github/v/release/ProteinQure/monomer-database-datasets?label=release&color=f5995b)](https://github.com/ProteinQure/monomer-database-datasets/releases/latest)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21684533-1682D4)](https://doi.org/10.5281/zenodo.21684533)
![Monomers](https://img.shields.io/badge/monomers-2488-2e6e8e)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/deed.en)

The monomer database is a curated, openly-licensed database of 2,488 peptide monomers; canonical and non-canonical amino-acid backbones (α/β/γ/δ/ε), N-/C-terminal caps, and side-chain modifications with physicochemical properties (MW, cLogP, tPSA), usage/availability signals, and structure identifiers (SMILES, InChIKey), for peptide and macrocycle design.

This repository contains versioned output formats for the monomer database. The files are generated from the authoritative [`monomer-database-source`](https://github.com/ProteinQure/monomer-database-source) repository and are available for download and archival through [Zenodo]((https://doi.org/10.5281/zenodo.21684533)). [ProteinQure](https://proteinqure.com) is identified as the organizational creator; see [ZENODO.md](ZENODO.md).

## Download and verify

For reproducible work, use a tagged GitHub release or its corresponding Zenodo
version rather than `main`. Generated artifacts are kept under `data/` so they
remain separate from repository administration and documentation. Each release
contains:

- `data/monomers.json` — the generated structured representation for that
  version;
- `data/monomers.csv` — a deterministic tabular conversion;
- `data/monomers.tsv` — the equivalent tab-separated conversion;
- `data/monomers.sdf` — an SD file containing 2D structures and all JSON
  fields as molecule properties;
- `data/monomers.schema.json` — the JSON Schema for the structured data; and
- `data/SHA256SUMS` — checksums for all five dataset artifacts.

After downloading all six files, checksums can be verified without additional
software:

```shell
cd data
sha256sum --check SHA256SUMS
```

JSON records have a consistent set of fields. Tabular columns follow the key
order of the first JSON record. UTF-8 text and LF line endings are used
throughout.

For full validation, place the six files under `data/` in a checkout of this
repository and run `uv run scripts/verify_release.py data`. The verifier
reconstructs CSV, TSV, and SDF from the JSON source, compares their bytes,
validates the JSON Schema, and verifies `SHA256SUMS`. Its dependencies are
declared in inline PEP 723 metadata. Run its tests with
`uv run scripts/run_tests.py`.

## Provenance and versioning

Every datasets release is created from the identically tagged source release.
For example, datasets tag `v0.0.1` is derived from source tag `v0.0.1`.
The source workflow performs the conversion; this repository independently
reconstructs each generated output format, compares it byte-for-byte, verifies
the checksums, and then creates the datasets GitHub release.

`main` may advance after a release. A tag, GitHub release, or version-specific
Zenodo DOI identifies an immutable snapshot.

The latest archived dataset is available from the
[Zenodo record for all versions](https://doi.org/10.5281/zenodo.21684533).
Version `v1.0.0` is permanently available at
[doi:10.5281/zenodo.21684534](https://doi.org/10.5281/zenodo.21684534).

## Corrections and contributions

Do not directly edit generated files or propose data changes in this
repository. Report problems and propose data, schema, tooling, or documentation
changes in
[`ProteinQure/monomer-database-source`](https://github.com/ProteinQure/monomer-database-source).
Include the affected record identifiers and version or DOI. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Citation and licenses

When using version `v1.0.0`, cite the archived dataset:

> ProteinQure. (2026). *Monomer database datasets* (Version v1.0.0)
> [Dataset]. Zenodo.
> https://doi.org/10.5281/zenodo.21684534

For another version, use the citation and version-specific DOI on its Zenodo
record. GitHub-readable citation metadata is provided in
[`CITATION.cff`](CITATION.cff), and the authoritative data source is the
[`monomer-database-source`](https://github.com/ProteinQure/monomer-database-source)
repository.

The dataset, schema, and documentation are licensed under
[Creative Commons Attribution-ShareAlike 4.0 International](LICENSE).
The requested attribution name is **ProteinQure**.
Repository automation is licensed under the
[GNU Affero General Public License v3.0 or later](LICENSE-CODE).
Repository-side Zenodo and GitHub citation metadata are described in
[ZENODO.md](ZENODO.md).
