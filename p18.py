import pdb

FNAME = "in18.txt"

points = set()
def parse_line(line):
  points.add(tuple([int(i) for i in line.split(',')]))

for line in open(FNAME).read().splitlines():
  parse_line(line)

exposed = 0

for x, y, z in points:
  for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
    if (x + dx, y + dy, z + dz) not in points:
      exposed += 1

print("Part 1:", exposed)

wrapper_points = set()

# find some point on the the top of the blob
maxz = max(z for x, y, z in points)
x, y, z = 0, 0, 0
for x, y, z in points:
  if z == maxz:
    break
    
wrapper_points.add((x, y, z + 1))

expandq = [(x, y, z + 1)]
while expandq:
  x, y, z = expandq.pop(0)
  for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
    adjx, adjy, adjz = x + dx, y + dy, z + dz
    if (adjx, adjy, adjz) not in points and (adjx, adjy, adjz) not in wrapper_points:
      for ddx, ddy, ddz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0), (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1), (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1), (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)):
        if (adjx + ddx, adjy + ddy, adjz + ddz) in points:
          wrapper_points.add((adjx, adjy, adjz))
          expandq.append((adjx, adjy, adjz))
          #print(len(wrapper_points), len(expandq))
          break

exposed = 0
for x, y, z in points:
  for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
    if (x + dx, y + dy, z + dz) in wrapper_points:
      exposed += 1

print("Part 2:", exposed) 

pdb.set_trace()
