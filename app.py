#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a State class for Task 
Group no: C9
Student ID : 100538270
Student Name: Maiusana Suthesan

"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from copy import deepcopy
import os
from a1_state import state
from a3_agent import agent

app = Flask(__name__)
CORS(app)

game_state = {
    'current_state': None,
    'initial_state': None,
    'move_history': [],
    'current_player': 'A',
    'winner': None,
    'game_mode': 'human_vs_human'
}


def get_hinger_positions(st):
    """Get all hinger positions in current state"""
    hingers = []
    base_regions = st.numRegions()

    for i in range(st.rows):
        for j in range(st.cols):
            if st.grid[i][j] == 1:
                new_grid = deepcopy(st.grid)
                new_grid[i][j] = 0
                new_state = state(new_grid)
                new_regions = new_state.numRegions()

                if new_regions > base_regions:
                    hingers.append([i, j])

    return hingers


def is_hinger_move(st, row, col):
    """Check if move at (row, col) triggers a hinger win"""
    if st.grid[row][col] != 1:
        return False

    current_regions = st.numRegions()

    new_grid = deepcopy(st.grid)
    new_grid[row][col] = 0
    new_state = state(new_grid)
    new_regions = new_state.numRegions()

    return new_regions > current_regions


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/api/init_game', methods=['POST'])
def init_game():
    data = request.json
    grid = data.get('grid')
    mode = data.get('mode', 'human_vs_human')

    if not grid:
        return jsonify({'success': False, 'error': 'No grid provided'}), 400

    initial_st = state(grid)

    game_state['current_state'] = state(grid)
    game_state['initial_state'] = initial_st
    game_state['move_history'] = []
    game_state['current_player'] = 'A'
    game_state['winner'] = None
    game_state['game_mode'] = mode

    return jsonify({
        'success': True,
        'grid': game_state['current_state'].grid,
        'regions': game_state['current_state'].numRegions(),
        'hingers': game_state['current_state'].numHingers(),
        'current_player': game_state['current_player'],
        'move_history': game_state['move_history'],
        'winner': None,
        'is_draw': False
    })


@app.route('/api/get_state', methods=['GET'])
def get_state():
    if not game_state['current_state']:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    return jsonify({
        'success': True,
        'grid': game_state['current_state'].grid,
        'regions': game_state['current_state'].numRegions(),
        'hingers': game_state['current_state'].numHingers(),
        'current_player': game_state['current_player'],
        'move_history': game_state['move_history'],
        'winner': game_state['winner'],
        'is_draw': game_state['winner'] is None and len(get_available_moves()) == 0
    })


def get_available_moves():
    """Get all available moves from current state"""
    if not game_state['current_state']:
        return []

    moves = []
    st = game_state['current_state']
    for i in range(st.rows):
        for j in range(st.cols):
            if st.grid[i][j] > 0:
                moves.append([i, j])
    return moves


@app.route('/api/make_move', methods=['POST'])
def make_move():
    data = request.json
    row = data.get('row')
    col = data.get('col')

    if game_state['winner']:
        return jsonify({'success': False, 'error': 'Game already ended'}), 400

    st = game_state['current_state']

    if row < 0 or row >= st.rows or col < 0 or col >= st.cols:
        return jsonify({'success': False, 'error': 'Invalid position'}), 400

    if st.grid[row][col] <= 0:
        return jsonify({'success': False, 'error': 'No counters at this position'}), 400

    hinger = is_hinger_move(st, row, col)

    st.grid[row][col] -= 1

    game_state['move_history'].append({
        'player': game_state['current_player'],
        'position': [row, col],
        'was_hinger': hinger
    })

    if hinger:
        game_state['winner'] = game_state['current_player']
        message = f"Player {game_state['current_player']} WINS by removing a hinger!"
        return jsonify({
            'success': True,
            'grid': st.grid,
            'regions': st.numRegions(),
            'hingers': st.numHingers(),
            'current_player': game_state['current_player'],
            'move_history': game_state['move_history'],
            'winner': game_state['winner'],
            'is_hinger': True,
            'is_draw': False,
            'message': message
        })

    available = get_available_moves()
    if len(available) == 0:
        message = " Game Draw - No more moves!"
        return jsonify({
            'success': True,
            'grid': st.grid,
            'regions': st.numRegions(),
            'hingers': st.numHingers(),
            'current_player': game_state['current_player'],
            'move_history': game_state['move_history'],
            'winner': None,
            'is_draw': True,
            'message': message
        })

    game_state['current_player'] = 'B' if game_state['current_player'] == 'A' else 'A'

    return jsonify({
        'success': True,
        'grid': st.grid,
        'regions': st.numRegions(),
        'hingers': st.numHingers(),
        'current_player': game_state['current_player'],
        'move_history': game_state['move_history'],
        'winner': None,
        'is_draw': False,
        'ai_turn': False
    })


@app.route('/api/check_hingers', methods=['GET'])
def check_hingers():
    if not game_state['current_state']:
        return jsonify({'success': False, 'error': 'No active game'}), 400

    hingers = get_hinger_positions(game_state['current_state'])

    return jsonify({
        'success': True,
        'hingers': hingers,
        'count': len(hingers)
    })


if __name__ == '__main__':
    print("="*50)
    print("Hinger Game Web Server")
    print("="*50)
    print("Starting server at http://localhost:5000")
    print("Open browser and navigate to http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("="*50)
    app.run(debug=True, port=5000)
