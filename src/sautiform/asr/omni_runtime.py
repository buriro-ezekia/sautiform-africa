"""Runtime compatibility checks for Meta Omnilingual ASR."""
from __future__ import annotations

FAIRSEQ2_CPU_VARIANT_HINT = (
    "fairseq2n variant mismatch: install the CPU fairseq2n wheel that exactly "
    "matches the installed PyTorch version; run "
    "bash scripts/repair_omni_cpu_variant.sh"
)


def omni_runtime_error(
    *,
    platform_name: str,
    python_version: tuple[int, int],
) -> str | None:
    """Return a human-readable incompatibility reason, or None when supported."""
    if platform_name == "Windows":
        return (
            "native Windows is unsupported because fairseq2n publishes no Windows wheel; "
            "use WSL2/Linux"
        )

    if python_version not in {(3, 10), (3, 11)}:
        major, minor = python_version
        return (
            f"Python {major}.{minor} is unsupported for the pinned omnilingual-asr 0.2.0 "
            "runtime; use Python 3.10 or 3.11"
        )

    return None


def omni_import_error_hint(message: str) -> str | None:
    """Return a repair hint for known Omnilingual import failures."""
    lowered = message.lower()
    if (
        "fairseq2 requires a cuda" in lowered
        and "cpu-only build of pytorch" in lowered
    ):
        return FAIRSEQ2_CPU_VARIANT_HINT
    return None
