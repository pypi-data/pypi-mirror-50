#!/usr/bin/env python3

"""Read json trie in stdin, keep majority value at each node, remove
useless leaf nodes and output trie to stdout"""

import json
import sys

trie = json.load(sys.stdin)

def get_majority(d):
  """What are the most probable values?"""
  mx = max(d.values())
  return [k for k in d.keys() if d[k] == mx]

def majority(trie):
  """Keep only the most probable values at each node"""
  if len(trie[1].keys()) == 0:
    # keep all options at leaf nodes
    trie[0] = list(trie[0].keys())
  else:
    trie[0] = get_majority(trie[0])
  useless = []
  for child in trie[1].keys():
    majority(trie[1][child])
    # if it is relabeled to our majority value and is a leaf, drop it
    if trie[1][child][0] == trie[0] and trie[1][child][1] == {}:
      useless.append(child)
  for child in useless:
    del(trie[1][child])

majority(trie)

print(json.dumps(trie))

