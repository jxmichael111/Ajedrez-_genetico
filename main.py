import pygame
import pickle
import threading
import config

from game.board import Board
from game.renderer import Renderer
from ai.player_ai import AIPlayer
from ai.genetic_algorithm import Individual
from ai.evaluation import board_to_vector
from ai.visualizer import SimpleNetVisualizer


def main():
    pygame.init()

    # Dimensiones
    CHESS_WIDTH = config.WINDOW_SIZE
    VIZ_WIDTH = 400
    WINDOW_WIDTH = CHESS_WIDTH + VIZ_WIDTH
    WINDOW_HEIGHT = config.WINDOW_SIZE

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ajedrez Genético - IA vs IA")
    clock = pygame.time.Clock()

    chess_surface = pygame.Surface((CHESS_WIDTH, WINDOW_HEIGHT))
    viz_surface = pygame.Surface((VIZ_WIDTH, WINDOW_HEIGHT))

    board = Board()
    renderer = Renderer(chess_surface, board)

    visualizer_white = SimpleNetVisualizer(viz_surface, (0, 0), (VIZ_WIDTH, WINDOW_HEIGHT // 2))
    visualizer_black = SimpleNetVisualizer(viz_surface, (0, WINDOW_HEIGHT // 2), (VIZ_WIDTH, WINDOW_HEIGHT // 2))

    with open("best_individual_white_best.pkl", "rb") as f:
        best_individual_white = pickle.load(f)
    with open("best_individual_black_best.pkl", "rb") as f:
        best_individual_black = pickle.load(f)

    ai_white = AIPlayer(board, best_individual_white)
    ai_black = AIPlayer(board, best_individual_black)

    move_ready = False
    next_move = None
    ai_thread = None
    ai_thinking = False

    # Delay antes de que IA comience a pensar
    THINK_DELAY_MS = 2000
    last_move_time = pygame.time.get_ticks()

    def ai_think():
        nonlocal move_ready, next_move, ai_thinking
        if board.current_turn == 'white':
            next_move = ai_white.get_best_move()
            print(f"IA BLANCA juega: {next_move}")
        else:
            next_move = ai_black.get_best_move()
            print(f"IA NEGRA juega: {next_move}")
        move_ready = True
        ai_thinking = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        chess_surface.fill((255, 255, 255))
        viz_surface.fill((30, 30, 30))

        renderer.draw()
        input_vector = board_to_vector(board)
        if board.current_turn == 'white':
            visualizer_white.draw_network(best_individual_white, input_vector)
        else:
            visualizer_black.draw_network(best_individual_black, input_vector)

        screen.blit(chess_surface, (0, 0))
        screen.blit(viz_surface, (CHESS_WIDTH, 0))
        pygame.display.flip()

        now = pygame.time.get_ticks()

        if move_ready:
            if next_move:
                board.apply_move(next_move)
            next_move = None
            move_ready = False
            last_move_time = pygame.time.get_ticks()

        elif not ai_thinking and (now - last_move_time >= THINK_DELAY_MS):
            ai_thinking = True
            ai_thread = threading.Thread(target=ai_think)
            ai_thread.start()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
