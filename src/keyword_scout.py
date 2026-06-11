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


def keyword_density(text: str, limit: int = 10) -> list[dict[str, float | int | str]]:
    """Return top keywords with their share of all non-stop-word tokens."""
    tokens = tokenize(text)
    total = len(tokens)
    if total == 0:
        return []
    return [
        {
            "keyword": keyword,
            "count": count,
            "share": count / total,
        }
        for keyword, count in Counter(tokens).most_common(limit)
    ]


def score_keywords(text: str, limit: int = 10) -> list[dict[str, float | int | str]]:
    """Return scored keywords and adjacent two-word phrases."""
    tokens = tokenize(text)
    singles = Counter(tokens)
    phrases = Counter(" ".join(pair) for pair in zip(tokens, tokens[1:]))
    scores: dict[str, dict[str, float | int | str]] = {}

    for keyword, count in singles.items():
        scores[keyword] = {
            "keyword": keyword,
            "count": count,
            "score": float(count * (1 + min(len(keyword), 12) / 12)),
        }

    for phrase, count in phrases.items():
        if count < 2:
            continue
        scores[phrase] = {
            "keyword": phrase,
            "count": count,
            "score": float(count * 3),
        }

    return sorted(
        scores.values(),
        key=lambda row: (-float(row["score"]), str(row["keyword"])),
    )[:limit]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract top keyword frequencies from text.")
    parser.add_argument("text", help="Text to analyze.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum keywords to return.")
    parser.add_argument("--scored", action="store_true", help="Return weighted keyword and phrase scores.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.scored:
        rows = score_keywords(args.text, args.limit)
    else:
        rows = [
            {"keyword": keyword, "count": count}
            for keyword, count in count_keywords(args.text, args.limit)
        ]
    print(json.dumps(rows, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
