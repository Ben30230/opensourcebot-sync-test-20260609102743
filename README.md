# OpenSourceBot Keyword Scout

OpenSourceBot Keyword Scout is a small Python CLI for extracting frequent keywords
from short text snippets. It is intentionally dependency-free and uses only the
Python standard library.

The scorer can now surface repeated two-word phrases, using frequency and phrase
length to rank higher-signal terms ahead of one-off keywords.

## Usage

```bash
python3 src/keyword_scout.py "Scout feedback scout, and bots." --limit 2
```

Example output:

```json
[{"keyword": "scout", "count": 2}, {"keyword": "feedback", "count": 1}]
```

Weighted phrase scoring:

```bash
python3 src/keyword_scout.py "Open source feedback helps open source maintainers." --scored --limit 1
```

## Development

Run the test suite with:

```bash
python3 -m unittest discover -s tests
```
