FNAME = "in22.txt"

# convert a facing value into dx, dy values of direction
DX_DY_LUT = {0:(1, 0), 1:(0, 1), 2:(-1, 0), 3:(0, -1)}

FACING_LUT = {0:"RIGHT", 1:"DOWN", 2:"LEFT", 3:"UP"}

grid, raw_instructions = open(FNAME).read().split('\n\n')

grid = grid.splitlines()
HEIGHT = len(grid)
# some rows shorter than others because they don't bother w/ trailing spaces
WIDTH = max(len(i) for i in grid) 

# for now we'll just pad partial rows with spaces to get them full width to
# make the algo simpler, but we could actually leave as is with a slightly 
# faster but more complex algo
for i in range(len(grid)):
    tail_length = WIDTH - len(grid[i])
    grid[i] += ' ' * tail_length
    
# starting coordinates and orientation
x = grid[0].index('.')
y = 0
facing = 0

# parse the instruction stream one character at a time
# sifting grouped numeric values from L/R
instructions = [raw_instructions[0]]
for i in raw_instructions[1:]:
    if i in 'LR':
        instructions.append(i)            
    elif instructions[-1] in 'LR':
        instructions.append(i)
    else:
        instructions[-1] += i
for i in range(len(instructions)):
    if instructions[i] not in 'LR':
        instructions[i] = int(instructions[i])
    
# move the sprite forward up to nmoves or collision
def move(nmoves):
    global x, y
    dx, dy = DX_DY_LUT[facing]
    for _ in range(nmoves):
        nextx, nexty = x + dx, y + dy
        nextx %= WIDTH
        nexty %= HEIGHT
        
        # move past any empty spaces
        # could make this a bit faster by just precomputing a single time,
        # but I suspect it won't matter much
        while grid[nexty][nextx] == ' ':
            nextx += dx
            nexty += dy
            nextx %= WIDTH
            nexty %= HEIGHT
            
        if grid[nexty][nextx] == '#':
            return
        
        x, y = nextx, nexty
    
def go():
    global facing
    for i in instructions:
        if i == 'L':
            facing = (facing - 1) % 4
        elif i == 'R':
            facing = (facing + 1) % 4
        else:
            move(i)
go()
    
def hash():
    return 1000 * (y + 1) + 4 * (x + 1) + facing
print("Part 1:", hash())

# Part 2 - I will assume that all inputs match mine in structure, i.e. is laid
# out with faces like this, with each face 50x50:
#  01
#  2
# 34
# 5
# a more generalized solver for any folding would be substantially more complex

# reset to start
x = grid[0].index('.')
y = 0
facing = 0

def move(nmoves):
    global x, y, facing
    for _ in range(nmoves):
        nextx, nexty, nextfacing = get_next(x, y, facing)
        #print(f" Attempting to move to ({nextx},{nexty}) on face {getface(nextx, nexty)} facing {FACING_LUT[facing]}")
            
        if grid[nexty][nextx] == '#':
            #print(" CAN'T!!!")
            return
        
        #print(" SUCCESS!!!")
        assert grid[nexty][nextx] == '.'
        x, y, facing = nextx, nexty, nextfacing
        
# indicate which numbered face (per diagram above) a particular coordinate is on
# useful (and only necessary) for debugging
def getface(x, y):
    if 0 <= y < 50 and 50 <= x < 100:
        return 0
    elif 0 <= y < 50 and 100 <= x < 150:
        return 1
    elif 50 <= y < 100 and 50 <= x < 100:
        return 2
    elif 100 <= y < 150 and 0 <= x < 50:
        return 3
    elif 100 <= y < 150 and 50 <= x < 100:
        return 4
    elif 150 <= y < 200 and 0 <= x < 50:
        return 5
    else:
        raise ValueError(f"Coordinates map to face unknown: ({x}, {y})")
    
