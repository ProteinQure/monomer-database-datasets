# Contributing

This is a generated release repository. Do not directly edit
`data/monomers.json`, `data/monomers.csv`, `data/monomers.tsv`,
`data/monomers.sdf`, `data/monomers.schema.json`, or `data/SHA256SUMS`, and do
not open pull requests that change the data here.

Report problems and propose data, schema, conversion, validation, or
documentation changes in
[`ProteinQure/monomer-database-source`](https://github.com/ProteinQure/monomer-database-source).
Include:

- the affected record identifiers;
- the GitHub tag or Zenodo DOI;
- the expected values or behavior; and
- supporting provenance or validation information.

Do not include confidential, personal, access-controlled, or third-party data
in a public issue.

Changes to repository verification code must keep dependencies in the
scripts' inline PEP 723 metadata and pass `uv run scripts/run_tests.py`.
