# Development Lock

## Status

Phase 2 speech-model and parser development is locked after the 10-clip Kiswahili-English pilot.
Samples `tz-sw-en-001` through `tz-sw-en-010` are development-only data and must not appear in the
final held-out competition benchmark.

The locked Whisper configuration is:

```text
model=turbo
language=sw
temperature=0
```

## Final development regression

The final regression used all 10 development clips after bounded parser hardening.

```text
backend=whisper
n=10
mean_wer=0.518336834733894
mean_cer=0.170981661474138
mean_field_exact_match=0.400000000000000
complete_form_accuracy=0.100000000000000
mean_latency_seconds=27.1166395999957
```

These values are diagnostic development results, not held-out competition scores.

The key regression property is that WER and CER were unchanged from the selected Turbo transcription
run while field exact match improved from 0.30 to 0.40 and complete-form accuracy improved from 0.00
to 0.10. This isolates the effect of downstream parser hardening from speech-model changes.

## Parser boundary

No further parser changes should be made from development clips unless a new safety defect is found.
The locked parser may repair structural or orthographic variation that does not change semantic
content. It must not silently map a misrecognised district, occupation or public-service request to
the intended reference value.

Examples that remain errors include:

- `Mbosy` for `Mbozi`;
- `Alusha` for `Arusha`;
- `Mwaza` for `Mwanza`;
- `besi certificate` or `base certificate` for `birth certificate`.

Uncertain fields are intentionally left wrong or missing so that the clarification and explicit
human-confirmation workflow remains authoritative.

## Held-out boundary

The final evaluation must use new, unseen recordings under a separate private workspace:

```text
data/private/heldout/
  audio/
  benchmark_manifest.jsonl
```

Use sample identifiers that cannot be confused with development IDs, for example
`tz-sw-en-h001`, `tz-sw-en-h002`, and so on.

References must be created before any ASR output is inspected. Once the held-out manifest has been
manually checked, freeze it with `scripts/freeze_benchmark_manifest.py`. Sahara, Whisper, MMS and
Omnilingual ASR must then receive that exact same frozen manifest.

Do not tune model configuration, parser rules or reference transcripts after held-out inference has
begun.
