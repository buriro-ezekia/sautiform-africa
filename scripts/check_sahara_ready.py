"""Validate Sahara configuration and optionally smoke-test development audio."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from sautiform.asr.sahara import SaharaBackend

HELDOUT_ID = re.compile(r"tz-sw-en-h\d{3}", re.IGNORECASE)


def _reject_heldout(path: Path) -> None:
    normalised = path.as_posix().lower()
    if "data/private/heldout/" in normalised or HELDOUT_ID.search(path.stem):
        raise SystemExit(
            "SAHARA_SMOKE_TEST=BLOCKED reason=heldout_audio_not_allowed"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio",
        type=Path,
        help="Optional development audio clip for a single Sahara API smoke test.",
    )
    args = parser.parse_args()

    backend = SaharaBackend()

    print("SAHARA_CONFIG=PASS")
    print(f"SAHARA_FILE_FIELD={backend.file_field}")
    print(f"SAHARA_MODEL={backend.model or 'unspecified'}")
    print(f"SAHARA_MODEL_FIELD={backend.model_field}")
    print(f"SAHARA_RESPONSE_TEXT_PATH={backend.response_text_path}")
    print(f"SAHARA_AUTH_HEADER={backend.auth_header}")
    print(f"SAHARA_AUTH_SCHEME={backend.auth_scheme or 'none'}")
    print(f"SAHARA_TIMEOUT_SECONDS={backend.timeout_seconds:g}")

    if args.audio is None:
        return

    audio = args.audio.resolve()
    _reject_heldout(audio)

    if not audio.is_file():
        raise SystemExit(f"SAHARA_SMOKE_TEST=FAIL reason=audio_not_found path={audio}")

    result = backend.transcribe(audio)
    print("SAHARA_SMOKE_TEST=PASS")
    print(f"SAHARA_BACKEND={result.backend}")
    print(f"SAHARA_LATENCY_SECONDS={result.latency_seconds}")
    print(f"SAHARA_TRANSCRIPT={result.text}")


if __name__ == "__main__":
    main()
