from functools import cmp_to_key

FNAME = "in13.txt"
    
def parse_chunk(chunk):
    a, b = chunk
    return eval(a), eval(b)
    
chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
data = [parse_chunk(chunk) for chunk in chunks]

def compare(left, right):
    if type(left) == type(right) == type(0):
        if left == right:
            return 'tie'
        return left < right
    elif type(left) == type(right) == type([]):
        for l, r in zip(left, right):
            current = compare(l, r)
            if current == 'tie':
                continue
            return current;
        if len(left) == len(right):
            return 'tie'
        return len(left) < len(right)
    elif type(left) == type(0):
        return compare([left], right)
    else: # type(right) == type(0):
        return compare(left, [right])   
            
index_total = 0
for i, pair in enumerate(data):
    left, right = pair
    if compare(left, right):
        index_total += i + 1
        
print("Part 1:", index_total)

all_packets = [[[2]], [[6]]]
for a, b in data:
    all_packets.append(a)
    all_packets.append(b)
    
# comparator must return a positive/negative/zero, not True/False
# so have to repackage it a bit to get it to work as sort comparator
all_packets.sort(key=cmp_to_key(lambda l, r: -1 if compare(l, r) else 1))

# original inefficient but adequate bubble sort 
# when I couldn't figure out the black magic above
#for _ in range(len(all_packets)):
#    for i in range(len(all_packets) - 1):
#        left = all_packets[i]
#        right = all_packets[i + 1]
#        result = compare(left, right)
#        assert result == True or result == False
#        if not result:
#            all_packets[i], all_packets[i + 1] = all_packets[i + 1], all_packets[i]

a = all_packets.index([[2]])
b = all_packets.index([[6]])
print("Part 2:", (a + 1) * (b + 1))
