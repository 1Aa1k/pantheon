#!/usr/bin/env python3
"""Search one persona's transcript corpus for passages relevant to a question.

Usage: search.py <persona|all> <term> [term ...] [--top N] [--width CHARS]
Ranks fixed-size windows by how many DISTINCT terms they contain (then total hits),
keeps at most 2 windows per file so one long podcast cannot crowd out the rest,
and prints them with the file name so quotes can be tagged [file]. Whitespace is
collapsed first because YouTube captions break lines mid-sentence.
Output is bounded (--top, default 12) so it is safe to read into context.
"""
import re, sys, os, glob, tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_TOP, MAX_WIDTH = 40, 1500
CORPUS = os.path.expanduser(os.environ.get("PANTHEON_CORPUS", "~/pantheon-corpus"))


def load_personas():
    with open(os.path.join(HERE, "..", "personas.toml"), "rb") as f:
        return tomllib.load(f)


def windows(text, terms, width):
    low = text.lower()
    hits = sorted(m.start() for t in terms for m in re.finditer(re.escape(t), low))
    used_until = -1
    for pos in hits:
        if pos < used_until:
            continue
        start = max(0, pos - width // 3)
        chunk = low[start:start + width]
        distinct = sum(1 for t in terms if t in chunk)
        total = sum(chunk.count(t) for t in terms)
        yield distinct, total, text[start:start + width]
        used_until = start + width


def main(argv):
    args, top, width = [], 12, 600
    it = iter(argv)
    for a in it:
        if a == "--top":
            top = min(int(next(it)), MAX_TOP)
        elif a == "--width":
            width = min(int(next(it)), MAX_WIDTH)
        else:
            args.append(a)
    if len(args) < 2:
        sys.exit(__doc__)
    personas = load_personas()
    who, terms = args[0], [t.lower() for t in args[1:]]
    keys = list(personas) if who == "all" else [who]
    for k in keys:
        if k not in personas:
            sys.exit(f"unknown persona {k!r}; known: {', '.join(personas)}")
    results = []
    for k in keys:
        tdir = os.path.join(CORPUS, os.path.expanduser(personas[k]["transcripts"]))
        if not os.path.isdir(tdir):
            print(f"[{k}] no corpus at {tdir} - build it with pipeline/ first", file=sys.stderr)
            continue
        for path in glob.glob(os.path.join(tdir, "*")):
            text = re.sub(r"\s+", " ", open(path, errors="ignore").read())
            best = sorted(windows(text, terms, width), reverse=True)[:2]
            for d, t, snip in best:
                results.append((d, t, k, os.path.basename(path), snip))
    results.sort(key=lambda r: (r[0], r[1]), reverse=True)
    for d, t, k, name, snip in results[:top]:
        print(f"--- [{k}] {name}  (terms {d}/{len(terms)}, hits {t})\n{snip}\n")
    if not results:
        print("no matches; try synonyms or fewer terms")


if __name__ == "__main__":
    main(sys.argv[1:])
