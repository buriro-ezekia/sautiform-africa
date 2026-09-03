"""Run one validated manifest across the four challenge ASR backends."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sautiform.asr.factory import CHALLENGE_BACKENDS, build_backend
from sautiform.benchmark.integrity import verify_sha256
from sautiform.benchmark.manifest import load_validated_manifest
from sautiform.benchmark.runner import run_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--backends",
        nargs="+",
        choices=CHALLENGE_BACKENDS,
        default=list(CHALLENGE_BACKENDS),
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Record a backend failure and continue with the remaining models.",
    )
    parser.add_argument(
        "--expected-manifest-sha256",
        help=(
            "Fail before model loading if the manifest does not match this "
            "frozen SHA-256 digest."
        ),
    )
    args = parser.parse_args()

    if args.expected_manifest_sha256:
        digest = verify_sha256(args.manifest, args.expected_manifest_sha256)
        print(f"MANIFEST_SHA256_VERIFIED={digest}")

    rows = load_validated_manifest(args.manifest, check_audio=True)
    reports: dict[str, object] = {}
    failures: dict[str, str] = {}
    for name in args.backends:
        try:
            reports[name] = run_rows(rows, build_backend(name))
        except Exception as exc:
            if not args.continue_on_error:
                raise
            failures[name] = f"{type(exc).__name__}: {exc}"

    payload = {"reports": reports, "failures": failures}
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"completed": list(reports), "failed": failures},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
