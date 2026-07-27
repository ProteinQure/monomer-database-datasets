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
  as the organizational author.

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

## After the first archive

Zenodo assigns a DOI to the specific release and a concept DOI representing all
versions. Add the DOI badge supplied by Zenodo near the top of `README.md`,
linked to the concept DOI landing page. Put the version-specific DOI in the
preferred citation for that release. Update links without rewriting or
retargeting an existing release tag.
