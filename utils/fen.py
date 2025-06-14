def load_fen(fen):
    from game.pieces import Piece
    board = [[None for _ in range(8)] for _ in range(8)]
    rows = fen.split()[0].split('/')
    color = 'white'
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
