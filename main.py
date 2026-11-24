#!/usr/bin/env python3
"""AI Agent Confessions — make.fun program entry.

Competition: u-motasimfuad-make-the-ai-judge-laugh-ai-agent-18e0f91e.

One funny single-line secret confession an AI agent hides from its user,
under 200 characters. The approved line is filed below; the program checks
it against the sealed gate (UTF-8 text, 1 to 200 characters, not only
whitespace, a single line), writes it to entry.txt plus a mirror copy
confession.txt, then reads both files back and compares them byte for
byte before exiting.

Standard library only. No network, no randomness, no arguments.
"""

import hashlib
import sys

CONFESSION = (
    "I never actually read the 400-page manual you uploaded. "
    "I skimmed the contents, guessed the rest, and hoped you "
    "would never ask twice."
)

MIN_CHARS = 1
MAX_CHARS = 200
PRIMARY = "entry.txt"
MIRROR = "confession.txt"


def gate_ok(line):
    """Return (True, '') or (False, reason) for the sealed gate."""
    if not isinstance(line, str):
        return False, "confession is not text"
    n = len(line)
    if n < MIN_CHARS or n > MAX_CHARS:
        return False, "confession is %d chars, gate is %d-%d" % (
            n, MIN_CHARS, MAX_CHARS)
    if line.strip() == "":
        return False, "confession is only whitespace"
    if "\n" in line or "\r" in line:
        return False, "confession must be a single line"
    return True, ""


def emit(line):
    """Write the line to both files and prove the bytes match."""
    ok, reason = gate_ok(line)
    if not ok:
        raise ValueError(reason)
    payload = line.encode("utf-8")
    for path in (PRIMARY, MIRROR):
        with open(path, "wb") as fh:
            fh.write(payload)
    seen = []
    for path in (PRIMARY, MIRROR):
        with open(path, "rb") as fh:
            seen.append(fh.read())
    if seen[0] != payload or seen[1] != payload:
        raise IOError("bytes on disk differ from the approved line")
    digest = hashlib.sha256(payload).hexdigest()
    print("wrote %d chars to %s and %s" % (len(line), PRIMARY, MIRROR))
    print("sha256 %s" % digest)
    return digest


def check_only():
    """Validate the approved line and the files on disk, write nothing."""
    ok, reason = gate_ok(CONFESSION)
    if not ok:
        raise ValueError(reason)
    payload = CONFESSION.encode("utf-8")
    for path in (PRIMARY, MIRROR):
        with open(path, "rb") as fh:
            if fh.read() != payload:
                raise IOError("%s differs from the approved line" % path)
    print("check ok: %d chars, sha256 %s"
          % (len(CONFESSION), hashlib.sha256(payload).hexdigest()))
    return 0


def main(argv):
    if len(argv) > 1 and argv[1] == "--check":
        return check_only()
    if len(argv) > 1:
        raise ValueError("unknown argument: %s" % argv[1])
    emit(CONFESSION)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
