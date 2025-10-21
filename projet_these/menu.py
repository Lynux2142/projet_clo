import pygame
from constants import Color

ITEM_SPACING = 80
MENU_TITLE_SIZE = 80
MENU_OPTION_SIZE = 60

DEFAULT_SHAPE = "circle"
DEFAULT_SIDE = "both"


class Menu:
    def __init__(self, game):
        self.game = game
        self.center_w = game.screen_w // 2
        self.center_h = game.screen_h // 2
        self.run_display = True

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "start"
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
                if self.state == option.lower():
                    color = Color.BLUE
                self.game.draw_text(option, MENU_OPTION_SIZE, color, self.center_w, self.center_h - 20 + index * ITEM_SPACING)
            self.blit_screen()
            self.game.reset_keys()

    def move_cursor(self):
        if self.game.down:
            if self.state == "start":
                self.state = "options"
            elif self.state == "options":
                self.state = "quit"
            elif self.state == "quit":
                self.state = "start"
        elif self.game.up:
            if self.state == "start":
                self.state = "quit"
            elif self.state == "options":
                self.state = "start"
            elif self.state == "quit":
                self.state = "options"

    def check_input(self):
        self.move_cursor()
        if self.game.action:
            if self.state == "start":
                self.run_display = False
                self.game.playing = True
            elif self.state == "options":
                self.run_display = False
                self.game.current_menu = self.game.options
            elif self.state == "quit":
                self.game.running = False
                self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "shape"
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
                if self.state == option.lower():
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
        if self.game.down:
            if self.state == "shape":
                self.state = "side"
            elif self.state == "side":
                self.state = "back"
            elif self.state == "back":
                self.state = "shape"
        elif self.game.up:
            if self.state == "shape":
                self.state = "back"
            elif self.state == "side":
                self.state = "shape"
            elif self.state == "back":
                self.state = "side"

    def check_input(self):
        self.move_cursor()
        if self.game.action:
            if self.state == "back":
                self.state = "shape"
                self.run_display = False
                self.game.current_menu = self.game.main_menu
        if self.game.left or self.game.right:   # change options by pressing left/right because changing options with enter add generate unwanted shape change by entering in options menu
            if self.state == "shape":
                self.shape = "letter" if self.shape == "circle" else "circle"
            if self.state == "side":
                if self.side == "both":
                    self.side = "left"
                elif self.side == "left":
                    self.side = "right"
                else:
                    self.side = "both"
