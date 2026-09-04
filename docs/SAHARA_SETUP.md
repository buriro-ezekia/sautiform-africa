# Sahara Setup

## Authoritative challenge API

SautiForm uses the Intron Voice API for the Sahara CodeSwitch Africa challenge.

The official participant path is:

1. sign in at `https://voice.intron.io`;
2. open the **Developer** tab;
3. copy the API key;
4. use the Intron Voice documentation at `https://docs.voice.intron.io`.

For synchronous speech-to-text, the documented endpoint is:

```text
POST https://infer.voice.intron.io/file/v1/upload/sync
Authorization: Bearer <API_KEY>
```

Required multipart fields are:

```text
audio_file_name=<non-unique name>
audio_file_blob=<audio file>
```

For SautiForm's Kiswahili-English benchmark, the documented code-switched language selection is:

```text
use_language_asr_input=sw
```

The transcript is returned at:

```text
data.audio_transcript
```

The synchronous endpoint accepts WAV, MP3, MP4, M4A, OGG, WebM and FLAC and supports audio up to
120 seconds. The final SautiForm held-out clips are all well below this limit.

## Benchmark configuration

For the final ASR comparison SautiForm uses:

```text
SAHARA_API_URL=https://infer.voice.intron.io/file/v1/upload/sync
SAHARA_LANGUAGE=sw
SAHARA_DISABLE_LLM_CORRECTIONS=TRUE
SAHARA_RESPONSE_TEXT_PATH=data.audio_transcript
SAHARA_TIMEOUT_SECONDS=120
```

`use_disable_llm_corrections=TRUE` is deliberately selected before any Sahara held-out inference.
The purpose is to benchmark the speech recogniser rather than add a language-model correction stage
that the Whisper, MMS and Omnilingual comparators do not receive. This setting must remain fixed once
the first held-out Sahara result is inspected.

Do not enable category-specific post-processing for the benchmark. SautiForm performs its own
deterministic downstream field extraction so every ASR system is evaluated through the same form
pipeline.

## Local API key

Never commit the key. In PowerShell:

```powershell
$env:SAHARA_API_KEY = "<YOUR_PRIVATE_INTRON_API_KEY>"
```

The remaining benchmark settings already have repository defaults.

## Configuration preflight

```powershell
python scripts/check_sahara_ready.py
```

Required marker:

```text
SAHARA_CONFIG=PASS
```

The script never prints the API key.

## Development-only smoke test

Use exactly one development clip, not a held-out clip:

```powershell
$dev = Get-Content .\data\private\benchmark_manifest.jsonl |
  Select-Object -First 1 |
  ConvertFrom-Json

python scripts/check_sahara_ready.py `
  --audio "$($dev.audio_path)"
```

The script rejects paths under `data/private/heldout/` and IDs matching
`tz-sw-en-h001` through `tz-sw-en-h024`.

Required markers:

```text
SAHARA_CONFIG=PASS
SAHARA_SMOKE_TEST=PASS
SAHARA_BACKEND=sahara
SAHARA_TRANSCRIPT=...
```

Use development audio only to verify connectivity, authentication and the documented request/response
contract. Do not tune the parser or references to Sahara output.

## Final held-out run

After the development smoke test succeeds, keep the Sahara settings fixed and run:

```powershell
$manifest = "data/private/heldout/benchmark_manifest.jsonl"
$hash = "794eddca2d656b176c0064dd7edd92da61b79266d113287de47247dc72a16448"

python scripts/run_benchmark.py `
  --manifest $manifest `
  --backend sahara `
  --output benchmark_results_final_sahara.json `
  --expected-manifest-sha256 $hash
```

The upload endpoint is documented at 30 requests per minute. The benchmark runner is sequential and
contains only 24 clips, but any rate-limit response must be treated as an operational API failure,
not as a model-quality result.

After the run, independently re-check the frozen manifest SHA-256 before accepting the result.


## Development smoke-test lock

The Intron Sahara synchronous API integration was successfully verified on one development-only
recording before any Sahara held-out inference. The request completed with the fixed benchmark
configuration above and returned a valid Sahara transcript. The observed smoke-test latency was
16.55983063 seconds. This result is operational evidence only and is not part of the held-out
benchmark.

From this point onward, Sahara endpoint, language selection, LLM-correction setting, response path,
parser rules and benchmark references are locked for the final 24-clip Sahara evaluation.
