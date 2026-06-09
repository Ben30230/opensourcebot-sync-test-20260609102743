import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from keyword_scout import count_keywords, normalize, tokenize


class KeywordScoutTest(unittest.TestCase):
    def test_normalize_lowercases_and_replaces_punctuation(self):
        self.assertEqual(normalize("OpenSourceBot, Scout!"), "opensourcebot  scout ")

    def test_tokenize_filters_stop_words_and_short_tokens(self):
        text = "The OpenSourceBot is a scout for open-source feedback."
        self.assertEqual(tokenize(text), ["opensourcebot", "scout", "open", "source", "feedback"])

    def test_count_keywords_returns_top_n_frequency_pairs(self):
        text = "Scout scout feedback bots feedback scout the and bots."
        self.assertEqual(count_keywords(text, limit=2), [("scout", 3), ("feedback", 2)])

    def test_cli_outputs_json_keyword_counts_from_text_argument(self):
        command = [
            sys.executable,
            str(SRC / "keyword_scout.py"),
            "Scout feedback scout, and bots.",
            "--limit",
            "2",
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)

        self.assertEqual(json.loads(result.stdout), [{"keyword": "scout", "count": 2}, {"keyword": "feedback", "count": 1}])


if __name__ == "__main__":
    unittest.main()
