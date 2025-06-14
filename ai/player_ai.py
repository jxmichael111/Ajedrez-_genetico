# ai/player_ai.py
from ai.evaluation import board_to_vector

class AIPlayer:
    def __init__(self, board, individual):
        self.board = board
        self.individual = individual

    def get_best_move(self):
        current_color = self.board.current_turn
        opponent_color = 'black' if current_color == 'white' else 'white'

        best_score = float('-inf')
        best_move = None

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

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate_board(self):
        vector = board_to_vector(self.board)

        return self.individual.evaluate(vector)
