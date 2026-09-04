#!/usr/bin/env bash
# Purpose: replace a CUDA fairseq2n wheel with the matching CPU variant in WSL/Linux.
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "OMNI_CPU_VARIANT_REPAIR=FAIL reason=linux_required"
    exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "OMNI_CPU_VARIANT_REPAIR=FAIL reason=uv_not_found"
    exit 1
fi

TORCH_BASE="$(python - <<'PY'
from importlib.metadata import version
print(version("torch").split("+", 1)[0])
PY
)"

FAIRSEQ2N_VERSION="$(python - <<'PY'
from importlib.metadata import version
print(version("fairseq2n"))
PY
)"

FAIRSEQ2_VERSION="$(python - <<'PY'
from importlib.metadata import version
print(version("fairseq2"))
PY
)"

CPU_INDEX="https://fair.pkg.atmeta.com/fairseq2/whl/pt${TORCH_BASE}/cpu"

echo "OMNI_TORCH_BASE=${TORCH_BASE}"
echo "OMNI_FAIRSEQ2_VERSION=${FAIRSEQ2_VERSION}"
echo "OMNI_FAIRSEQ2N_VERSION=${FAIRSEQ2N_VERSION}"
echo "OMNI_FAIRSEQ2_CPU_INDEX=${CPU_INDEX}"

uv pip install \
  --reinstall \
  --no-deps \
  --index-url "${CPU_INDEX}" \
  "fairseq2n==${FAIRSEQ2N_VERSION}"

python - <<'PY'
import torch
import fairseq2n

print(f"TORCH_VERSION={torch.__version__}")
print(f"CUDA_AVAILABLE={torch.cuda.is_available()}")
print(f"FAIRSEQ2N_VERSION={fairseq2n.__version__}")
print(f"FAIRSEQ2N_TORCH_VERSION={fairseq2n.torch_version()}")
print(f"FAIRSEQ2N_TORCH_VARIANT={fairseq2n.torch_variant()}")
if torch.cuda.is_available():
    raise SystemExit("OMNI_CPU_VARIANT_REPAIR=FAIL reason=torch_cuda_enabled")
if fairseq2n.torch_variant() != "CPU-only":
    raise SystemExit("OMNI_CPU_VARIANT_REPAIR=FAIL reason=fairseq2n_not_cpu")
print("OMNI_CPU_VARIANT_REPAIR=PASS")
PY
