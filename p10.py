FNAME = "in10.txt"
    
def parse_line(line):
    if line == 'noop':
        return line
    line = line.split()
    assert line[0] == 'addx'
    return line[0], int(line[1])

x = 1 # register
cycle = 1 # cycle count
display = '' # final output string

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

cares = []
def report():
    if cycle % 40 == 20:
        cares.append(cycle * x)
        
# haven't been able to sit and think about this long enough,
# but shifting by one here, then slightly animating prior to incrementing reg
# solves weird phase error I was getting :shrug: TODO understand this better
def animate():
    global display
    if 0 <= (cycle - 1) % 40 - x <= 2:
        display += '#'
    else:
        display += '.'
        
for command in data:
    if command == 'noop':
        cycle += 1
        report()
        animate()
    else:
        d = command[1]
        cycle += 1
        report()
        animate()
        cycle += 1
        animate() # see comment above
        x += d
        report()
         
print("Part 1:", sum(cares))

print("Part 2:")
for i in range(0, len(display), 40):
    print(display[i:i+40])
