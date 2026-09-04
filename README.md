# SautiForm Africa

SautiForm Africa is a code-switching voice assistant for public-service form completion. A citizen
or field officer can speak naturally in mixed Kiswahili and English, after which the application
transcribes the audio, extracts structured fields, identifies missing information, validates the
record and requires explicit human confirmation before any submission step.

The project is being developed for the Sahara CodeSwitch Africa Challenge under **Legal & Public
Services**. Speech recognition is intentionally separated from downstream form logic so that the
same consented audio can be benchmarked fairly across multiple ASR systems.

## Application workflow

```text
audio
  -> ASR
  -> transcript
  -> structured field extraction
  -> validation
  -> clarification when required
  -> editable read-back
  -> explicit user confirmation
```

The Phase 2 prototype captures four required fields: district, occupation, household size and
service request. It does not automatically submit records to a government system.

## Four-model challenge benchmark

The challenge matrix is explicit and reproducible:

1. Intron Sahara v2.5;
2. OpenAI Whisper;
3. Meta MMS;
4. Meta Omnilingual ASR (`omniASR_CTC_300M_v2` by default).

A generic HTTP adapter remains available for experiments, but it is not one of the four named
challenge backends.

Every model is evaluated on the same benchmark rows using:

- word error rate (WER);
- character error rate (CER);
- field exact-match accuracy;
- complete-form accuracy;
- mean transcription latency where available.

Complete-form accuracy is the primary downstream task metric. WER and CER remain useful diagnostic
measures, but transcription quality alone does not establish that a public-service record was
completed correctly.

## Challenge submission package

The written submission package is indexed in
[`docs/SUBMISSION_INDEX.md`](docs/SUBMISSION_INDEX.md). It includes the polished Solution
Description, four-model Benchmark Report, Ethics & Inclusion Note, demo-video script and final
submission checklist.

The benchmark is complete: Sahara, Whisper, MMS and Omnilingual were evaluated on the identical
frozen 24-clip held-out manifest. No further parser or model tuning is permitted from those results.

## Local development

Python 3.12 remains suitable for the core application, Whisper and MMS. Meta Omnilingual ASR is evaluated separately under WSL2/Linux with Python 3.10 or 3.11 because its published 0.2.0 package metadata rejects normal Python 3.12 patch releases and its `fairseq2n` dependency does not publish native Windows wheels.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
ruff check .
pytest -q
```

The deterministic form workflow can be tested without installing any large speech model:

```powershell
$demoText = "Ninaishi Mbozi District, occupation yangu ni farmer, " + `
  "household ina watu sita, nataka birth certificate."
python -m sautiform.cli demo --text $demoText
```

## Interactive prototype

Install the lightweight demo dependency and start Streamlit:

```powershell
python -m pip install -e ".[demo]"
$env:SAHARA_API_KEY = "<PRIVATE_INTRON_API_KEY>"
streamlit run app.py
```

The competition product path is fixed to **Intron Sahara v2.5** for live Swahili-English speech.
Whisper, MMS and Omnilingual remain benchmark comparators rather than selectable demo backends. A
developer transcript fallback is retained only for testing the downstream form workflow without an
API call.

## Speech backends

Install backends separately rather than downloading every model at once:

```powershell
python -m pip install -e ".[whisper]"
python -m pip install -e ".[mms]"
# Omnilingual ASR: use WSL2/Linux with Python 3.10 or 3.11.
# CPU runs also require the matching fairseq2n CPU variant.
# See docs/OMNILINGUAL_SETUP.md
```

Sahara uses the official Intron Voice synchronous STT endpoint. Only the private participant API key
must be supplied locally; it must never be committed.

```text
SAHARA_API_KEY=...
SAHARA_API_URL=https://infer.voice.intron.io/file/v1/upload/sync
SAHARA_LANGUAGE=sw
SAHARA_DISABLE_LLM_CORRECTIONS=TRUE
SAHARA_RESPONSE_TEXT_PATH=data.audio_transcript
```

See `docs/SAHARA_SETUP.md` for the locked challenge configuration and development-only smoke-test
boundary.

## Private benchmark collection

The repository includes a local-only collection path that keeps raw recordings and the working
manifest outside version control. Start with one consented clip, validate it, and run Whisper before
collecting the larger pilot set.

```powershell
python scripts/add_benchmark_sample.py --help
python scripts/check_whisper_ready.py
```

See `docs/BENCHMARK_COLLECTION_PROTOCOL.md` for the reference-first collection procedure, manifest
freezing and the exact Whisper command. `docs/DEVELOPMENT_LOCK.md` records the locked development
configuration and the boundary between development and held-out evaluation. The fixed 24-clip final
design is in `docs/HELDOUT_COLLECTION_PLAN.md`; `scripts/ingest_heldout_plan.py` provides a guarded
batch-ingestion path that performs no ASR inference. `docs/HELDOUT_FREEZE.md` records the frozen
24-row manifest identity and the SHA-256 guard required for every final model run. Aggregate final
held-out results are recorded in `docs/FINAL_HELDOUT_EVALUATION.md`; private audio and per-clip
held-out transcripts remain outside version control. `docs/OMNILINGUAL_SETUP.md` documents the separate WSL2/Linux runtime required for the Omnilingual comparator.

## Consent-aware benchmark manifest

Benchmark audio is deliberately excluded from the public repository. Each JSONL row contains a
unique sample identifier, an audio path, a reference transcript, reference form fields and metadata.
The metadata must explicitly record `consented: true` before a row is accepted.

Validate the example schema without requiring private audio to exist:

```powershell
python scripts/validate_manifest.py `
  --manifest examples/benchmark_manifest.jsonl `
  --metadata-only
```

When real consented audio is present under `data/private/`, remove `--metadata-only` so file format,
existence and size safeguards are also checked.

Run a single configured backend:

```powershell
python scripts/run_benchmark.py `
  --manifest data/private/benchmark_manifest.jsonl `
  --backend sahara `
  --output benchmark_results_sahara.json
```

Run the four-model matrix:

```powershell
python scripts/run_benchmark_matrix.py `
  --manifest data/private/benchmark_manifest.jsonl `
  --output benchmark_results_matrix.json `
  --continue-on-error
```

The matrix runner records model failures instead of fabricating results. The `mock` backend in the
single-model script exists only for deterministic software testing and must never be reported as a
competition benchmark result.

## Responsible use

SautiForm Africa is an assistive form-completion prototype, not a legal or administrative decision
system. Raw voice data should be collected only with informed consent and retained only when needed.
Missing fields are not guessed, users can correct extracted values, and confirmation is required
before a record is treated as complete.

See `docs/RESPONSIBLE_AI.md`, `docs/BENCHMARK_PROTOCOL.md` and
`docs/PHASE_2_SPECIFICATION.md` for the evaluation and safety assumptions.

## Repository status

Version `0.2.0` is the Phase 2 candidate. The 10-clip development pilot is locked and remains
strictly development-only. Whisper is locked to `turbo`, forced Swahili (`sw`) and temperature zero,
and the parser is frozen after its final bounded hardening pass. The final 24-clip held-out benchmark
is frozen, and Sahara, Whisper, MMS and Omnilingual ASR have all completed their final runs on the
identical manifest. Sahara achieved the lowest WER (0.4592) and mean latency (3.08 s), while Whisper
achieved the lowest CER (0.1660) and highest field exact-match score (0.3021). All four systems scored
0/24 on complete-form accuracy, reinforcing the need for clarification and explicit human
confirmation. The frozen held-out manifest SHA-256 is
`794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448`.
