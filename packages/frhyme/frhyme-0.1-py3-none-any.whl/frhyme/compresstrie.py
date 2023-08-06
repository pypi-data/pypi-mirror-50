#!/usr/bin/env python3

"""Read json trie in stdin, trim unneeded branches and output json dump
to stdout"""

import json
import sys

trie = json.load(sys.stdin)

def compress(trie):
  """Compress the trie"""
  ref = None
  num = 0
  ok = True
  if trie[0] != {}:
    if len(trie[0].keys()) > 1:
      return None
    ref = list(trie[0].keys())[0]
    num = trie[0][ref]
  for child in trie[1].values():
    x = compress(child)
    if not ok or x == None:
      ok = False
      continue
    r, n = x
    if ref == None:
      ref = r
    if ref != r:
      ok = False
    num += n
  if not ok:
    return None
  trie[0] = {}
  trie[0][ref] = num
  trie[1] = {}
  #print(ref, file=sys.stderr)
  return ref, num

compress(trie)

print(json.dumps(trie))

