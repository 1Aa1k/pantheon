# Merge task (one person) -> notes/<key>_profile.md

Inputs: every notes/<key>_batchNN.md, plus <key>/STATUS.md and <key>/catalog.csv for dates/provenance.
If other profiles already exist in notes/, read one's headings first and match its shape.

Write notes/<key>_profile.md:
- Title line + 3-line scope (sources, years, words) and a "Source caveats" section (notes-not-verbatim files,
  third-party/auto transcripts, edited transcripts, approximate dates, duplicates of one event).
- "The core of how they operate": top 10-15 patterns ranked by DISTINCT EVENTS/SOURCES (not quote count), one line each.
- Sections: 1 Reasoning methods, 2 Decision rules, 3 How they build, 4 How they run orgs, 5 Money/strategy/selling,
  6 Worldview, 7 Habits. Each pattern: ### name, one plain sentence, 2-3 best verbatim quotes [file, year],
  recurrence (n sources, earliest-latest year).
- 8 Shifts over time (dated, both sides quoted). 9 Contradictions / tensions. 10 Where they would clash with the other personas
  (one line each, cite their own quote; for the others cite notes/*_profile.md).
- 11 "For a small operator" (set this to your own situation): 5-10 transfers, each tied to a pattern above,
  marked (direct) when they addressed it or (extrapolation) when applied.
- Dedupe across batches. Never invent quotes. Re-verify EVERY quote you keep with
  `grep -F -c "<6-10 word substring>" <file>` (join wrapped lines if needed: tr '\n' ' ' < file | grep -F -c ...);
  drop any that return 0. Keep the (notes, not verbatim) tag where a batch had it. Label critics and political
  assertions as such. End with `VERIFIED: <n> checked, <m> fixed, <k> dropped`.
Edit only notes/<key>_profile.md. Return: path, line count, pattern count, VERIFIED line, top 5 patterns.
