### game/renderer.py
import pygame
from config import TILE_SIZE

class Renderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board

    def draw(self):
        colors = [(240, 217, 181), (181, 136, 99)]
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, colors[(x+y)%2], rect)
                piece = self.board.board[y][x]
                if piece:
                    pygame.draw.circle(self.screen, (0,0,0) if piece.color=='black' else (255,255,255), rect.center, TILE_SIZE//3)

