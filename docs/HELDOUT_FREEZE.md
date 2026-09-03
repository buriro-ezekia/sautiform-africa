# Held-out Benchmark Freeze

## Authoritative benchmark identity

The final SautiForm Africa held-out evaluation set contains 24 consented Kiswahili-English
recordings using sample IDs `tz-sw-en-h001` through `tz-sw-en-h024`.

The local manifest is:

```text
data/private/heldout/benchmark_manifest.jsonl
```

The authoritative SHA-256 frozen on 3 September 2026 is:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

The digest was independently recomputed from the manifest and matched the generated SHA-256 sidecar.
The private audio and manifest remain outside version control.

## Evaluation invariant

Every final ASR run must verify this exact digest before model loading:

```text
--expected-manifest-sha256 794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

A mismatch is a hard failure. Do not edit the held-out manifest, its references, structured fields,
metadata or audio after this point.

The parser and Whisper configuration are also frozen:

```text
WHISPER_MODEL=turbo
WHISPER_LANGUAGE=sw
WHISPER_TEMPERATURE=0
```

Development samples `tz-sw-en-001` through `tz-sw-en-010` are excluded from this held-out
benchmark.

## Final model matrix

The four required systems are evaluated on this identical frozen manifest:

1. Intron Sahara v2.5;
2. OpenAI Whisper;
3. Meta MMS;
4. Meta Omnilingual ASR.

Model failures remain part of the evaluation record and must not be replaced with fabricated scores
or silently removed from the denominator.
