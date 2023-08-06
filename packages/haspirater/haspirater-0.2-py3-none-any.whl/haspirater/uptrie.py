#!/usr/bin/env python3

"""Read json trie in stdin, make internal node decisions and output json dump to
stdout"""

import itertools
import operator
import json
import sys

trie = json.load(sys.stdin)

def uptrie(trie):
  """Make internal node decisions if possible"""
  for child in trie[1].values():
    uptrie(child)
  decided_children = [(list(t[0].items())[0][0], t) for t in trie[1].values() if
          len(t[0].keys()) == 1]
  dchild_g = {}
  for (x, y) in decided_children:
      if x not in dchild_g.keys():
          dchild_g[x] = []
      dchild_g[x].append(y)
  sums = [(x, len(y)) for (x, y) in dchild_g.items()]
  if len(sums) == 0:
    return
  best = max(sums, key=operator.itemgetter(1))
  if best[1] >= 2:
    # compress here
    trie.append(best[0])
    nchildren = {}
    for key, child in trie[1].items():
      if len(child[0].keys()) != 1 or list(child[0].items())[0][0] != best[0]:
        nchildren[key] = child
    trie[1] = nchildren

uptrie(trie)

print(json.dumps(trie))

