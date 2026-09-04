# Phase 2 Specification

## Objective

Convert the Phase 1 deterministic form workflow into a testable voice-AI prototype and establish a
reproducible benchmark harness for Sahara plus three named comparison ASR systems.

## In scope

Phase 2 adds:

- microphone and transcript input through a Streamlit demonstration interface;
- an editable structured record and explicit confirmation gate;
- Sahara, Whisper, MMS and Meta Omnilingual ASR as named challenge backends;
- consent-aware benchmark metadata and unique sample identifiers;
- audio extension, existence and size checks before model calls;
- single-backend and four-model benchmark runners;
- WER, CER, field exact match, complete-form accuracy and latency summaries;
- failure isolation so an unavailable model is recorded rather than replaced by invented results;
- regression tests for consent, audio safeguards and backend registration.

## Out of scope

Phase 2 does not include:

- automatic submission to a public authority;
- identity verification;
- legal eligibility decisions;
- storage of raw audio in the public repository;
- benchmark scores generated without real model inference;
- production-grade authentication, encryption or retention infrastructure.

## Acceptance criteria

1. The Phase 1 form and dialogue tests continue to pass unchanged in behaviour.
2. The four challenge backends are explicitly named as Sahara, Whisper, MMS and Omnilingual ASR.
3. Benchmark rows without explicit consent fail validation.
4. Duplicate benchmark sample identifiers fail validation.
5. Unsupported or missing audio fails before a model call.
6. The example manifest can be validated in metadata-only mode without private audio.
7. A real manifest is validated with audio checks before benchmarking begins.
8. The matrix runner applies the same validated rows to every selected backend.
9. Backend failures are visible in the output artefact when continuation is requested.
10. The Streamlit interface permits human correction and confirmation but performs no external
    submission.
11. Ruff, the complete test suite and Python compilation pass locally.

## Evidence required before Phase 2 is locked

The repository code can be accepted locally before model downloads. Challenge benchmark claims,
however, require a separate evidence gate consisting of:

- confirmed Sahara participant API configuration;
- consented Kiswahili-English audio;
- the same frozen benchmark manifest for all four systems;
- retained raw per-sample outputs and summary metrics;
- documented hardware and software environment for reproducibility.
