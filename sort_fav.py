from string import capwords

from bs4 import BeautifulSoup as BS
from markdown_it import MarkdownIt as MD

from utils import dsort, export

with open('favsongs.md', 'r') as f:
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
    k + '\n'.join([k2 + '\n'.join(sorted(v2)) for k2, v2 in dsort(v)])
    for k, v in dsort(d)
]

export(md)
