# Final Held-out Evaluation

## Frozen benchmark

The final evaluation uses 24 unseen, consented Kiswahili-English recordings. The authoritative
manifest SHA-256 is:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

The manifest hash was verified before every final inference run and independently checked afterwards.
All four final systems used the same frozen 24-row manifest, the same reference transcripts and
fields, and the same downstream deterministic form parser.

## Intron Sahara v2.5

Configuration:

```text
endpoint=https://infer.voice.intron.io/file/v1/upload/sync
language=sw
code_switching=Swahili-English
use_disable_llm_corrections=TRUE
response_text_path=data.audio_transcript
```

Final held-out result:

```text
backend=sahara
n=24
mean_wer=0.45922181372549026
mean_cer=0.2559374583347081
mean_field_exact_match=0.25
complete_form_accuracy=0.0
mean_latency_seconds=3.078093576165884
```

This corresponds to 24 exactly correct required fields out of 96 and zero completely correct forms
out of 24. The authoritative manifest SHA-256 was independently confirmed unchanged after Sahara
inference.

Sahara achieved the lowest WER and lowest mean latency in this held-out comparison. Whisper retained
the lowest CER and highest downstream field exact-match score. Sahara's result therefore demonstrates
that lower WER does not necessarily translate directly into higher structured-field recovery for this
public-service form task.

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

## Meta Omnilingual ASR

Configuration:

```text
package=omnilingual-asr==0.2.0
model_card=omniASR_CTC_300M_v2
runtime=WSL2/Linux, Python 3.11, CPU
```

Final held-out result:

```text
backend=omni
n=24
mean_wer=0.7633753501400561
mean_cer=0.2789565633485864
mean_field_exact_match=0.07291666666666667
complete_form_accuracy=0.0
mean_latency_seconds=200.80138507704154
```

This corresponds to 7 exactly correct required fields out of 96 and zero completely correct forms
out of 24. The authoritative manifest SHA-256 was independently confirmed unchanged after the
Omnilingual run.

The Omnilingual comparator required a separate WSL2/Linux runtime because its fairseq2 dependency
does not support native Windows. Its latency is therefore reported as observed on the same local
machine but should be interpreted with the runtime difference in mind.

## Final four-model comparison

| Model | WER ↓ | CER ↓ | Field exact match ↑ | Exact fields | Complete forms | Mean latency ↓ |
|---|---:|---:|---:|---:|---:|---:|
| Intron Sahara v2.5 | **0.4592** | 0.2559 | 0.2500 | 24/96 | 0/24 | **3.08 s** |
| OpenAI Whisper Turbo | 0.5074 | **0.1660** | **0.3021** | **29/96** | 0/24 | 25.60 s |
| Meta MMS | 0.7067 | 0.2759 | 0.0625 | 6/96 | 0/24 | 12.51 s |
| Meta Omnilingual ASR | 0.7634 | 0.2790 | 0.0729 | 7/96 | 0/24 | 200.80 s |

Sahara provides the strongest WER and latency result, while Whisper provides the strongest CER and
downstream field recovery. MMS is substantially faster than Whisper but recovers few exact fields.
Omnilingual recovers one more field than MMS but is the slowest system in this local CPU setup.

All four systems have zero complete-form accuracy. This is an important product finding rather than
a reason to hide the benchmark: none of the evaluated ASR systems is sufficiently reliable to let
SautiForm silently treat a four-field public-service form as complete. The clarification, editable
read-back and explicit human-confirmation stages are therefore necessary safety controls.

These are final held-out results. They must not be used to tune the parser, model configurations or
benchmark references.
