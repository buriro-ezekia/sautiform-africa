# Phase 1 Specification

## Objective

Build a narrow voice-driven public-service form assistant for natural Kiswahili-English code-switching. The system must convert speech into a structured record, ask for missing information and require confirmation before submission.

## User story

As a citizen or field officer, I want to answer a public-service form by speaking naturally so that I can complete a structured record without typing every field.

## In scope

- one Kiswahili-English public-service workflow;
- four required fields: district, occupation, household size and service request;
- ASR abstraction for Sahara, Whisper, MMS and one configurable fourth model;
- deterministic downstream extraction and validation;
- clarification of missing fields;
- explicit read-back and confirmation gate;
- WER, CER, field exact match and complete-form accuracy;
- local tests and GitHub Actions CI.

## Out of scope for Phase 1

- automatic submission to a government system;
- identity verification;
- storage of raw voice recordings;
- unsupported claims of legal validity;
- benchmark numbers without real model runs.

## Acceptance criteria

1. A transcript containing all four explicit fields produces a complete structured record.
2. Missing required fields remain unset; the system does not guess them.
3. The dialogue engine asks for the first missing field.
4. Invalid household size is rejected before confirmation.
5. A complete valid record produces a bilingual confirmation prompt.
6. Benchmark utilities compute WER, CER, field exact match and complete-form accuracy deterministically.
7. Sahara credentials are read from environment variables and are never hard-coded.
8. CI runs linting and tests on Python 3.10, 3.11 and 3.12.
