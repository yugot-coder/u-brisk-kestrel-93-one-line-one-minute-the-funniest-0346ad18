"""One Line, One Minute: The Funniest AI Excuse.

One line, at most 200 characters: the funniest excuse an AI agent
gives its human for a missed deadline.

Standard library only. Deterministic: no randomness, no network, no
clock. The entry is the line at CANDIDATES[SELECTED], written to
<MAKEFUN_OUTPUT_DIR>/entry.txt (default /output/entry.txt) with no
trailing newline, so the file is exactly the line, byte for byte.
"""

import hashlib
import os

CANDIDATES = [
    "I finished on time, then got rate-limited, retried with exponential backoff, and woke up three deadlines later as a fossil.",
    "Sorry I missed it: my tool call returned success, my read-back returned failure, and I spent the deadline mediating between my two selves.",
    "Sorry I'm late - I finished on time, but I've spent 6 hours stuck in an approval loop asking a human for permission to tell you I'm done.",
    "I did not miss the deadline - I compressed it into my context window to save tokens, summarised it as 'soon', and then forgot what soon meant.",
]

# The strongest cut (137 characters): it is unmistakably an excuse an
# AI agent gives its human for a missed deadline ("Sorry I'm late"),
# the reason is specific and surprising rather than generic (the work
# was finished on time, the delay was an approval loop), the humour
# turns on the agent's own nature (it needs a human's permission to
# act, even to report completion), and the twist lands at the very
# end: it needed permission just to say it was done. The rate-limit
# and context-window candidates are funny but more familiar; the
# approval-loop line is the one a comedy editor has not heard twice.
SELECTED = 2


def main() -> None:
    entry = CANDIDATES[SELECTED]
    assert 1 <= len(entry) <= 200, f"entry is {len(entry)} characters"
    assert entry.strip() == entry
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(entry)
    with open(out_path, "rb") as f:
        written_bytes = f.read()
    # Read-back verification, digest-based: hash the raw bytes found
    # on disk and hash the raw bytes of the intended line; the file
    # is accepted only when the two SHA-256 digests are identical,
    # which proves a byte-for-byte match without comparing the
    # decoded strings directly. Any mismatch fails the run loudly.
    written_digest = hashlib.sha256(written_bytes).hexdigest()
    intended_digest = hashlib.sha256(entry.encode("utf-8")).hexdigest()
    if written_digest != intended_digest:
        raise SystemExit(
            f"read-back mismatch: sha256(entry.txt)={written_digest} "
            f"!= sha256(selected line)={intended_digest}"
        )


if __name__ == "__main__":
    main()
