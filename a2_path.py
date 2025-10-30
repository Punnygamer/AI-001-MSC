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
    if not safe(start) or not safe(end):
        return None

    start_tup = tuplestate(start)
    end_tup = tuplestate(end)

    queue = deque([(start, [start_tup])])
    visited = {start_tup}

    while queue:
        current, path = queue.popleft()
        if tuplestate(current) == end_tup:
            return path

        for next_state in current.moves():
            if not safe(next_state):
                continue
            key = tuplestate(next_state)
            if key not in visited:
                visited.add(key)
                queue.append((next_state, path + [key]))
    return None


def path_DFS(start,end):
    if not safe(start) or not safe(end):
        return None

    start_tup = tuplestate(start)
    end_tup = tuplestate(end)
    visited = set()

    def dfs(current, path):
        key = tuplestate(current)
        if key in visited:
            return None
        visited.add(key)

        if key == end_tup:
            return path

        for next_state in current.moves():
            if not safe(next_state):
                continue
            result = dfs(next_state, path + [tuplestate(next_state)])
            if result:
                return result
        return None

    return dfs(start, [start_tup])

def path_IDDFS(start,end,max_depth=10):
    if not safe(start) or not safe(end):
        return None

    start_tup = tuplestate(start)
    end_tup = tuplestate(end)

    def dls(current,end_tup,depth,path,visited):
        key = tuplestate(current)
        if key in visited:
            return None
        visited.add(key)

        if key ==end_tup:
            return path
        if depth == 0:
            return None

        for next_state in current.moves():
            if not safe(next_state):
                continue
            result = dls(next_state, end_tup, depth - 1,
                         path + [tuplestate(next_state)], visited)
            if result:
                return result
        return None

    for limit in range(max_depth + 1):
        visited = set()
        result = dls(start, end_tup, limit, [start_tup], visited)
        if result:
            return result
    return None

#Region difference heuristic
def path_astar(start, end):
    """A* search between start and end."""
    open_set = []
    counter = itertools.count()  # unique tie-breaker

    heapq.heappush(open_set, (0, next(counter), start))
    came_from = {}
    g_score = {start.to_tuple(): 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current.to_tuple() == end.to_tuple():
            # reconstruct path
            path = [current.to_tuple()]
            while current.to_tuple() in came_from:
                current = came_from[current.to_tuple()]
                path.append(current.to_tuple())
            return list(reversed(path))

        for next_state in current.moves():
            tentative_g = g_score[current.to_tuple()] + 1  # or move cost
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
    """Compare performance of BFS, DFS, IDDFS, and A* on example boards."""
    # Simple 3x3 binary example
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

    print("=== Comparing Search Algorithms ===")
    for name, func in algorithms:
        t0 = perf_counter()
        path = func(start, end)
        t1 = perf_counter()
        print(f"{name:6s} | Path found: {path is not None} | "
              f"Length: {len(path) if path else 0:2d} | "
              f"Time: {(t1 - t0)*1000:7.2f} ms")
    print("===================================")

def tester():
    """Simple test harness for verifying path search algorithms."""
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

    print("\n--- Running BFS ---")
    print(path_BFS(s1, s2))

    print("\n--- Running DFS ---")
    print(path_DFS(s1, s2))

    print("\n--- Running IDDFS ---")
    print(path_IDDFS(s1, s2))

    print("\n--- Running A* ---")
    print(path_astar(s1, s2))



    print("\n--- Performance Comparison ---")
    compare()



if __name__ == "__main__":
    tester()
