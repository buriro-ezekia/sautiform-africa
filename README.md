# SautiForm Africa

SautiForm Africa is a code-switching voice assistant for public-service form completion. It is designed around a narrow, auditable workflow: a citizen or field officer speaks naturally in mixed Kiswahili and English, the speech-recognition layer returns a transcript, the application extracts structured fields, identifies missing or ambiguous information, asks for clarification, validates the record and requires explicit confirmation before any submission step.

The project is being developed for the Sahara CodeSwitch Africa Challenge under **Legal & Public Services**. The prototype deliberately separates speech recognition from downstream form logic so that the same audio can be benchmarked fairly across Sahara and other ASR systems.

## Why this is an agentic voice application

SautiForm does more than transcribe speech. A transcript drives a structured action:

`audio -> ASR -> field extraction -> validation -> clarification -> read-back -> confirmation`

The initial public-service form captures:

- district;
- occupation;
- household size;
- service request.

No record is considered ready until required fields are present and the user confirms the read-back.

## Benchmark design

The main-challenge implementation is designed for four ASR backends:

1. Intron Sahara v2.5;
2. OpenAI Whisper;
3. Meta MMS;
4. a configurable fourth backend through the generic HTTP adapter.

The benchmark reports both transcription and task-level measures:

- word error rate (WER);
- character error rate (CER);
- field exact-match accuracy;
- complete-form accuracy.

Task-level metrics matter because two transcripts with similar WER can lead to very different downstream form quality.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m sautiform.cli demo --text "Ninaishi Mbozi District, occupation yangu ni farmer, household ina watu sita, nataka birth certificate."
```

Expected workflow: the parser extracts the available fields, reports anything missing, then produces a confirmation prompt rather than silently submitting data.

## Voice input

A real audio file can be transcribed through an enabled backend. Sahara credentials and endpoint details are supplied through environment variables rather than committed to the repository.

```bash
export SAHARA_API_URL="https://..."
export SAHARA_API_KEY="..."
python -m sautiform.cli transcribe --backend sahara --audio path/to/audio.wav
```

The Sahara adapter uses a deliberately configurable request contract because participant API details may differ during the research-preview period. Set `SAHARA_FILE_FIELD`, `SAHARA_MODEL`, and `SAHARA_RESPONSE_TEXT_PATH` if the onboarding contract requires them.

## Benchmark manifest

See `examples/benchmark_manifest.jsonl`. Each line contains an audio path, a reference transcript and reference fields. Run:

```bash
python scripts/run_benchmark.py \
  --manifest examples/benchmark_manifest.jsonl \
  --backend mock \
  --output benchmark_results.json
```

The `mock` backend exists only for deterministic local tests; it must not be reported as a competition result.

## Responsible use

SautiForm follows five baseline safeguards:

- obtain consent before recording or retaining voice data;
- minimise collection and avoid unnecessary personal data;
- never infer a required field when speech is ambiguous;
- require human confirmation before submission;
- report benchmark limitations by language pair, accent, device and noise condition.

See `docs/RESPONSIBLE_AI.md` for the submission-ready responsible-use framework.

## Repository status

Version `0.1.0` is the Phase 1 challenge foundation: deterministic form logic, ASR interfaces, benchmarking metrics, CLI workflow, tests and CI. Live Sahara benchmarking requires participant API credentials and consented benchmark audio, neither of which is stored in this repository.
