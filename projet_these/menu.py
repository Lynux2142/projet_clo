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


class Menu:
    def __init__(self, game):
        self.game = game
        self.center_w = game.screen_w // 2
        self.center_h = game.screen_h // 2
        self.run_display = True

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.flip()


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
            self.game.display.fill(Color.BLACK)
            self.game.draw_text("MAIN MENU", MENU_TITLE_SIZE, Color.WHITE, self.center_w, self.center_h - 100)
            for index, option in enumerate(self.menu_options):
                color = Color.WHITE
                if self.state == index:
                    color = Color.BLUE
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
            self.game.display.fill(Color.BLACK)
            self.game.draw_text("OPTIONS", MENU_TITLE_SIZE, Color.WHITE, self.center_w, self.center_h - 100)
            for index, option in enumerate(self.menu_options):
                color = Color.WHITE
                if self.state == index:
                    color = Color.BLUE
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

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(Color.BLACK)
            self.game.draw_text(
                "What was the color of the circle?",
                50,
                Color.WHITE,
                self.center_w,
                self.center_h - 100,
            )
            circle_radius = self.game.config.getint("circle", "radius") # 30
            choice = [
                {"color": Color.RED, "position": (self.center_w - 200, self.center_h)},
                {"color": Color.GREEN, "position": (self.center_w, self.center_h)},
                {"color": Color.BLUE, "position": (self.center_w + 200, self.center_h)},
            ]
            square_gap = 10
            for index, option in enumerate(choice):
                pygame.draw.circle(
                    self.game.display,
                    option["color"],
                    option["position"],
                    circle_radius,
                )
                if self.state == index:
                    pygame.draw.rect(
                        self.game.display,
                        Color.WHITE,
                        (
                            option["position"][0] - circle_radius - square_gap,
                            option["position"][1] - circle_radius - square_gap,
                            circle_radius * 2 + square_gap * 2,
                            circle_radius * 2 + square_gap * 2,
                        ),
                        2,
                    )
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
            self.run_display = False
            self.game.new_shape = True
