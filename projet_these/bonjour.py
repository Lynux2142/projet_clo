from random import randint, choice
from time import sleep, time
import pygame
from constants import Color

CROSS_SIZE = 10
CROSS_BORDER_WIDTH = 3

SQUARE_SIZE = 100
SQUARE_BORDER_WIDTH = 1

CIRCLE_RADIUS = SQUARE_SIZE // 3 - SQUARE_BORDER_WIDTH

FONT_NAME = "Comic Sans MS"
FONT_SIZE = 80

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
            for color in [Color.RED, Color.GREEN, Color.BLUE]
        ]
        self.letters = [
            Letter(rows, cols, letter, Color.WHITE, side)
            for letter in ['A', 'B', 'C']
        ]

    def draw_center_cross(self, surface):
        center_h = surface.get_width() // 2
        center_w = surface.get_height() // 2
        pygame.draw.line(
            surface,
            Color.WHITE,
            (center_h - CROSS_SIZE, center_w - CROSS_SIZE),
            (center_h + CROSS_SIZE, center_w + CROSS_SIZE),
            CROSS_BORDER_WIDTH,
        )
        pygame.draw.line(
            surface,
            Color.WHITE,
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
                    Color.GRAY,             # color
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
        text_surface = font.render(letter.letter, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        surface.blit(text_surface, text_rect)
        del letter.possible_positions[
            letter.possible_positions.index((row, col))
        ]
        if not letter.possible_positions:
            del self.letters[
                self.letters.index(letter)
            ]

    def draw_random_shape(self, surface, shape):
        if shape == "circle" and self.circles:
            self.draw_random_circle(surface)
        elif shape == "letter" and self.letters:
            self.draw_random_letter(surface)
