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
3. **Frozen benchmark:** approximately 24-40 clips after the pilot design is stable.

Keep clips short. For compatibility with the current Omnilingual ASR CTC path, target less than
30 seconds per clip and do not exceed 40 seconds.

## Development versus held-out evaluation

A clip becomes **development/pilot data** as soon as its transcript, prediction or downstream errors
are used to change extraction logic, prompts, normalisation rules or model configuration. Such a clip
must not be counted in the final held-out competition benchmark.

The first smoke-test clip `tz-sw-en-001` is therefore development evidence. It proves the real
audio-to-metrics path and may be used for debugging, but it must be excluded from the final frozen
evaluation manifest after any code is tuned in response to its output.

Create the final evaluation manifest only after parser and collection design are stable. Do not
inspect model outputs from those held-out clips until the software and model configurations are
frozen.

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

## First smoke-test utterance

Use a non-sensitive, fictional record:

```text
Ninaishi Mbozi District, occupation yangu ni farmer, household ina watu sita,
nataka birth certificate.
```

Reference fields:

```text
district=Mbozi
occupation=farmer
household_size=6
service_request=birth certificate
```

## Add the first clip

Save the recording anywhere outside the repository first, for example:

```text
C:\recordings\tz-sw-en-001.wav
```

Then add it to the ignored private workspace:

```powershell
$clip = "C:\recordings\tz-sw-en-001.wav"
$reference = "Ninaishi Mbozi District, occupation yangu ni farmer, " + `
  "household ina watu sita, nataka birth certificate."

python scripts/add_benchmark_sample.py `
  --audio $clip `
  --sample-id tz-sw-en-001 `
  --transcript $reference `
  --district Mbozi `
  --occupation farmer `
  --household-size 6 `
  --service-request "birth certificate" `
  --device "laptop microphone" `
  --noise "quiet room" `
  --consented
```

The script copies the clip to `data/private/audio/` and appends one validated JSONL row to
`data/private/benchmark_manifest.jsonl`.

## Validate before inference

```powershell
python scripts/validate_manifest.py `
  --manifest data/private/benchmark_manifest.jsonl
```

Expected:

```text
BENCHMARK_MANIFEST_VALID=YES rows=1
```

## Whisper readiness

Install Whisper only after the software tests are green:

```powershell
python -m pip install -e ".[whisper]"
python scripts/check_whisper_ready.py
```

The readiness check verifies both the Python package and the FFmpeg executable. It does not download
a Whisper model.

The selected model is controlled by `WHISPER_MODEL`. The repository default is `small`. Keep the
model name fixed once the final benchmark is frozen.

## First real Whisper run

```powershell
$env:WHISPER_MODEL = "small"

python scripts/run_benchmark.py `
  --manifest data/private/benchmark_manifest.jsonl `
  --backend whisper `
  --output benchmark_results_whisper.json
```

The first run may download the selected Whisper model. Retain the JSON output; do not copy its
predicted transcript back into the benchmark reference.

## Freeze before four-model comparison

After the pilot is complete and the final manifest has been checked manually:

```powershell
python scripts/freeze_benchmark_manifest.py `
  --manifest data/private/benchmark_manifest.jsonl
```

Record the printed SHA-256 value in the final evaluation notes. All four ASR systems must then use
that exact frozen manifest.
