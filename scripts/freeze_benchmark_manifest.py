"""Validate and freeze the private benchmark manifest with a SHA-256 sidecar."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from sautiform.benchmark.manifest import load_validated_manifest


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    rows = load_validated_manifest(args.manifest, check_audio=True)
    digest = _sha256(args.manifest)
    sidecar = args.manifest.with_suffix(args.manifest.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {args.manifest.name}\n", encoding="utf-8")

    print(f"BENCHMARK_MANIFEST_FROZEN=YES rows={len(rows)}")
    print(f"BENCHMARK_MANIFEST_SHA256={digest}")
    print(f"BENCHMARK_MANIFEST_SHA256_FILE={sidecar}")


if __name__ == "__main__":
    main()
