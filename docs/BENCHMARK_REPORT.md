# SautiForm Africa — Benchmark Report

## Executive summary

SautiForm Africa benchmarks Intron Sahara v2.5 against OpenAI Whisper Turbo, Meta MMS and Meta
Omnilingual ASR on the same frozen Kiswahili–English code-switching speech set.

On 24 held-out recordings, **Sahara achieved the best word error rate (0.4592) and the fastest mean
transcription latency (3.08 seconds)**. **Whisper achieved the best character error rate (0.1660) and
the highest downstream field exact-match score (0.3021, or 29 of 96 required fields)**. MMS and the
tested Omnilingual CTC model were substantially weaker on this task.

No system produced a completely correct four-field form on any held-out recording. That result is
central to the product design: transcription output is never accepted silently. SautiForm requires
clarification, editable read-back and explicit human confirmation.

## 1. Benchmark objective

The benchmark asks two related but different questions:

1. How accurately does each speech model transcribe Kiswahili–English code-switched speech?
2. How reliably can the resulting transcript support a structured public-service form?

The second question is necessary because a transcript can have a reasonable aggregate error rate
while still changing one critical administrative value.

## 2. Systems evaluated

### Intron Sahara v2.5

Sahara is the challenge product backend. The final run used the official Intron Voice synchronous
speech-to-text endpoint with Swahili–English code-switching selected by `sw`. Optional LLM transcript
correction was disabled before held-out evaluation so that Sahara, Whisper, MMS and Omnilingual all
fed their direct ASR output into the same deterministic form parser.

### OpenAI Whisper Turbo

Whisper used the multilingual `turbo` model, forced Swahili language selection and temperature zero.
This configuration was selected on a separate 10-clip development set and locked before the held-out
benchmark was created.

### Meta MMS

MMS used `facebook/mms-1b-all` with the Swahili adapter `swh`. This is a monolingual Swahili
adapter and therefore has an inherent limitation on within-utterance English code-switching.

### Meta Omnilingual ASR

The Omnilingual comparator used `omniASR_CTC_300M_v2` through `omnilingual-asr==0.2.0`. It ran
under WSL2/Linux with Python 3.11 on CPU because the model's fairseq2 runtime was not supported
natively in the project's Windows environment.

## 3. Held-out dataset

The final benchmark contains **24 consented, previously unseen Kiswahili–English recordings**. The
development clips used to select Whisper configuration and harden the parser are excluded.

The held-out design was fixed before inference and balances:

- three speech structures: Kiswahili-first, English-first and mixed-clause;
- four service requests;
- 12 districts;
- 12 occupations;
- household sizes from 2 to 9;
- four recording device/noise cells.

Each recording represents one four-field form, giving **96 required field decisions** in total.

The authoritative manifest SHA-256 is:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

The digest was checked before every final model run and independently confirmed unchanged after each
run.

## 4. Metrics

### Word error rate

WER is edit distance over lower-cased whitespace-separated words divided by the number of reference
words. Lower is better.

### Character error rate

CER is edit distance over lower-cased characters divided by the number of reference characters.
Lower is better.

### Field exact match

Each transcript is passed through the same deterministic extractor for district, occupation,
household size and service request. A field counts as correct only when the extracted value exactly
matches the frozen reference. Higher is better.

### Complete-form accuracy

A form counts as correct only when **all four fields** match the reference. Higher is better. This is
the most stringent downstream measure.

### Mean latency

Mean wall-clock transcription latency is reported for the observed evaluation environment. Latency
is useful operational evidence, but it is not a perfectly controlled hardware benchmark because the
systems use different execution paths: Sahara is a hosted API, Whisper and MMS ran locally, and
Omnilingual used a separate WSL2 runtime.

## 5. Final results

| Model | WER ↓ | CER ↓ | Field exact ↑ | Exact fields | Complete forms | Mean latency ↓ |
|---|---:|---:|---:|---:|---:|---:|
| **Intron Sahara v2.5** | **0.4592** | 0.2559 | 0.2500 | 24/96 | 0/24 | **3.08 s** |
| **OpenAI Whisper Turbo** | 0.5074 | **0.1660** | **0.3021** | **29/96** | 0/24 | 25.60 s |
| **Meta MMS** | 0.7067 | 0.2759 | 0.0625 | 6/96 | 0/24 | 12.51 s |
| **Meta Omnilingual ASR** | 0.7634 | 0.2790 | 0.0729 | 7/96 | 0/24 | 200.80 s |

