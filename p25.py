FNAME = "in25.txt"
    
input_snafu_numbers = open(FNAME).read().splitlines()

SNAFU_LUT = {'0':0, '1':1, '2':2, '-':-1, '=':-2}
SNIT_LUT = '012=-' # convert value to snafu digit aka snit

# compute the value of a string representation snafu_number
def evaluate_snafu(snafu_number):
    total = 0
    place_value = 1
    for i in reversed(snafu_number):
        total += place_value * SNAFU_LUT[i]
        place_value *= 5
    return total
    
total = sum(evaluate_snafu(n) for n in input_snafu_numbers)

# find the largest value representible with a certain number of snafu digits 
# aka snits
# could precompute these once then use a memo, or use some clever formula,
# but I don't think it'll matter
def max_reachable(n_snits):
    return evaluate_snafu('2' * n_snits)
    
# snafuize a value
# can specify how many snits to use (w/ zero padding on the left)
# or if None, will use minimal amount
def snafuize(target_value, n_snits = None):
    
    # determine how many snits are needed to represent the number
    # could use a log base 5, but eh
    if not n_snits:
        n_snits = 1
        while max_reachable(n_snits) < target_value:
            n_snits += 1
            
    # safety check that the above logic worked as intended
    # and that we didn't get handed an impossible task
    # like represent a million in two digits
    limit = max_reachable(n_snits)
    assert -limit <= target_value <= limit
        
    # recursion base case
    if n_snits == 1:
        return SNIT_LUT[target_value]
    
    # determine what snit to use in max place value, then recurse on the rest
    # could optimize with some sort of binary search, or more clever
    # computation, but with just five values, what's the point?
    current_place_value = 5 ** (n_snits - 1) # start at max place value
    delta = max_reachable(n_snits - 1) # spread that can be covered with rest
    for v in range(-2, 3):
        upper_bound = current_place_value * v + delta
        lower_bound = current_place_value * v - delta
        if lower_bound <= target_value <= upper_bound:
            residual = target_value - current_place_value * v
            return SNIT_LUT[v] + snafuize(residual, n_snits - 1)
        
    raise RuntimeError("What the hell? Shouldn't be possible to get here.")
        
print("Part 1:", snafuize(total))

# no Part 2 for Day 25
