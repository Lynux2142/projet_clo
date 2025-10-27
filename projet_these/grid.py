from abc import ABC, abstractmethod
from time import time
from random import choice, randrange
import pygame
from constants import Color


class Shape(ABC):
    def __init__(self, game, rows, cols, side):
        self.game = game
        self.possible_positions = [
            (col, row)
            for row in range(0, rows)
            for col in range(
                0 if side != "right" else cols // 2,
                cols if side != "left" else cols // 2,
            )
        ]
        self.cell_width = self.game.config.getint("grid", "square_width")
        self.cell_height = self.game.config.getint("grid", "square_height")
        self.hiding_timestamp = None
        self.position = None

    @abstractmethod
    def draw(self, row, col, color):
        pass


class Circle(Shape):
    def __init__(self, game, rows, cols, color, side):
        super().__init__(game, rows, cols, side)
        self.color = color.value
        self.id = color.name

    def draw(self):
        self.position = choice(self.possible_positions)
        center = (
            self.position[0] * self.cell_width + self.cell_width // 2,
            self.position[1] * self.cell_height + self.cell_height // 2,
        )
        pygame.draw.circle(
            self.game.display,
            self.color,
            center,
            self.game.config.getint("circle", "radius"),
        )
        del self.possible_positions[
            self.possible_positions.index(self.position)
        ]

class Letter(Shape):
    def __init__(self, game, rows, cols, letter, side):
        super().__init__(game, rows, cols, side)
        self.id = letter

    def draw(self):
        self.position = choice(self.possible_positions)
        size = self.game.config.getint("font", "size")
        center = (
            self.position[0] * self.cell_width + self.cell_width // 2,
            self.position[1] * self.cell_height + self.cell_height // 2,
        )
        self.game.draw_text(self.id, size, Color.WHITE.value, *center)
        del self.possible_positions[
            self.possible_positions.index(self.position)
        ]

class Grid:
    def __init__(self, game):
        self.game = game
        self.cols = self.game.screen_w // self.game.config.getint("grid", "square_width")
        self.rows = self.game.screen_h // self.game.config.getint("grid", "square_height")
        self.cell_width = self.game.config.getint("grid", "square_width")
        self.cell_height = self.game.config.getint("grid", "square_height")
        side = self.game.option_menu.side
        shape = self.game.option_menu.shape
        self.shapes = (
            [
                Circle(self.game, self.rows, self.cols, color, side)
                for color in [Color.RED, Color.GREEN, Color.BLUE]
            ]
            if shape == "circle"
            else [
                Letter(self.game, self.rows, self.cols, letter, side)
                for letter in ["A", "B", "C"]
            ]
        )

    def draw_center_cross(self):
        center_h = self.game.display.get_width() // 2
        center_w = self.game.display.get_height() // 2
        cross_size = self.game.config.getint("cross", "size")
        pygame.draw.line(
            self.game.display,
            Color.WHITE.value,
            (center_h - cross_size, center_w - cross_size),
            (center_h + cross_size, center_w + cross_size),
            self.game.config.getint("cross", "border_width"),
        )
        pygame.draw.line(
            self.game.display,
            Color.WHITE.value,
            (center_h + cross_size, center_w - cross_size),
            (center_h - cross_size, center_w + cross_size),
            self.game.config.getint("cross", "border_width"),
        )

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_width,
                    row * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )
                pygame.draw.rect(
                    self.game.display,
                    Color.GRAY.value,
                    rect,
                    self.game.config.getint("grid", "border_width"),
                )

    def draw_random_shape(self, shape):
        shape = choice(self.shapes)
        shape.draw()
        self.game.last_displayed_shape = shape
        if not shape.possible_positions:
            del self.shapes[
                self.shapes.index(shape)
            ]
