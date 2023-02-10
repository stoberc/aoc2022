from collections import defaultdict

FNAME = "in23.txt"

# dx, dy for eight adjacent spots in grid
EIGHT_WAYS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
    
base_grid = [list(i) for i in open(FNAME).read().splitlines()]
grid = defaultdict(lambda: '.')
for x in range(len(base_grid[0])):
    for y in range(len(base_grid)):
        grid[(x, y)] = base_grid[y][x]

# print the grid for debug
def render():
    minx = min(x for x, y in grid)
    maxx = max(x for x, y in grid)
    miny = min(y for x, y in grid)
    maxy = max(y for x, y in grid)  
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[(x, y)], end='')
        print()
    print()

# if the way is clear in the chosen cardinal direction,
# log the intent of moving that way
# returns True if that was possible, else False
def move_north(x, y):
    global sources, destinations
    if '.' == grid[(x - 1, y - 1)] == grid[(x, y - 1)] == grid[(x + 1, y - 1)]:
        sources.append((x, y))
        destinations.append((x, y - 1))
        return True
    return False
        
def move_south(x, y):
    global sources, destinations
    if '.' == grid[(x - 1, y + 1)] == grid[(x, y + 1)] == grid[(x + 1, y + 1)]:
        sources.append((x, y))
        destinations.append((x, y + 1))
        return True
    return False
        
def move_west(x, y):
    global sources, destinations
    if '.' == grid[(x - 1, y - 1)] == grid[(x - 1, y)] == grid[(x - 1, y + 1)]:
        sources.append((x, y))
        destinations.append((x - 1, y))
        return True
    return False

def move_east(x, y):
    global sources, destinations
    if '.' == grid[(x + 1, y - 1)] == grid[(x + 1, y)] == grid[(x + 1, y + 1)]:
        sources.append((x, y))
        destinations.append((x + 1, y))
        return True
    return False
    
movement_functions = [move_north, move_south, move_west, move_east]
    
def round():
    global sources, destinations, movement_functions
    sources = [] # elves would like to move from these points
    destinations = [] # to these points
    
    movement = False # keep track of if any elf has moved for Part 2
    
    # need to separate these steps and first find elf locations
    # because grid doesn't like being changed during iteration
    elf_locations = []
    for point in grid:
        if grid[point] == '#':
            elf_locations.append(point)
        
    for x, y in elf_locations:
        # elf stays put if all adjacent spots are empty
        if all(grid[(x + dx, y + dy)] == '.' for dx, dy in EIGHT_WAYS):
            continue
            
        for move_func in movement_functions:
            if move_func(x, y):
                break
                    
    # perform any moves that would not result in a collision
    for s, d in zip(sources, destinations):
        if destinations.count(d) == 1:
            grid[s] = '.'
            grid[d] = '#'
            movement = True
    
    movement_functions = movement_functions[1:] + [movement_functions[0]]
    return movement
    
    
for _ in range(10):
    round()

elf_locations = []
for point in grid:
    if grid[point] == '#':
        elf_locations.append(point)
            
minx = min(x for x, y in elf_locations)
maxx = max(x for x, y in elf_locations)
miny = min(y for x, y in elf_locations)
maxy = max(y for x, y in elf_locations)

rectangle_area = (maxx - minx + 1) * (maxy - miny + 1)
print("Part 1:", rectangle_area - len(elf_locations))

roundcount = 11 # assuming it'll always take at least ten rounds already past
while round():
    roundcount += 1
print("Part 2:", roundcount)
