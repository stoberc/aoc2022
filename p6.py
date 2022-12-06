FNAME = "in6.txt"
    
stream = open(FNAME).read().strip()

# Part 1: search until four consecutive distinct characters are found
for i in range(4, len(stream)):
    if len(set(stream[i-4:i])) == 4:
        print("Part 1:", i)
        break

# Part 2: search until fourteen...
for i in range(14, len(stream)):
    if len(set(stream[i-14:i])) == 14:
        print("Part 2:", i)
        break
