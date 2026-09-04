"""Tests for Omnilingual ASR runtime compatibility."""
from sautiform.asr.omni_runtime import (
    FAIRSEQ2_CPU_VARIANT_HINT,
    omni_import_error_hint,
    omni_runtime_error,
)


def test_omni_accepts_linux_python_311():
    assert (
        omni_runtime_error(platform_name="Linux", python_version=(3, 11))
        is None
    )


def test_omni_accepts_linux_python_310():
    assert (
        omni_runtime_error(platform_name="Linux", python_version=(3, 10))
        is None
    )


def test_omni_rejects_native_windows():
    error = omni_runtime_error(
        platform_name="Windows",
        python_version=(3, 11),
    )
    assert error is not None
    assert "WSL2/Linux" in error


def test_omni_rejects_python_312_patch_line():
    error = omni_runtime_error(
        platform_name="Linux",
        python_version=(3, 12),
    )
    assert error is not None
    assert "Python 3.10 or 3.11" in error


def test_omni_identifies_cuda_fairseq2n_with_cpu_torch():
    message = (
        "fairseq2 requires a CUDA 12.8 build of PyTorch 2.8.0, "
        "but the installed version is a CPU-only build of PyTorch 2.8.0."
    )
    assert omni_import_error_hint(message) == FAIRSEQ2_CPU_VARIANT_HINT


def test_omni_leaves_unknown_import_error_unclassified():
    assert omni_import_error_hint("unrelated import failure") is None
