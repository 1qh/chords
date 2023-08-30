with open('README.md', 'r') as f:
    md = '\n' + f.read()

h1 = [i.strip() for i in md.split('\n# ') if i]
d = {}
for i in h1:
    k = i.split('\n')[0]
    child = '\n'.join(i.split('\n')[1:])
    h2 = [j.strip() for j in child.split('\n## ') if j]
    d[k] = {}
    for j in h2:
        k2 = j.split('\n')[0]
        d[k][k2] = '\n'.join(j.split('\n')[1:])

md = ''
for k, v in dict(sorted(d.items())).items():
    md += f'\n# {k}\n'
    for k2, v2 in dict(sorted(v.items())).items():
        md += f'\n## {k2}\n{v2}\n'

with open('_README.md', 'w') as f:
    f.write(md.strip())
