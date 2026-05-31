"""Command-line interface for Beauty Content Kit."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from .generator import generate_ideas, preview_lines, supported_features


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="beauty-content-kit",
        description="Generate trust-first beauty short-video content angles.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate content ideas.")
    generate.add_argument(
        "--feature",
        default="all",
        choices=(*supported_features(), "all"),
        help="Feature area to generate for.",
    )
    generate.add_argument(
        "--count",
        default=5,
        type=int,
        help="Number of ideas to generate.",
    )
    generate.add_argument(
        "--format",
        default="text",
        choices=("text", "json"),
        help="Output format.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        try:
            ideas = generate_ideas(args.feature, args.count)
        except ValueError as exc:
            parser.error(str(exc))

        if args.format == "json":
            print(json.dumps([idea.to_dict() for idea in ideas], ensure_ascii=False, indent=2))
        else:
            print("\n".join(preview_lines(ideas)))
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
