# Benchmark Protocol

## Principle

Every speech model must receive the same frozen, consented benchmark audio. References must not be
changed after inspecting a model's output.

## Required systems

The challenge matrix uses four explicitly named systems:

1. Intron Sahara v2.5;
2. OpenAI Whisper;
3. Meta MMS;
4. Meta Omnilingual ASR.

The default Omnilingual configuration is `omniASR_CTC_300M_v2`, selected as the lighter comparison
model. Meta's reference implementation currently limits CTC and LLM inference to audio shorter than
40 seconds, so benchmark clips used with this backend must satisfy that constraint.

MMS is configured with the Swahili language adapter by default. Because code-switching performance
may differ from monolingual performance, this limitation must be stated when interpreting results.

## Manifest requirements

Each row must contain:

- a unique `sample_id`;
- an audio path;
- a reference transcript;
- complete reference form fields;
- language pair;
- country or accent context;
- recording device category;
- noise condition;
- explicit consent status.

Rows for which consent is not explicitly `true` are rejected before inference. Raw benchmark audio
belongs under `data/private/` or another non-public location unless its licence and participant
consent explicitly permit redistribution.

## Metrics

Report, for every backend:

- WER;
- CER;
- field exact-match accuracy;
- complete-form accuracy;
- latency where measurable.

Complete-form accuracy is the primary downstream measure. Field exact match identifies which form
fields fail. WER and CER explain transcription behaviour but are not sufficient measures of the
application task.

Where sample size permits, stratify results by language mix, accent or country, device and noise
condition. Do not conceal failed samples or failed model runs from the reported denominator.

## Whisper pilot configuration

Whisper is initially evaluated with its library defaults: automatic language detection and the
library's fallback temperature schedule. During pilot development only, `WHISPER_LANGUAGE` and
`WHISPER_TEMPERATURE` may be set explicitly to compare configurations. The benchmark output records
the requested language, resulting language, model, device and requested temperature for every item.

Any final Whisper configuration must be selected using development/pilot audio, documented, then
frozen before held-out evaluation. Do not tune Whisper configuration on final benchmark clips.

## Reproducibility

Freeze the benchmark manifest before the final comparison. Record model identifiers, package
versions, hardware, operating system and relevant inference configuration. Keep raw model outputs so
summary tables can be regenerated rather than manually transcribed.

The deterministic `mock` backend is strictly a software-test utility and must never appear in the
competition evidence table.
