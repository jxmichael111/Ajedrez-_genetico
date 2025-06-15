from game.pieces import Piece

class Board:
    def __init__(self):
        self.board = self.create_start_position()
        self.current_turn = 'white'
        self.history = []

    def create_start_position(self):
        board = [[None]*8 for _ in range(8)]
        setup = [
            ('rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'),
            ['pawn']*8
        ]
        for i in range(8):
            board[1][i] = Piece('pawn', 'black')
            board[6][i] = Piece('pawn', 'white')
        for i in range(8):
            board[0][i] = Piece(setup[0][i], 'black')
            board[7][i] = Piece(setup[0][i], 'white')
        return board

    def apply_move(self, move):
        x1, y1, x2, y2 = move
        moving_piece = self.board[y1][x1]
        captured_piece = self.board[y2][x2]
        self.board[y2][x2] = moving_piece
        self.board[y1][x1] = None
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

        # Guardar la firma del tablero para detectar ciclos
        signature = self.board_signature()
        self.history.append((move, captured_piece, signature))

    def undo_move(self):
        if not self.history:
            return
        (x1, y1, x2, y2), captured_piece, _ = self.history.pop()
        self.board[y1][x1] = self.board[y2][x2]
        self.board[y2][x2] = captured_piece
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def board_signature(self):
        signature = ''
        for row in self.board:
            for piece in row:
                if piece:
                    signature += piece.color[0] + piece.name[0]
                else:
                    signature += '..'
        signature += self.current_turn[0]  # 'w' o 'b'
        return signature

    def is_in_check(self, color):
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.name == 'king' and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break
        if not king_pos:
            return True

        enemy_color = 'black' if color == 'white' else 'white'
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color == enemy_color:
                    original_piece = self.board[king_pos[1]][king_pos[0]]
                    temp = self.board[king_pos[1]][king_pos[0]]
                    self.board[king_pos[1]][king_pos[0]] = None
                    moves = self.get_legal_moves(enemy_color, skip_check=True)
                    self.board[king_pos[1]][king_pos[0]] = original_piece
                    if (king_pos[0], king_pos[1]) in [(mx2, my2) for _, _, mx2, my2 in moves]:
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        return len(self.get_legal_moves(color)) == 0

    def get_legal_moves(self, color, skip_check=False):
        moves = []
        directions = {
            'pawn':   [(-1, -1), (0, -1), (1, -1)] if color == 'white' else [(-1, 1), (0, 1), (1, 1)],
            'rook':   [(0,1), (1,0), (0,-1), (-1,0)],
            'bishop': [(-1,1), (1,1), (-1,-1), (1,-1)],
            'queen':  [(0,1), (1,0), (0,-1), (-1,0), (-1,1), (1,1), (-1,-1), (1,-1)],
            'king':   [(0,1), (1,0), (0,-1), (-1,0), (-1,1), (1,1), (-1,-1), (1,-1)],
            'knight': [(-2,1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1)]
        }
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    name = piece.name
                    if name == 'pawn':
                        for dx, dy in directions['pawn']:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 8 and 0 <= ny < 8:
                                target = self.board[ny][nx]
                                if dx == 0 and target is None:
                                    moves.append((x, y, nx, ny))
                                elif dx != 0 and target and target.color != color:
                                    moves.append((x, y, nx, ny))
                    elif name == 'knight':
                        for dx, dy in directions['knight']:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 8 and 0 <= ny < 8:
                                target = self.board[ny][nx]
                                if not target or target.color != color:
                                    moves.append((x, y, nx, ny))
                    elif name in ['rook', 'bishop', 'queen']:
                        for dx, dy in directions[name]:
                            for i in range(1, 8):
                                nx, ny = x + dx*i, y + dy*i
                                if not (0 <= nx < 8 and 0 <= ny < 8):
                                    break
                                target = self.board[ny][nx]
                                if target is None:
                                    moves.append((x, y, nx, ny))
                                elif target.color != color:
                                    moves.append((x, y, nx, ny))
                                    break
                                else:
                                    break
                    elif name == 'king':
                        for dx, dy in directions['king']:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 8 and 0 <= ny < 8:
                                target = self.board[ny][nx]
                                if not target or target.color != color:
                                    moves.append((x, y, nx, ny))

        if not skip_check:
            legal_moves = []
            for move in moves:
                self.apply_move(move)
                if not self.is_in_check(color):
                    legal_moves.append(move)
                self.undo_move()
            return legal_moves
        return moves
