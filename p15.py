import re

FNAME = "in15.txt" #"in15b.txt"
PART1Y = 2000000 #10
PART2LIMIT = 4000000 #20

def manhattan_distance(x0, y0, x1, y1):
    return abs(x1-x0) + abs(y1-y0)
    
def parse_line(line):
    a = [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers
    a.append(manhattan_distance(*a)) # precompute this once to save time
    return a # sensorx, sensory, beaconx, beacony, manhattan_distance

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

# need O(1) access
beacon_locations = set()
for _, _, bx, by, _ in data:
    beacon_locations.add((bx, by))
    
# kind of slow for Part 1, but simple
# we'll just loop though the row and keep track of 
count = 0 # number of ineligible spaces in this row
minbx = min(i[2] for i in data)
maxbx = max(i[2] for i in data)
assert minbx < 0 and maxbx > 0
# these bounds are very sloppy and chosen a bit by trial and error
# there is no guarantee that they'll work for other inputs
# I do suspect we could tighten them quite a bit and get an accurate result
# for my particular input
# better yet, we could probably calculate a reasonable boundary horizon
# based on the specific inputs #TODO
lower_bound = minbx * 10
upper_bound = maxbx * 2
print(f"Part 1: Looping x from {lower_bound} to {upper_bound}...")
print(" Count should start at zero, and")
print(" once it stablizes, could've stopped looping")
for x in range(lower_bound, upper_bound): 
    if x % 1000000 == 0:
        print(f"Current x: {x}  Count so far: {count}")
    valid = True # is this a (x, PART1Y) a valid beacon location?
    for sx, sy, bx, by, d in data:
        # maybe it already IS a beacon location
        if (x, PART1Y) in beacon_locations: 
            continue
        # or maybe it's too close to a sensor
        if manhattan_distance(x, PART1Y, sx, sy) <= d:
            valid = False
            break
    if not valid:
        count += 1

print("Part 1:", count)

# Part 2 we'll scan the whole space looking for a valid location
# though this'd take forever, so we'll use some cleverness to skip past certain
# sections, so it only takes 0.1 * forever, or whatever
done = False
# check all possible x's (could also optimize with skipping like for y?)
print(f"Part 2: scanning all x from 0 to {PART2LIMIT}...")
for x in range(0, PART2LIMIT + 1): 
    if x % 100000 == 0:
        print(f"Current x: {x}")
    y = 0
    while y <= PART2LIMIT:
        #print(" Y:", y)
        # every time we move past one sensore, we need to reset to ensure
        # we haven't entered the domain of an already-visited sensor
        reset = False 
        for sx, sy, bx, by, d in data:
            if manhattan_distance(x, y, sx, sy) <= d:
                d2 = manhattan_distance(x, y, sx, sy)
                #print("CANDIDATE AT", (x, y), "is", d2, "away from sensor at", (sx, sy), "with closest beacon", (bx, by), "at distance", d)
                # must advance this much to move to this sensor's boundary
                margin = d - d2 
                if y < sy: # make sure we're already past the sensor, though
                    y = sy + (sy - y)
                y += margin + 1
                #print("NEW Y:", y)
                reset = True
                break
        if reset:
            continue
                
        # if we managed to loop through all sensors without a conflict,
        # we've found the spot!
        print("Part 2:", x * 4000000 + y)
        done = True
        break
    if done:
        break
