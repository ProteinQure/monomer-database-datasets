# GitHub–Zenodo publication notes

Zenodo should archive this generated datasets repository, not the source
repository. This keeps each archived record limited to the released monomer
files, checksums, documentation, and metadata.

## Active metadata

The repository contains two active metadata files:

- `.zenodo.json` declares the upload as an open dataset, identifies ProteinQure
  as the organizational creator, applies CC BY-SA 4.0, supplies the title,
  description, English language, keywords, and related source repository.
- `CITATION.cff` enables GitHub's citation interface and identifies ProteinQure
  as the organizational author. It identifies the latest archived release,
  `v1.0.0`, with its version-specific DOI and publication date.

Zenodo gives `.zenodo.json` precedence when both files exist. Do not hard-code
a release version in `.zenodo.json`; the GitHub release tag supplies it.

Validate the JSON locally:

```shell
python -m json.tool .zenodo.json >/dev/null
```

Validate `CITATION.cff` with a current Citation File Format validator. Inspect
Zenodo's generated record metadata before announcing the release.

Contributors and roles, funding/grant identifiers, related publication DOIs,
and a Zenodo community are currently omitted. Add them later if applicable;
do not infer them from Git commit history.

## DOI records

Zenodo assigned `10.5281/zenodo.21684534` to the immutable `v1.0.0` release and
`10.5281/zenodo.21684533` as the concept DOI representing all versions. The
badge in `README.md` links to the concept DOI, while the preferred citation and
`CITATION.cff` use the version-specific DOI.

For a future release, update the preferred citation and release fields in
`CITATION.cff` to the new version-specific Zenodo record. Do not rewrite or
retarget an existing release tag.
