from a1_state import state
from copy import deepcopy
from collections import deque

def safe(state):
    if state.numHingers== 0:
        return True
    else:
        return False
    
def tuptualstate(state):
    tup=[]
    for row in state.grid:
        tup.append(tuple(row))
    return tuple(tup)
    
def path_BFS(start,end):
    
    
    return 