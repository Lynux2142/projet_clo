from random import choice, randrange
import pygame
from constants import Color


class Shape:
    def __init__(self, rows, cols, color, side):
        self.color = color
        self.possible_positions = [
            (row, col)
            for row in range(0, rows)
            for col in range(
                0 if side != "right" else cols // 2,
                cols if side != "left" else cols // 2,
            )
        ]


class Circle(Shape):
    def __init__(self, rows, cols, color, side):
        super().__init__(rows, cols, color, side)

class Letter(Shape):
    def __init__(self, rows, cols, letter, color, side):
        super().__init__(rows, cols, color, side)
        self.letter = letter

class Grid:
    def __init__(self, game):
        self.game = game
        self.rows = self.game.screen_h // self.game.config.getint("square", "size")
        self.cols = self.game.screen_w // self.game.config.getint("square", "size")
        self.cell_size = self.game.config.getint("square", "size")
        side = self.game.option_menu.side
        self.circles = [
            Circle(self.rows, self.cols, color, side)
            for color in [Color.RED, Color.GREEN, Color.BLUE]
        ]
        self.letters = [
            Letter(self.rows, self.cols, letter, Color.WHITE, side)
            for letter in ["A", "B", "C"]
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
        self.game.last_displayed_shape = randrange(len(self.circles))
        circle = self.circles[self.game.last_displayed_shape]
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
        size = self.game.config.getint("font", "size")
        self.game.last_displayed_shape = randrange(len(self.letters))
        letter = self.letters[self.game.last_displayed_shape]
        row, col = choice(letter.possible_positions)
        center = (
            col * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )
        self.game.draw_text(letter.letter, size, Color.WHITE, *center)
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
