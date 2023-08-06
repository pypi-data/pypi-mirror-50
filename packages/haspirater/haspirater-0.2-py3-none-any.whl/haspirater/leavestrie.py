#!/usr/bin/env python3

"""Read json trie in stdin, produce leaves and values
argv[1] is 1 or -1 to reverse the label sequence or not"""

import json
import sys

trie = json.load(sys.stdin)

def leaves(trie, prefix="", provisional=None):
  """Keep only the most probable values at each node"""
  if len(trie[1].keys()) == 0:
    assert(len(trie[0].keys()) == 1)
    k, v = trie[0].popitem()
    if (k != provisional):
      # does not agree with provisional decision so far
      print("%s\t%s" % (k, prefix[::int(sys.argv[1])]))
  # decided nodes
  if len(trie) == 3 and trie[2]:
    if (trie[2] != provisional):
      # does not agree with provisional decision so far
      print("%s\t%s" % (trie[2], prefix[::int(sys.argv[1])]))
  if len(trie) == 3:
    provisional = trie[2]
  for child in trie[1].keys():
    leaves(trie[1][child], prefix + child, provisional)

leaves(trie)

