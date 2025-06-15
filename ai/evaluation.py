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

    # Material + estructura evaluada por la red/genoma
    score = individual.evaluate(vector)

    # Evaluar movilidad
    current_moves = len(board.get_legal_moves(board.current_turn))
    opponent_moves = len(board.get_legal_moves('black' if board.current_turn == 'white' else 'white'))
    mobility_score = (current_moves - opponent_moves) * 0.1
    score += mobility_score

    # Penalización por jaque mate
    if board.is_checkmate(board.current_turn):
        score -= 1000
    elif board.is_checkmate('black' if board.current_turn == 'white' else 'white'):
        score += 1000

    # Penalización por repetición de estados
    repetition_count = {}
    for _, _, signature in board.history:
        repetition_count[signature] = repetition_count.get(signature, 0) + 1

    current_signature = board.board_signature()
    rep = repetition_count.get(current_signature, 0)

    if rep >= 2:
        score -= rep * 10  # Penaliza 10 puntos por repetición

    return score
