"""Validate benchmark schema, consent, references and optional audio paths."""
from __future__ import annotations

import argparse
from pathlib import Path

from sautiform.benchmark.manifest import load_validated_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Validate schema and consent without requiring audio files.",
    )
    args = parser.parse_args()
    rows = load_validated_manifest(
        args.manifest,
        check_audio=not args.metadata_only,
    )
    print(f"BENCHMARK_MANIFEST_VALID=YES rows={len(rows)}")


if __name__ == "__main__":
    main()
