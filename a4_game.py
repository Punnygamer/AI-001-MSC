#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a State class for Task 4
Group no: C9
Student ID : 100538270
Student Name: Maiusana Suthesan

"""

import time
from copy import deepcopy
from a3_agent import agent
from a1_state import state


def is_legal_move(st, move):
    grid = st.grid if hasattr(st, "grid") else st
    r, c = move
    return (
        0 <= r < len(grid)        
        and 0 <= c < len(grid[0])  
        and grid[r][c] > 0         
    )



def play(st, agentA, agentB, modeA="alphabeta", modeB="alphabeta", time_limit=60, log_file="game_log.txt"):
    
    if hasattr(st, "grid"):
        current_state = state(st.grid)
    else:
        current_state = state(st)

    move_history = []
    total_time = {"A": 0.0, "B": 0.0}
    move_count = {"A": 0, "B": 0}

    

    def is_hinger_move(state_obj, move):
        r, c = move
        if state_obj.grid[r][c] != 1:
            return False
        current_regions = state_obj.numRegions()
        new_grid = deepcopy(state_obj.grid)
        new_grid[r][c] = 0
        new_state = state(new_grid)
        new_regions = new_state.numRegions()
        return new_regions > current_regions



    def available_moves():
        moves = []
        for i in range(current_state.rows):
            for j in range(current_state.cols):
                if current_state.grid[i][j] > 0:
                    moves.append((i, j))
        return moves

    

    def apply_move(move):
        r, c = move
        if current_state.grid[r][c] == 1:
            current_state.grid[r][c] = 0
        elif current_state.grid[r][c] > 1:
            current_state.grid[r][c] -= 1

    
    def game_over():
        return len(available_moves()) == 0

    print("Initial state:")
    print(current_state)

    turn = 0
    winner = None
    start_time = time.time()

    
    with open(log_file, "w") as f:
        f.write("Hinger Game Log\n")
        f.write("="*20 + "\n")
        while True:
           
            player = "A" if turn % 2 == 0 else "B"
            current_agent = agentA if player == "A" else agentB
            mode = modeA if player == "A" else modeB
            print(f"\n--- Player {player}'s Turn ---")

            
            if game_over():
                print("No moves left - Draw!")
                winner = None
                break

        
            t0 = time.time()
            if current_agent is None:
              
                print("Available moves:", available_moves())
                try:
                    r = int(input("Enter row: "))
                    c = int(input("Enter col: "))
                    move = (r, c)
                except Exception:
                    print("Invalid input! Opponent wins.")
                    winner = "B" if player == "A" else "A"
                    break
            else:
                
                move = current_agent.move(current_state, mode)
                print(f"{current_agent.name} chooses {move}")

            
            elapsed = time.time() - t0
            total_time[player] += elapsed
            move_count[player] += 1

            if elapsed > time_limit:
                print(f"Player exceeded time limit!")
                winner = "B" if player == "A" else "A"
                break
            if not move or not is_legal_move(current_state, move):
                print(f"Illegal move! Opponent wins.")
                winner = "B" if player == "A" else "A"
                break

        
            hinger_triggered = is_hinger_move(current_state, move)
            apply_move(move)
            move_history.append((player, move))

            print(f"State after Player {player}'s move:")
            print(current_state)

            
            f.write(f"Turn {len(move_history)}: Player {player} -> {move}\n")

            
            if hinger_triggered:
                print(f"HINGER at {move}! Player {player} wins!")
                winner = player
                break

            if game_over():
                print("All counters removed. Draw.")
                winner = None
                break
            turn += 1

        f.write("\n=== GAME OVER ===\n")
        if winner:
            f.write(f"Winner: Player {winner}\n")
        else:
            f.write("Result: Draw\n")

    print("\n=== GAME OVER ===")
    if winner:
        print(f"Winner: Player {winner}")
    else:
        print("Draw")

    print(f"Moves: A={move_count['A']} | B={move_count['B']}")
    print(f"Time: A={total_time['A']:.2f}s | B={total_time['B']:.2f}s")
    print(f"Log saved to: {log_file}")

    return winner


def tester():
    print("=== Hinger Game: Play Tester ===\n")

    grid1 = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1]
    ]

    state1 = state(grid1)
    agentA = agent((3, 4), name="AgentA")
    agentB = agent((3, 4), name="AgentB")

    winner = play(state1, agentA, agentB, modeA="alphabeta", modeB="minimax", time_limit=10)
    print(f"\nTest complete. Winner: {winner}")

    print("\nTester completed.")

if __name__ == "__main__":
    tester()
