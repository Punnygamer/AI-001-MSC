#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a State class for Task 1

@author: C9 (100397265 Joshua Galvao)
@date:   29/09/2025

"""

from copy import deepcopy
from collections import deque
#state class basically the underlying logic of the game
class State():
    #a initialiser that creates a grid from an input of a 2d array
    def __init__(self, grid):
        self.grid = deepcopy(grid)
        self.rows = len(grid)
        if self.rows > 0:
            self.cols = len(grid[0])
        else:
            self.cols = 0
    
    #string method that outputs the current grid
    def __str__(self):
        string=""
        for rows in self.grid:
            for cell in rows:
                string+=str(cell)+" "
            string+="\n"
        return string
    
    #checks to see if the coordinates is in bounds
    def in_grid(self, y, x):
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return True
        else:
            return False
        
    #checks if a cell is active
    def is_active(self, y, x):
        if self.grid[y][x] > 0:
            return True
        else:
            return False
        
    #returns all cells ajacent to the coordinates of the current one 
    def adjacent_cells(self,y,x):
        ajcells=[-1,0,1]
        for ajy in ajcells:
            for ajx in ajcells:
                if ajx == 0 and ajy == 0:
                    continue
                nx= x +ajx
                ny=  y+ ajy
                if self.in_grid(ny,nx):
                    yield (ny,nx)
    
    #returns all possible moves that can be made
    def moves(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] > 0:
                    new_grid = deepcopy(self.grid)
                    new_grid[y][x] -= 1
                    yield State(new_grid)

    #makes a move on the grid itself
    def makemove(self,y,x):
        self.grid[y][x]-=1
        return
    
    '''
    This function finds regions by first creating a visited variable that will be a copy of the grid size but
    with every value inside set to false. this then once it encounters an active value it will iterate through any 
    adjacent active values until it stops finding any and that will be classified as a reigon and also will be classed as visited so
    that the same reigon cant be counted more than once 
    '''
    def numRegions(self):
        visited = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(False)
            visited.append(row)

        regions = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_active(i, j) and visited[i][j]== False:
                    regions += 1
                    queue = deque([(i, j)])
                    visited[i][j] = True
                    while queue:
                        ci,cj = queue.popleft()
                        for ni,nj in self.adjacent_cells(ci, cj):
                            if self.is_active(ni, nj) and not visited[ni][nj]:
                                visited[ni][nj] = True
                                queue.append((ni, nj))
        return regions
    

    def numHingers(self):
        count = 0
        regions = self.numRegions()

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    # Simulate removing this cell
                    ngrid = deepcopy(self.grid)
                    ngrid[i][j] = 0
                    nstate = State(ngrid)
                    nregions = nstate.numRegions()

                    if nregions > regions:
                        count += 1
        return count
    
    def to_tuple(self):
        result = []
        for row in self.grid:
            new_row = []
            for val in row:
                new_row.append(val)
            result.append(tuple(new_row))
        return tuple(result)


def tester():
    print("State Class test")

    sa_grid = [
        [0, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    sa = State(sa_grid)
    print("State A:\n", sa)
    print("Num of regions: ", sa.numRegions())
    print("Num of hingers: ", sa.numHingers())

    print("\nPossible next states (1-move each):")
    for idx, next_state in enumerate(sa.moves(), 1):
        print("\nMove ",idx,": ")
        print(next_state)

    print("\nTest completed.")

if __name__ == "__main__":
    tester()
