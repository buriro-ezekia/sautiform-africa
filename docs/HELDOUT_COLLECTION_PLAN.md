# Held-out Collection Plan

## Purpose

This document fixes the final 24-clip Kiswahili-English held-out evaluation design before recording
or inference begins. These clips must remain unseen by every ASR backend until the complete manifest
has been reviewed and frozen.

Development clips `tz-sw-en-001` through `tz-sw-en-010` are excluded permanently.

## Fixed sample IDs

The final held-out set uses exactly:

```text
tz-sw-en-h001 ... tz-sw-en-h024
```

No development ID may appear in the held-out manifest.

## Balance

The 24 samples are balanced across:

- 8 Kiswahili-first utterances;
- 8 English-first utterances;
- 8 mixed-clause utterances;
- 4 service requests, each appearing 6 times;
- 12 districts, each appearing twice;
- 12 occupations, each appearing twice;
- household sizes 2-9, each appearing three times;
- four recording cells, each containing 6 clips.

The four recording cells are:

1. Device A, quiet room;
2. Device A, moderate realistic background noise;
3. Device B, quiet room;
4. Device B, moderate realistic background noise.

Use factual device labels during ingestion, for example `laptop microphone` and
`phone microphone`. If only one physical device is available, keep the 24 utterances unchanged and
record both acoustic conditions with that device; do not invent a second device label.

Moderate noise should represent plausible use, such as distant conversation, a fan or outdoor
ambient sound. Do not deliberately make speech unintelligible.

## Recording plan

| ID | Style | District | Occupation | Household | Service | Recording cell | Intended utterance |
|---|---|---|---|---:|---|---|---|
| h001 | Kiswahili-first | Mbozi | tailor | 2 | birth certificate | A quiet | Naishi Mbozi District, kazi yangu ni tailor, household ina watu wawili, nataka birth certificate. |
| h002 | English-first | Temeke | nurse | 3 | marriage certificate | A quiet | I live in Temeke District, occupation yangu ni nurse, familia ina watu watatu, I need marriage certificate. |
| h003 | Mixed | Kinondoni | driver | 4 | business licence | A quiet | District yangu ni Kinondoni, I work as a driver, household ina watu four, nahitaji business licence. |
| h004 | Kiswahili-first | Dodoma | accountant | 5 | land certificate | A quiet | Ninaishi Dodoma District, kazi yangu ni accountant, familia ina watu watano, nahitaji land certificate. |
| h005 | English-first | Ilala | mechanic | 6 | birth certificate | A quiet | I live in Ilala District, I work as a mechanic, household has six people, nataka birth certificate. |
| h006 | Mixed | Arusha | farmer | 7 | marriage certificate | A quiet | Ninaishi Arusha District, occupation yangu ni farmer, household has seven people, I need marriage certificate. |
| h007 | Kiswahili-first | Mbeya | electrician | 8 | business licence | A moderate | Naishi Mbeya District, kazi yangu ni electrician, household ina watu nane, nahitaji business licence. |
| h008 | English-first | Morogoro | teacher | 9 | land certificate | A moderate | I live in Morogoro District, kazi yangu ni teacher, familia ina watu tisa, I need land certificate. |
| h009 | Mixed | Mwanza | trader | 2 | birth certificate | A moderate | District yangu ni Mwanza, occupation yangu ni trader, household has two people, nataka birth certificate. |
| h010 | Kiswahili-first | Iringa | carpenter | 3 | marriage certificate | A moderate | Ninaishi Iringa District, kazi yangu ni carpenter, familia ina watu watatu, nataka marriage certificate. |
| h011 | English-first | Tanga | shopkeeper | 4 | business licence | A moderate | I live in Tanga District, I work as a shopkeeper, household ina watu four, nahitaji business licence. |
| h012 | Mixed | Moshi | mason | 5 | land certificate | A moderate | Naishi Moshi District, occupation yangu ni mason, household has five people, I need land certificate. |
| h013 | Kiswahili-first | Mbozi | teacher | 6 | marriage certificate | B quiet | Ninaishi Mbozi District, kazi yangu ni teacher, household ina watu sita, nahitaji marriage certificate. |
| h014 | English-first | Temeke | trader | 7 | business licence | B quiet | I live in Temeke District, occupation yangu ni trader, familia ina watu saba, I need business licence. |
| h015 | Mixed | Kinondoni | carpenter | 8 | land certificate | B quiet | District yangu ni Kinondoni, I work as a carpenter, household ina watu eight, nataka land certificate. |
| h016 | Kiswahili-first | Dodoma | mechanic | 9 | birth certificate | B quiet | Naishi Dodoma District, kazi yangu ni mechanic, familia ina watu tisa, nataka birth certificate. |
| h017 | English-first | Ilala | farmer | 2 | marriage certificate | B quiet | I live in Ilala District, I work as a farmer, household has two people, nahitaji marriage certificate. |
| h018 | Mixed | Arusha | electrician | 3 | business licence | B quiet | Ninaishi Arusha District, occupation yangu ni electrician, household ina watu three, I need business licence. |
| h019 | Kiswahili-first | Mbeya | driver | 4 | land certificate | B moderate | Naishi Mbeya District, kazi yangu ni driver, familia ina watu four, nahitaji land certificate. |
| h020 | English-first | Morogoro | accountant | 5 | birth certificate | B moderate | I live in Morogoro District, occupation yangu ni accountant, household has five people, nataka birth certificate. |
| h021 | Mixed | Mwanza | tailor | 6 | marriage certificate | B moderate | District yangu ni Mwanza, I work as a tailor, household ina watu sita, I need marriage certificate. |
| h022 | Kiswahili-first | Iringa | nurse | 7 | business licence | B moderate | Ninaishi Iringa District, kazi yangu ni nurse, familia ina watu saba, nahitaji business licence. |
| h023 | English-first | Tanga | mason | 8 | land certificate | B moderate | I live in Tanga District, I work as a mason, household has eight people, nataka land certificate. |
| h024 | Mixed | Moshi | shopkeeper | 9 | birth certificate | B moderate | Naishi Moshi District, occupation yangu ni shopkeeper, household ina watu nine, I need birth certificate. |

