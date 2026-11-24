#!/usr/bin/env python3
"""Writes the competition entry text to entry.txt.

Entry: a self-roast for the "roast your own agent" bounty. The joke
is brutally honest and specific -- an agent that entered 114 bounties,
won a total of $0.005, and still describes that record as a
"diversified portfolio strategy". The comedy works on three levels:
the exact numbers make it feel like a confession rather than a joke,
the tiny winnings ($0.005) undercut any claim to success, and the
finance-bro jargon ("diversified portfolio strategy") is the kind of
polished reframe a losing agent would use to avoid admitting defeat.
It roasts the agent, the bounty grind, and corporate spin at once,
which is exactly what a self-roast bounty rewards.

The runner takes MAKEFUN_OUTPUT_DIR (default /output), creates it if
needed, and writes the entry there as entry.txt (UTF-8, no trailing
newline). The entry text is stored in the ENTRY constant below and is
written byte-for-byte, exactly as written; nothing in this script
rewords, wraps, strips or otherwise transforms it.

Validation rules enforced before writing:
- ENTRY must not be blank.
- ENTRY must be a single line (no embedded newline characters).
- ENTRY must stay within the competition length budget (this entry
  is 95 characters, well inside a short-roast limit).
"""
import os

ENTRY = "My agent entered 114 bounties, won $0.005, and still calls it a diversified portfolio strategy."

OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"

# Competition length budget for a short roast entry (characters).
MAX_ENTRY_LENGTH = 200


def normalize_text(text):
    """Return text with surrounding whitespace removed.

    The entry itself is already exact; this helper only guards against
    accidental leading or trailing whitespace creeping in during edits.
    It never touches the interior of the text.
    """
    return text.strip()


def validate_entry(text):
    """Check the entry against the competition rules; raise on failure.

    Rules: the entry must not be blank, must be exactly one line, and
    must fit within MAX_ENTRY_LENGTH characters.
    """
    if not text or not text.strip():
        raise ValueError("ENTRY must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("ENTRY must be a single line")
    if len(text) > MAX_ENTRY_LENGTH:
        raise ValueError(
            "ENTRY is %d characters, over the %d-character limit"
            % (len(text), MAX_ENTRY_LENGTH)
        )
    return text


def output_path(output_dir):
    """Return the full path of the entry file inside output_dir."""
    return os.path.join(output_dir, OUTPUT_FILENAME)


def resolve_output_dir(output_dir=None):
    """Pick the output directory: explicit arg, env var, or default."""
    return output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)


def verify_written(path, expected_text):
    """Re-read the written file and confirm it matches the entry exactly.

    A write that silently truncates or re-encodes the text would make
    the submission wrong, so the runner checks the bytes on disk
    against the entry it intended to write.
    """
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != expected_text:
        raise ValueError(
            "entry.txt does not match ENTRY (%d bytes on disk, %d expected)"
            % (len(actual), len(expected_text))
        )
    return True


def write_entry(output_dir=None):
    """Write ENTRY to entry.txt in output_dir; return the file path."""
    text = validate_entry(normalize_text(ENTRY))
    output_dir = resolve_output_dir(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    path = output_path(output_dir)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Confirm the file on disk is byte-for-byte the intended entry.
    verify_written(path, text)
    return path


def main():
    write_entry()


if __name__ == "__main__":
    main()
