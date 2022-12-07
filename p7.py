FNAME = "in7.txt"
PART1_LIMIT = 100000
DISK_SIZE = 70000000
FREE_SPACE_NEEDED = 30000000

data = open(FNAME).read().splitlines()

# root is the only directory initially known to exist
directory_list = ['/'] 

# LUT to find the parent directory of a specific directory
# could save memory and just do by removing the final directory
# in the path, but this is less work atm
parent = {}

# LUT with subdirectories of a given directory
children = {'/':[]}

# A list of directories that have already been ls'ed
# I assume it's a property of the input that the same directory is not
# ls'ed twice, but we'll keep a log just in case
searched = []

# A list of (size, filenames) contents indexed by directory
direct_file_contents = {'/':[]}

assert data[0] == '$ cd /' # presumably we always start by going to root
current_directory = '/'
pc = 1 # program counter

# now process the lines of the input one at a time
while pc < len(data):
    command = data[pc]
    if command == '$ ls':
        assert current_directory not in searched
        searched.append(current_directory)
        pc += 1
        
        # process ls outputs
        while pc < len(data) and '$' not in data[pc]:
            if data[pc].startswith('dir '): # a subdirectory
                dirname = data[pc].split()[1]
                fullpath = current_directory + dirname + '/'
                directory_list.append(fullpath)
                parent[fullpath] = current_directory
                children[current_directory].append(fullpath)
                children[fullpath] = []
                direct_file_contents[fullpath] = []
            else: # a file
                size, fname = data[pc].split()
                size = int(size)
                direct_file_contents[current_directory].append((size, fname))
            pc += 1
    elif command == '$ cd ..':
        current_directory = parent[current_directory]
        pc += 1
    elif command.startswith('$ cd '):
        target = command.split()[-1]
        current_directory = current_directory + target + '/'
        pc += 1
    else:
        raise ValueError("Unrecognized command:", command)
        
# find the total size of a directory recursively with memoization
cumulative_sizes = {} # memo
def get_cumulative_size(directory):
    if directory in cumulative_sizes:
        return cumulative_sizes[directory]
    total_size = 0
    for size, fname in direct_file_contents[directory]:
        total_size += size
    for child_directory in children[directory]:
        total_size += get_cumulative_size(child_directory)
    cumulative_sizes[directory] = total_size
    return total_size

sizes = [get_cumulative_size(i) for i in directory_list]
print("Part 1:",  sum([size for size in sizes if size <= PART1_LIMIT]))

currently_unused_space = DISK_SIZE - get_cumulative_size('/')
extra_space_needed = FREE_SPACE_NEEDED - currently_unused_space
assert extra_space_needed > 0

print("Part 2:", min([size for size in sizes if size >= extra_space_needed]))
