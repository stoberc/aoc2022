import pdb
from collections import defaultdict
from aoc_utils import *
import re

FNAME = "in3.txt"
    
def parse_line(line):
    l = len(line) // 2
    return line[:l], line[l:]
    #return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers

def common(a, b):
    x = set(a).intersection(set(b))
    assert len(x) == 1
    return list(x)[0]
    
#chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
#data = [[parse_line(line) for line in chunk] for chunk in chunks]

data = [parse_line(line) for line in open(FNAME).read().splitlines()] # in chunks[0]]

#data = [int(i) for i in open(FNAME).read().split(',')]

d = [common(*i) for i in data]

def score(letter):
    if ord('a') <= ord(letter) <= ord('z'):
        return ord(letter) - ord('a') + 1
    else:
        return ord(letter) - ord('A') + 1 + 26

print("Part 1:", sum([score(i) for i in d]))

data = [a + b for a, b in data]

data2 = []
while len(data) > 0:
    x = []
    x.append(data.pop(0))
    x.append(data.pop(0))
    x.append(data.pop(0))
    data2.append(x)

#pdb.set_trace()

def score_group(a, b, c):
    a = set(a)
    b = set(b)
    c = set(c)
    x = a.intersection(b).intersection(c)
    assert len(x) == 1
    return score(list(x)[0])

print("Part 2:", sum([score_group(*i) for i in data2]))

pdb.set_trace()
    