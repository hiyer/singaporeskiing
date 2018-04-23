#!/home/hiyer/.venv3/bin/python
from functools import total_ordering

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
        
lines = []
with open("/home/hiyer/Downloads/map.txt") as f:
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
    longest_path = None
    
    #print("Finding longest path from {}, {} at elevation {}".format(x, y, elevation))
    
    if path_points[y][x].is_valid():
        return path_points[y][x]
    
    for j, k in neighbours(x, y):
        if j < 0 or j > num_cols - 1 or k < 0 or k > num_rows - 1:
            continue
                
        if lines[k][j] < elevation:
            path = find_longest_path(j, k)
                
            if path is None:
                continue
                
            if longest_path is None or longest_path < path:
                tmp_path = PathPoint(path_points[k][j]._length, path_points[k][j]._elevation)
                tmp_path.add(elevation - lines[k][j])
                longest_path = tmp_path
    
    if longest_path is not None:
        path_points[y][x] = longest_path
        #print("Longest path from {}, {} is {}, {}".format(x, y, longest_path._length, longest_path._elevation))
    else:
        longest_path = PathPoint(0, 0)
        path_points[y][x] = longest_path
        #print("No path from {}, {}".format(x, y))
        
    return longest_path

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
