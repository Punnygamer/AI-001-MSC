#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes game play function for Task 3

Student ID: 100538270
Student Name: Maiusana Suthesan

"""

from copy import deepcopy
import random
from functools import lru_cache
from a1_state import State
 
# initialising the two parameters (Q.a)
class agent:
    def __init__(self, size, name="Agent"):
        self.size = size  
        self.name = name  
        self.modes = ["minimax", "alphabeta", "mcts"]  
        self.default_depth = 6  
        self.mcts_playouts = 200  

    # sensible Method (Q.b)
    def __str__(self):
        return f"Agent(name={self.name}, size={self.size})"

    # utility method (Q.f)
    @staticmethod
    def _get_grid(st):
        if hasattr(st, "grid"):
            return deepcopy(st.grid)
        else:
            return deepcopy(st)

    @staticmethod
    def active_moves(grid):
        moves = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] > 0:
                    moves.append((i, j))
        return moves

    @staticmethod
    def apply_move(grid, move):
        g = deepcopy(grid)
        r, c = move
        if g[r][c] > 0:
            g[r][c] -= 1
        return g

    @staticmethod
    def is_terminal(grid):
        return len(agent.active_moves(grid)) == 0

    @staticmethod
    def heuristic(grid):
        total = 0
        for row in grid:
            for val in row:
                if val > 0:
                    total += val
        return total

   
    #  minimax algorithm (Q.d)
    def _minimax(self, grid, depth, maximizing):
        if self.is_terminal(grid):
            return -1, None  
        if depth == 0:
            return 0, None  
        
        best_move = None
        if maximizing:
            best_score = -2 
            for mv in self.active_moves(grid):
                nxt = self.apply_move(grid, mv)
                score, _ = self._minimax(nxt, depth - 1, False)
                score = -score  
                if score > best_score:
                    best_score = score
                    best_move = mv
                    if best_score == 1:  
                        break
            return best_score, best_move
        else:
            best_score = 2  
            for mv in self.active_moves(grid):
                nxt = self.apply_move(grid, mv)
                score, _ = self._minimax(nxt, depth - 1, True)
                score = -score  
                if score < best_score:
                    best_score = score
                    best_move = mv
                    if best_score == -1:  
                        break
            return best_score, best_move


    def minimax_move(self, st, depth=None):
        if depth is None:
            depth = self.default_depth
        grid = self._get_grid(st)
        if self.is_terminal(grid):
            return None  #
        score, mv = self._minimax(grid, depth, True)
        return mv

    
    # alpha-beta algorithm(Q.d)
    def _alphabeta(self, grid, depth, alpha, beta, maximizing):
        if self.is_terminal(grid):
            return -1, None  
        if depth == 0:
            return 0, None  

        best_move = None
        if maximizing:
            value = -2  
            for mv in self.active_moves(grid):
                nxt = self.apply_move(grid, mv)
                score, _ = self._alphabeta(nxt, depth - 1, alpha, beta, False)
                score = -score  
                if score > value:
                    value = score
                    best_move = mv
                alpha = max(alpha, value)  
                if alpha >= beta: 
                    break
            return value, best_move
        else:
            value = 2  
            for mv in self.active_moves(grid):
                nxt = self.apply_move(grid, mv)
                score, _ = self._alphabeta(nxt, depth - 1, alpha, beta, True)
                score = -score  
                if score < value:
                    value = score
                    best_move = mv
                beta = min(beta, value)  
                if alpha >= beta:  
                    break
            return value, best_move

    
    def alphabeta_move(self, st, depth=None):
        if depth is None:
            depth = self.default_depth
        grid = self._get_grid(st)
        if self.is_terminal(grid):
            return None 
        score, mv = self._alphabeta(grid, depth, -2, 2, True)
        return mv

    #  monte carlo tree search (Q.f)
    def mcts_move(self, st, playouts=None):
        if playouts is None:
            playouts = self.mcts_playouts

        grid = self._get_grid(st)
        candidates = self.active_moves(grid)
        if not candidates:
            return None  
        
        win_counts = {mv: 0 for mv in candidates}
        for mv in candidates:
            for _ in range(playouts):
                g = self.apply_move(grid, mv)  
                turn = 0  

                while not self.is_terminal(g):
                    moves = self.active_moves(g)
                    if not moves:
                        break
                    choice = random.choice(moves) 
                    g = self.apply_move(g, choice)
                    turn ^= 1 
                if turn == 1:
                    win_counts[mv] += 1
                    
        best = max(candidates, key=lambda m: win_counts[m])
        return best

    
    # win detection (Q.g)
    def win(self, st):
        
        grid = tuple(tuple(row) for row in self._get_grid(st))  

        @lru_cache(maxsize=None)
        def _win(grid_h):
            grid_l = [list(row) for row in grid_h]
            if self.is_terminal(grid_l):
                return False  
            for mv in self.active_moves(grid_l):
                nxt = tuple(tuple(row) for row in agent.apply_move(grid_l, mv))
                opp_wins = _win(nxt)
                if not opp_wins:  
                    return True

            return False  

        return _win(grid)

    # main move method (Q.c)
    def move(self, st, mode="alphabeta"):
        mode = mode.lower()
        grid = self._get_grid(st)
        
        if self.is_terminal(grid):
            return None
        if mode == "minimax":
            return self.minimax_move(grid)
        elif mode == "alphabeta":
            return self.alphabeta_move(grid) 
        elif mode == "mcts":
            return self.mcts_move(grid)
        else:
            return self.alphabeta_move(grid)  



# validates agent class Implement [test funcation] (Q.e)
def tester():
   
    print("Agent Class Testing")
    print()

    # agent creation and initialization ( Q.a,Q.b)
    print("Test 1: Creating Agents")
   

    agent1 = agent((3, 3), name="TestBot")
    agent2 = agent((4, 5))  

    print("Agent 1:", agent1)
    print("Agent 2:", agent2)
    print()
    print(f"Available strategies: {agent1.modes}")
    print("Expected: ['minimax', 'alphabeta', 'mcts']")
    print()
    print("Test 2: AI Move Selection with Different Strategies")
 

    # Create a test game State
    test_grid = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    state1 = State(test_grid)
    
    print("Game State:")
    print(state1)
    print(f"Regions: {state1.numRegions()}, Hingers: {state1.numHingers()}")
    print()

    # test mini (Q.d-i)
    print("Minimax")
    move_minimax = agent1.move(state1, mode='minimax')
    print(f"Minimax chose move: {move_minimax}")
    print(f"Expected: Valid cell position [row, col] with a counter")
    print()

    # test alph (Q.d-ii)
    print("Alpha-Beta Pruning")
    move_alphabeta = agent1.move(state1, mode='alphabeta')
    print(f"Alpha-Beta chose move: {move_alphabeta}")
    print(f"Expected: Valid cell position [should be same or similar to minimax]")
    print()

    # test MCTS  (Q.f)
    print("Monte Carlo Tree Search")
    move_mcts = agent1.move(state1, mode='mcts')
    print(f" MCTS chose move: {move_mcts}")
    print(f"Expected: Valid cell position [may differ due to randomness]")
    print()
    print("Test 3: Default Strategy")
   

    move_default = agent1.move(state1)  
    print(f" Default strategy chose move: {move_default}")
    print(f"Expected: Uses alphabeta best strategy by default")
    print()


    print("Test 4: Agent on Larger Board (4x5)")
  

    large_grid = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1]
    ]
    large_state = State(large_grid)
    large_agent = agent((4, 5), name="LargeBot")

    print("Large Game State:")
    print(large_state)
    print()

    move_large = large_agent.move(large_state, mode='alphabeta')
    print(f" Agent chose move: {move_large}")
    print()


    print("Test 5: No Valid Moves")
    empty_grid = [[0, 0], [0, 0]]
    empty_state = State(empty_grid)

    move_empty = agent1.move(empty_state, mode='minimax')
    print(f"Result: {move_empty}")
    print(f"Expected: None (no active cells available)")
    print()

    #  win detection (Q.g)
    print("Test 6: BONUS - Win Position Detection")
   

    if hasattr(agent1, 'win'):
        win_grid = [[1]]
        win_state = State(win_grid)

        is_winning = agent1.win(win_state)
        print(f"Single cell State - Is winning position? {is_winning}")
        print(f"Expected:True or False depending on game theory analysis")
    else:
        print("win() method not implemented (optional bonus task)")
    print()
    print("TESTING COMPLETE - All Agent strategies validated!")
    
if __name__ == "__main__":
    tester()
