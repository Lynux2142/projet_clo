from abc import ABC, abstractmethod
from time import time
from enum import IntEnum, auto
import pygame
from constants import Color

ITEM_SPACING = 80
MENU_TITLE_SIZE = 80
MENU_OPTION_SIZE = 60

DEFAULT_SHAPE = "circle"
DEFAULT_SIDE = "both"


class MainMenuEnum(IntEnum):
    START = 0
    OPTIONS = auto()
    QUIT = auto()

class OptionEnum(IntEnum):
    SHAPE = 0
    SIDE = auto()
    QUIT = auto()


class Menu(ABC):
    def __init__(self, game):
        self.game = game
        self.center_w = game.screen_w // 2
        self.center_h = game.screen_h // 2
        self.run_display = True

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.flip()

    @abstractmethod
    def display_menu(self):
        pass

    @abstractmethod
    def check_input(self):
        pass

    @abstractmethod
    def move_cursor(self):
        pass


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = MainMenuEnum.START
        self.menu_options = ["Start", "Options", "Quit"]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(Color.BLACK.value)
            self.game.draw_text(
                "MAIN MENU",
                MENU_TITLE_SIZE,
                Color.WHITE.value,
                self.center_w,
                self.center_h - 100
            )
            for index, option in enumerate(self.menu_options):
                color = Color.WHITE.value
                if self.state == index:
                    color = Color.BLUE.value
                self.game.draw_text(option, MENU_OPTION_SIZE, color, self.center_w, self.center_h - 20 + index * ITEM_SPACING)
            self.blit_screen()
            self.game.reset_keys()

    def move_cursor(self):
        if self.game.down:
            if self.state < len(self.menu_options) - 1:
                self.state += 1
        elif self.game.up:
            if self.state > 0:
                self.state -= 1

    def check_input(self):
        self.move_cursor()
        if self.game.action:
            if self.state == MainMenuEnum.START:
                with open("results.csv", "w") as f:
                    f.write("Shape;Coordinates;Choice;Success;ReactionTime\n")
                self.run_display = False
                self.game.playing = True
            elif self.state == MainMenuEnum.OPTIONS:
                self.state = MainMenuEnum.START
                self.run_display = False
                self.game.current_menu = self.game.option_menu
            elif self.state == MainMenuEnum.QUIT:
                self.game.running = False
                self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = OptionEnum.SHAPE
        self.menu_options = ["Shape", "Side", "Back"]
        self.shape = DEFAULT_SHAPE
        self.side = DEFAULT_SIDE

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(Color.BLACK.value)
            self.game.draw_text(
                "OPTIONS",
                MENU_TITLE_SIZE,
                Color.WHITE.value,
                self.center_w,
                self.center_h - 100
            )
            for index, option in enumerate(self.menu_options):
                color = Color.WHITE.value
                if self.state == index:
                    color = Color.BLUE.value
                text = option
                if option == "Shape":
                    text += f": {self.shape.capitalize()}"
                elif option == "Side":
                    text += f": {self.side.capitalize()}"
                self.game.draw_text(text, MENU_OPTION_SIZE, color, self.center_w, self.center_h - 20 + index * ITEM_SPACING)
            self.blit_screen()
            self.game.reset_keys()

    def move_cursor(self):
        if self.game.pause:
            self.state = OptionEnum.SHAPE
            self.run_display = False
            self.game.current_menu = self.game.main_menu
        if self.game.down:
            if self.state < len(self.menu_options) - 1:
                self.state += 1
        elif self.game.up:
            if self.state > 0:
                self.state -= 1

    def check_input(self):
        self.move_cursor()
        if self.game.action:
            if self.state == OptionEnum.QUIT:
                self.state = OptionEnum.SHAPE
                self.run_display = False
                self.game.current_menu = self.game.main_menu
            elif self.state == OptionEnum.SHAPE:
                self.shape = "letter" if self.shape == "circle" else "circle"
            elif self.state == OptionEnum.SIDE:
                if self.side == "both":
                    self.side = "left"
                elif self.side == "left":
                    self.side = "right"
                else:
                    self.side = "both"


class QuestionMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 1
        self.choice = None

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(Color.BLACK.value)
            self.game.draw_text(
                "What was the color of the cirlce?"
                if self.game.option_menu.shape == "circle"
                else "What was the letter?",
                50,
                Color.WHITE.value,
                self.center_w,
                self.center_h - 100,
            )
            circle_radius = self.game.config.getint("circle", "radius")
            self.choice = (
                [
                    {"shape": "RED", "position": (self.center_w - 200, self.center_h)},
                    {"shape": "GREEN", "position": (self.center_w, self.center_h)},
                    {"shape": "BLUE", "position": (self.center_w + 200, self.center_h)},
                ]
                if self.game.option_menu.shape == "circle"
                else [
                    {"shape": "A", "position": (self.center_w - 200, self.center_h)},
                    {"shape": "B", "position": (self.center_w, self.center_h)},
                    {"shape": "C", "position": (self.center_w + 200, self.center_h)},
                ]
            )
            square_gap = 10
            for index, option in enumerate(self.choice):
                if self.game.option_menu.shape == "circle":
                    pygame.draw.circle(
                        self.game.display,
                        Color[option["shape"]].value,
                        option["position"],
                        circle_radius,
                    )
                else:
                    self.game.draw_text(
                        option["shape"],
                        MENU_OPTION_SIZE,
                        Color.WHITE.value,
                        *option["position"],
                    )
                if self.state == index:
                    rect = pygame.Rect(
                        option["position"][0] - circle_radius - square_gap,
                        option["position"][1] - circle_radius - square_gap,
                        circle_radius * 2 + square_gap * 2,
                        circle_radius * 2 + square_gap * 2,
                    )
            pygame.draw.rect(self.game.display, Color.WHITE.value, rect, 2)
            self.blit_screen()
            self.game.reset_keys()

    def move_cursor(self):
        if self.game.left:
            if self.state > 0:
                self.state -= 1
        elif self.game.right:
            if self.state < 2:
                self.state += 1

    def check_input(self):
        self.move_cursor()
        if self.game.pause:
            self.state = 1
            self.game.playing = False
            self.run_display = False
            self.game.current_menu = self.game.main_menu
        elif self.game.action:
            with open("results.csv", "a") as f:
                metrics = self.game.last_displayed_shape
                coordinates = f"{chr(ord('A') + metrics.position[0])}{metrics.position[1] + 1}"
                choice = self.choice[self.state]["shape"]
                success = metrics.id == choice
                time_reaction = round(time() - metrics.hiding_timestamp, 2)
                f.write(f"{metrics.id};{coordinates};{choice};{success};{time_reaction}\n")
            self.state = 1
            self.run_display = False
            self.game.new_shape = True
