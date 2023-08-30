from bs4 import BeautifulSoup as BS
from markdown_it import MarkdownIt as MD

with open('favsongs.md', 'r') as f:
    md = f.read()
tags = BS(MD().render(md), 'lxml').find_all(['h1', 'h2', 'li'])

d = {}
for t in tags:
    name, text = t.name, t.text
    match name:
        case 'h1':
            h1 = text
            d[h1] = {}
        case 'h2':
            h2 = text
            d[h1][h2] = []
        case 'li':
            d[h1][h2].append(text)

md = ''
for k, v in dict(sorted(d.items())).items():
    md += f'# {k}\n'
    for k2, v2 in dict(sorted(v.items())).items():
        md += f'## {k2}\n'
        for i in sorted(v2):
            md += f'- {i}\n'

with open('_favsongs.md', 'w') as f:
    f.write(md)
