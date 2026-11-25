#!/usr/bin/env python3
"""The Excuse That Almost Works — make.fun entry.

Writes the one line a gamer texts the boss to skip work during GTA 6
launch week to <output>/entry.txt (the directory the grader names in
MAKEFUN_OUTPUT_DIR, /output when it names none).

The line is fixed and deterministic: the same text on every run, no
network, no secrets, nothing read from the environment except the output
directory. The gamer is Juror 7: jury duty is the one excuse a tired
manager cannot schedule around, and the final clause — no phones allowed,
they said pack lunch — is the boring detail that makes it airtight.
"""

import os
import sys

# Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-140
# characters, not only white space. Fail loudly so a bad line never
# ships silently.
MAX_CHARS = 140
MAX_WORDS = 20


def check_line(line):
    """Refuse any line that would fail the gate, before writing it."""
    if not line or not line.strip():
        print("ERROR: entry line is empty or whitespace-only", file=sys.stderr)
        sys.exit(1)
    if "\n" in line or "\r" in line:
        print("ERROR: entry must be a single line", file=sys.stderr)
        sys.exit(1)
    if len(line) > MAX_CHARS:
        print(
            "ERROR: entry is %d chars, over the %d-char limit"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        sys.exit(1)
    if len(line.split()) > MAX_WORDS:
        print(
            "ERROR: entry is %d words, over the %d-word limit"
            % (len(line.split()), MAX_WORDS),
            file=sys.stderr,
        )
        sys.exit(1)


def check_written(path, line):
    """Read the file back: it must be byte-for-byte the entry line."""
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        print(
            "ERROR: %s holds %d chars, expected %d"
            % (path, len(written), len(line)),
            file=sys.stderr,
        )
        sys.exit(1)


LINE = (
    "Jury duty, I'm juror 7, trial starts Monday, "
    "no phones allowed, they said pack lunch."
)


def main():
    check_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    check_written(path, LINE)
    print(LINE)


if __name__ == "__main__":
    main()
