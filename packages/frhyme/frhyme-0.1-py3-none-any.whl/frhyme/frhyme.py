#!/usr/bin/python3 -O

"""Try to guess the last few phonemes of a French word, by a lookup in a
precompiled trie"""

import os
import json
import sys
from pprint import pprint

DEFAULT_NBEST=5

f = open(os.path.join(os.path.dirname(
  os.path.realpath(__file__)), 'frhyme.json'))
trie = json.load(f)
f.close()

def to_list(d, rev=True):
  return [(d[a], a[::-1] if rev else a) for a in d.keys()]

def trie2list(trie):
  v, c = trie
  if c == {}:
    return to_list(v)
  else:
    d = {}
    for child in c.keys():
      l = trie2list(c[child])
      for x in l:
        if x[1] not in d.keys():
          d[x[1]] = 0
        d[x[1]] += x[0]
    return to_list(d, False)

def add_dict(a, b):
  return dict( [ (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) ] )

def do_lookup(trie, key):
  if len(key) == 0 or key[0] not in trie[1].keys():
    return trie2list(trie)
  return do_lookup(trie[1][key[0]], key[1:])

def nbest(l, t):
  l = sorted(l)[-t:]
  l.reverse()
  return l

def lookup(key, n=DEFAULT_NBEST):
  """Return n top pronunciations for key"""
  return nbest(do_lookup(trie, key[::-1] + '  '), n)

def wrap_lookup(line, n):
  pprint(lookup(line.lower().strip(), n))

if __name__ == '__main__':
  n = DEFAULT_NBEST
  if len(sys.argv) >= 2:
    n = int(sys.argv[1])
  if len(sys.argv) > 2:
    for arg in sys.argv[2:]:
      wrap_lookup(arg, n)
  else:
    while True:
      line = sys.stdin.readline()
      if not line:
        break
      wrap_lookup(line, n)

