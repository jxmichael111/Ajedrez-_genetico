# ai/player_ai.py
from ai.evaluation import board_to_vector
import random  # Asegúrate de importar esto arriba si no está

class AIPlayer:
    def __init__(self, board, individual):
        self.board = board
        self.individual = individual

    

    def get_best_move(self):
        current_color = self.board.current_turn
        opponent_color = 'black' if current_color == 'white' else 'white'

        best_score = float('-inf')
        best_moves = []

        for move in self.board.get_legal_moves(current_color):
            self.board.apply_move(move)

            # Nivel 2: simular respuesta del oponente
            opponent_moves = self.board.get_legal_moves(opponent_color)
            if not opponent_moves:
                score = self.evaluate_board()
            else:
                worst_response = float('inf')
                for opp_move in opponent_moves:
                    self.board.apply_move(opp_move)
                    score = self.evaluate_board()
                    worst_response = min(worst_response, score)
                    self.board.undo_move()
                score = worst_response

            self.board.undo_move()

            # Comparar con el mejor score encontrado hasta ahora
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        # Si hay varios movimientos igual de buenos, escoge uno aleatorio
        return random.choice(best_moves) if best_moves else None


    def evaluate_board(self):
        score = self.individual.evaluate(board_to_vector(self.board))
    
        # BONUS: movilidad
        legal_moves = len(self.board.get_legal_moves(self.board.current_turn))
        score += 0.1 * legal_moves
    
        # BONUS: control del centro (e4, d4, e5, d5)
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        control = 0
        for x, y in center_squares:
            piece = self.board.board[y][x]
            if piece and piece.color == self.board.current_turn:
                control += 1
        score += 0.5 * control
    
        return score

