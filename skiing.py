#!/home/hiyer/.venv3/bin/python

from functools import total_ordering
import sys

@total_ordering
class PathPoint:
    def __init__(self, length=0, elevation=0):
        self._length = length
        self._elevation = elevation
        
    def __eq__(self, other):
        if self._length == other._length and self._elevation == other._elevation:
            return True
        
        return False
    
    def __lt__(self, other):
        if self._length < other._length:
            return True
        elif self._length == other._length:
            return self._elevation < other._elevation
        
        return False
    
    def add(self, elevation):
        self._length += 1
        self._elevation += elevation
        
    def is_valid(self):
        return self._length >= 0
        

def neighbours(x, y):
    return [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]

if len(sys.argv) != 2:
    print("Usage: skiing.py <filename>")
    sys.exit(1)
    
lines = []
with open(sys.argv[1]) as f:
    for line in f:
        lines.append([int(x) for x in line.split()])

(num_cols, num_rows) = lines.pop(0)

path_points = []
for j in range(num_rows):
    row = []
    for k in range(num_cols):
        row.append(PathPoint(-1, -1))
    path_points.append(row)
    
def find_longest_path(x, y):
    elevation = lines[y][x]
    longest_subpath = None
    next_point = None
    
    if path_points[y][x].is_valid():
        return path_points[y][x]

    for (j, k) in neighbours(x, y):
        if j < 0 or j > num_cols - 1 or k < 0 or k > num_rows - 1 or lines[k][j] >= elevation:
            continue
        
        #print("Looking in sub-path {}, {} for {}, {}".format(j, k, x, y))
        subpath = find_longest_path(j, k)
        tmp_path = PathPoint(subpath._length, subpath._elevation)
        tmp_path.add(elevation - lines[k][j])
        
        if longest_subpath is None or longest_subpath < tmp_path:
            longest_subpath = tmp_path
            #print("Longest sub-path: {}, {} at {}, {}".format(longest_path._length, longest_path._elevation, x, y))
                
    if longest_subpath is not None:
        path_points[y][x] = longest_subpath
        #print("Longest path from {}, {} is {}, {} to {}, {}".format(x, y, longest_subpath._length, longest_subpath._elevation, next_point._x, next_point._y))
    else:
        longest_subpath = PathPoint(0, 0)
        path_points[y][x] = longest_subpath
        #print("No path from {}, {}".format(x, y))
        
    return longest_subpath

longest_path = None
for y, line in enumerate(lines):
    for x, point in enumerate(line):
        path = find_longest_path(x, y)
        
        if path is None:
            continue
        
        if path is not None and (longest_path is None or longest_path < path):
            longest_path = path

if longest_path is None:
    print("No path found")
else:
    print("Longest path is {}, {}".format(longest_path._length+1, longest_path._elevation))
