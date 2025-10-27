from time import time
from random import randint
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
        display_info = pygame.display.Info()
        self.screen_w = display_info.current_w
        self.screen_h = display_info.current_h
        self.running, self.playing = True, False
        self.display = pygame.Surface((self.screen_w, self.screen_h))
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.main_menu = MainMenu(self)
        self.option_menu = OptionsMenu(self)
        self.question_menu = QuestionMenu(self)
        self.current_menu = self.main_menu
        self.last_displayed_shape = None

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.action = False
        self.pause = False

    def game_loop(self):
        clock = pygame.time.Clock()
        grid = Grid(self)
        first_phase_lower_time = self.config.getint("shape", "first_phase_lower_time")
        first_phase_upper_time = self.config.getint("shape", "first_phase_upper_time")
        first_phase_time = randint(first_phase_lower_time, first_phase_upper_time)
        second_phase_time = self.config.getint("shape", "second_phase_time") / 1000
        third_phase_time = self.config.getint("shape", "third_phase_time") / 1000
        start = time()
        new_shape = True
        phase = 1
        while self.playing:
            self.check_events()
            self.check_input()

            if phase == 1:
                self.display.fill(Color.BLACK.value)
                grid.draw_center_cross()
                if time() - start > first_phase_time / 1000:
                    phase += 1
                    start = time()

            if phase == 2:
                if self.config.getboolean("grid", "show_grid"):
                    grid.draw_grid()
                grid.draw_center_cross()
                if new_shape:
                    grid.draw_random_shape(self.option_menu.shape)
                    new_shape = False
                if time() - start > second_phase_time:
                    phase += 1
                    start = time()

            if phase == 3:
                self.display.fill(Color.BLACK.value)
                grid.draw_center_cross()
                if time() - start > third_phase_time:
                    phase += 1

            if phase == 4:
                self.last_displayed_shape.hiding_timestamp = time()
                self.question_menu.display_menu()
                phase = 1
                new_shape = True
                first_phase_time = randint(first_phase_lower_time, first_phase_upper_time)
                start = time()

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
