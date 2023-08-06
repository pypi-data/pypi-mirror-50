#!/usr/bin/env python3

"""Read json trie in stdin, trim unneeded branches and output json dump
to stdout"""

import json
import sys

trie = json.load(sys.stdin)

def compress(trie):
  """Compress the trie"""
  if len(trie[0].keys()) <= 1:
    # no need for children, there is no more doubt
    trie[1] = {}
  for child in trie[1].values():
    compress(child)

compress(trie)

print(json.dumps(trie))

