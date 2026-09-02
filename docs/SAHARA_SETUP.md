# Sahara Setup

Sahara credentials and endpoint details are intentionally absent from the repository. The official
participant onboarding material is the authority for the endpoint, authentication mechanism, model
identifier, upload field and response shape.

## Local configuration

Create a local `.env` or set environment variables in the active shell. Never commit credentials.
The adapter currently expects bearer-token authentication and exposes these configuration values:

```text
SAHARA_API_URL=
SAHARA_API_KEY=
SAHARA_FILE_FIELD=file
SAHARA_MODEL=
SAHARA_RESPONSE_TEXT_PATH=text
```

`SAHARA_RESPONSE_TEXT_PATH` accepts a dot-separated path such as `data.text` when the transcript is
nested in a JSON response.

## Verification sequence

Before running the benchmark matrix:

1. confirm the current participant API contract;
2. set the environment variables locally;
3. test one short consented audio file with the Sahara CLI backend;
4. inspect the returned transcript manually;
5. only then run Sahara against the frozen benchmark manifest.

Do not change the reference transcript or reference fields to match Sahara output. Benchmark
references must remain model-independent.
