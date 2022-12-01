def load(fname):
    lines = open(fname).readlines();
    return [list(line.strip()) for line in lines]
    