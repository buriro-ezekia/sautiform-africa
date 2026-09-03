"""Runtime compatibility checks for Meta Omnilingual ASR."""
from __future__ import annotations


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
