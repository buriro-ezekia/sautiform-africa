# Benchmark Protocol

Use the same consented audio set for every model. Do not alter references between model runs.

For each sample record:

- language pair;
- domain;
- accent/country;
- device type;
- noise condition;
- reference transcript;
- reference structured fields.

Report four model backends for the main challenge: Sahara plus three comparison systems. For each backend report WER, CER, field exact-match accuracy, complete-form accuracy and latency where available.

The principal downstream metric is complete-form accuracy. Field exact match is the diagnostic metric. WER and CER explain transcription quality but should not be treated as sufficient evidence that the form workflow works.

Do not report mock-backend results as competition evidence. The mock backend exists solely for deterministic software tests.