# feels silly/inelegant, but we'll just handle each edge separately
# explaining these edges really benefits from a 3D model (which I made)
# there's a whole lot of debug in here that I used to trace out a typo
# decided to just leave it in since it required extensive restructuring
def get_next(x, y, facing):
    startx, starty = x, y # debug
    dx, dy = DX_DY_LUT[facing]
    #print(f"Trying to move {FACING_LUT[facing]} from ({x}, {y}), end='')
    #print(f"on face {getface(x, y)} to ", end='')
    x += dx
    y += dy
    #print(f"({x},{y})")
    
    # stayed in easy bounds
    if 0 <= x < WIDTH and 0 <= y < HEIGHT and grid[y][x] != ' ':
        return x, y, facing
      
    # moved up off of top of face 0 onto left of face 5
    if y == -1 and 50 <= x < 100:
        assert facing == 3
        assert getface(startx, starty) == 0
        nextx, nexty, nextfacing = 0, x + 100, 0
        assert getface(nextx, nexty) == 5
        
    # moved up off of top of face 1 onto bottom of face 5
    elif y == -1:
        assert facing == 3 and 100 <= x < 150
        assert getface(startx, starty) == 1
        nextx, nexty, nextfacing = x - 100, 199, 3
        assert getface(nextx, nexty) == 5
        
    # moved up off of top of face 3 onto left of face 2
    elif y == 99 and 0 <= x < 50 and facing == 3:
        assert getface(startx, starty) == 3
        nextx, nexty, nextfacing = 50, x + 50, 0
        assert getface(nextx, nexty) == 2
        
    # moved left off left of face 0 onto left of face 3
    elif x == 49 and 0 <= y < 50:
        assert facing == 2
        assert getface(startx, starty) == 0
        nextx, nexty, nextfacing = 0, 149 - y, 0
        assert getface(nextx, nexty) == 3
        
    # moved left off of left of face 2 onto top of face 3
    elif x == 49 and 50 <= y < 100 and facing == 2:
        assert getface(startx, starty) == 2
        nextx, nexty, nextfacing = y - 50, 100, 1
        assert getface(nextx, nexty) == 3
        
    # moved left off of left of face 3 onto left of face 0
    elif x == -1 and 100 <= y < 150:
        assert facing == 2
        assert getface(startx, starty) == 3
        nextx, nexty, nextfacing = 50, 149 - y, 0
        assert getface(nextx, nexty) == 0
    
    # moved left off of left of face 5 onto top of face 0
    elif x == -1:
        assert facing == 2 and 150 <= y < 200
        assert getface(startx, starty) == 5
        nextx, nexty, nextfacing = y - 100, 0, 1
        assert getface(nextx, nexty) == 0
        
    # moved down off of bottom of face 1 onto right of face 2
    elif y == 50 and 100 <= x < 150 and facing == 1:
        assert getface(startx, starty) == 1
        nextx, nexty, nextfacing = 99, x - 50, 2
        assert getface(nextx, nexty) == 2
        
    # moved down off of bottom of face 4 onto right of face 5
    elif y == 150 and 50 <= x < 100 and facing == 1:
        assert getface(startx, starty) == 4
        nextx, nexty, nextfacing = 49, x + 100, 2
        assert getface(nextx, nexty) == 5
    
    # moved down off of bottom of face 5 onto top of face 1
    elif y == 200:
        assert facing == 1 and 0 <= x < 50
        assert getface(startx, starty) == 5
        nextx, nexty, nextfacing = x + 100, 0, 1
        assert getface(nextx, nexty) == 1
    
    # moved right off of right of face 1 onto right of face 4
    elif x == 150:
        assert facing == 0 and 0 <= y < 50
        assert getface(startx, starty) == 1
        nextx, nexty, nextfacing = 99, 149 - y, 2
        assert getface(nextx, nexty) == 4
    
    # moved right off of right of face 2 onto bottom of face 1
    elif x == 100 and 50 <= y < 100 and facing == 0:
        assert getface(startx, starty) == 2
        nextx, nexty, nextfacing = y + 50, 49, 3 
        assert getface(nextx, nexty) == 1
    
    # moved right off of right of face 4 onto right of face 1
    elif x == 100 and 100 <= y < 150:
        assert facing == 0
        assert getface(startx, starty) == 4
        nextx, nexty, nextfacing = 149, 149 - y, 2
        assert getface(nextx, nexty) == 1
        
    # moved right off of right of face 5 onto bottom of face 4
    elif x == 50 and 150 <= y < 200 and facing == 0:
        assert getface(startx, starty) == 5
        nextx, nexty, nextfacing = y - 100, 149, 3
        assert getface(nextx, nexty) == 4
        
    else:
        raise ValueError(f"Unhandled out-of-bounds case: ({x}, {y}, {FACING_LUT[facing]})")
    
    return nextx, nexty, nextfacing

go()
print("Part 2:", hash())
