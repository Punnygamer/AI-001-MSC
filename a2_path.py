"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a Search algorithms for task 2
Group no: C9
Student ID : 100397265
Student Name: Joshua Galvao

"""

from a1_state import State
from copy import deepcopy
from collections import deque
import heapq
from time import perf_counter
import itertools

#check if the current board doesnt have hingers; aka theres no immediate win
def safe(state):
    if state.numHingers()== 0:
        return True
    else:
        return False

#converts the state into a tuple of tuples which can be used as a key 
def tuplestate(State):
    tup=[]
    for row in State.grid:
        tup.append(tuple(row))
    return tuple(tup)

#the breadth first search algorithm
def path_BFS(start,end):
    #checks if the board doesnt have any hingers and wont result in any hingers
    if safe(start) == False or safe(end)== False:
        return None

    stup = tuplestate(start)
    etup = tuplestate(end)

    queue = deque([(start, [stup])])
    visited = {stup}

    while queue:
        item = queue.popleft()
        current = item[0]
        path = item[1]
        if tuplestate(current) == etup:
            return path

        for next_state in current.moves():
            if safe(next_state)==False:
                continue
            key = tuplestate(next_state)
            if key not in visited:
                visited.add(key)
                queue.append((next_state, path + [key]))
    return None


def path_DFS(start,end):
    if safe(start)==False or safe(end)==False:
        return None

    stup = tuplestate(start)
    etup = tuplestate(end)
    visited = set()

    def dfs(current, path):
        key = tuplestate(current)
        if key in visited:
            return None
        visited.add(key)

        if key == etup:
            return path

        for next_state in current.moves():
            if safe(next_state)==False:
                continue
            result = dfs(next_state, path + [tuplestate(next_state)])
            if result:
                return result
        return None

    return dfs(start, [stup])

def path_IDDFS(start,end, maxdepth=50):
    if safe(start)==False or safe(end)==False:
        return None

    stup = tuplestate(start)
    etup = tuplestate(end)

    def dls(current,etup,depth,path,visited):
        key = tuplestate(current)
        if key in visited:
            return None
        visited.add(key)

        if key ==etup:
            return path
        if depth == 0:
            return None

        for next_state in current.moves():
            if safe(next_state)==False:
                continue
            result = dls(next_state, etup, depth - 1,
                         path + [tuplestate(next_state)], visited)
            if result:
                return result
        return None

    for limit in range(maxdepth + 1):
        visited = set()
        result = dls(start, etup, limit, [stup], visited)
        if result:
            return result
    return None

#Region difference heuristic
def path_astar(start, end):
    open_set = []
    counter = itertools.count()

    heapq.heappush(open_set, (0, next(counter), start))
    came_from = {}
    g_score = {start.to_tuple(): 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current.to_tuple() == end.to_tuple():
            path = [current.to_tuple()]
            while current.to_tuple() in came_from:
                current = came_from[current.to_tuple()]
                path.append(current.to_tuple())
            return list(reversed(path))

        for next_state in current.moves():
            tentative_g = g_score[current.to_tuple()] + 1
            next_tup = next_state.to_tuple()

            if tentative_g < g_score.get(next_tup, float('inf')):
                came_from[next_tup] = current
                g_score[next_tup] = tentative_g


                h = abs(current.numRegions() - end.numRegions())
                f = tentative_g + h
                heapq.heappush(open_set, (f, next(counter), next_state))

    return None

#compares each algorithm
def compare():
    grid_start = [
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    grid_end = [
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    start = State(grid_start)
    end = State(grid_end)

    algorithms = [
        ("BFS", path_BFS),
        ("DFS", path_DFS),
        ("IDDFS", path_IDDFS),
        ("A*", path_astar),
    ]

    print("Comparing Search Algorithms\n")
    for name, func in algorithms:
        t0 = perf_counter()
        path = func(start, end)
        t1 = perf_counter()
        print(f"{name:6s} | Path found: {path is not None} | "
              f"Length: {len(path) if path else 0:2d} | "
              f"Time: {(t1 - t0)*1000:7.2f} ms")
    print("//////////////////////////////////////////////////////////////////////////////")

def pathtester():
    print("=== Hinger Path Tester ===")
    grid_start = [
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    grid_end = [
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    s1 = State(grid_start)
    s2 = State(grid_end)

    print("Start State:\n", s1)
    print("End State:\n", s2)

    print("\n BFS---------------------------")
    print(path_BFS(s1, s2))

    print("\n DFS---------------------")
    print(path_DFS(s1, s2))

    print("\n IDDFS-----------------------")
    print(path_IDDFS(s1, s2))

    print("\n A*----------------------------")
    print(path_astar(s1, s2))



    print("\nComparison -------------------")
    compare()



if __name__ == "__main__":
    pathtester()
