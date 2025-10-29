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
    return

def path_IDDFS(start,end):
    return

def path_astar(start,end):
    return

def compare(state):
    return