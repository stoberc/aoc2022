FNAME = "in14.txt"

points = [] # just keep a list all points that are occupied by anything

def parse_line(line):
    vertices = line.split(' -> ')
    for i in range(len(vertices) - 1):
        start, end = vertices[i], vertices[i + 1]
        sx, sy = [int(i) for i in start.split(',')]
        ex, ey = [int(i) for i in end.split(',')]
        assert sx == ex or sy == ey
        if sx == ex:
            for y in range(min(sy, ey), max(sy, ey) + 1):
                points.append((sx, y))
        else:
            assert sy == ey
            for x in range(min(sx, ex), max(sx, ex) + 1):
                points.append((x, sy))
        
for line in open(FNAME).read().splitlines():
    parse_line(line)

points = set(points) # convert to a set to reduce amortized lookup time
maxy = max(y for x, y in points)

source = 500, 0

# try to add one unit of sand
# returns True if successful, or False if it would fall forever
def add_one_sand():
    sandx, sandy = 500, 0
    
    while sandy < maxy:
        if (sandx, sandy + 1) not in points:
            sandy += 1
        elif (sandx - 1, sandy + 1) not in points:
            sandx, sandy = sandx - 1, sandy + 1
        elif (sandx + 1, sandy + 1) not in points:
            sandx, sandy = sandx + 1, sandy + 1
        else:
            points.add((sandx, sandy))
            return True
    return False
    
i = 0
while add_one_sand():
    i += 1

print("Part 1:", i)

floory = maxy + 2

for x in range(500 - 2 * floory, 500 + 2 * floory):
    points.add((x, floory))
    
def add_one_sand():
    sandx, sandy = 500, 0
    
    while (500, 0) not in points:
        if (sandx, sandy + 1) not in points:
            sandy += 1
        elif (sandx - 1, sandy + 1) not in points:
            sandx, sandy = sandx - 1, sandy + 1
        elif (sandx + 1, sandy + 1) not in points:
            sandx, sandy = sandx + 1, sandy + 1
        else:
            points.add((sandx, sandy))
            return True
    return False
    
while add_one_sand():
    i += 1

print("Part 2:", i)