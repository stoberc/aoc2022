FNAME = "in21.txt"
    
# store each parsed input in a LUT
monkey_vals = {}
def parse_line(line):
    line = line.split()
    name = line[0][:-1]
    if len(line) == 2:
        val = int(line[1]) # assume only ints are possible (else raise)
        monkey_vals[name] = val
    else:
        monkey_vals[name] = line[1:]
        
for line in open(FNAME).read().splitlines():
    parse_line(line)

# get the value for a monkey, evaluating recursively as necessary
# for Part 2 return None if the humn is in this branch, recursively
def evaluate(name):
    v = monkey_vals[name]
    if type(v) == type(0) or v is None:
        return v
        
    op1, operator, op2 = v
    op1 = evaluate(op1)
    op2 = evaluate(op2)
    if op1 is None or op2 is None:
        return None
        
    expression = f"{evaluate(v[0])}{v[1]}{evaluate(v[2])}"
    assert v[1] in '+-*/==' # cybersec safety check for eval :)
    v = int(eval(expression)) # assumption: all calculations yield integers
    monkey_vals[name] = v
    return v
    
print("Part 1:", evaluate('root'))
    
# reload the input, but tweak for Part 2
# would be faster to only open the file once, but eh
for line in open(FNAME).read().splitlines():
    parse_line(line)
monkey_vals['root'][1] = '=='
monkey_vals['humn'] = None
    
# force a particular monkey to have a particular value
# by recursively forcing the humn to the correct value
def force(target_name, target_value):
    if target_name == 'humn':
        monkey_vals[target_name] = target_value
        return
        
    name1, operator, name2 = monkey_vals[target_name]
    val1 = evaluate(name1)
    val2 = evaluate(name2)
    
    # crossing my fingers that the input is a tree, at least wrt humn
    # otherwise this gets WAY more complicated
    assert (val1 is None) ^ (val2 is None)
    
    # figure out which operand is missing and needs to be recursively forced
    if val2 is None:
        subtarget_name = name2
        partial_value = val1
    else:
        subtarget_name = name1
        partial_value = val2

    if operator== '+': # commutative
        subtarget_value = target_value - partial_value
    elif operator == '-': # not commutative
        if val2:
            subtarget_value = target_value + partial_value
        else:
            subtarget_value = partial_value - target_value
    elif operator == '*': # commutative
        # assume integer operations only
        subtarget_value = int(target_value / partial_value)
    elif operator == '/': # not commutative
        if val2:
            subtarget_value = target_value * partial_value
        else:
            subtarget_value = int(parial_value / target_value)
    elif operator == '==': # reflexive
        assert target_value # should only ever be assigning this to True
        subtarget_value = partial_value
    else:
        raise ValueError("Unrecognized operand:", operator)
    force(subtarget_name, subtarget_value)
    
force('root', True)
print("Part 2:", evaluate('humn'))
