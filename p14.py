FNAME = "in14.txt"

points = [] # just keep a list all points that are occupied by anything

def parse_line(line):
    line = line.split(' -> ')
    for i in range(len(line) - 1):
        start, end = line[i], line[i + 1]
        sx, sy = [int(i) for i in start.split(',')]
        ex, ey = [int(i) for i in end.split(',')]
        assert sx == ex or sy == ey
        if sx == ex:
            dx = 0
            dy = 1 if sy < ey else -1
        else:
            assert sy == ey
            dy = 0
            dx = 1 if sx < ex else -1
        points.append((sx, sy))
        while sx != ex or sy != ey:
            sx += dx
            sy += dy
            points.append((sx, sy))
        
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
