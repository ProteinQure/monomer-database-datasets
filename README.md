# Monomer database datasets

This repository contains versioned output formats for the monomer database.
The files are generated from the authoritative
[`monomer-database-source`](https://github.com/ProteinQure/monomer-database-source)
repository and are intended for download and Zenodo archival.

The bootstrap commit intentionally contains no generated dataset. Publishing
the source repository's initial `v0.0.1` release will create this repository's
second commit and first tagged release, containing the 20 canonical amino
acids. ProteinQure is identified as the organizational creator; see
[ZENODO.md](ZENODO.md).

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

## Corrections and contributions

Do not directly edit generated files or propose data changes in this
repository. Report problems and propose data, schema, tooling, or documentation
changes in
[`ProteinQure/monomer-database-source`](https://github.com/ProteinQure/monomer-database-source).
Include the affected record identifiers and version or DOI. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Citation and licenses

ProteinQure is the organizational creator in `CITATION.cff` and
`.zenodo.json`. Once the first Zenodo archive exists, this section should
contain:

1. the preferred dataset citation using the version-specific DOI;
2. a Zenodo DOI badge linked to the concept DOI landing page; and
3. links to both the latest Zenodo record and the source repository.

The dataset, schema, and documentation are licensed under
[Creative Commons Attribution-ShareAlike 4.0 International](LICENSE).
The requested attribution name is **ProteinQure**.
Repository automation is licensed under the
[GNU Affero General Public License v3.0 or later](LICENSE-CODE).
Repository-side Zenodo and GitHub citation metadata are described in
[ZENODO.md](ZENODO.md).
