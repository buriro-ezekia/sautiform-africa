# Omnilingual ASR Local Setup

## Supported local runtime

The final Omnilingual comparator is `omniASR_CTC_300M_v2` using
`omnilingual-asr==0.2.0`.

For the reproducible local evaluation path, use:

```text
OS: Linux or WSL2
Python: 3.10 or 3.11
Package: omnilingual-asr==0.2.0
Model card: omniASR_CTC_300M_v2
```

Do not use native Windows. Omnilingual depends on `fairseq2`, whose native `fairseq2n`
component does not publish Windows wheels.

Do not use a normal Python 3.12 patch release with the pinned PyPI package. The published
`omnilingual-asr 0.2.0` metadata declares `Python <=3.12`, which causes versions such as
Python 3.12.10 to be rejected by pip. Python 3.10 or 3.11 avoids that metadata edge case.

## WSL2 setup from the Windows repository

Open WSL and move to the existing repository:

```bash
cd "/mnt/d/DESKTOP/Buriro/GitHub Desktop/SautiForm Africa/sautiform-africa"
```

Ubuntu 24.04 ships Python 3.12 by default and may not provide Python 3.11 in the enabled APT
repositories. Use Astral `uv` to install and manage a compatible Python 3.11 interpreter without
changing the system Python:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"

uv --version
uv python install 3.11

mkdir -p ~/.venvs
uv venv --python 3.11 ~/.venvs/sautiform-omni311
source ~/.venvs/sautiform-omni311/bin/activate

python --version
python -m pip install --upgrade pip
python -m pip install -e ".[dev,omni]"
python scripts/check_omni_ready.py
```

The managed interpreter remains isolated from Ubuntu's system Python and from the Windows virtual
environment used for Whisper and MMS.

The required readiness markers are:

```text
OMNI_RUNTIME_COMPATIBLE=YES platform=Linux python=3.11
OMNI_PACKAGE_IMPORT=PASS version=0.2.0
```

or the equivalent Python 3.10 marker.

## Model-load gate

After package readiness passes:

```bash
export OMNIASR_MODEL_CARD=omniASR_CTC_300M_v2

python -c "from sautiform.asr.omni import OmniASRBackend; b=OmniASRBackend(); print('OMNI_MODEL_LOAD=PASS'); print('OMNI_MODEL_CARD=' + b.model_card)"
```

Do not run held-out inference until the model-load gate succeeds.

## Frozen benchmark

The final held-out manifest remains on the mounted Windows repository and can be accessed from WSL
using the same repository-relative path:

```text
data/private/heldout/benchmark_manifest.jsonl
```

Its authoritative SHA-256 remains:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

Every final Omnilingual run must verify this digest before model loading.
