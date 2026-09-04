# SautiForm Africa — Submission Checklist

## Challenge deliverables

| Deliverable | Repository evidence | Status |
|---|---|---|
| Solution Description | `docs/SUBMISSION_SOLUTION_DESCRIPTION.md` | Complete |
| Demo video plan | `docs/DEMO_VIDEO_SCRIPT.md` | Script complete; recording pending |
| Code / technical documentation | `README.md`, `docs/PHASE_2_SPECIFICATION.md`, setup and benchmark docs | Complete |
| Benchmark Report, Sahara + 3 comparators | `docs/BENCHMARK_REPORT.md` | Complete |
| Ethics & Inclusion Note | `docs/ETHICS_AND_INCLUSION_NOTE.md` | Complete |
| Optional benchmark audio | Private held-out workspace | Do not publish unless consent permits |

## Final benchmark state

```text
Sahara        = FINAL
Whisper       = FINAL
MMS           = FINAL
Omnilingual   = FINAL
held-out n    = 24
manifest SHA  = 794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

No further parser or model tuning should be performed from held-out results.

## Before recording the demo

- Pull the latest Phase 2 branch.
- Run `ruff check .`.
- Run `pytest -q`.
- Run Python compilation.
- Confirm `SAHARA_API_KEY` is set locally and is not shown on screen.
- Launch `streamlit run app.py`.
- Confirm the product UI is fixed to Intron Sahara v2.5.
- Use fresh development/demo speech, not a held-out recording.

## Before final submission

- Record and review the demo video.
- Check that the video shows a real Sahara audio request.
- Ensure the repository contains no API key, private benchmark audio or per-clip held-out output.
- Confirm the GitHub repository link opens without authentication if a public link is required.
- Review the final Solution Description for any submission-form character limit.
- Copy benchmark values from the committed report rather than retyping from memory.
- Submit only once if the challenge access token permits a single final submission.
- Preserve a local copy of the final submission text and video URL.

## Claims that are safe to make

- SautiForm supports Kiswahili–English code-switching.
- The live product uses the Intron Sahara API.
- Four speech systems were evaluated on the same 24 frozen held-out recordings.
- Sahara achieved the best WER and observed mean latency in this benchmark.
- Whisper achieved the best CER and field exact-match score.
- All four systems scored 0/24 complete forms.
- The prototype requires correction/read-back/explicit confirmation.
- The prototype does not submit records to a government system.

## Claims to avoid

Do not claim:

- production deployment;
- government endorsement or integration;
- identity verification;
- legal eligibility decisions;
- population-scale impact;
- demographic fairness;
- offline Sahara inference;
- perfect form completion;
- that the 24-clip benchmark represents all Tanzanian or African speakers.
