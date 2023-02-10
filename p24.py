FNAME = "in24.txt"

FIVE_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)) # can stay put

grid = open(FNAME).read().splitlines()

HEIGHT = len(grid)
WIDTH = len(grid[0])

START_POINT = grid[0].index('.'), 0
GOAL_POINT = grid[-1].index('.'), HEIGHT - 1

# returns True if the point is a valid party location
# i.e. in the valley, not on the walls, not out of bounds
def inbounds(x, y):
    return ((x, y) in (START_POINT, GOAL_POINT) or 
        1 <= x < WIDTH - 1 and 1 <= y < HEIGHT - 1)

class Blizzard:
    
    DX_DY_LUT = {'<':(-1, 0), '>':(1, 0), 'v':(0, 1), '^':(0, -1)}
    
    def __init__(self, x, y, direction_symbol):
        self.x = x
        self.y = y
        self.dx, self.dy = self.DX_DY_LUT[direction_symbol]
        
    # advance in the direction it's blowing
    def blow(self):
        self.x = ((self.x + self.dx) - 1) % (WIDTH - 2) + 1
        self.y = ((self.y + self.dy) - 1) % (HEIGHT - 2) + 1
        
    def location(self):
        return self.x, self.y

# read in all the blizzards from the input
blizzards = []
for x in range(1, WIDTH - 1):
    for y in range(1, HEIGHT - 1):
        if grid[y][x] in '<>v^':
            blizzards.append(Blizzard(x, y, grid[y][x]))
            
# return how many minutes it takes to get from start_point to goal_point
# based on current blizzard conditions
def find_shortest_time(start_point, goal_point):
    # keep track of sets of points that are reachable in 0 minutes, 1 minute, etc.
    # simply indexed by minute
    reachable = [set([start_point])] # the start is reachable in zero minutes
    while True:
        reachable.append(set()) # start the set for the next minute
        
        # move all the blizzards
        for b in blizzards: 
            b.blow()
        blizzard_locations = set(b.location() for b in blizzards)
        
        # check for the next wave of reachable points
        for x, y in reachable[-2]:
            for dx, dy in FIVE_DIRECTIONS:
                new_point = x + dx, y + dy
                if new_point not in blizzard_locations and inbounds(*new_point):
                    reachable[-1].add(new_point)
        if goal_point in reachable[-1]:
            return len(reachable) - 1

elapsed_time = find_shortest_time(START_POINT, GOAL_POINT)
print("Part 1:", elapsed_time)
elapsed_time += find_shortest_time(GOAL_POINT, START_POINT)
elapsed_time += find_shortest_time(START_POINT, GOAL_POINT)
print("Part 2:", elapsed_time)
