FNAME = "in20.txt"

data = [int(i) for i in open(FNAME).read().splitlines()]

# a node will keep track of the associated value, and the neighbors (next/prev)
# won't track initial position, since they are permanently stored in order of 
# initial position in the nodes list, only pointers to neighbors are changed
class Node:

    # next is not yet known when the node is born
    # will set when next node is instantiated
    # will declare it now to keep all of our attributes in one place
    def __init__(self, value, prev):
        self.value = value
        self.next = None
        self.prev = prev
     
    # shift (mix) the node by advancing by the appropriate delta
    def shift(self, delta):
 
        if delta == 0:
            return
            
        # to save time, never move more than half way around the ring
        delta %= len(nodes) - 1
        if delta > len(nodes) / 2:
            delta -= (len(nodes) - 1)
            
        # remove from current position
        self.prev.next = self.next
        self.next.prev = self.prev
        
        if delta > 0:
            # advance to next node delta times to identify new successor
            for _ in range(delta):
                self.next = self.next.next
            # identify new predecessor
            self.prev = self.next.prev
        else:
            # move back delta times to identify new predecessor
            for _ in range(abs(delta)):
                self.prev = self.prev.prev
            # identify new successor
            self.next = self.prev.next

        # update successor/predecessor to direct to self
        self.prev.next = self
        self.next.prev = self

# print the entire ring in sequence for debugging
# different start convention than examples, but ring property is conserved
def display_nodes():
    current = nodes[0]
    for _ in range(len(nodes)) - 1:
        print(current.value, end=", ")
        current = current.next
    print(current.value)
        
# load the input data into the node data structures
# nodes are stored in a list that will never change order in order to easily
# iterate based on initial position
# only pointers to neighbors will change to implement mixing
nodes = [Node(data[0], None)]
for val in data[1:]:
    nodes.append(Node(val, nodes[-1]))
    nodes[-2].next = nodes[-1]
nodes[0].prev = nodes[-1]
nodes[-1].next = nodes[0]

# now run the mixing operation - functionalized for later use
def mix():
    for node in nodes:
        node.shift(node.value)
mix()
     
# now run the hash - functionalized for later use
def hash():
    
    # find the node with zero value to start the hash
    for node in nodes:
        if node.value == 0:
            break
    
    # find the 1000th, 2000th, and 3000th successors
    vals = []
    for _ in range(3):
        for _ in range(1000):
            node = node.next
        vals.append(node.value)
    return sum(vals)

print("Part 1:", hash())

# begin Part 2
DECRYPTION_KEY = 811589153

# reload the input data into the node data structures
nodes = [Node(data[0] * DECRYPTION_KEY, None)]
for val in data[1:]:
    nodes.append(Node(val * DECRYPTION_KEY, nodes[-1]))
    nodes[-2].next = nodes[-1]
nodes[0].prev = nodes[-1]
nodes[-1].next = nodes[0]

for _ in range(10):
    mix()
    
print("Part 2:", hash())
