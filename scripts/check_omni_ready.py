"""Check runtime and package readiness for Meta Omnilingual ASR."""
from __future__ import annotations

import platform
import sys

from sautiform.asr.omni_runtime import omni_runtime_error


def main() -> None:
    system = platform.system()
    version = sys.version_info[:2]
    error = omni_runtime_error(
        platform_name=system,
        python_version=version,
    )
    if error:
        raise SystemExit(
            "OMNI_RUNTIME_COMPATIBLE=NO "
            f"platform={system} python={version[0]}.{version[1]}; {error}"
        )

    try:
        import omnilingual_asr
    except ImportError as exc:
        raise SystemExit(
            "OMNI_PACKAGE_IMPORT=FAIL; install with "
            'python -m pip install -e ".[omni]"'
        ) from exc

    package_version = getattr(omnilingual_asr, "__version__", "unknown")
    print(
        "OMNI_RUNTIME_COMPATIBLE=YES "
        f"platform={system} python={version[0]}.{version[1]}"
    )
    print(f"OMNI_PACKAGE_IMPORT=PASS version={package_version}")


if __name__ == "__main__":
    main()
