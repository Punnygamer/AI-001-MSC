#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project - Pygame Visualization
Coursework 001 for: CMP-7058A Artificial Intelligence

TASK 4b: GUI Visualization using Pygame (ALLOWED library)
Provides a desktop window interface for playing the Hinger game


"""

import pygame
import sys
import os
from copy import deepcopy

# Suppress tester output during import
_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
try:
    from a1_state import state
    from a3_agent import agent
finally:
    sys.stdout.close()
    sys.stdout = _stdout


pygame.init()


COLOR_BG = (44, 62, 80)          # Dark blue-grey background
COLOR_BOARD = (52, 73, 94)       # Slightly lighter for board
COLOR_CELL_EMPTY = (189, 195, 199)  # Light grey for empty cells
COLOR_CELL_ACTIVE = (52, 152, 219)  # Blue for active cells
COLOR_CELL_HINGER = (231, 76, 60)   # Red for hingers
COLOR_CELL_HOVER = (46, 204, 113)   # Green for hover
COLOR_TEXT = (236, 240, 241)     # Off-white text
COLOR_TEXT_DIM = (149, 165, 166) # Dimmed text
COLOR_PLAYER_A = (52, 152, 219)  # Blue for player A
COLOR_PLAYER_B = (155, 89, 182)  # Purple for player B
COLOR_WIN = (46, 204, 113)       # Green for win
COLOR_DRAW = (241, 196, 15)      # Yellow for draw
COLOR_BUTTON = (41, 128, 185)    # Button color
COLOR_BUTTON_HOVER = (52, 152, 219)  # Button hover


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
CELL_SIZE = 80
CELL_MARGIN = 5
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18

# Fonts
FONT_LARGE = pygame.font.Font(None, FONT_SIZE_LARGE)
FONT_MEDIUM = pygame.font.Font(None, FONT_SIZE_MEDIUM)
FONT_SMALL = pygame.font.Font(None, FONT_SIZE_SMALL)



class HingerGamePygame:
    
    def __init__(self, initial_grid=None, mode="human_vs_human"):
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hinger Game - Pygame Visualization")
        self.clock = pygame.time.Clock()

        if initial_grid is None:
            initial_grid = [
                [1, 1, 0, 1],
                [1, 2, 1, 0],
                [0, 1, 1, 1],
                [1, 0, 1, 1]
            ]

        self.initial_grid = deepcopy(initial_grid)
        self.current_state = state(initial_grid)
        self.rows = self.current_state.rows
        self.cols = self.current_state.cols

        # Game mode
        self.mode = mode
        if mode == "human_vs_ai":
            self.ai_agent = agent((self.rows, self.cols), name="AI")
        else:
            self.ai_agent = None

        # Game state tracking
        self.current_player = "A"
        self.winner = None
        self.game_over = False
        self.move_history = []
        self.move_count = {"A": 0, "B": 0}

        # UI state
        self.hovered_cell = None
        self.show_hingers = False
        self.hinger_positions = []

        # Calculate board position (centered)
        board_width = self.cols * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        board_height = self.rows * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        self.board_x = 50
        self.board_y = 160

        # Button definitions
        self.buttons = {
            'new_game': pygame.Rect(WINDOW_WIDTH - 180, 20, 160, 40),
            'show_hingers': pygame.Rect(WINDOW_WIDTH - 180, 70, 160, 40),
            'mode_toggle': pygame.Rect(WINDOW_WIDTH - 180, 120, 160, 40)
        }

        self.running = True

    def get_cell_rect(self, row, col):
        """Get the rectangle for a cell on the board"""
        x = self.board_x + col * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        y = self.board_y + row * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def get_cell_from_pos(self, pos):
        """Get cell coordinates from mouse position"""
        mouse_x, mouse_y = pos

        for row in range(self.rows):
            for col in range(self.cols):
                rect = self.get_cell_rect(row, col)
                if rect.collidepoint(mouse_x, mouse_y):
                    return (row, col)
        return None

    def is_hinger(self, row, col):
        """Check if a cell is a hinger"""
        if self.current_state.grid[row][col] != 1:
            return False

        base_regions = self.current_state.numRegions()
        temp_grid = deepcopy(self.current_state.grid)
        temp_grid[row][col] = 0
        temp_state = state(temp_grid)
        return temp_state.numRegions() > base_regions

    def update_hinger_positions(self):
        """Update the list of hinger positions"""
        self.hinger_positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_hinger(row, col):
                    self.hinger_positions.append((row, col))

    def make_move(self, row, col):
        """
        Make a move at the specified position
        Returns True if move was successful, False otherwise
        """
        if self.game_over:
            return False

        # Check if move is legal
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False

        if self.current_state.grid[row][col] <= 0:
            return False

        # Check if it's a hinger BEFORE making the move
        is_hinger_move = self.is_hinger(row, col)

        # Apply the move
        self.current_state.grid[row][col] -= 1

        # Record move
        self.move_history.append({
            'player': self.current_player,
            'position': (row, col),
            'was_hinger': is_hinger_move
        })
        self.move_count[self.current_player] += 1

        # Check win condition
        if is_hinger_move:
            self.winner = self.current_player
            self.game_over = True
            return True

        # Check if game is over (no moves left)
        has_moves = any(
            self.current_state.grid[i][j] > 0
            for i in range(self.rows)
            for j in range(self.cols)
        )

        if not has_moves:
            self.winner = None  # Draw
            self.game_over = True
            return True

        # Switch player
        self.current_player = 'B' if self.current_player == 'A' else 'A'

        return True

    def ai_move(self):
        """Let AI make a move"""
        if self.ai_agent is None or self.game_over:
            return

        move = self.ai_agent.move(self.current_state, mode='alphabeta')
        if move:
            row, col = move
            self.make_move(row, col)

    def reset_game(self):
        """Reset the game to initial state"""
        self.current_state = state(self.initial_grid)
        self.current_player = "A"
        self.winner = None
        self.game_over = False
        self.move_history = []
        self.move_count = {"A": 0, "B": 0}
        self.show_hingers = False
        self.hinger_positions = []

    def toggle_mode(self):
        """Toggle between Human vs Human and Human vs AI"""
        if self.mode == "human_vs_human":
            self.mode = "human_vs_ai"
            self.ai_agent = agent((self.rows, self.cols), name="AI")
        else:
            self.mode = "human_vs_human"
            self.ai_agent = None
        self.reset_game()

    def draw_board(self):
        """Draw the game board"""
        for row in range(self.rows):
            for col in range(self.cols):
                rect = self.get_cell_rect(row, col)
                cell_value = self.current_state.grid[row][col]

                # Determine cell color
                if self.show_hingers and (row, col) in self.hinger_positions:
                    color = COLOR_CELL_HINGER
                elif self.hovered_cell == (row, col) and cell_value > 0:
                    color = COLOR_CELL_HOVER
                elif cell_value > 0:
                    color = COLOR_CELL_ACTIVE
                else:
                    color = COLOR_CELL_EMPTY

                # Draw cell
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, COLOR_TEXT_DIM, rect, 2)

                # Draw cell value
                if cell_value > 0:
                    text = FONT_LARGE.render(str(cell_value), True, COLOR_TEXT)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def draw_ui(self):
        """Draw UI elements (title, stats, buttons)"""
        # Title
        title = FONT_LARGE.render("Hinger Game", True, COLOR_TEXT)
        self.screen.blit(title, (20, 20))

        # Game stats
        stats_y = 60
        regions = self.current_state.numRegions()
        hingers = self.current_state.numHingers()

        stats_text = [
            f"Regions: {regions}",
            f"Hingers: {hingers}",
            f"Moves: A={self.move_count['A']}, B={self.move_count['B']}"
        ]

        for i, text in enumerate(stats_text):
            surf = FONT_SMALL.render(text, True, COLOR_TEXT_DIM)
            self.screen.blit(surf, (20, stats_y + i * 25))

        # Current player or game result
        status_y = self.board_y + self.rows * (CELL_SIZE + CELL_MARGIN) + 30

        if self.game_over:
            if self.winner:
                status_text = f"Player {self.winner} WINS!"
                status_color = COLOR_WIN
            else:
                status_text = "DRAW!"
                status_color = COLOR_DRAW
        else:
            status_text = f"Player {self.current_player}'s Turn"
            status_color = COLOR_PLAYER_A if self.current_player == 'A' else COLOR_PLAYER_B

        status_surf = FONT_MEDIUM.render(status_text, True, status_color)
        self.screen.blit(status_surf, (self.board_x, status_y))

        # Draw buttons
        self.draw_button('new_game', "New Game")
        self.draw_button('show_hingers', "Show Hingers" if not self.show_hingers else "Hide Hingers")
        mode_text = "vs AI" if self.mode == "human_vs_human" else "vs Human"
        self.draw_button('mode_toggle', mode_text)

        # Mode indicator
        mode_display = "Human vs AI" if self.mode == "human_vs_ai" else "Human vs Human"
        mode_surf = FONT_SMALL.render(mode_display, True, COLOR_TEXT_DIM)
        self.screen.blit(mode_surf, (WINDOW_WIDTH - 180, 170))

        # Move history
        history_y = 220
        history_title = FONT_SMALL.render("Move History:", True, COLOR_TEXT)
        self.screen.blit(history_title, (WINDOW_WIDTH - 180, history_y))

        # Show last 10 moves
        start_idx = max(0, len(self.move_history) - 10)
        for i, move in enumerate(self.move_history[start_idx:]):
            # Display "AI" instead of "B" when in AI mode
            player_name = move['player']
            if self.mode == "human_vs_ai" and player_name == 'B':
                player_name = "AI"

            move_text = f"{player_name}: ({move['position'][0]},{move['position'][1]})"
            if move['was_hinger']:
                move_text += " WIN!"
            move_surf = FONT_SMALL.render(move_text, True, COLOR_TEXT_DIM)
            self.screen.blit(move_surf, (WINDOW_WIDTH - 170, history_y + 25 + i * 20))

    def draw_button(self, button_name, text):
        """Draw a button"""
        rect = self.buttons[button_name]
        mouse_pos = pygame.mouse.get_pos()

        # Check hover
        if rect.collidepoint(mouse_pos):
            color = COLOR_BUTTON_HOVER
        else:
            color = COLOR_BUTTON

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)

        text_surf = FONT_SMALL.render(text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def handle_click(self, pos):
        """Handle mouse click"""
        # Check button clicks
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_name == 'new_game':
                    self.reset_game()
                elif button_name == 'show_hingers':
                    self.show_hingers = not self.show_hingers
                    if self.show_hingers:
                        self.update_hinger_positions()
                    else:
                        self.hinger_positions = []
                elif button_name == 'mode_toggle':
                    self.toggle_mode()
                return

        # Check board clicks
        if not self.game_over:
            cell = self.get_cell_from_pos(pos)
            if cell:
                row, col = cell
                success = self.make_move(row, col)

                # If in AI mode and move was successful, let AI move
                if success and self.mode == "human_vs_ai" and self.current_player == 'B' and not self.game_over:
                    pygame.time.wait(500)  # Small delay for better UX
                    self.ai_move()

    def run(self):
        """Main game loop"""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.hovered_cell = self.get_cell_from_pos(event.pos)

            # Drawing
            self.screen.fill(COLOR_BG)
            self.draw_board()
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()



PRESET_GRIDS = {
    '4x4_default': [
        [1, 1, 0, 1],
        [1, 2, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 1, 1]
    ],
    '4x5_complex': [
        [0, 1, 0, 0, 2],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ],
    '5x5_large': [
        [1, 1, 0, 1, 1],
        [1, 2, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 1, 2]
    ]
}



def main():
    
    print("Hinger Game")
    print("Starting GUI application...")
    print()

    # Choose grid (can be modified)
    grid = PRESET_GRIDS['4x4_default']

    # Create and run game
    game = HingerGamePygame(initial_grid=grid, mode="human_vs_human")
    game.run()


if __name__ == "__main__":
    main()
