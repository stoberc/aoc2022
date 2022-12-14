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

# convert to a set to reduce amortized lookup time
# also removes all the duplicated end vertices from each segment
points = set(points) 

# lower limit beyond which we know sand will fall forever
maxy = max(y for x, y in points)

# where the floor is placed for Part 2
floory = maxy + 2

sand_counter = 0 # keep track of how many units of sand have settled

# try to add one unit of sand
# returns True if successful, or False if it would fall forever (Part 1)
# or if it would clog the source (Part 2)
def add_one_sand():
    global sand_counter
    sandx, sandy = 500, 0 # all sand originates here
    
    while sandy < floory:
        if (sandx, sandy + 1) not in points:
            sandy += 1
        elif (sandx - 1, sandy + 1) not in points:
            sandx, sandy = sandx - 1, sandy + 1
        elif (sandx + 1, sandy + 1) not in points:
            sandx, sandy = sandx + 1, sandy + 1
        else:
            points.add((sandx, sandy))
            sand_counter += 1
            if sandy == 0:
                return False
            return True
    return False
    
while add_one_sand():
    pass

print("Part 1:", sand_counter)

# insert the floor for Part 2
for x in range(500 - floory - 1, 500 + floory + 1):
    points.add((x, floory))
        
while add_one_sand():
    pass

print("Part 2:", sand_counter)
