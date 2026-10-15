# usage: split.py <key>  -> bundles/<key>_NN.list, ~65k words per batch
import glob, os, sys
key = sys.argv[1]
# prefer <key>/view/ (speaker-filtered, see speaker_view.py) when it exists
d = os.path.join(os.path.expanduser(os.environ.get('PANTHEON_CORPUS', '~/pantheon-corpus')), key)
fs = sorted(glob.glob(f'{d}/view/*.txt' if os.path.isdir(f'{d}/view') else f'{d}/transcripts/*.txt'))
b, cur, w = [], [], 0
for f in fs:
    n = len(open(f, encoding='utf-8', errors='replace').read().split())
    if cur and w + n > 65000: b.append(cur); cur, w = [], 0
    cur.append(f); w += n
if cur: b.append(cur)
for i, x in enumerate(b, 1): open(f'bundles/{key}_{i:02d}.list', 'w').write('\n'.join(x) + '\n')
print(key, len(fs), 'files', len(b), 'batches')
