# SautiForm Africa — Demo Video Script and Recording Plan

## Goal

Show a complete, real Sahara-powered product flow, then demonstrate why the human-confirmation design
is necessary using the final four-model benchmark.

The submission limit is **5 minutes maximum** and the video must be hosted on YouTube as **Public** or **Unlisted** so judges can embed and view it. Target **3:15-3:45**: this leaves margin for live API latency while keeping the story focused. The recording must visibly demonstrate genuine Kiswahili-English code-mixing.

## Before recording

1. Pull the final submission branch and run the local quality gate.
2. Start a fresh terminal and set `SAHARA_API_KEY` without displaying it.
3. Confirm `ffmpeg -version` works in the same terminal; the demo decodes browser microphone audio
to canonical 16 kHz mono PCM and uploads it as AAC/M4A, a format already proven through the Sahara API.
4. Run `streamlit run app.py`.
5. Confirm the page states **Intron Sahara v2.5 · Swahili–English**.
6. Close terminals or windows that expose local paths, secrets or private benchmark data.
7. Test microphone permission.
8. Keep the benchmark table open separately for the evidence section.
9. Do not use a held-out benchmark clip as the live demo input.
10. Keep `docs/SautiForm_Africa_Benchmark_Report.pdf` open for the evidence section.
11. After recording, upload to YouTube as Public or Unlisted and verify playback in a signed-out/private browser window.

## Suggested narration

### 0:00–0:20 — Problem

**On screen:** SautiForm Africa title and a simple public-service form context.

**Narration:**

> Public-service forms are usually written as if people speak one language at a time. In practice, a
> Tanzanian user may describe their household in Kiswahili, use an English occupation term and name a
> public service in English in the same sentence. SautiForm Africa lets that person speak naturally
> while keeping them in control of the final structured record.

### 0:20–0:35 — Product architecture

**On screen:** Briefly show the workflow from the README.

**Narration:**

> The product uses Intron Sahara v2.5 for Swahili–English code-switching. Sahara produces the
> transcript, SautiForm extracts four form fields, checks what is missing, reads the structured record
> back and requires explicit confirmation. It does not make an eligibility decision or submit to a
> government system.

### 0:35–1:35 — Live Sahara demo

**On screen:** Streamlit application. Do not show the API key.

Record a fresh, clearly code-mixed utterance such as:

> Ninaishi Mbozi District, occupation yangu ni farmer, household ina watu sita, nataka birth
> certificate.

Click **Process response**.

**Narration while processing:**

> This is a live Sahara API call, not a prerecorded transcript.

When the transcript appears:

> Sahara returns the recognised response. SautiForm then converts the transcript into district,
> occupation, household size and service request.

Show the four editable fields.

If all extracted fields look correct:

> Even when the extraction looks correct, the record is not accepted automatically.

If one field is missing or wrong:

> Here the speech model has not recovered every administrative value correctly. SautiForm does not
> hide that failure. I can correct the field before confirming the record.

Make any required correction visibly.

Tick the confirmation checkbox only after reviewing the fields.

> The user explicitly confirms the read-back. The prototype stops here; it performs no external
> government submission.

## 1:35–2:25 — Benchmark evidence

**On screen:** Final four-model table from `docs/SautiForm_Africa_Benchmark_Report.pdf`.

**Narration:**

> I evaluated the same 24 frozen, consented Kiswahili–English recordings across Sahara, Whisper,
> Meta MMS and Meta Omnilingual ASR. Sahara achieved the best word error rate at 0.4592 and the
> fastest observed mean latency at 3.08 seconds. Whisper achieved the best character error rate and
> the best structured field accuracy, recovering 29 of 96 fields exactly. Sahara recovered 24 of 96.

Pause on the complete-form column.

> The most important result is that every model scored zero out of 24 on completely correct forms.
> That is why SautiForm is deliberately assistive rather than autonomous. A good transcript is not
> automatically a safe administrative record.

## 2:25–2:50 — Ethics and inclusion

**On screen:** Human-confirmation control, then short bullets from the Ethics & Inclusion Note.

**Narration:**

> The design minimises data, keeps private benchmark audio out of the public repository, does not
> infer missing sensitive information and requires human confirmation. Voice is intended to reduce
> language and typing friction, not to remove people's ability to see and correct what a system has
> captured.

## 2:50–3:05 — Close

**On screen:** Project name and repository.

**Narration:**

> SautiForm Africa combines Sahara's code-switching speech capability with a safety layer designed
> for structured public-service data. The next step is broader user testing and authorised service
> integration, while keeping clarification and human confirmation at the centre of the workflow.

## Recording guidance

- Record at 1080p if practical.
- Keep browser zoom high enough for the recognised transcript and fields to be readable.
- Use a clean browser window with no personal tabs visible.
- Never display the Sahara API key.
- Prefer one continuous live Sahara interaction so judges can see that the product is functional.
- If the live transcript contains an error, keep it in the video and demonstrate correction rather
  than rerecording solely to obtain a perfect transcript.
- Avoid claiming production deployment, government integration or measured population impact.
- Keep the four-model result table on screen long enough to read the key values.
- Keep the final video comfortably below 5:00; aim for 3:15-3:45.
- Upload as YouTube Public or Unlisted, never Private.

## Evidence to capture in the final recording

The finished video should visibly establish:

- SautiForm Africa is the product;
- Sahara is the speech backend;
- the input is genuinely Kiswahili–English code-switched speech;
- the transcript comes from a live audio interaction;
- four structured fields are produced;
- the fields are editable;
- confirmation is required;
- no external submission occurs;
- the four-model benchmark exists;
- model limitations are reported rather than hidden.
