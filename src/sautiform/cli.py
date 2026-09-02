"""Command-line interface for SautiForm Africa."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sautiform.asr.factory import SUPPORTED_BACKENDS, build_backend
from sautiform.audio import validate_audio_path
from sautiform.dialogue.engine import next_prompt
from sautiform.forms.extraction import extract_form


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sautiform")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser(
        "demo",
        help="Run downstream form logic from a transcript",
    )
    demo.add_argument("--text", required=True)

    transcribe = sub.add_parser("transcribe", help="Transcribe an audio file")
    transcribe.add_argument(
        "--backend",
        choices=SUPPORTED_BACKENDS,
        required=True,
    )
    transcribe.add_argument("--audio", type=Path, required=True)
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command == "demo":
        form = extract_form(args.text)
        print(json.dumps(form.to_dict(), ensure_ascii=False, indent=2))
        print(next_prompt(form))
        return

    audio_path = validate_audio_path(args.audio)
    backend = build_backend(args.backend)
    result = backend.transcribe(audio_path)
    form = extract_form(result.text)
    print(result.text)
    print(json.dumps(form.to_dict(), ensure_ascii=False, indent=2))
    print(next_prompt(form))


if __name__ == "__main__":
    main()
