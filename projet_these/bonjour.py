from random import randint, choice
from time import sleep, time
import pygame

NEW_CIRCLE_INTERVAL = 1
SHAPE = "circle"            # options: "circle", "letter"

CROSS_SIZE = 10
CROSS_BORDER_WIDTH = 3

SQUARE_SIZE = 100
SQUARE_BORDER_WIDTH = 1

CIRCLE_RADIUS = SQUARE_SIZE // 3 - SQUARE_BORDER_WIDTH

FONT_NAME = "Comic Sans MS"
FONT_SIZE = 80
FONT_COLOR = (255, 255, 255)

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

class Circle:
    def __init__(self, rows, cols, color, side):
        self.color = color
        self.possible_positions = [
            (row, col)
            for row in range(0, rows)
            for col in range(
                0 if side != "right" else cols // 2,
                cols if side != "left" else cols // 2
            )
        ]

class Letter:
    def __init__(self, rows, cols, letter, color, side):
        self.letter = letter
        self.color = color
        self.possible_positions = [
            (row, col)
            for row in range(0, rows)
            for col in range(
                0 if side != "right" else cols // 2,
                cols if side != "left" else cols // 2
            )
        ]

class Grid:
    def __init__(self, rows, cols, cell_size, side="both"):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.circles = [
            Circle(rows, cols, color, side)
            for color in [RED, GREEN, BLUE]
        ]
        self.letters = [
            Letter(rows, cols, letter, WHITE, side)
            for letter in ['A', 'B', 'C']
        ]

    def draw_center_cross(self, surface):
        center_h = surface.get_width() // 2
        center_w = surface.get_height() // 2
        pygame.draw.line(
            surface,
            WHITE,
            (center_h - CROSS_SIZE, center_w - CROSS_SIZE),
            (center_h + CROSS_SIZE, center_w + CROSS_SIZE),
            CROSS_BORDER_WIDTH,
        )
        pygame.draw.line(
            surface,
            WHITE,
            (center_h + CROSS_SIZE, center_w - CROSS_SIZE),
            (center_h - CROSS_SIZE, center_w + CROSS_SIZE),
            CROSS_BORDER_WIDTH,
        )

    def draw_grid(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_size,   # x position
                    row * self.cell_size,   # y position
                    self.cell_size,         # width
                    self.cell_size,         # height
                )
                pygame.draw.rect(
                    surface,                # surface to draw on
                    GREY,                   # color
                    rect,                   # pygame.Rect object
                    SQUARE_BORDER_WIDTH,    # border width
                )

    def draw_circle(self, surface, row, col, color):
        center_x = col * self.cell_size + self.cell_size // 2
        center_y = row * self.cell_size + self.cell_size // 2
        pygame.draw.circle(
            surface,
            color,
            (center_x, center_y),           # center coordinates
            CIRCLE_RADIUS,                  # circle radius
        )

    def draw_random_circle(self, surface):
        circle = choice(self.circles)
        row, col = choice(circle.possible_positions)
        self.draw_circle(surface, row, col, circle.color)
        del circle.possible_positions[
            circle.possible_positions.index((row, col))
        ]
        if not circle.possible_positions:
            del self.circles[
                self.circles.index(circle)
            ]

    def draw_random_letter(self, surface):
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        letter = choice(self.letters)
        row, col = choice(letter.possible_positions)
        center_x = col * self.cell_size + self.cell_size // 2
        center_y = row * self.cell_size + self.cell_size // 2
        text_surface = font.render(letter.letter, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        surface.blit(text_surface, text_rect)
        del letter.possible_positions[
            letter.possible_positions.index((row, col))
        ]
        if not letter.possible_positions:
            del self.letters[
                self.letters.index(letter)
            ]

    def draw_random_shape(self, surface, shape: str = "circle"):
        if shape == "circle" and self.circles:
            self.draw_random_circle(surface)
        elif shape == "letter" and self.letters:
            self.draw_random_letter(surface)

def main():
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)                  # hide cursor
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.flip()
    clock = pygame.time.Clock()
    display_info = pygame.display.Info()
    grid = Grid(
        rows=display_info.current_h // SQUARE_SIZE,  # number of rows
        cols=display_info.current_w // SQUARE_SIZE,  # number of columns
        cell_size=SQUARE_SIZE                        # cell size
    )

    start = 0

    running = True
    while running:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
            ):
                running = False

        if time() - start > NEW_CIRCLE_INTERVAL:
            screen.fill(BLACK)
            pygame.display.flip()
            #grid.draw_grid(screen)
            grid.draw_random_shape(screen, shape=SHAPE)
            pygame.display.flip()
            start = time()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
