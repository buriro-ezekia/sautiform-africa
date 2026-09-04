"""Check runtime and package readiness for Meta Omnilingual ASR."""
from __future__ import annotations

import platform
import sys

from sautiform.asr.omni_runtime import (
    omni_import_error_hint,
    omni_runtime_error,
)


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
    except Exception as exc:
        hint = omni_import_error_hint(str(exc))
        detail = f"; {hint}" if hint else ""
        raise SystemExit(
            "OMNI_PACKAGE_IMPORT=FAIL "
            f"error={type(exc).__name__}: {exc}{detail}"
        ) from exc

    package_version = getattr(omnilingual_asr, "__version__", "unknown")
    print(
        "OMNI_RUNTIME_COMPATIBLE=YES "
        f"platform={system} python={version[0]}.{version[1]}"
    )
    print(f"OMNI_PACKAGE_IMPORT=PASS version={package_version}")


if __name__ == "__main__":
    main()
