# SautiForm Africa — Ethics & Inclusion Note

## Purpose and boundary

SautiForm Africa is an assistive interface for completing structured public-service forms from
Kiswahili–English speech. It is **not** a legal decision-maker, identity system or autonomous
government service.

The prototype is designed around a simple principle: speech recognition may suggest structured
values, but only the user can confirm the record.

## Consent and transparency

A user should know when audio is being recorded, why speech is being processed and what will happen
to the resulting record.

The challenge benchmark uses consented recordings. Raw benchmark audio is kept outside the public
repository. A production version should present a clear notice before recording and should explain
that audio is processed by an external speech service when Sahara is used.

Consent for speech processing should not be treated as consent for unrelated reuse, model training or
indefinite retention.

## Data minimisation

The prototype captures only four fields needed for the demonstration workflow: district, occupation,
household size and service request.

SautiForm does not attempt to infer ethnicity, religion, health status, political affiliation,
identity number or other sensitive characteristics from a person's voice. Unrelated speech should
not be retained merely because it was present in the recording.

A production deployment should collect only the fields required by the specific authorised service.

## Third-party speech processing

The competition product sends recorded audio to the Intron Sahara speech-to-text API. API credentials
are loaded through environment variables and are never stored in the repository.

A real deployment would need to disclose this processing relationship to users and review the
applicable service terms, retention behaviour, data location, security controls and public-sector
data-protection obligations before handling identifiable citizen data.

The challenge prototype does not make claims about production retention or regulatory compliance
that have not been independently verified.

## Human control and correction

ASR errors are expected under code-switching, accent variation, names, numbers and noise. SautiForm
therefore does not silently convert a transcript into an authoritative administrative record.

The interface:

- shows the recognised transcript;
- exposes each extracted field for review;
- leaves missing information unresolved rather than guessing it;
- provides clarification when required;
- allows correction before confirmation;
- requires an explicit confirmation action.

The benchmark reinforces this design: Sahara, Whisper, MMS and Omnilingual all scored 0/24 on
complete-form accuracy on the frozen held-out set.

## No autonomous eligibility or legal decisions

SautiForm does not decide whether a person qualifies for a service, whether a document is legally
valid, or whether an application should be approved or rejected.

Any future integration with a public authority should preserve a clear boundary between voice
assistance and the authority's legally accountable decision process.

## Inclusion

The prototype focuses on Kiswahili–English code-switching because mixed-language speech is a normal
interaction pattern for many bilingual speakers. Supporting code-switching can reduce the need for a
user to translate their own thoughts into one prescribed interface language before providing basic
form information.

However, inclusion cannot be claimed from language support alone. Users differ by accent, age,
literacy, disability, device, connectivity, background noise and familiarity with administrative
terms.

A production programme should therefore test with a substantially broader group of users and provide
a non-voice alternative. Voice must be an option, not a requirement.

## Fairness and benchmark interpretation

The benchmark reports all four model results, including weak results and zero complete-form scores.
No failed sample is removed from the denominator.

The held-out set includes variation in code-switch structure, service request, district, occupation,
household size, recording device and noise condition. That improves the usefulness of the prototype
benchmark, but 24 recordings are too few to establish demographic fairness.

The current results should not be interpreted as proof that one model is universally better for all
Swahili speakers or all African code-switching contexts.

## Error consequences and safe failure

For public-service forms, a small transcription error can have disproportionate consequences. A
wrong district, household number or service name may send a record down the wrong workflow.

SautiForm therefore prefers an incomplete record over a silently invented value. The safe failure
mode is to ask, show or allow correction.

The system should never use benchmark reference values, lookup tables or hidden defaults to repair an
ASR error without the user seeing and confirming the change.

## Security and secret handling

The Sahara API key is not committed. It is supplied at runtime through an environment variable.

The prototype deletes the temporary audio file created by the Streamlit application after the
transcription request completes. This reduces local persistence, although a production security
review would still be required for logging, browser uploads, server storage, network transport,
third-party processing and incident response.

## Accessibility and redress

Future versions should support users who cannot or do not wish to provide voice input. Accessible
alternatives may include typed entry, assisted entry, clear focus order, screen-reader testing and
language-appropriate instructions.

Users should also have a simple way to correct a record and, in any real service deployment, to
challenge or amend information after submission through the responsible public authority.

## Benchmark data governance

Reference transcripts and form fields were fixed before final model inference. Development and
held-out recordings are separated, and the held-out manifest is protected by SHA-256.

Private audio and per-clip held-out outputs are not committed to the repository. Optional release of
benchmark audio should occur only where the relevant speaker consent explicitly permits public
distribution.

## Current limitations

The prototype has not undergone:

- production security testing;
- public-sector privacy assessment;
- accessibility conformance testing;
- population-scale user research;
- legal or regulatory approval;
- integration with a government transaction system.

Those are deployment requirements, not features that should be implied by a challenge demonstration.

## Ethics position

The intended role of SautiForm Africa is to make an existing form interaction easier while keeping
the person whose information is being captured in control of the final record. Where the speech model
is uncertain or wrong, the correct product behaviour is not to conceal the error; it is to surface
the record for clarification and confirmation.
