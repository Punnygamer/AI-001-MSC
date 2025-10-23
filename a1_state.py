from copy import deepcopy
from collections import deque

class state():
    def __init__(self, grid):
        self.grid = deepcopy(grid)
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def in_bounds(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def adjacent_cells(self, i, j):
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if self.in_bounds(ni, nj):
                    yield (ni, nj)

    def is_active(self, i, j):
        return self.grid[i][j] > 0

    def moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] > 0:
                    new_grid = deepcopy(self.grid)
                    new_grid[i][j] -= 1
                    yield state(new_grid)

    def numRegions(self):
        visited = [[False] * self.cols for _ in range(self.rows)]
        regions = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_active(i, j) and not visited[i][j]:
                    regions += 1
                    queue = deque([(i, j)])
                    visited[i][j] = True
                    while queue:
                        ci, cj = queue.popleft()
                        for ni, nj in self.adjacent_cells(ci, cj):
                            if self.is_active(ni, nj) and not visited[ni][nj]:
                                visited[ni][nj] = True
                                queue.append((ni, nj))
        return regions

    def numHingers(self):
        count = 0
        base_regions = self.numRegions()

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    # Simulate removing this cell
                    new_grid = deepcopy(self.grid)
                    new_grid[i][j] = 0
                    new_state = state(new_grid)
                    new_regions = new_state.numRegions()

                    if new_regions > base_regions:
                        count += 1
        return count


def tester():
    print("=== Hinger Game: State Tester ===")

    sa_grid = [
        [0, 1, 0, 0, 2],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    sa = state(sa_grid)
    print("State A:\n", sa)
    print("Number of regions:", sa.numRegions())
    print("Number of hingers:", sa.numHingers())

    print("\nPossible next states (1-move each):")
    for idx, next_state in enumerate(sa.moves(), 1):
        print(f"\nMove {idx}:")
        print(next_state)

    print("\nTester completed.")

tester()