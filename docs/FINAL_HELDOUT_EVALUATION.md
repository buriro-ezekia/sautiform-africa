# Final Held-out Evaluation

## Frozen benchmark

The final evaluation uses 24 unseen, consented Kiswahili-English recordings. The authoritative
manifest SHA-256 is:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

The manifest hash was verified before Whisper inference and independently confirmed unchanged after
the run.

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
out of 24. These are final held-out results and must not be used to tune the parser, Whisper model
configuration or benchmark references.

## Remaining systems

The same frozen manifest must be used, without modification, for:

1. Meta MMS with the declared Swahili adapter;
2. Meta Omnilingual ASR;
3. Intron Sahara v2.5.

Every run must verify the authoritative manifest SHA-256 before model loading.
