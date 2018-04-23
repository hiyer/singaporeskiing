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
        
lines = []
with open("/home/hiyer/Downloads/map.txt") as f:
    for line in f:
        lines.append([int(x) for x in line.split()])

(num_cols, num_rows) = lines.pop(0)

path_points = []
for j in range(num_cols):
    row = []
    for k in range(num_rows):
        row.append(PathPoint(0, 0))
        
    path_points.append(row)
    
def neighbours(x, y):
    return [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
        
def best_ending_at(x, y):
    elevation = lines[x][y]
    best_elevation = 0
    best_point = None
    best_path_point = None
    for j, k in neighbours(x, y):
        if j < 0 or j > (num_cols - 1) or k < 0 or (k > num_rows - 1):
            continue

        #print("Evaluating {}, {}, elevation {}".format(j, k, elevation))
        if lines[j][k] > elevation:
            #print("Evaluating {}, {}, difference in elevation {}".format(j, k, lines[j][k] - elevation))
            path_point = path_points[j][k]
            candidate_point = PathPoint(path_point._length, path_point._elevation)
            #print("Path point is {}, {}".format(path_point._length, path_point._elevation))
            candidate_point.add(lines[j][k] - elevation)
            #print("Candidate point is {}, {}".format(candidate_point._length, candidate_point._elevation))
            if best_path_point is None or best_path_point < candidate_point:
                best_path_point = candidate_point
                
    if best_path_point is None:
        path_points[x][y] = PathPoint(0, 0)
        #print("No paths to {}, {}".format(x, y))
    else:
        path_points[x][y] = best_path_point
        #print("Best for {}, {} is {}, {}".format(x, y, best_path_point._length, best_path_point._elevation))
        
    return best_path_point


best_overall = None
for x, line in enumerate(lines):
    for y, point in enumerate(line):
        best_for_point = best_ending_at(x, y)
        
        if best_for_point is not None and (best_overall is None or best_overall < best_for_point):
            best_overall = best_for_point
            
print("Best overall is {}, {}".format(best_overall._length+1, best_overall._elevation))
