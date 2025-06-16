# utils/fen.py

import random

def load_fen(piece_placement_fen):
    from game.pieces import Piece
    board = [[None for _ in range(8)] for _ in range(8)]
    rows = piece_placement_fen.split('/')
    for y, row in enumerate(rows):
        x = 0
        for char in row:
            if char.isdigit():
                x += int(char)
            else:
                piece_color = 'white' if char.isupper() else 'black'
                name_map = {
                    'p': 'pawn', 'n': 'knight', 'b': 'bishop',
                    'r': 'rook', 'q': 'queen', 'k': 'king'
                }
                name = name_map[char.lower()]
                board[y][x] = Piece(name, piece_color)
                x += 1
    return board



import random

def generate_random_fen():
    piece_pool = {
        'white': ['P'] * 8 + ['N', 'B', 'R', 'Q'],
        'black': ['p'] * 8 + ['n', 'b', 'r', 'q']
    }

    # Siempre incluir los 2 reyes
    all_pieces = ['K', 'k']
    all_pieces += random.sample(piece_pool['white'], k=random.randint(5, 10))
    all_pieces += random.sample(piece_pool['black'], k=random.randint(5, 10))

    # Colocar las piezas aleatoriamente en el tablero
    positions = random.sample(range(64), k=len(all_pieces))
    board = [None] * 64
    for pos, piece in zip(positions, all_pieces):
        board[pos] = piece

    # Convertimos a filas estilo FEN
    fen_rows = []
    for rank in range(8):
        row = ''
        empty = 0
        for file in range(8):
            piece = board[rank * 8 + file]
            if piece is None:
                empty += 1
            else:
                if empty > 0:
                    row += str(empty)
                    empty = 0
                row += piece
        if empty > 0:
            row += str(empty)
        fen_rows.append(row)

    # Turno aleatorio
    turn = random.choice(['w', 'b'])

    # Resto de campos FEN
    castling = '-'
    en_passant = '-'
    halfmove_clock = '0'
    fullmove_number = '1'

    fen = f"{'/'.join(fen_rows)} {turn} {castling} {en_passant} {halfmove_clock} {fullmove_number}"
    return fen
