import math
import copy

FNAME = "in11.txt" # TODO: actually use this (see below)

class Monkey:
    
    def __init__(self, itemlist, opf, divisor, truetarget, falsetarget):
        self.itemlist = itemlist # list of items currently held
        self.opf = opf # worry function
        self.divisor = divisor # divisor for passing rule
        self.truetarget = truetarget # which monkey to pass to if test is true
        self.falsetarget = falsetarget # " false
        self.handlecount = 0 # how many times has this monkey handled an item?
        
    # execute one round
    def round(self):
        while len(self.itemlist) > 0:
            target = self.itemlist.pop(0)
            if ruleset == 1: # rules for Part 1
                target = self.opf(target) // 3
            elif ruleset == 2: # this seems mathematically sound to just operated modulo lcm
                # alternative: detect stable cycles on per-monkey or per-item basis and ex
                target = self.opf(target) % all_divisors_lcm
            else:
                raise ValueError("Unrecognized ruleset:", self.ruleset)
                
            if target % self.divisor == 0:
                monkeys[self.truetarget].itemlist.append(target)
            else:
                monkeys[self.falsetarget].itemlist.append(target)
            self.handlecount += 1
      
# TODO: automated parsing of input file; just manually translated this for 
# now because it was way faster than writing a parser
monkeys = []
monkeys.append(Monkey([54, 89, 94], lambda x : x * 7, 17, 5, 3))
monkeys.append(Monkey([66, 71], lambda x : x + 4, 3, 0, 3))
monkeys.append(Monkey([76, 55, 80, 55, 55, 96, 78], lambda x : x + 2, 5, 7, 4))
monkeys.append(Monkey([93, 69, 76, 66, 89, 54, 59, 94], lambda x : x + 7, 7, 5, 2))
monkeys.append(Monkey([80, 54, 58, 75, 99], lambda x : x * 17, 11, 1, 6))
monkeys.append(Monkey([69, 70, 85, 83], lambda x : x + 8, 19, 2, 7))
monkeys.append(Monkey([89], lambda x : x + 6, 2, 0, 1))
monkeys.append(Monkey([62, 80, 58, 57, 93, 56], lambda x : x * x, 13, 6, 4))
monkeysbk = copy.deepcopy(monkeys) # save initial state for quick reset for Part 2

# Part 1
ruleset = 1 # which part are we one, Part 1 or Part 2?
for _ in range(20):
    for i in range(len(monkeys)):
        monkeys[i].round()

counts = [m.handlecount for m in monkeys]
counts.sort()
print("Part 1:", counts[-1] * counts[-2])

# Part 2
monkeys = monkeysbk
all_divisors_lcm = math.prod([m.divisor for m in monkeys])
ruleset = 2

for _ in range(10000):
    for i in range(len(monkeys)):
        monkeys[i].round()    

counts = [m.handlecount for m in monkeys]
counts.sort()
print("Part 2:", counts[-1] * counts[-2])
