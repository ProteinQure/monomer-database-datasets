from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIRECTORY = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

from verify_release import (  # noqa: E402
    ARTIFACT_FILENAMES,
    expected_tabular_output,
    verify_release,
    write_expected_sdf,
)


class ReleaseVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory_context = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory_context.name)
        self.records = [
            {
                "PQ_SYMBOL": "A",
                "SMILES": "N[C@@H](C)C(=O)O",
                "VALUE": 1.5,
                "ENABLED": True,
                "NOTE": None,
            },
            {
                "PQ_SYMBOL": "G",
                "SMILES": "NCC(=O)O",
                "VALUE": 2,
                "ENABLED": False,
                "NOTE": "example",
            },
        ]
        self._write_valid_release()

    def tearDown(self) -> None:
        self.temporary_directory_context.cleanup()

    def _write_valid_release(self) -> None:
        (self.directory / "monomers.json").write_text(
            json.dumps(self.records, indent=2) + "\n",
            encoding="utf-8",
        )
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": list(self.records[0]),
                "properties": {
                    "PQ_SYMBOL": {"type": "string"},
                    "SMILES": {"type": "string"},
                    "VALUE": {"type": "number"},
                    "ENABLED": {"type": "boolean"},
                    "NOTE": {"type": ["string", "null"]},
                },
            },
        }
        (self.directory / "monomers.schema.json").write_text(
            json.dumps(schema, indent=2) + "\n",
            encoding="utf-8",
        )
        (self.directory / "monomers.csv").write_text(
            expected_tabular_output(self.records, ","),
            encoding="utf-8",
        )
        (self.directory / "monomers.tsv").write_text(
            expected_tabular_output(self.records, "\t"),
            encoding="utf-8",
        )
        write_expected_sdf(self.records, self.directory / "monomers.sdf")

        checksum_lines = []
        for filename in ARTIFACT_FILENAMES:
            digest = hashlib.sha256((self.directory / filename).read_bytes()).hexdigest()
            checksum_lines.append(f"{digest}  {filename}\n")
        (self.directory / "SHA256SUMS").write_text(
            "".join(checksum_lines),
            encoding="utf-8",
        )

    def test_valid_release_passes(self) -> None:
        verify_release(self.directory)

    def test_changed_tabular_data_is_rejected(self) -> None:
        (self.directory / "monomers.csv").write_text(
            "PQ_SYMBOL,SMILES,VALUE,ENABLED,NOTE\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "monomers.csv does not exactly match"):
            verify_release(self.directory)

    def test_changed_sdf_data_is_rejected(self) -> None:
        sdf_path = self.directory / "monomers.sdf"
        sdf_path.write_bytes(sdf_path.read_bytes().replace(b">  <VALUE>", b">  <OTHER>", 1))

        with self.assertRaisesRegex(ValueError, "monomers.sdf does not exactly match"):
            verify_release(self.directory)

    def test_changed_checksum_manifest_is_rejected(self) -> None:
        (self.directory / "SHA256SUMS").write_text("", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "SHA256SUMS"):
            verify_release(self.directory)


if __name__ == "__main__":
    unittest.main()
