DIRECTIONS4 = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIRECTIONS8 = DIRECTIONS4 + ((1, 1), (-1, -1), (1, -1), (-1, 1))

# take a collection of points and render them as '#' with non rendered-points as '.'
# useful for e.g. aoc2021/p13 when a set of points represents a visual message
def render(points):
    minx = min(x for x, y in points)
    maxx = max(x for x, y in points)
    miny = min(y for x, y in points)
    maxy = max(y for x, y in points)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()


    

