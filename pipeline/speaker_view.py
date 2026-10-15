# usage: speaker_view.py <key> <Speaker>  -> <key>/view/: labelled podcasts reduced to <Speaker>'s turns
# (+ the prior turn's first 200 chars as context); every other file symlinked unchanged.
# Why: REWORK is ~60% other speakers; cutting them shrinks extraction ~2x and stops misattributed quotes.
# Speaker text is copied byte-exact so quotes still verify against the original file too.
import glob, os, re, sys
key, who = sys.argv[1], sys.argv[2]
base = os.path.join(os.path.expanduser(os.environ.get('PANTHEON_CORPUS', '~/pantheon-corpus')), key)
out = f'{base}/view'; os.makedirs(out, exist_ok=True)
# three label styles: "Jason: (00:01:08)", "Jason Fried:" alone, "Jason Fried (00:14):"
turn = re.compile(r'^([A-Z][\w .\'-]{0,40}?)(?: \(\d[\d:]*\))?:\s*(\(\d[\d:]*\))?\s*$')
for f in sorted(glob.glob(f'{base}/transcripts/*.txt')):
    name = os.path.basename(f); dst = f'{out}/{name}'
    if os.path.lexists(dst): os.remove(dst)
    lines = open(f, encoding='utf-8').read().split('\n')
    if 'speakers labelled' not in '\n'.join(lines[:6]):
        os.symlink(f, dst); continue
    hdr, body = [], []
    i = 0
    while i < len(lines) and lines[i].strip(): hdr.append(lines[i]); i += 1
    cur, prev, buf = None, None, []
    def flush():
        if cur and cur.split()[0] == who and buf:
            if prev: body.append(f'[context] {prev}')
            body.extend(buf); body.append('')
    for ln in lines[i:]:
        m = turn.match(ln)
        if m:
            flush()
            if cur and cur.split()[0] != who and buf: prev = f'{cur}: ' + ' '.join(x for x in buf[1:] if not x.startswith('('))[:200]
            cur, buf = m.group(1), [ln]
        elif cur: buf.append(ln)
    flush()
    if not body: continue  # episode where the speaker never talks: leave it out of the view
    hdr.append(f'VIEW: only {who} turns kept (+[context] = prior speaker, truncated); full text in ../transcripts/{name}')
    open(dst, 'w', encoding='utf-8').write('\n'.join(hdr) + '\n\n' + '\n'.join(body))
print('done', out)
