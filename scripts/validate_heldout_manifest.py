"""Validate the fixed 24-row held-out benchmark before freezing."""
from __future__ import annotations

import argparse
from pathlib import Path

from sautiform.benchmark.heldout import validate_heldout_rows
from sautiform.benchmark.manifest import load_validated_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/private/heldout/benchmark_manifest.jsonl"),
    )
    args = parser.parse_args()

    rows = load_validated_manifest(args.manifest, check_audio=True)
    errors = validate_heldout_rows(rows)
    if errors:
        for error in errors:
            print(f"HELDOUT_ERROR={error}")
        raise SystemExit(1)

    print(f"HELDOUT_MANIFEST_VALID=YES rows={len(rows)}")
    print("HELDOUT_DEVELOPMENT_LEAKAGE=NO")
    print("HELDOUT_READY_TO_FREEZE=YES")


if __name__ == "__main__":
    main()
