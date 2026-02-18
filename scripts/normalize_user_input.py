from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.modules.user_input.api import normalize_user_input


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Active user input payload.")
    parser.add_argument(
        "--input-file",
        required=True,
        help="Path to input JSON relative to repository root.",
    )
    parser.add_argument(
        "--output-file",
        default="",
        help="Optional output JSON path relative to repository root.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat normalization errors as failure (non-zero exit).",
    )
    args = parser.parse_args()

    input_path = ROOT / args.input_file
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    result = normalize_user_input(payload, strict=args.strict)

    output = {
        "normalized": result.normalized.model_dump(),
        "report": result.report.model_dump(),
    }

    if args.output_file:
        output_path = ROOT / args.output_file
    else:
        output_path = input_path.with_name(f"{input_path.stem}.normalized.json")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Warnings: {len(result.report.warnings)}")
    print(f"Errors: {len(result.report.errors)}")

    if args.strict and result.report.errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

