import pdb

# arena coordinate system:
# one vertical wall at x = 0, andother at x = 8, so x = 1..7 is open space
# floor is at y = 0, so y = 1 is the lowest place a rock will be

FNAME = "in17.txt"
winds = open(FNAME).read().strip()

windi = 0 # index to keep track of current wind
stable_points = set() # set of all points occupied by rocks that have settled
peaky = 0 # highest extant y so we don't have to max on stable_points repeatedly

class Rock:
    
    # type = 0, 1, 2, 3, or 4 as described below for the five possible shapes
    # y is the height of the lowest piece of this rock
    def __init__(self, type, y):
        # set these up relative to (0, 0) == lower left (open space in case of plus)
        if type == 0: # horizontal bar
            self.points = [[0, 0], [1, 0], [2, 0], [3, 0]]
        elif type == 1: # plus
            self.points = [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]]
        elif type == 2: # J
            self.points = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
        elif type == 3: # vertical bar
            self.points = [[0, 0], [0, 1], [0, 2], [0, 3]]
        elif type == 4: # square
            self.points = [[0, 0], [1, 0], [0, 1], [1, 1]]
            
        # now shift the base shape to the actual spawn point
        for i in range(len(self.points)):
            self.points[i][0] += 3 # x == 0 is the left edge, so need to shift by 3
            self.points[i][1] += y # shift up to the desired height
    
    def can_move_down(self):
        # this check is pointless for almost all rocks
        # refactor if performance becomes a concern
        if min(y for x, y in self.points) == 1: # ground
            return False
        for x, y in self.points: # is there a rock below this one?
            if (x, y - 1) in stable_points:
                return False
        return True
        
    def can_move_left(self):
        if min(x for x, y in self.points) == 1: # left wall
            return False
        for x, y in self.points: # is there a rock to the left of this one?
            if (x - 1, y) in stable_points:
                return False
        return True        
            
    def can_move_right(self):
        if max(x for x, y in self.points) == 7: # right wall
            return False
        for x, y in self.points: # is there a rock to the right of this one?
            if (x + 1, y) in stable_points:
                return False
        return True                
            
    def move_down(self):
        for i in range(len(self.points)):
            self.points[i][1] -= 1
    
    def move_left(self):
        for i in range(len(self.points)):
            self.points[i][0] -= 1
    
    def move_right(self):
        for i in range(len(self.points)):
            self.points[i][0] += 1
            
    # add this rock to stable_points and update peaky--it's done moving
    def commit(self):
        global peaky
        for x, y in self.points:
            stable_points.add((x, y))
            if y > peaky:
                peaky = y
    
# for debug, draw the column
def render():
    print()
    for y in range(peaky, 0, -1):
        line = '|'
        for x in range(1, 8):
            if (x, y) in stable_points:
                line += '#'
            else:
                line += '.'
        line += '|'
        print(line)
    print('+-------+\n')
    
# Part 1: simulate 2022 rocks
for i in range(2022):
    # rocks cycle through all five, and are always 3 above highest extant rock (edge to edge)
    r = Rock(i % 5, peaky + 4) 
    
    # loop until downward progress is impeded, then commit
    while True:
        w = winds[windi]
        windi = (windi + 1) % len(winds)
        
        if w == '<' and r.can_move_left():
            r.move_left()
        elif w == '>' and r.can_move_right():
            r.move_right()
            
        if r.can_move_down():
            r.move_down()
        else:
            r.commit()
            #render()
            #pdb.set_trace()
            break
            
print("Part 1:", peaky)

# Part 2

PART2_NROCKS = 1000000000000

# magic numbers found via manual ish tinkering with my specific input
# TODO: automate/generalize
TOTAL_ROCK_CYCLE_GAIN = 1690 # amount of extra rocks with every periodic cycle
HEIGHT_CYCLE_GAIN = 2647 # amount of extra height with every periodic cycle

# Part 1 is fast, so minor loss to just reset everything instead of carefully continuing prior simulation
windi = 0
stable_points = set() # set of all points occupied by rocks that have settled
peaky = 0
rocki = 0
total_rocks = 0

# vestiges of tinkering code that could be expanded into full-blown automation
#lastheight = 0
#lasttotalrocks = 0

while True:
    
    # spawn new rock
    r = Rock(rocki, peaky + 4)
    rocki = (rocki + 1) % 5
    total_rocks += 1
    
    # loop until downward progress is impeded, then commit
    while True:
        w = winds[windi]
        windi = (windi + 1) % len(winds)
        if w == '<' and r.can_move_left():
            r.move_left()
        elif w == '>' and r.can_move_right():
            r.move_right()
        if r.can_move_down():
            r.move_down()
        else:
            r.commit()
            break
            
    # if we're cycle aligned with the target, print a status update
    if total_rocks % TOTAL_ROCK_CYCLE_GAIN == PART2_NROCKS % TOTAL_ROCK_CYCLE_GAIN:
        #print(f"{total_rocks} rocks have fallen and the height is now {peaky}")
        rocksneeded = PART2_NROCKS - total_rocks
        extraheight = rocksneeded // TOTAL_ROCK_CYCLE_GAIN * HEIGHT_CYCLE_GAIN
        print("Part 2 extrapolation:", peaky + extraheight, "(if stable, ctrl-c and submit)")
        break # for this input, it is immediately stable
        
        # vestiges of tinkering code that could be expanded into full-blown automation
        #heightchange = peaky - lastheight
        #lastheight = peaky
        #
        #rockchange = total_rocks - lasttotalrocks
        #lasttotalrocks = total_rocks
        
        #print("FRESH WIND WITH ROCK, WIND", rocki, windi, total_rocks, rockchange, peaky, heightchange)
    
#pdb.set_trace()
