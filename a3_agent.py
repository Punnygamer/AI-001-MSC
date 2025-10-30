#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a State class for Task 3
Group no: C9
Student ID : 100538270
Student Name: Maiusana Suthesan

"""

from copy import deepcopy
import random
from functools import lru_cache
from a1_state import state

class agent:
    
    def __init__(self, size, name="Agent"):
        self.size = size  
        self.name = name  
        self.modes = ["minimax", "alphabeta", "mcts"]  
        self.default_depth = 6  
        self.mcts_playouts = 200  

    
    def __str__(self):
        return f"Agent(name={self.name}, size={self.size})"

    
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
            return None  
        score, mv = self._minimax(grid, depth, True)
        return mv

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

def tester():
    print("=== Hinger Game: Agent Tester ===\n")
    ag = agent((3, 4), name="TestAgent")
    print(ag)  

    board1 = [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1]
    ]

    state1 = state(board1)

    print("\nBoard:")
    print(state1)
    print("\nAvailable moves:", ag.active_moves(board1))
    mv_ab = ag.move(board1, mode="alphabeta")  
    mv_mm = ag.move(board1, mode="minimax")    
    mv_mcts = ag.move(board1, mode="mcts")     
    print("Alphabeta move:", mv_ab)
    print("Minimax move:", mv_mm)
    print("MCTS move:", mv_mcts)

    print("\nTester completed.")

if __name__ == "__main__":
    tester()
