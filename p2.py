#import pdb

FNAME = "in2.txt"

# phase 1 interpretation of strategy
# could just use the symbols directly, but this is easier for my brain
map1 = {'A':'R', 'B':'P', 'C':'S'} # opponent😡
map2 = {'X':'R', 'Y':'P', 'Z':'S'} # you😃

# score value of what you played
score_map = {'R':1, 'P':2, 'S':3}

def parse_line(line):
    a, b = line.split()#✂️
    return map1[a], b # for Part 2 need to leave b intact 🔜

# a = player choice (RPS), b = your choice (RPS)
def score(a, b):
    if a == b: # 3 points for a draw😐
        base = 3
    elif a + b in ('RP', 'PS', 'SR'): # 6 points for a win😁
        base = 6
    else: # 0 points for a loss😒
        base = 0
    return base + score_map[b] # plus the score for your selection
    
# part 2: figure out what you should play based on
# a = opponent choice (RPS)
# b = strategy guide (XYZ)
# then return the score associated with that overall game
# could more compactly implement with a LUT, but eh
def deduce(a, b):
    if b == 'X': # you need to lose😒
        if a == 'R':#🗿
            b = 'S'
        elif a == 'P':#📄
            b = 'R'
        else:       #✂️
            b = 'P'
    elif b == 'Y': # you need to draw😐
        b = a
    else: # b == 'Z' you need to win😁
        if a == 'R':#🗿
            b = 'P'
        elif a == 'P':#📄
            b = 'S'
        else:       #✂️
            b = 'R'
    return score(a, b)
    
data = [parse_line(line) for line in open(FNAME).read().splitlines()] #✨✨✨

print("Part 1:", sum([score(a, map2[b]) for a, b in data]))
print("Part 2:", sum([deduce(*i) for i in data]))

#pdb.set_trace()
    