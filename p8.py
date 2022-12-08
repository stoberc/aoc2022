FNAME = "in8.txt"
    
def parse_line(line):
    return [int(i) for i in line]

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

height = len(data)
width = len(data[0])

# save some time by not bothering to check the perimeter (all visible)
outer_viz = width * 2 + height * 2 - 4  
inner_viz = 0

for x in range(1, width - 1):
    for y in range(1, height - 1):
        tree_height = data[y][x]
        
        visible = True
        dx = 1
        while x + dx < width:
            if data[y][x + dx] >= tree_height:
                visible = False
                break
            dx += 1
        if visible:
            inner_viz += 1
            continue
            
        visible = True
        dx = -1
        while x + dx >= 0:
            if data[y][x + dx] >= tree_height:
                visible = False
                break
            dx -= 1
        if visible:
            inner_viz += 1
            continue

        visible = True
        dy = 1
        while y + dy < height:
            if data[y + dy][x] >= tree_height:
                visible = False
                break
            dy += 1
        if visible:
            inner_viz += 1
            continue
            
        visible = True
        dy = -1
        while y + dy >= 0:
            if data[y + dy][x] >= tree_height:
                visible = False
                break
            dy -= 1
        if visible:
            inner_viz += 1
            continue
            
print("Part 1:", outer_viz + inner_viz)
    
# don't bother to check the perimeter--all guaranteed to have score of zero
scores = []
for x in range(1, width - 1):
    for y in range(1, height - 1):
        tree_height = data[y][x]
        
        dx = 1
        right = 0
        while x + dx < width:
            right += 1
            if data[y][x + dx] >= tree_height:
                break
            dx += 1
            
        dx = -1
        left = 0
        while x + dx >= 0:
            left += 1
            if data[y][x + dx] >= tree_height:
                break
            dx -= 1
            
        dy = 1
        bottom = 0
        while y + dy < height:
            bottom += 1
            if data[y + dy][x] >= tree_height:
                break
            dy += 1
            
        dy = -1
        top = 0
        while y + dy >= 0:
            top += 1
            if data[y + dy][x] >= tree_height:
                break
            dy -= 1
            
        scores.append(left * right * top * bottom)
        
print("Part 2:", max(scores))
