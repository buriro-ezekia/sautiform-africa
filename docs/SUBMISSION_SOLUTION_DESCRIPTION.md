# SautiForm Africa — Solution Description

## Challenge category

**Legal & Public Services**

## One-line description

SautiForm Africa is a Sahara-powered voice assistant that turns mixed Kiswahili–English speech into
an editable public-service form record and requires the user to confirm every completed record before
it can be treated as final.

## The problem

Public-service forms are usually designed around written, single-language interaction. In practice,
people often speak more naturally by moving between Kiswahili and English within the same
conversation. A citizen may know a service by its English administrative name while describing their
location, household or occupation in Kiswahili. Requiring them to switch into one prescribed language
or type every field can create avoidable friction, particularly on mobile devices and in
field-assisted workflows.

Speech recognition alone does not solve that problem. An ASR system can produce a plausible
transcript while still changing a district, occupation, number or service name. For a public-service
record, those errors matter more than whether the overall sentence looks fluent.

SautiForm Africa therefore treats speech recognition as the beginning of the interaction, not the
authority for the final record.

## How the prototype works

The competition prototype follows a deliberately simple pipeline:

```text
Kiswahili–English speech
  -> Intron Sahara v2.5
  -> transcript
  -> deterministic field extraction
  -> missing/invalid-field check
  -> clarification or editable correction
  -> read-back
  -> explicit user confirmation
```

The current demonstration captures four fields:

- district;
- occupation;
- household size;
- service request.

A typical utterance is:

> Ninaishi Mbozi District, occupation yangu ni farmer, household ina watu sita, nataka birth
> certificate.

The recorded audio is sent to the Intron Sahara v2.5 synchronous speech-to-text API using the
Swahili–English code-switching configuration. SautiForm then extracts only values that are present in
the returned transcript. It does not silently infer a missing district, replace a misrecognised
service with the expected answer, or submit the record automatically.

The user can review and edit every field. If required information is missing or invalid, the dialogue
layer asks for clarification. A complete record is accepted only after an explicit confirmation
checkbox.

## Why Sahara is central to the product

The product interface is fixed to **Intron Sahara v2.5** for speech recognition. The other speech
systems in the repository are benchmark comparators, not selectable production backends in the
competition demo.

This distinction matters. The challenge product demonstrates a real Sahara API call, while the
benchmark separately asks whether Sahara performs better or worse than alternative systems on the
same held-out speech.

## Evidence from the four-model benchmark

SautiForm was evaluated on 24 frozen, consented Kiswahili–English recordings. Every model received the
same audio and the same reference data.

| Model | WER ↓ | CER ↓ | Field exact match ↑ | Complete forms | Mean latency ↓ |
|---|---:|---:|---:|---:|---:|
| Intron Sahara v2.5 | **0.4592** | 0.2559 | 0.2500 | 0/24 | **3.08 s** |
| OpenAI Whisper Turbo | 0.5074 | **0.1660** | **0.3021** | 0/24 | 25.60 s |
| Meta MMS | 0.7067 | 0.2759 | 0.0625 | 0/24 | 12.51 s |
| Meta Omnilingual ASR | 0.7634 | 0.2790 | 0.0729 | 0/24 | 200.80 s |

Sahara produced the lowest word error rate and the lowest observed mean latency. Whisper produced the
lowest character error rate and recovered the largest share of exact form fields.

The most important product result is that **no model produced a completely correct four-field form on
any of the 24 held-out recordings**. SautiForm therefore does not equate a fluent transcript with a
valid administrative record. The benchmark directly supports the product's clarification, editable
read-back and human-confirmation controls.

## Product value

SautiForm Africa is designed to reduce the language and input burden around structured public-service
data collection. The intended value is not autonomous administration. It is a better interface
between natural mixed-language speech and the structured information that an existing service
workflow requires.

For citizens, the approach can make form interaction more conversational while preserving the right
to correct the record. For field officers, the same workflow could reduce repeated manual typing
while keeping human review in place. For public institutions, the structured output provides a clear
boundary between speech recognition and any future authorised submission system.

These benefits are proposed product outcomes; the current challenge prototype has not been deployed
at population scale and does not claim measured service-delivery impact.

## What is intentionally out of scope

The challenge prototype does **not**:

- submit data to a government system;
- verify identity;
- determine legal eligibility;
- make administrative decisions;
- infer sensitive attributes;
- treat ASR output as authoritative;
- store benchmark audio in the public repository.

A production deployment would require integration with the relevant public authority, security and
retention controls, accessibility testing, user support and redress procedures, and domain-specific
validation.

## Technical implementation

The repository separates speech recognition from form logic. The Sahara adapter communicates with
the official Intron Voice synchronous STT endpoint. The form extractor and validation logic are
deterministic and model-independent, allowing all benchmark systems to be scored through the same
downstream path.

The benchmark manifest is frozen by SHA-256 before final evaluation:

```text
794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

Private audio and per-clip held-out outputs remain outside version control. Aggregate evidence is
documented in the public repository.

## Current status

The Sahara API integration has been exercised successfully on development audio and on the full
24-clip final held-out benchmark. The four-model evaluation is complete. The remaining competition
work is presentation and submission rather than further model or parser tuning.
