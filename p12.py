FNAME = "in12.txt"
    
grid = [list(line) for line in open(FNAME).read().splitlines()]

height = len(grid)
width = len(grid[0])

# convert grid to numeric heights 'a' = 0, 'z' = 25
# and log locations of start and end
for x in range(width):
    for y in range(height):
        if grid[y][x] == 'S':
            startx, starty = x, y
            grid[y][x] = 'a'
        elif grid[y][x] == 'E':
            goalx, goaly = x, y
            grid[y][x] = 'z'
        grid[y][x] = ord(grid[y][x]) - ord('a')
    
# for Part 2 it's more convenient to search out from goal than from start
expandq = [(goalx, goaly)] # more efficient as deque?
distance = {(goalx, goaly):0} # distance from goal

part2 = False # have we found the closest 'a' to E yet?
while (startx, starty) not in distance:
    currentx, currenty = expandq.pop(0)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        adjx = currentx + dx
        adjy = currenty + dy
        
        if (0 <= adjx < width and 0 <= adjy < height and 
            grid[adjy][adjx] >= grid[currenty][currentx] - 1 and 
            (adjx, adjy) not in distance):
            
            distance[(adjx, adjy)] = distance[(currentx, currenty)] + 1
            expandq.append((adjx, adjy))
            if grid[adjy][adjx] == 0 and not part2:
                print("Part 2:", distance[(adjx, adjy)])
                part2 = True
        
print("Part 1:", distance[(startx, starty)])
