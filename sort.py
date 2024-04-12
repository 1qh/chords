#!/usr/bin/env python3

from string import capwords

from bs4 import BeautifulSoup as BS
from markdown_it import MarkdownIt as MD
from text_unidecode import unidecode


def dsort(d: dict):
  return dict(sorted(d.items(), key=lambda x: unidecode(x[0]))).items()


def export(l: list, fn: str):
  with open(fn, 'w') as f:
    f.write('\n'.join(l))


def l2md(l: list):
  return '\n' + ''.join(sorted([f'- {i}\n' for i in l], key=lambda x: unidecode(x))) + '\n'


favsongs = []
haschord = []

# =============================================================================

file = 'favsongs.md'
with open(file, 'r') as f:
  md = f.read()

tags = BS(MD().render(md), 'lxml').find_all(['h1', 'h2', 'li'])

d = {}
h1, h2 = '', ''
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
      favsongs.append(text)
md = [
  k + '\n'.join([k2 + '\n'.join(sorted(v2, key=lambda x: unidecode(x))) for k2, v2 in dsort(v)])
  for k, v in dsort(d)
]
export(md, file)

# =============================================================================

file = 'README.md'
with open(file, 'r') as f:
  md = '\n' + f.read()

h1 = [i.strip() for i in md.split('\n# ') if i.strip()]
d = {}
for i in h1:
  k = i.split('\n')[0]
  k = f'\n\n# {k}\n\n'
  child = '\n'.join(i.split('\n')[1:])
  h2 = [j.strip() for j in child.split('\n## ') if j]
  d[k] = {}
  for j in h2:
    if k2 := capwords(j.split('\n')[0]):
      song = k2.split('-')[0].strip()
      if '/' in song:
        haschord.extend([i.strip() for i in song.split('/')])
      else:
        haschord.append(song)
      k2 = f'\n## {k2}\n'
      d[k][k2] = '\n'.join(j.split('\n')[1:])

md = [k + '\n'.join([k2 + v2 for k2, v2 in dsort(v)]) for k, v in dsort(d)]

export(md, file)

# =============================================================================

only_chord = set(haschord) - set(favsongs)
only_fav = set(favsongs) - set(haschord)
mutual = set(favsongs) & set(haschord)
only_chord, only_fav, mutual = l2md(only_chord), l2md(only_fav), l2md(mutual)

md = f'# Not fav yet{only_chord}# Chord not available{only_fav}# Fav has chord{mutual}'
with open('_.md', 'w') as f:
  f.write(md)
