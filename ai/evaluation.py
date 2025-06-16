# ai/evaluation.py
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

    # Codifica el turno (0 para blancas, 1 para negras)
    turn_value = 1.0 if board.current_turn == 'black' else 0.0
    vector = np.append(vector, turn_value)

    return vector


def evaluate_board(board, individual):
    vector = board_to_vector(board)
    base_score = individual.evaluate(vector)  # ∈ [-1, 1]

    # BONUS: movilidad reducida
    current_moves = len(board.get_legal_moves(board.current_turn))
    opponent_moves = len(board.get_legal_moves('black' if board.current_turn == 'white' else 'white'))
    mobility_score = (current_moves - opponent_moves) / 100.0

    # BONUS: control del centro
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    center_control = 0
    for x, y in center_squares:
        piece = board.board[y][x]
        if piece and piece.color == board.current_turn:
            center_control += 1
    center_score = center_control / 8.0  # Máx. 0.5

    # BONUS: capturas
    capture_bonus = 0.0
    if board.history:
        last_move = board.history[-1]
        captured_piece = last_move[1] if len(last_move) > 1 else None
        if captured_piece:
            # Bonificación según el valor relativo de la pieza capturada
            piece_value = {
                'pawn': 1, 'knight': 3, 'bishop': 3,
                'rook': 5, 'queen': 9, 'king': 0  # nunca debería capturar rey
            }
            value = piece_value.get(captured_piece.name, 0)
            capture_bonus = value / 100.0  # máximo +0.09

    # Total preliminar
    score = base_score + mobility_score + center_score + capture_bonus

    # Penalización o recompensa por jaque mate
    if board.is_checkmate(board.current_turn):
        score = -1.0
    elif board.is_checkmate('black' if board.current_turn == 'white' else 'white'):
        score = 1.0

    # Penalización por repetición
    repetition_count = {}
    for _, _, signature in board.history:
        repetition_count[signature] = repetition_count.get(signature, 0) + 1

    current_signature = board.board_signature()
    rep = repetition_count.get(current_signature, 0)
    score -= rep * 0.01

    # Clamp final
    return max(-1.0, min(1.0, score))
