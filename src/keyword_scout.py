"""Small keyword frequency scout for CLI and library use."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
}


def normalize(text: str) -> str:
    """Lowercase text and replace non-alphanumeric separators with spaces."""
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def tokenize(text: str) -> list[str]:
    """Return normalized tokens after removing stop words and one-letter tokens."""
    return [
        token
        for token in normalize(text).split()
        if len(token) > 1 and token not in STOP_WORDS
    ]


def count_keywords(text: str, limit: int = 10) -> list[tuple[str, int]]:
    """Return the most common keyword frequency pairs."""
    return Counter(tokenize(text)).most_common(limit)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract top keyword frequencies from text.")
    parser.add_argument("text", help="Text to analyze.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum keywords to return.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = [
        {"keyword": keyword, "count": count}
        for keyword, count in count_keywords(args.text, args.limit)
    ]
    print(json.dumps(rows, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
