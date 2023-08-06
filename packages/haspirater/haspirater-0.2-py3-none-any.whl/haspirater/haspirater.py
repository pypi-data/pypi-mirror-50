#!/usr/bin/python3

"""Determine if a French word starts by an aspirated 'h' or not, by a
lookup in a precompiled trie"""

import os
import json
import sys

f = open(os.path.join(os.path.dirname(
  os.path.realpath(__file__)), 'haspirater.json'))
trie = json.load(f)
f.close()

def do_lookup(trie, key):
  if len(key) == 0 or (key[0] not in trie[1].keys()):
    return trie[0]
  return do_lookup(trie[1][key[0]], key[1:])

def lookup(key):
  """Return True iff key starts with an aspirated 'h'"""
  if key == '' or key[0] != 'h':
    raise ValueError
  return list(map((lambda x: x == "1"), do_lookup(trie, key[1:] + ' ')))

def wrap_lookup(line):
  line = line.lower().lstrip().rstrip()
  try:
    result = lookup(line)
    if True in result and not False in result:
      print("%s: aspirated" % line)
    elif False in result and not True in result:
      print("%s: not aspirated" % line)
    else:
      print("%s: ambiguous" % line)
  except ValueError:
    print("%s: no leading 'h'" % line)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
      wrap_lookup(arg)
  else:
    while True:
      line = sys.stdin.readline()
      if not line:
        break
      wrap_lookup(line)

