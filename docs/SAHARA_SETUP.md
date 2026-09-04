# Sahara Setup

Sahara credentials and endpoint details are intentionally absent from the repository. The official
participant onboarding material is the authority for the endpoint, authentication mechanism, model
identifier, upload field and response shape.

The public CodeSwitch Africa material confirms participant access to Sahara v2.5 APIs and developer
onboarding, but it does not publish the participant request contract. Do not infer that contract
from the public benchmarking repository: that repository benchmarks a local NeMo Sahara model rather
than the participant API.

## Local configuration

Set the participant values in the active shell or a local untracked environment file. Never commit
credentials.

The adapter can match either bearer-token or raw API-key authentication and allows the multipart
field, model field, extra headers, extra form values and transcript response path to be configured.

```text
SAHARA_API_URL=
SAHARA_API_KEY=
SAHARA_AUTH_HEADER=Authorization
SAHARA_AUTH_SCHEME=Bearer
SAHARA_FILE_FIELD=file
SAHARA_MODEL_FIELD=model
SAHARA_MODEL=
SAHARA_RESPONSE_TEXT_PATH=text
SAHARA_TIMEOUT_SECONDS=120
SAHARA_HEADERS_JSON={}
SAHARA_FORM_JSON={}
```

Examples:

- bearer authentication: `SAHARA_AUTH_HEADER=Authorization`, `SAHARA_AUTH_SCHEME=Bearer`;
- raw API-key header: `SAHARA_AUTH_HEADER=x-api-key`, `SAHARA_AUTH_SCHEME=`;
- nested transcript response: `SAHARA_RESPONSE_TEXT_PATH=data.transcript`;
- additional participant form parameter: `SAHARA_FORM_JSON={"language":"sw-en"}`.

Do not use these examples as claims about the real participant contract. Use only the values supplied
by Intron onboarding or the challenge support channel.

## Configuration preflight

After setting the official participant values:

```powershell
python scripts/check_sahara_ready.py
```

This validates configuration without sending audio and never prints the API key.

## Development-only smoke test

Use exactly one development clip, for example one of `tz-sw-en-001` through `tz-sw-en-010`.
Never debug the Sahara contract using the frozen `tz-sw-en-h001` through `tz-sw-en-h024` set.

Example:

```powershell
python scripts/check_sahara_ready.py `
  --audio data/private/audio/tz-sw-en-001.ogg
```

The script explicitly blocks audio under `data/private/heldout/` and held-out sample IDs.

Required success markers:

```text
SAHARA_CONFIG=PASS
SAHARA_SMOKE_TEST=PASS
SAHARA_BACKEND=sahara
SAHARA_TRANSCRIPT=...
```

Only after this succeeds should Sahara be run against the frozen 24-row benchmark.

## Final held-out run

The final Sahara benchmark must use the unchanged manifest:

```text
data/private/heldout/benchmark_manifest.jsonl
SHA-256=794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

Run:

```powershell
python scripts/run_benchmark.py `
  --manifest data/private/heldout/benchmark_manifest.jsonl `
  --backend sahara `
  --output benchmark_results_final_sahara.json `
  --expected-manifest-sha256 794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448
```

Do not change the references, parser or Sahara configuration after inspecting held-out output.
