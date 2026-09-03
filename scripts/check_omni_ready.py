"""Check Python and package readiness for Meta Omnilingual ASR."""
from __future__ import annotations

import sys


def main() -> None:
    if not ((3, 10) <= sys.version_info[:2] <= (3, 12)):
        raise SystemExit(
            "OMNI_PYTHON_COMPATIBLE=NO "
            f"python={sys.version_info.major}.{sys.version_info.minor}; "
            "omnilingual-asr 0.2.0 requires Python 3.10-3.12"
        )

    try:
        import omnilingual_asr
    except ImportError as exc:
        raise SystemExit(
            "OMNI_PACKAGE_IMPORT=FAIL; install with python -m pip install -e \".[omni]\""
        ) from exc

    version = getattr(omnilingual_asr, "__version__", "unknown")
    print(
        "OMNI_PYTHON_COMPATIBLE=YES "
        f"python={sys.version_info.major}.{sys.version_info.minor}"
    )
    print(f"OMNI_PACKAGE_IMPORT=PASS version={version}")


if __name__ == "__main__":
    main()
