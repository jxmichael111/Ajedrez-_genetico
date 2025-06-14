## ai/evaluation.py

import numpy as np

def board_to_vector(board):
    piece_map = {
        'pawn': 0, 'knight': 1, 'bishop': 2,
        'rook': 3, 'queen': 4, 'king': 5
    }
    vector = np.zeros(64 * 12)

    for y in range(8):
        for x in range(8):
            piece = board.board[y][x]
            if piece:
                index = y * 8 + x
                offset = piece_map[piece.name] + (0 if piece.color == 'white' else 6)
                vector[index * 12 + offset] = 1

    # Nueva línea: codifica el turno (0 para blancas, 1 para negras)
    turn_value = 1.0 if board.current_turn == 'black' else 0.0
    vector = np.append(vector, turn_value)

    return vector


def evaluate_board(board, individual):
    vector = board_to_vector(board)
    return individual.evaluate(vector)
