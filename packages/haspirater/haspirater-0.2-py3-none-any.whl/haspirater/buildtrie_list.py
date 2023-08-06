#!/usr/bin/env python3

"""From a list of values (arbitrary) and keys (words), create a trie
representing this mapping"""

# this modified version is used by plint
# see https://a3nm.net/git/plint

import haspirater.buildtrie
import json
import sys

trie = buildtrie.empty_node()

for line in sys.stdin.readlines():
  line = line.split()
  value = line[0]
  word = line[1:]
  buildtrie.insert(trie, word+['-', '-'], value)

print(json.dumps(trie))

