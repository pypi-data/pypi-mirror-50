#!/usr/bin/env python3

"""Takes json as input with labels [value1, value2] and produces dot,
usage: trie2dot.py prefix value1 value2"""

import json
import sys
from math import log

trie = json.load(sys.stdin)

free_id = 0

def cget(d, k):
  try:
    if k in d.keys():
      return d[k]
    else:
      return 0
  except AttributeError:
    # we have a list, not a dictionary
    # this happens after majoritytrie.py
    if k in d:
      return 1
    else:
      return 0

def int2strbyte(i):
  s = hex(i).split('x')[1]
  if len(s) == 1:
    return '0' + s
  else:
    return s

def fraction2rgb(fraction):
  n = int(255*fraction)
  return int2strbyte(n)+'00'+int2strbyte(255 - n)

def total(x):
  key, node = x
  try:
    return sum(node[0].values())
  except AttributeError:
    # we have only one value, not a dictionary
    return 1

def to_dot(trie, prefix=''):
  global free_id

  values, children = trie
  my_id = free_id
  free_id += 1
  count = cget(values, v1) + cget(values, v2)
  fraction = cget(values, v2) / count

  print("%d [label=\"%s\",color=\"#%s\",penwidth=%d]" % (my_id, prefix,
    fraction2rgb(fraction), 1+int(log(count))))

  for (key, child) in sorted(children.items(), key=total, reverse=True):
    i = to_dot(child, prefix+key)
    print("%d -> %d [penwidth=%d]" % (my_id, i,
      1+int(log(total((None, child))))))

  return my_id

print("digraph G {\naspect=\"1\"\n")
prefix = sys.argv[1]
v1 = sys.argv[2]
v2 = sys.argv[3]
to_dot(trie, prefix)
print("}")
