#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "jsonschema>=4.18,<5",
#   "rdkit==2026.3.4",
# ]
# ///
"""Run the datasets repository's complete test suite with managed dependencies."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


def main() -> int:
    repository_root = Path(__file__).parents[1]
    suite = unittest.defaultTestLoader.discover(str(repository_root / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