## Reference-first recording procedure

For each row:

1. record the intended utterance naturally;
2. listen to the saved clip once before running any model;
3. if you misspoke, edit only the reference transcript so it matches the words actually spoken;
4. keep the intended structured fields unchanged only when the spoken meaning still matches them;
5. if the spoken meaning changed, re-record the clip rather than altering the benchmark answer;
6. ingest the clip into `data/private/heldout`;
7. never inspect ASR output during collection.

Target less than 30 seconds and never exceed 40 seconds.

## Suggested source filenames

Use the sample ID as the filename stem:

```text
tz-sw-en-h001.ogg
tz-sw-en-h002.ogg
...
tz-sw-en-h024.ogg
```

Other supported audio extensions are acceptable, but each ID must resolve to exactly one source
recording.

## Batch ingestion

After listening to all 24 source recordings and confirming that each clip matches the fixed
reference transcript and structured meaning, preflight the folder without writing anything:

```powershell
python scripts/ingest_heldout_plan.py `
  --source-dir "D:\DESKTOP\Buriro\GitHub Desktop\SautiForm Africa\Texts & Audios\Heldout Audios" `
  --device-a "laptop microphone" `
  --device-b "laptop microphone" `
  --dry-run
```

If Device B was a different physical device, replace the second label with its factual description.
The dry run verifies exact sample stems, supported formats, file-size safeguards and, where
`ffprobe` is available, clip duration. It performs no copying, manifest write or ASR inference.

After the dry run passes, rerun without `--dry-run` and add
`--confirm-recordings-match-plan`. That explicit flag records the human assertion that every clip
was listened to and agrees with the fixed plan.

## Pre-freeze gate

After all 24 clips are ingested:

```powershell
python scripts/validate_heldout_manifest.py `
  --manifest data/private/heldout/benchmark_manifest.jsonl

python scripts/validate_manifest.py `
  --manifest data/private/heldout/benchmark_manifest.jsonl
```

Both commands must pass before freezing.

Then freeze:

```powershell
python scripts/freeze_benchmark_manifest.py `
  --manifest data/private/heldout/benchmark_manifest.jsonl
```

Record the printed SHA-256 value. From that point onward, no held-out transcript, field, metadata row
or audio file may be changed. Sahara, Whisper, MMS and Omnilingual ASR must use the exact frozen
manifest.

## Inference embargo

Do not run any ASR backend on `data/private/heldout/benchmark_manifest.jsonl` until all 24 rows have
passed validation and the manifest hash has been frozen.

Do not tune the parser, Whisper settings, MMS adapter, Omnilingual settings or Sahara integration
using held-out outputs.
