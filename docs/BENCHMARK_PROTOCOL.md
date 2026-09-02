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

## Selected Whisper configuration

Whisper configuration was selected entirely on development audio before creation of the held-out
benchmark. The 10-clip pilot first established that forced Swahili with temperature zero was more
reproducible than automatic language detection for the local CPU environment. The same 10 clips then
compared the `small` and `turbo` multilingual models and finally compared Turbo under forced
Swahili against automatic language detection.

The selected configuration is:

```text
model=turbo
language=sw
temperature=0
```

On the 10 development clips, Turbo with forced Swahili materially reduced WER and CER and doubled
field exact-match accuracy relative to the earlier Small configuration, although it increased CPU
latency. Turbo with automatic language detection was both slower and less accurate on the same
development set.

Samples `tz-sw-en-001` through `tz-sw-en-010` are therefore development-only evidence. They must
not appear in the final competition benchmark or be used to claim held-out performance.

The benchmark output records the requested language, resulting language, model, device and requested
temperature for every item.

## Parser development boundary

Parser changes may use the development clips, but only bounded structural normalisation is allowed.
Examples include token-boundary repair, harmless articles and UK/US spelling equivalence. Content
errors such as a misrecognised district or service name must not be silently replaced with the
reference answer. Uncertain fields remain missing and are handled by clarification and explicit human
confirmation.

## Reproducibility

Freeze the benchmark manifest before the final comparison. Record model identifiers, package
versions, hardware, operating system and relevant inference configuration. Keep raw model outputs so
summary tables can be regenerated rather than manually transcribed.

The deterministic `mock` backend is strictly a software-test utility and must never appear in the
competition evidence table.
