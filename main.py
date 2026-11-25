"""boss6: stamp office. Weighs the one word about the boss and bins it."""
import enum
import functools
import json
import os
import sys
from pathlib import Path

LIMIT = 30


class Slot(enum.Enum):
    WORD = "entry.txt"
    BIN = "out"


@functools.singledispatch
def weigh(x):
    return 0


@weigh.register
def _(x: str):
    body = x.strip()
    return len(body) if body else 0


def pull(root: Path):
    return (root / Slot.WORD.value).read_text(encoding="utf-8").strip()


def bin_it(word: str, target: Path):
    target.mkdir(parents=True, exist_ok=True)
    sheet = target / Slot.WORD.value
    sheet.write_bytes(word.encode("utf-8"))
    return sheet


def main():
    root = Path(__file__).resolve().parent
    word = pull(root)
    span = weigh(word)
    ok = 1 <= span <= LIMIT
    where = bin_it(word, Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or Slot.BIN.value)) if ok else None
    print("VERDICT", json.dumps({"office": "boss-stamp-r1", "span": span, "keep": ok, "bin": str(where)}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
