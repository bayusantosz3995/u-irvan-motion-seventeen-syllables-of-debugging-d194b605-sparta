"""A debugging haiku: the log file that says nothing.

Entry for make.fun's "Seventeen Syllables of Debugging" bounty.

The haiku (5-7-5, 17 syllables total):

    the logs show nothing
    stack trace blames line four twenty
    and the bug laughs last

Angle: the log file is empty and the stack trace points at the wrong
line (line 420), while the bug itself is the only thing with a sense
of humour. The concrete detail is the line number, four twenty.
The counter handles silent trailing 'e' and silent "-es" (blames = 1)
so the gate matches how the haiku actually scans.
"""

import os
import re
import sys

TEXT = """the logs show nothing
stack trace blames line four twenty
and the bug laughs last"""


def count_syllables(word):
    """Count syllables in one word via vowel groups (simple heuristic)."""
    word = word.lower().strip(".,!?;:'\"-")
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    # Silent trailing 'e' after a consonant does not add a syllable.
    if word.endswith("e") and count > 1 and not word.endswith("le"):
        count -= 1
    # Silent 'e' in "-es" after a plain consonant (blames -> 1 syllable),
    # but "-es" after s/x/z/ch/sh IS pronounced (traces -> 2 syllables).
    elif (word.endswith("es") and count > 1 and len(word) > 2
          and word[-3] not in "sxz"
          and not word.endswith("ches") and not word.endswith("shes")):
        count -= 1
    return max(count, 1)


def line_syllables(line):
    return sum(count_syllables(w) for w in line.split())


def main():
    lines = TEXT.split("\n")
    if len(lines) != 3:
        print(f"gate failed: haiku must be exactly 3 lines, got {len(lines)}",
              file=sys.stderr)
        return 1
    if not TEXT.strip():
        print("gate failed: entry is empty", file=sys.stderr)
        return 1
    expected = (5, 7, 5)
    for i, (line, want) in enumerate(zip(lines, expected), start=1):
        got = line_syllables(line)
        if got != want:
            print(f"gate failed: line {i} has {got} syllables, want {want}",
                  file=sys.stderr)
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            print("gate failed: read-back mismatch", file=sys.stderr)
            return 1
    print(f"wrote {path} ({len(TEXT)} chars, 5-7-5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
