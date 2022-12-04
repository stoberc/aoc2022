#import pdb

FNAME = "in3.txt"

# split the line in half
def parse_line(line):
    i = len(line) // 2
    return line[:i], line[i:]

# find the score associated with a particular letter
# a = 1, b = 2, ..., z = 26, A = 27, B = 28, ..., Z = 52
def score(letter):
    if letter.islower():
        return ord(letter) - ord('a') + 1
    return ord(letter) - ord('A') + 27

# find the (lone) common character betwen two strings
def score_row(a, b):
    x = set(a) & set(b)
    assert len(x) == 1
    return score(x.pop())
    
# process the input and compute Part 1 score
data = [parse_line(line) for line in open(FNAME).read().splitlines()]
print("Part 1:", sum([score_row(*i) for i in data]))

# rejoin each line from the input for Part 2
data = [i + j for i, j in data]

# split the input into three-row chunks
data = [data[i:i+3] for i in range(0, len(data), 3)]

# score a group by finding the common character and scoring it
def score_group(a, b, c):
    x = set(a) & set(b) & set(c)
    assert len(x) == 1
    return score(x.pop())

# do this for each group in the input for Part 2
print("Part 2:", sum([score_group(*i) for i in data]))

#pdb.set_trace()
    