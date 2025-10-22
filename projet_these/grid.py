from random import choice
import pygame
from constants import Color

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
    def __init__(self, game, rows, cols, cell_size, side="both"):
        self.game = game
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

    def draw_center_cross(self):
        center_h = self.game.display.get_width() // 2
        center_w = self.game.display.get_height() // 2
        cross_size = self.game.config.getint("cross", "size")
        pygame.draw.line(
            self.game.display,
            Color.WHITE,
            (center_h - cross_size, center_w - cross_size),
            (center_h + cross_size, center_w + cross_size),
            self.game.config.getint("cross", "border_width"),
        )
        pygame.draw.line(
            self.game.display,
            Color.WHITE,
            (center_h + cross_size, center_w - cross_size),
            (center_h - cross_size, center_w + cross_size),
            self.game.config.getint("cross", "border_width"),
        )

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(
                    self.game.display,
                    Color.GRAY,
                    rect,
                    self.game.config.getint("square", "border_width"),
                )

    def draw_circle(self, surface, row, col, color):
        center_x = col * self.cell_size + self.cell_size // 2
        center_y = row * self.cell_size + self.cell_size // 2
        pygame.draw.circle(
            surface,
            color,
            (center_x, center_y),
            self.game.config.getint("circle", "radius"),
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
        font = pygame.font.SysFont(
            self.game.config.get("font", "name"),
            self.game.config.getint("font", "size"),
        )
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

    def draw_random_shape(self, shape):
        if shape == "circle" and self.circles:
            self.draw_random_circle(self.game.display)
        elif shape == "letter" and self.letters:
            self.draw_random_letter(self.game.display)
