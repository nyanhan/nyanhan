import pygame
import random

# Game configuration
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 1],
     [1, 1]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 1, 1],
     [0, 0, 1]],
]

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = int(len(shape[0]) / 2 + 5)
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.width = WINDOW_WIDTH // BLOCK_SIZE
        self.height = WINDOW_HEIGHT // BLOCK_SIZE
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = self.new_piece()

    def new_piece(self):
        idx = random.randrange(len(SHAPES))
        shape = SHAPES[idx]
        color = COLORS[idx]
        return Piece(shape, color)

    def collide(self, piece, dx, dy):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + dx
                    new_y = piece.y + y + dy
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False

    def freeze(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell and piece.y + y >= 0:
                    self.board[piece.y + y][piece.x + x] = piece.color
        self.clear_lines()
        self.current_piece = self.new_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.width)])
        self.board = new_board

    def move(self, dx, dy):
        piece = self.current_piece
        if not self.collide(piece, dx, dy):
            piece.x += dx
            piece.y += dy
        elif dy:
            self.freeze(piece)

    def rotate(self):
        piece = self.current_piece
        original_shape = piece.shape
        piece.rotate()
        if self.collide(piece, 0, 0):
            piece.shape = original_shape

    def draw_board(self, screen):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        cell,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )
        piece = self.current_piece
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        piece.color,
                        ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate()

            self.move(0, 1)

            screen.fill(BLACK)
            self.draw_board(screen)
            pygame.display.flip()
            clock.tick(5)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
