import re

FNAME = "in5.txt"
    
chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]

# parse the initial configuration of the stacks
initial_config = chunks[0]
number_of_stacks = len(initial_config[-1].split())
assert number_of_stacks < 10 # otherwise the spacing becomes inconsistent
stacks = [[row[i] for row in chunks[0][:-1]] for i in range(1, 4 * number_of_stacks, 4)]
stacks = [list(reversed(''.join(i).strip())) for i in stacks]

# realized it's way faster to just manually enter these than to code a parser
# leaving for quick reference, even though automatic parsing has now been implemented
#stacks = ['NCRTMZP', 'DNTSBZ', 'MHQRFCTG', 'GRZ', 'ZNRH', 'FHSWPZLD', 'WDZRCGM', 'SJFLHWZQ', 'SQPWN']
#stacks = [list(i) for i in stacks]

stacksbk = [i[:] for i in stacks] # backup for Part 2

# extract the three key numbers from a command
def parse_line(line):
    return [int(i) for i in re.findall('\d+', line)] # grab all the numbers

commands = [parse_line(line) for line in chunks[1]]

# Part 1 rules: move one at a time
def process_command(count, source, dest):
    for _ in range(count):
        stacks[dest - 1].append(stacks[source - 1].pop())
    
for command in commands:
    process_command(*command)
    
print("Part 1:", ''.join([i[-1] for i in stacks]))

# reset
stacks = stacksbk

# Part 2 rules: move a whole block in one shot
def process_command2(count, source, dest):
    stacks[dest - 1] += stacks[source - 1][-count:]
    stacks[source - 1] = stacks[source - 1][:-count]
    
for command in commands:
    process_command2(*command)
 
print("Part 2:", ''.join([i[-1] for i in stacks]))
