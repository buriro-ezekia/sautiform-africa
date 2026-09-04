"""Meta Omnilingual ASR adapter for the fourth challenge benchmark system."""
from __future__ import annotations

import os
import time
from pathlib import Path

from sautiform.asr.base import TranscriptResult


class OmniASRBackend:
    """Run the reference Omnilingual ASR inference pipeline."""

    name = "omni"

    def __init__(self, model_card: str | None = None) -> None:
        try:
            from omnilingual_asr.models.inference.pipeline import ASRInferencePipeline
        except ImportError as exc:
            raise RuntimeError("Install the 'omni' optional dependency") from exc

        self.model_card = model_card or os.getenv(
            "OMNIASR_MODEL_CARD",
            "omniASR_CTC_300M_v2",
        )
        self.pipeline = ASRInferencePipeline(model_card=self.model_card)

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        outputs = self.pipeline.transcribe([str(audio_path)], batch_size=1)
        if not outputs or not isinstance(outputs[0], str):
            raise RuntimeError("Omnilingual ASR returned no text transcription")
        return TranscriptResult(
            outputs[0].strip(),
            self.name,
            time.perf_counter() - start,
        )
