import pygame
import os
from config import TILE_SIZE

class Renderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.piece_images = self.load_piece_images()

    def load_piece_images(self):
        images = {}
        base_path = os.path.join("assets", "sprites")
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']

        for color in colors:
            for piece in pieces:
                filename = f"{color}_{piece}.png"
                path = os.path.join(base_path, filename)
                if os.path.exists(path):
                    image = pygame.image.load(path).convert_alpha()
                    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    images[(color, piece)] = image
                else:
                    print(f"⚠️ Imagen no encontrada: {path}")
        return images

    def draw(self):
        colors = [(240, 217, 181), (181, 136, 99)]  # light/dark tiles
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, colors[(x+y)%2], rect)

                piece = self.board.board[y][x]
                if piece:
                    image = self.piece_images.get((piece.color, piece.name))
                    if image:
                        self.screen.blit(image, (x*TILE_SIZE, y*TILE_SIZE))