Unrounded aggregate values are retained in `docs/FINAL_HELDOUT_EVALUATION.md`.

## 6. Interpretation

### Sahara

**Strengths**

- Best WER of the four systems.
- Fastest observed mean latency by a large margin.
- Directly supports the Swahili–English language pair required by the product.
- Simple hosted API path avoids the local model-loading burden seen with larger comparators.

**Limitations**

- CER was materially higher than Whisper's.
- Downstream field exact match was 0.2500, below Whisper's 0.3021.
- Zero complete forms means Sahara output still requires user review for this task.
- Hosted latency is not directly comparable with local CPU inference as a pure model-speed measure.

### Whisper Turbo

**Strengths**

- Best CER.
- Best downstream field exact match: 29 of 96 required fields.
- Strongest of the evaluated systems for structured field recovery.

**Limitations**

- WER was worse than Sahara's.
- Mean local latency was 25.60 seconds, substantially slower than the Sahara API in this evaluation.
- It is a comparator rather than the challenge product backend.

### Meta MMS

**Strengths**

- Open model with a straightforward Swahili adapter.
- Faster locally than Whisper in the observed environment.

**Limitations**

- The `swh` adapter is monolingual and does not explicitly model the English portion of
  Kiswahili–English code-switching.
- Field exact match was only 6 of 96.
- Zero complete forms.

### Meta Omnilingual ASR

**Strengths**

- Broad multilingual model family.
- Provides an additional open comparator beyond Whisper and MMS.

**Limitations**

- Highest WER and CER in this evaluation.
- Only 7 of 96 exact fields.
- Mean latency of 200.80 seconds in the CPU/WSL2 environment.
- More complex local runtime requirements than the other systems.

## 7. Why WER alone is insufficient

Sahara led on WER, whereas Whisper led on CER and exact field recovery. This divergence is important.
Public-service forms are not scored on average sentence similarity; they depend on a small number of
specific values being correct.

For example, one substituted district or certificate type can make an otherwise readable transcript
unsuitable as a final administrative record. SautiForm therefore evaluates both transcription
quality and downstream structured accuracy.

## 8. Product implication: human confirmation is required

All four models recorded:

```text
complete_form_accuracy = 0.0
complete_forms = 0/24
```

This is not hidden or treated as a failed experiment. It is the clearest evidence for the product's
safety architecture.

SautiForm:

1. extracts only what it can find in the transcript;
2. identifies missing or invalid fields;
3. allows the user to edit the structured record;
4. reads the record back;
5. requires explicit confirmation.

The benchmark shows why those controls are necessary.

## 9. Benchmark integrity

To reduce benchmark leakage and post-hoc tuning:

- development IDs `tz-sw-en-001` to `tz-sw-en-010` were permanently separated from held-out
  evaluation;
- the 24-row held-out design was fixed before final inference;
- references were created independently of model output;
- the parser and model configurations were frozen before held-out scoring;
- every final run checked the same manifest SHA-256;
- private audio and per-sample final transcripts are excluded from the public repository;
- aggregate results include all 24 held-out samples;
- no model was retuned from final held-out errors.

## 10. Limitations

The benchmark is deliberately small and task-specific. It contains 24 recordings and four form
fields, so it should not be interpreted as a general ranking of African speech models.

The evaluation focuses on one language pair, Kiswahili–English, and does not establish performance
for the other Sahara code-switching pairs. The speaker, device and noise coverage is useful for a
challenge prototype but is not representative of the full diversity of Tanzanian or African public
service users.

Latency is also environment-dependent. Sahara is a remote service, while the comparison systems were
run locally under different runtime constraints.

Finally, exact-match metrics are intentionally strict. They are appropriate for structured public
service fields, but they do not capture every semantically acceptable variation in free text.

## 11. Reproducibility

Public repository code contains:

- benchmark manifest validation;
- manifest freezing and SHA verification;
- model adapters;
- deterministic metrics;
- deterministic field extraction;
- single-model and matrix runners;
- configuration and runtime documentation.

Raw consented benchmark audio and per-clip held-out outputs remain private. This keeps the public
repository reproducible at the software and aggregate-evidence level without publishing private
recordings.
