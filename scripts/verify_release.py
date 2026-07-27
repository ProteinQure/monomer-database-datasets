#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "jsonschema>=4.18,<5",
#   "rdkit==2026.3.4",
# ]
# ///
"""Independently verify every generated monomer release artifact."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from rdkit import Chem
from rdkit.Chem import rdDepictor

ARTIFACT_FILENAMES = (
    "monomers.json",
    "monomers.csv",
    "monomers.tsv",
    "monomers.sdf",
    "monomers.schema.json",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_records(path: Path) -> list[dict[str, Any]]:
    records = load_json(path)
    if not isinstance(records, list) or not records:
        raise ValueError("monomers.json must be a non-empty array")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("every JSON record must be an object")

    expected_fields = set(records[0])
    for index, record in enumerate(records, start=1):
        if set(record) != expected_fields:
            raise ValueError(f"JSON record {index} has inconsistent fields")
    return records


def delimited_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def expected_tabular_output(
    records: list[dict[str, Any]], delimiter: str
) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=list(records[0]),
        delimiter=delimiter,
        lineterminator="\n",
    )
    writer.writeheader()
    for record in records:
        writer.writerow({key: delimited_value(value) for key, value in record.items()})
    return output.getvalue()


def sdf_property_value(value: Any) -> str:
    return str(delimited_value(value))


def write_expected_sdf(records: list[dict[str, Any]], path: Path) -> None:
    molecules = []
    for index, record in enumerate(records, start=1):
        molecule = Chem.MolFromSmiles(record.get("SMILES", ""))
        if molecule is None:
            raise ValueError(f"JSON record {index} has an invalid SMILES value")
        rdDepictor.Compute2DCoords(molecule, canonOrient=True)
        title = str(record.get("PQ_SYMBOL") or "")
        molecule.SetProp("_Name", title)
        molecule.SetProp("rName", title)
        for field, value in record.items():
            molecule.SetProp(field, sdf_property_value(value))
        molecules.append(molecule)

    with Chem.SDWriter(str(path)) as writer:
        for molecule in molecules:
            writer.write(molecule)


def validate_schema(records: list[dict[str, Any]], schema_path: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(records))
    if errors:
        raise ValueError(f"monomers.json does not match its schema: {errors[0].message}")


def verify_checksums(directory: Path) -> None:
    expected_lines = []
    for filename in ARTIFACT_FILENAMES:
        digest = hashlib.sha256((directory / filename).read_bytes()).hexdigest()
        expected_lines.append(f"{digest}  {filename}\n")
    actual = (directory / "SHA256SUMS").read_text(encoding="utf-8")
    if actual != "".join(expected_lines):
        raise ValueError("SHA256SUMS does not exactly match the release artifacts")


def verify_release(directory: Path) -> None:
    records = load_records(directory / "monomers.json")
    validate_schema(records, directory / "monomers.schema.json")

    for filename, delimiter in (("monomers.csv", ","), ("monomers.tsv", "\t")):
        actual = (directory / filename).read_text(encoding="utf-8")
        if actual != expected_tabular_output(records, delimiter):
            raise ValueError(
                f"{filename} does not exactly match the deterministic JSON conversion"
            )

    with tempfile.TemporaryDirectory() as temporary_directory:
        expected_sdf = Path(temporary_directory) / "monomers.sdf"
        write_expected_sdf(records, expected_sdf)
        if (directory / "monomers.sdf").read_bytes() != expected_sdf.read_bytes():
            raise ValueError(
                "monomers.sdf does not exactly match the deterministic JSON conversion"
            )

    verify_checksums(directory)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.cwd() / "data",
        help="release artifact directory (default: ./data)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        verify_release(args.directory)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"release verification failed: {error}") from error
    print(f"verified release artifacts in {args.directory}")
