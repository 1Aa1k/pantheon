# Pantheon

A Claude Code skill that puts a question to a panel of simulated founders and
investors, each built from their own public words: Elon Musk, Palmer Luckey,
Paul Graham, Peter Thiel, Jeff Bezos, Charlie Munger, Tobi Lütke, Jason Fried
and Alex Hormozi.

Each persona runs as its own subagent. It reads a profile of how that person
reasons, searches their transcript corpus, and answers in their voice. Every
load-bearing claim is backed by a verbatim quote that has been grep-checked
against the source file, or is tagged `(extrapolation)`. The personas then read
each other's answers and argue, and the moderator ends with a verdict: what
they agree on, where they split and why, concrete moves, and which answers rest
on the weakest ground.

> **These are simulations, not the people.** They are built from public
> statements and are not affiliated with, endorsed by or reviewed by anyone
> named here. Treat every answer as a study aid. A quote is only as good as its
> source file.

## What is (and isn't) in this repo

- `skill/`: the skill itself (`SKILL.md`, `personas.toml`, `scripts/search.py`).
- `pipeline/`: task specs and helpers for building a corpus and profile per person.

**No transcripts and no profiles are included.** They are other people's
copyrighted words. You build your own corpus from freely posted sources with
`pipeline/`. Until you do, the personas have nothing to quote from.

## Install

```sh
git clone https://github.com/1Aa1k/pantheon
cp -r pantheon/skill ~/.claude/skills/pantheon
export PANTHEON_CORPUS=~/pantheon-corpus   # optional, this is the default
```

Requires Python 3.11+ (`tomllib`).

## Build a persona

Corpus layout under `$PANTHEON_CORPUS`:

```
<key>/transcripts/*.txt      one file per source, with SOURCE/DATE/TYPE header lines
<key>/STATUS.md              coverage and gaps
notes/<key>_batchNN.md       extraction notes
notes/<key>_profile.md       the merged profile the persona reads
sessions/                    saved panel transcripts
```

1. **Gather.** Give a Claude subagent `pipeline/GATHER_TASK.md` with the person's
   key. It collects freely posted text: essays, letters, transcripts. It never
   bypasses paywalls or logins, and it uses no pirated books.
2. **Split** into batches of about 65k words: `python3 pipeline/split.py <key>`.
   It writes `bundles/<key>_NN.list` in the current directory. For podcasts with
   labelled speakers, run `pipeline/speaker_view.py <key> "<Speaker Name>"` first
   to cut the other voices.
3. **Extract.** Run one subagent per batch with `pipeline/AGENT_TASK.md`. Each
   one writes `notes/<key>_batchNN.md` and grep-verifies its quotes.
4. **Merge.** Run one subagent with `pipeline/MERGE_TASK.md` to produce
   `notes/<key>_profile.md`. It dedupes by distinct event and re-verifies every
   quote.

To add someone new, build their corpus the same way and add a block to
`personas.toml`.

## Use

```
/pantheon <question>                   default panel: the 4-5 most relevant personas
/pantheon all <question>               all nine
ask elon and munger: <question>        exactly that panel
/pantheon only thiel,pg,hormozi <q>    exactly that panel
only elon <question>                   one persona, no crosstalk
/pantheon quick <question>             no subagents; answered from the profiles
/pantheon rounds 2 <question>          extra crosstalk rounds (max 3)
```

## License

MIT for the code and docs in this repo. This license covers nothing you
gather into your own corpus.
