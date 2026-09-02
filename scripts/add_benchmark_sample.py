"""Add one consented audio clip to a private benchmark workspace."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sautiform.benchmark.collection import add_benchmark_sample
from sautiform.forms.public_service import PublicServiceForm


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--sample-id", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--district", required=True)
    parser.add_argument("--occupation", required=True)
    parser.add_argument("--household-size", type=int, required=True)
    parser.add_argument("--service-request", required=True)
    parser.add_argument("--device", required=True)
    parser.add_argument("--noise", required=True)
    parser.add_argument("--country", default="Tanzania")
    parser.add_argument("--language-pair", default="sw-en")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data/private"),
        help=(
            "Private workspace root. Use a separate root such as "
            "data/private/heldout for final evaluation audio."
        ),
    )
    parser.add_argument(
        "--consented",
        action="store_true",
        help="Confirm that the speaker gave informed consent for this benchmark use.",
    )
    args = parser.parse_args()

    form = PublicServiceForm(
        district=args.district,
        occupation=args.occupation,
        household_size=args.household_size,
        service_request=args.service_request,
    )
    row = add_benchmark_sample(
        source_audio=args.audio,
        sample_id=args.sample_id,
        reference_transcript=args.transcript,
        form=form,
        device=args.device,
        noise=args.noise,
        consented=args.consented,
        country=args.country,
        language_pair=args.language_pair,
        root=args.root,
    )
    print("BENCHMARK_SAMPLE_ADDED=YES")
    print(json.dumps(row, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
