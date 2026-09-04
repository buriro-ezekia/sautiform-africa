# SautiForm Africa - Submission Benchmark Report Source

This file is the text source for the judge-facing PDF `SautiForm_Africa_Benchmark_Report.pdf`.
The PDF is intentionally limited to three pages.

## Benchmark scope

SautiForm Africa evaluates Kiswahili-English code-switched speech for a four-field public-service
form: district, occupation, household size and service request.

Four systems are compared on the same frozen held-out set:

1. Intron Sahara v2.5;
2. OpenAI Whisper Turbo;
3. Meta MMS (`facebook/mms-1b-all`, Swahili adapter `swh`);
4. Meta Omnilingual ASR (`omniASR_CTC_300M_v2`).

## Data

The final held-out benchmark contains 24 consented, de-identified recordings identified only by
sample IDs `tz-sw-en-h001` to `tz-sw-en-h024`. Total duration is 225.177 seconds
(3.753 minutes; 0.06255 hours), with individual clips ranging from 7.287 to 12.527 seconds.

The design balances 8 Kiswahili-first, 8 English-first and 8 mixed-clause utterances; four service
requests; 12 districts; 12 occupations; household sizes 2-9; and four device/noise cells. Each
recording represents one four-field form, giving 96 required field decisions.

Reference transcripts were created before inference. The 24-row manifest was frozen before any final
model run. Authoritative SHA-256:

`794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448`

All systems used the same source audio and same deterministic field extractor. Sahara LLM transcript
correction was disabled. No held-out result was used for post-hoc model or parser tuning.

## Metrics

- WER: lower-cased word edit distance divided by reference words.
- CER: lower-cased character edit distance divided by reference characters.
- Field exact match: exact correctness across the four required form fields.
- Complete-form accuracy: all four fields must exactly match the reference.
- Mean latency: observed wall-clock transcription time; not treated as a controlled hardware benchmark.

## Speech recognition results - Kiswahili-English

| Model | WER | CER | Mean latency |
|---|---:|---:|---:|
| Intron Sahara v2.5 | **0.4592** | 0.2559 | **3.08 s** |
| OpenAI Whisper Turbo | 0.5074 | **0.1660** | 25.60 s |
| Meta MMS | 0.7067 | 0.2759 | 12.51 s |
| Meta Omnilingual ASR | 0.7634 | 0.2790 | 200.80 s |

## Downstream form results - Kiswahili-English

| Model | Field exact | Exact fields | Complete forms |
|---|---:|---:|---:|
| Intron Sahara v2.5 | 0.2500 | 24/96 | 0/24 |
| OpenAI Whisper Turbo | **0.3021** | **29/96** | 0/24 |
| Meta MMS | 0.0625 | 6/96 | 0/24 |
| Meta Omnilingual ASR | 0.0729 | 7/96 | 0/24 |

Sahara achieved the best WER and observed mean latency. Whisper achieved the best CER and strongest
field recovery. Every system produced zero completely correct forms, supporting SautiForm's
clarification, editable read-back and explicit human-confirmation design.

## Qualitative findings

**Sahara:** strongest WER and fastest observed response, with direct support for the required
Kiswahili-English pair; weaker CER and field recovery than Whisper; 0/24 complete forms.

**Whisper Turbo:** best CER and structured-field recovery; slower local CPU inference and worse WER
than Sahara; 0/24 complete forms.

**Meta MMS:** open model and straightforward Swahili adapter; the monolingual `swh` adapter is a
clear limitation for within-utterance English switches; only 6/96 exact fields.

**Meta Omnilingual ASR:** broad multilingual open comparator; highest WER/CER here, 7/96 exact
fields, and substantial CPU/WSL2 runtime cost.

## Limitations

This is a small task-specific benchmark (24 clips; 0.06255 h) for one language pair. It does not
establish demographic fairness or a general ranking of African ASR systems. Latency environments
also differ: Sahara is hosted; Whisper/MMS ran locally; Omnilingual ran under WSL2/Linux on CPU.
