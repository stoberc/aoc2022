#import pdb

FNAME = "in1.txt"
    
def parse_line(line):
    return int(line)

chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
data = [sum([int(line) for line in chunk]) for chunk in chunks]

print("Part 1:", max(data))

data.sort()
print("Part 2:", sum(data[-3:]))

#pdb.set_trace()
