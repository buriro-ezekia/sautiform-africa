"""Meta MMS adapter with an explicit target-language adapter."""
from __future__ import annotations

import os
import time
from pathlib import Path

from sautiform.asr.base import TranscriptResult


class MMSBackend:
    """Run MMS using a declared language adapter instead of the default language."""

    name = "mms"

    def __init__(
        self,
        model_id: str = "facebook/mms-1b-all",
        target_lang: str | None = None,
    ) -> None:
        try:
            from transformers import AutoProcessor, Wav2Vec2ForCTC, pipeline
        except ImportError as exc:
            raise RuntimeError("Install the 'mms' optional dependency") from exc

        self.target_lang = target_lang or os.getenv("MMS_TARGET_LANG", "swa")
        processor = AutoProcessor.from_pretrained(
            model_id,
            target_lang=self.target_lang,
        )
        model = Wav2Vec2ForCTC.from_pretrained(
            model_id,
            target_lang=self.target_lang,
            ignore_mismatched_sizes=True,
        )
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
        )

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        result = self.pipe(str(audio_path))
        text = result["text"] if isinstance(result, dict) else str(result)
        return TranscriptResult(
            text.strip(),
            self.name,
            time.perf_counter() - start,
        )
