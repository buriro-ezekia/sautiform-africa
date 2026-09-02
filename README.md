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

## Local development

Python 3.12 is recommended for the full Phase 2 environment.

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
streamlit run app.py
```

The interface supports microphone input when a configured ASR backend is available. It also accepts
a transcript directly, which allows the downstream workflow and confirmation gate to be tested
without downloading a speech model.

## Speech backends

Install backends separately rather than downloading every model at once:

```powershell
python -m pip install -e ".[whisper]"
python -m pip install -e ".[mms]"
python -m pip install -e ".[omni]"
```

Sahara uses participant credentials supplied through environment variables. Copy `.env.example`
only as a configuration reference; do not commit a populated `.env` file.

```text
SAHARA_API_URL=...
SAHARA_API_KEY=...
```

The request and response fields remain configurable because the participant onboarding contract is
the authority for the actual Sahara API shape. See `docs/SAHARA_SETUP.md`.

## Private benchmark collection

The repository includes a local-only collection path that keeps raw recordings and the working
manifest outside version control. Start with one consented clip, validate it, and run Whisper before
collecting the larger pilot set.

```powershell
python scripts/add_benchmark_sample.py --help
python scripts/check_whisper_ready.py
```

See `docs/BENCHMARK_COLLECTION_PROTOCOL.md` for the reference-first collection procedure, the first
smoke-test utterance, manifest freezing and the exact Whisper command.

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

Version `0.2.0` is the Phase 2 candidate. It adds the named four-model benchmark architecture,
consent-aware manifest validation, audio safeguards, an interactive voice/form interface and local
benchmark orchestration. Real benchmark scores remain intentionally absent until Sahara credentials
and a consented evaluation audio set are available.
