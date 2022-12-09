FNAME = "in9.txt"
 
# translation table from direction to dx, dy
DIRECTION_LUT = {'R':(1, 0), 'L':(-1, 0), 'U':(0, 1), 'D':(0, -1)}

def parse_line(line):
    a, b = line.split()
    return a, int(b)

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

hx, hy = 0, 0 # head location
tx, ty = 0, 0 # tail location
t_visited = [(0, 0)] # log of tail-visited locations

for direction, moves in data:
    dx, dy = DIRECTION_LUT[direction]
    
    # there is probably a way to consolidate and execute all moves in one go
    # but I couldn't think of it on the fly, and n is small enough that it
    # doesn't matter, so we execute moves one at a time
    for _ in range(moves):
        hx += dx
        hy += dy
        
        if abs(hx - tx) > 1 or abs(hy - ty) > 1:
            if hx > tx:
                tx += 1
            elif hx < tx:
                tx -= 1
            if hy > ty:
                ty += 1
            elif hy < ty:
                ty -= 1

        t_visited.append((tx, ty))
        
print("Part 1:", len(set(t_visited)))


xlocations = [0] * 10 # sequence of x's, head to tail
ylocations = [0] * 10 # sequence of y's, head to tail
t_visited = [(0, 0)] # log of all tail-visited locations

for direction, moves in data:
    dx, dy = DIRECTION_LUT[direction]
    
    for _ in range(moves):
        # move the head first
        xlocations[0] += dx
        ylocations[0] += dy
        
        # then work your way down the chain
        for i in range(1, 10):
            hx = xlocations[i - 1]
            hy = ylocations[i - 1]
            tx = xlocations[i]
            ty = ylocations[i]
            
            if abs(hx - tx) > 1 or abs(hy - ty) > 1:
                if hx > tx:
                    xlocations[i] += 1
                elif hx < tx:
                    xlocations[i] -= 1
                if hy > ty:
                    ylocations[i] += 1
                elif hy < ty:
                    ylocations[i] -= 1
                    
        t_visited.append((xlocations[-1], ylocations[-1]))

print("Part 2:", len(set(t_visited)))
