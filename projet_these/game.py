from time import time
import pygame
from constants import Color
from menu import MainMenu, OptionsMenu, QuestionMenu
from configparser import ConfigParser
from grid import Grid


class Game:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("settings.ini")
        pygame.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.running, self.playing = True, False
        self.display = pygame.Surface((self.screen_w, self.screen_h))
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.main_menu = MainMenu(self)
        self.option_menu = OptionsMenu(self)
        self.question_menu = QuestionMenu(self)
        self.current_menu = self.main_menu
        self.new_shape = True

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.action = False
        self.pause = False

    def game_loop(self):
        clock = pygame.time.Clock()
        grid = Grid(self)
        start = time()
        self.new_shape = True
        while self.playing:
            self.check_events()
            self.check_input()

            if self.new_shape:
                self.display.fill(Color.BLACK)
                #grid.draw_grid()
                grid.draw_center_cross()
                grid.draw_random_shape(self.option_menu.shape)
                start = time()
                self.new_shape = False

            if time() - start > self.config.getint("shape", "display_time"):
                self.question_menu.display_menu()

            self.window.blit(self.display, (0, 0))
            pygame.display.flip()
            self.reset_keys()
            clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_RIGHT:
                    self.right = True
                if event.key == pygame.K_RETURN:
                    self.action = True

    def check_input(self):
        if self.pause:
            self.playing = False
            self.pause = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(self.config.get("font", "name"), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        self.up, self.down, self.left, self.right = False, False, False, False
        self.action, self.pause = False, False
