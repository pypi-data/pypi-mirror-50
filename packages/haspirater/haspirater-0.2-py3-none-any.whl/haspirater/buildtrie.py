#!/usr/bin/env python3

"""From a list of values (arbitrary) and keys (words), create a trie
representing this mapping"""

import json
import sys

# first item is a dictionnary from values to an int indicating the
# number of occurrences with this prefix having this value
# second item is a dictionnary from letters to descendent nodes
def empty_node():
  return [{}, {}]

def insert(trie, key, val):
  """Insert val for key in trie"""
  values, children = trie
  # create a new value, if needed
  if val not in values.keys():
    values[val] = 0
  # increment count for val
  values[val] += 1
  if len(key) > 0:
    # create a new node if needed
    if key[0] not in children.keys():
      children[key[0]] = empty_node()
    # recurse
    return insert(children[key[0]], key[1:], val)

if __name__ == '__main__':
  trie = empty_node()

  for line in sys.stdin.readlines():
    line = line.split()
    value = line[0]
    word = line[1].lower() if len(line) == 2 else ''
    # a trailing space is used to mark termination of the word
    # this is useful in cases where a prefix of a word is a complete,
    # different word with a different value
    insert(trie, word+' ', value)

  print(json.dumps(trie))

