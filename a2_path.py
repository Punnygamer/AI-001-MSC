"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a Search algorithms for task 2
Group no: C9
Student ID : 100397265
Student Name: Joshua Galvao

"""

from a1_state import state
from copy import deepcopy
from collections import deque

def safe(state):
    if state.numHingers== 0:
        return True
    else:
        return False
    
def tuptlestate(state):
    tup=[]
    for row in state.grid:
        tup.append(tuple(row))
    return tuple(tup)
    
def path_BFS(start,end):
    if not safe(start) or not safe(end):
        return None

    start_t = tuptlestate(start)
    end_t = tuptlestate(end)

    queue = deque([(start, [start_t])])
    visited = {start_t}

    while queue:
        current, path = queue.popleft()
        if tuptlestate(current) == end_t:
            return path

        for next_state in current.moves():
            if not safe(next_state):
                continue
            key = tuptlestate(next_state)
            if key not in visited:
                visited.add(key)
                queue.append((next_state, path + [key]))
    return None


def path_DFS(start,end):
    if not safe(start) or not safe(end):
        return None

    start_t = tuptlestate(start)
    end_t = tuptlestate(end)
    visited = set()

    def dfs(current, path):
        key = tuptlestate(current)
        if key in visited:
            return None
        visited.add(key)

        if key == end_t:
            return path

        for next_state in current.moves():
            if not safe(next_state):
                continue
            result = dfs(next_state, path + [tuptlestate(next_state)])
            if result:
                return result
        return None

    return dfs(start, [start_t])

def path_IDDFS(start,end,max_depth=10):
    if not safe(start) or not safe(end):
        return None

    start_t = tuptlestate(start)
    end_t = tuptlestate(end)

    def dls(current, end_t, depth, path, visited):
        key = tuptlestate(current)
        if key in visited:
            return None
        visited.add(key)

        if key == end_t:
            return path
        if depth == 0:
            return None

        for next_state in current.moves():
            if not safe(next_state):
                continue
            result = dls(next_state, end_t, depth - 1,
                         path + [tuptlestate(next_state)], visited)
            if result:
                return result
        return None

    for limit in range(max_depth + 1):
        visited = set()
        result = dls(start, end_t, limit, [start_t], visited)
        if result:
            return result
    return None

def path_astar(start,end):
    return

def compare(state):
    return