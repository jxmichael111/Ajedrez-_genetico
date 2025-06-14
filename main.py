import pygame
import pickle
import time
import config

from game.board import Board
from game.renderer import Renderer
from ai.player_ai import AIPlayer
from ai.genetic_algorithm import Individual

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))
    pygame.display.set_caption("Ajedrez Genético - IA vs IA")
    clock = pygame.time.Clock()

    board = Board()
    renderer = Renderer(screen, board)

    # Cargar las IAs entrenadas
    with open("best_individual_white_best.pkl", "rb") as f:
        best_individual_white = pickle.load(f)
    with open("best_individual_black_best.pkl", "rb") as f:
        best_individual_black = pickle.load(f)

    ai_white = AIPlayer(board, best_individual_white)
    ai_black = AIPlayer(board, best_individual_black)

    running = True
    while running:
        screen.fill((255, 255, 255))
        renderer.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Turno de la IA
        if board.current_turn == 'white':
            move = ai_white.get_best_move()
            print(f"IA BLANCA juega: {move}")
            if move:
                board.apply_move(move)
                time.sleep(config.SLEEP_TIME)
        elif board.current_turn == 'black':
            move = ai_black.get_best_move()
            print(f"IA NEGRA juega: {move}")
            if move:
                board.apply_move(move)
                time.sleep(config.SLEEP_TIME)

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
