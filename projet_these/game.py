from time import time
import pygame
from constants import Color
from menu import MainMenu, OptionsMenu
from bonjour import (
    NEW_CIRCLE_INTERVAL,
    SQUARE_SIZE,
    Grid,
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.running, self.playing = True, False
        self.display = pygame.Surface((self.screen_w, self.screen_h))
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.current_menu = self.main_menu

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.action = False
        self.pause = False

    def game_loop(self):
        grid = Grid(
            rows=self.screen_h // SQUARE_SIZE,
            cols=self.screen_w // SQUARE_SIZE,
            cell_size=SQUARE_SIZE,
            side=self.options.side,
        )
        start = 0
        while self.playing:
            self.check_events()
            self.check_input()

            if time() - start > NEW_CIRCLE_INTERVAL:
                self.display.fill(Color.BLACK)
                grid.draw_grid(self.display)
                grid.draw_center_cross(self.display)
                grid.draw_random_shape(self.display, shape=self.options.shape)
                start = time()

            self.window.blit(self.display, (0, 0))
            pygame.display.flip()
            self.reset_keys()

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
        if self.up:
            print("Up key pressed")
        if self.down:
            print("Down key pressed")
        if self.left:
            print("Left key pressed")
        if self.right:
            print("Right key pressed")
        if self.action:
            print("Action key pressed")

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont("Comic Sans MS", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        self.up, self.down, self.left, self.right = False, False, False, False
        self.action, self.pause = False, False
