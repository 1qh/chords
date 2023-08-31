from string import capwords

from bs4 import BeautifulSoup as BS
from markdown_it import MarkdownIt as MD
from unidecode import unidecode


def dsort(d: dict):
    return dict(sorted(d.items(), key=lambda x: unidecode(x[0]))).items()


def export(l: list, fn: str):
    with open(fn, 'w') as f:
        f.write('\n'.join(l))


# =============================================================================

file = 'favsongs.md'
with open(file, 'r') as f:
    md = f.read()

tags = BS(MD().render(md), 'lxml').find_all(['h1', 'h2', 'li'])

d = {}
for t in tags:
    name, text = t.name, capwords(t.text)
    match name:
        case 'h1':
            h1 = f'# {text}\n'
            d[h1] = {}
        case 'h2':
            h2 = f'## {text}\n'
            d[h1][h2] = []
        case 'li':
            d[h1][h2].append(f'- {text}')
md = [
    k
    + '\n'.join(
        [k2 + '\n'.join(sorted(v2, key=lambda x: unidecode(x))) for k2, v2 in dsort(v)]
    )
    for k, v in dsort(d)
]
export(md, file)

# =============================================================================

file = 'README.md'
with open(file, 'r') as f:
    md = '\n' + f.read()

h1 = [i.strip() for i in md.split('\n# ') if i]
d = {}
for i in h1:
    k = i.split('\n')[0]
    k = f'\n\n# {k}\n\n'
    child = '\n'.join(i.split('\n')[1:])
    h2 = [j.strip() for j in child.split('\n## ') if j]
    d[k] = {}
    for j in h2:
        k2 = capwords(j.split('\n')[0])
        k2 = f'\n## {k2}\n'
        d[k][k2] = '\n'.join(j.split('\n')[1:])

md = [k + '\n'.join([k2 + v2 for k2, v2 in dsort(v)]) for k, v in dsort(d)]

export(md, file)
