import re

FNAME = "in4.txt"
    
def parse_line(line):
    return [int(i) for i in re.findall('\d+', line)] # grab all the numbers

# check if the interval [a, b] is a subset of the interval [c, d]
# or vice versa
def contains(a, b, c, d):
    return a <= c and b >= d or c <= a and d >= b
    
# check if the interval [a, b] intersects the interval [c, d]
def overlaps(a, b, c, d):
    return b >= c and a <= d

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

print("Part 1:", sum([contains(*i) for i in data]))
print("Part 2:", sum([overlaps(*i) for i in data]))
