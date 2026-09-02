# Benchmark Collection Protocol

## Purpose

This protocol creates the private Kiswahili-English evaluation set used to test SautiForm Africa.
The benchmark must measure both speech-recognition quality and downstream form completion without
allowing model output to influence the reference answers.

## Privacy boundary

Raw audio, the working manifest and manifest hash are stored under `data/private/`. That directory
is excluded from Git. Do not place names, telephone numbers, identification numbers, precise home
addresses or other unnecessary personal data in benchmark utterances.

Only record your own voice or another speaker who has given informed consent for the stated
benchmark use. The ingestion script requires an explicit `--consented` flag and rejects the row
without it.

## Collection stages

Use three stages rather than recording the full benchmark immediately:

1. **Smoke test:** one clip to prove audio -> Whisper -> form -> metrics.
2. **Pilot:** 8-12 clips to expose wording, device and extraction problems.
3. **Frozen benchmark:** exactly 24 held-out clips after the pilot design is locked.

Keep clips short. For compatibility with the current Omnilingual ASR CTC path, target less than
30 seconds per clip and do not exceed 40 seconds.

## Development versus held-out evaluation

A clip becomes **development/pilot data** as soon as its transcript, prediction or downstream errors
are used to change extraction logic, prompts, normalisation rules or model configuration. Such a clip
must not be counted in the final held-out competition benchmark.

Samples `tz-sw-en-001` through `tz-sw-en-010` are development evidence. They proved the real
audio-to-metrics path, exposed parser safety issues and were used to select Whisper model and
inference configuration. They must therefore be excluded from the final frozen evaluation manifest.

Create the final evaluation manifest only after parser and collection design are stable. The fixed
24-row design is specified in `docs/HELDOUT_COLLECTION_PLAN.md`. Do not inspect model outputs from
those held-out clips until all 24 rows have been validated and the manifest has been frozen.

## Reference-first rule

For every sample:

1. choose the intended district, occupation, household size and service request;
2. draft the utterance before running any ASR model;
3. record the clip;
4. listen back once and edit the reference transcript so it matches what was actually spoken;
5. add the sample to the private manifest;
6. do not change the transcript or reference fields after inspecting model output.

This prevents benchmark references from drifting towards any particular model.

## Recommended variation

The final set should vary naturally across:

- Kiswahili-first, English-first and mixed-clause code-switching;
- digits and number words;
- several districts and occupations;
- several public-service requests;
- at least two recording devices if available;
- quiet and realistic moderate-noise conditions.

Do not manufacture noise that makes the utterance unintelligible. The benchmark should represent
realistic use rather than an adversarial stress test.

## Whisper readiness

Install Whisper only after the software tests are green:

```powershell
python -m pip install -e ".[whisper]"
python scripts/check_whisper_ready.py
```

The readiness check verifies both the Python package and the FFmpeg executable. It does not download
a Whisper model.

## Selected Whisper development configuration

The 10-clip pilot selected Turbo with forced Swahili and deterministic temperature-zero decoding:

```powershell
$env:WHISPER_MODEL = "turbo"
$env:WHISPER_LANGUAGE = "sw"
$env:WHISPER_TEMPERATURE = "0"
```

Use these settings unchanged after the final parser regression gate. Do not mix outputs from
different Whisper configurations in one summary.

The development comparison showed that Turbo was substantially more accurate than Small on the same
10 clips, while Turbo automatic language detection was slower and less accurate than forced Swahili.
Those development scores are diagnostic only and must not be presented as held-out competition
performance.

## Parser hardening boundary

Development clips may be used to strengthen deterministic extraction only where the transformation
does not invent content. Permitted examples include:

- repairing split structural tokens such as `na itaji` -> `nahitaji`;
- recognising ordinary Swahili number agreement such as `wawili`;
- stripping a harmless leading article from a service phrase;
- canonicalising `license` to UK English `licence`;
- preventing one field extractor from swallowing a following clause.

Do not map misrecognised values such as a wrong district or wrong certificate name back to the
reference answer. Such values must remain wrong or missing so the clarification and confirmation
workflow can handle them safely.

## Run the development regression

```powershell
$env:WHISPER_MODEL = "turbo"
$env:WHISPER_LANGUAGE = "sw"
$env:WHISPER_TEMPERATURE = "0"

python scripts/run_benchmark.py `
  --manifest data/private/benchmark_manifest.jsonl `
  --backend whisper `
  --output benchmark_results_whisper_turbo_parser_regression.json
```

Retain the JSON output; do not copy predicted transcripts back into benchmark references.

## Freeze before four-model comparison

Do not freeze the 10-row development manifest as the competition benchmark. After parser and model
configuration are locked, record the fixed 24-row held-out design under `data/private/heldout`. Run
`scripts/validate_heldout_manifest.py` and the general manifest validator, then freeze that held-out
manifest:

```powershell
python scripts/freeze_benchmark_manifest.py `
  --manifest data/private/<held-out-manifest>.jsonl
```

Record the printed SHA-256 value in the final evaluation notes. All four ASR systems must then use
that exact frozen held-out manifest.
