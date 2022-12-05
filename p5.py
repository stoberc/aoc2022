#import pdb
import re

FNAME = "in5.txt"
    
def parse_line(line):
    return [int(i) for i in re.findall('\d+', line)] # grab all the numbers

chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]

#initial_config = chunks[0]
#number_of_stacks = len(initial_config[-1].split())
#indices = [initial_config[-1].index(str(i)) for i in range(1, number_of_stacks + 1)]

# realized it's way faster to just manually enter these than to code a parser
stacks = ['NCRTMZP', 'DNTSBZ', 'MHQRFCTG', 'GRZ', 'ZNRH', 'FHSWPZLD', 'WDZRCGM', 'SJFLHWZQ', 'SQPWN']
stacks = [list(i) for i in stacks]
stacksbk = [i[:] for i in stacks]

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

#pdb.set_trace()
    