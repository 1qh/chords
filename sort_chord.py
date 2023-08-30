from string import capwords

from utils import dsort, export

with open('README.md', 'r') as f:
    md = '\n' + f.read()

h1 = [i.strip() for i in md.split('\n# ') if i]
d = {}
for i in h1:
    k = i.split('\n')[0]
    k = f'# {k}\n\n'
    child = '\n'.join(i.split('\n')[1:])
    h2 = [j.strip() for j in child.split('\n## ') if j]
    d[k] = {}
    for j in h2:
        k2 = capwords(j.split('\n')[0])
        k2 = f'## {k2}\n'
        d[k][k2] = '\n'.join(j.split('\n')[1:])

md = [k + '\n'.join([k2 + v2 for k2, v2 in dsort(v)]) for k, v in dsort(d)]

export(md)
