# Final Held-out Evaluation

## Frozen benchmark

The final evaluation uses 24 unseen, consented Kiswahili-English recordings. The authoritative
manifest SHA-256 is:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

The manifest hash is verified before every final inference run and independently checked afterwards.

## OpenAI Whisper

Configuration:

```text
model=turbo
language=sw
temperature=0
```

Final held-out result:

```text
backend=whisper
n=24
mean_wer=0.507395249766573
mean_cer=0.166024569504558
mean_field_exact_match=0.302083333333333
complete_form_accuracy=0.0
mean_latency_seconds=25.5986463374999
```

This corresponds to 29 exactly correct required fields out of 96 and zero completely correct forms
out of 24.

## Meta MMS

Configuration:

```text
model=facebook/mms-1b-all
target_lang=swh
```

Final held-out result:

```text
backend=mms
n=24
mean_wer=0.706744572829132
mean_cer=0.275927802793813
mean_field_exact_match=0.0625
complete_form_accuracy=0.0
mean_latency_seconds=12.5084474166627
```

This corresponds to 6 exactly correct required fields out of 96 and zero completely correct forms
out of 24. The manifest SHA-256 was independently confirmed unchanged after MMS inference.

MMS uses a monolingual Swahili adapter, which is an important limitation when interpreting its
performance on Kiswahili-English code-switched speech. The earlier local setup used `swa`, which is
not a vocabulary key for this checkpoint; the repository corrected this to `swh` before any MMS
held-out inference.

## Current comparison

| Model | WER | CER | Field exact match | Exact fields | Complete forms | Mean latency |
|---|---:|---:|---:|---:|---:|---:|
| Whisper Turbo | 0.5074 | 0.1660 | 0.3021 | 29/96 | 0/24 | 25.60 s |
| Meta MMS | 0.7067 | 0.2759 | 0.0625 | 6/96 | 0/24 | 12.51 s |

These are final held-out results and must not be used to tune the parser, model configuration or
benchmark references.

## Remaining systems

The same frozen manifest must be used, without modification, for:

1. Meta Omnilingual ASR;
2. Intron Sahara v2.5.

Every run must verify the authoritative manifest SHA-256 before model loading.
