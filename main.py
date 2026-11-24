"""Two Days of Quiet Dread.

Writes one code review comment — a single line of at most 140 characters
that approves a pull request while carrying quiet existential dread — to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt for local runs).

Python 3.13 standard library only. Deterministic, no network, no secrets.
The entry is self-checked against the competition gate before it is written:
UTF-8 text, 1 to 140 characters, a single line, not only whitespace.
"""

import os
import sys

# The chosen comment (see CANDIDATES.md for the full field of 10 and the
# scoring that picked it, 25/25): the biggest dread imaginable dismissed
# with the flattest ticket language. "Approved. Ship it." is real review
# voice; scoping cosmic annihilation out of a PR is the fresh turn.
ENTRY_PARTS = (
    "Approved. Ship it.",
    "The heat death of the universe is not in scope for this PR.",
)

MAX_CHARS = 140


def build_entry():
    """Join the comment's beats into the single submitted line."""
    return " ".join(ENTRY_PARTS)


def check_gate(text):
    """Enforce the competition gate; raise ValueError on any failure."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
    else:
        if not 1 <= len(text) <= MAX_CHARS:
            failures.append(
                "entry is %d characters, gate allows 1-%d" % (len(text), MAX_CHARS)
            )
        if text.strip() == "":
            failures.append("entry is only whitespace")
        if "\n" in text or "\r" in text:
            failures.append("entry must be a single line")
        try:
            text.encode("utf-8")
        except UnicodeEncodeError:
            failures.append("entry is not valid UTF-8")
    if failures:
        raise ValueError("; ".join(failures))
    return text


def main():
    entry = check_gate(build_entry())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts the file's characters, so the
    # written bytes are exactly the 78-character line, nothing more.
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(entry)
    print("wrote %s (%d characters)" % (path, len(entry)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
