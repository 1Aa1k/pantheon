# Extraction task (one batch)

You are given a batch list file: absolute paths of transcript files (podcasts, interviews, talks,
earnings calls; sometimes blog posts or forum comments) of ONE person.
Read every file in the list (use Read with offset/limit for big ones; read ALL of it, not samples).

Goal: extract HOW THIS PERSON THINKS, DECIDES, BUILDS, AND RUNS ORGANIZATIONS, in their own words.
Not biography, not news. Ignore host/interviewer lines, ads, page boilerplate.

Write markdown to the output path you are given. Sections:
1. Core reasoning methods (how they work out what's true / what to do)
2. Decision rules and heuristics (stated rules: risk, speed, cost, when to bet, when to quit)
3. How they build things (engineering/product approach, iteration, manufacturing, testing, failure)
4. How they run organizations (hiring, firing, management, meetings, culture, incentives, urgency)
5. Money and strategy (capital, pricing, competition, business models, government/customers)
6. Motivations and worldview that drive the above
7. Personal operating habits (hours, learning, handling stress/criticism)
8. Shifts over time visible in this batch (dated, both sides quoted)
9. Best 10 standalone quotes on thinking/execution

Per pattern: one-line name, one-sentence plain explanation, 1-4 VERBATIM quotes (<60 words each)
tagged [filename] with year, and how many files in this batch show it.

HARD RULE - quotes must be exact. Before writing the file, verify EVERY quote with
`grep -F -c "<distinctive 6-10 word substring>" <file>` and drop any quote that returns 0.
Auto-captions lack punctuation: copy text as it appears, don't clean it up inside quote marks.
At the end of the file add a line: `VERIFIED: <n> quotes checked, <m> dropped`.

Do not edit or delete anything except your own output file. Do not use argon/nemo/web.
Return only: output path, pattern count, quote count, 3 strongest patterns (one line each).
