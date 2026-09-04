"""Check local prerequisites for the first real Whisper smoke test."""
from __future__ import annotations

import shutil
import sys


def main() -> None:
    try:
        import whisper  # noqa: F401
    except ImportError:
        print("WHISPER_IMPORT=FAIL")
        print('Install with: python -m pip install -e ".[whisper]"')
        raise SystemExit(1) from None

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        print("WHISPER_IMPORT=PASS")
        print("WHISPER_FFMPEG=FAIL")
        print("Install FFmpeg and ensure ffmpeg.exe is on PATH.")
        raise SystemExit(1)

    print("WHISPER_IMPORT=PASS")
    print(f"WHISPER_FFMPEG=PASS path={ffmpeg}")
    print(f"WHISPER_READY=PASS python={sys.executable}")


if __name__ == "__main__":
    main()
