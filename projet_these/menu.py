import pygame
import sys

# --- Constants ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
FONT_SIZE = 60
ITEM_SPACING = 80
ITEM_RECT_WIDTH_RATIO = 0.6
ITEM_RECT_HEIGHT = 60


class MenuItem:
    """Represents one item in a menu."""

    def __init__(self, text, center_x, center_y, font, color_normal, color_selected, rect_width, rect_height):
        self.text = text
        self.font = font
        self.color_normal = color_normal
        self.color_selected = color_selected
        self.rect = pygame.Rect(0, 0, int(rect_width), int(rect_height))
        self.rect.center = (center_x, center_y)

    def draw(self, surface, is_selected):
        color = self.color_selected if is_selected else self.color_normal
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Menu:
    """Generic menu class."""

    def __init__(self, title, options, screen, on_select):
        self.title = title
        self.options = options
        self.screen = screen
        self.on_select = on_select
        self.selected_index = 0
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.items = []
        self.last_mouse_pos = (-1, -1)
        self._create_items()

    def _create_items(self):
        width, height = self.screen.get_size()
        total_height = len(self.options) * ITEM_SPACING
        start_y = (height - total_height) // 2 + ITEM_SPACING // 2
        center_x = width // 2
        rect_width = width * ITEM_RECT_WIDTH_RATIO
        rect_height = ITEM_RECT_HEIGHT

        self.items = [
            MenuItem(
                text,
                center_x,
                start_y + i * ITEM_SPACING,
                self.font,
                WHITE,
                BLUE,
                rect_width,
                rect_height,
            )
            for i, text in enumerate(self.options)
        ]

    def handle_event(self, event, mouse_pos):
        """Handle keyboard and mouse input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                self.on_select(self.items[self.selected_index].text)
            elif event.key == pygame.K_ESCAPE:
                self.on_select("Back")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, item in enumerate(self.items):
                if item.rect.collidepoint(mouse_pos):
                    self.on_select(item.text)

    def update_selection_with_mouse(self, mouse_pos):
        """Highlight item under mouse only if the mouse moved since last frame."""
        if mouse_pos != self.last_mouse_pos:
            for i, item in enumerate(self.items):
                if item.rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    break
        self.last_mouse_pos = mouse_pos

    def draw(self):
        self.screen.fill(BLACK)
        width, height = self.screen.get_size()

        title_surface = self.font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect(center=(width // 2, height // 4))
        self.screen.blit(title_surface, title_rect)

        for i, item in enumerate(self.items):
            item.draw(self.screen, i == self.selected_index)

        pygame.display.flip()


class MenuManager:
    """Controls menu switching and manages the main loop."""

    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Fullscreen Menu (Keyboard + Mouse)")
        self.clock = pygame.time.Clock()

        self.main_menu = Menu(
            "Main Menu",
            ["Play", "Options", "Quit"],
            self.screen,
            self.handle_main_selection,
        )

        self.options_menu = Menu(
            "Options",
            ["Shape: Circle", "Side: Both", "Back"],
            self.screen,
            self.handle_options_selection,
        )

        self.current_menu = self.main_menu

    # --- Menu callbacks ---
    def handle_main_selection(self, choice):
        if choice == "Play":
            print("Starting game... (placeholder)")
        elif choice == "Options":
            self.current_menu = self.options_menu
        elif choice == "Quit":
            pygame.quit()
            sys.exit()

    def handle_options_selection(self, choice):
        if choice.startswith("Shape"):
            if "Circle" in choice:
                self.options_menu.options[0] = "Shape: Letter"
            else:
                self.options_menu.options[0] = "Shape: Circle"
            self.options_menu._create_items()

        elif choice.startswith("Side"):
            current = self.options_menu.options[1]
            if "Both" in current:
                self.options_menu.options[1] = "Side: Left"
            elif "Left" in current:
                self.options_menu.options[1] = "Side: Right"
            else:
                self.options_menu.options[1] = "Side: Both"
            self.options_menu._create_items()

        elif choice == "Back":
            self.current_menu = self.main_menu

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.current_menu.handle_event(event, mouse_pos)

            # Mouse only updates selection if it moves
            self.current_menu.update_selection_with_mouse(mouse_pos)
            self.current_menu.draw()
            self.clock.tick(60)


def main():
    pygame.init()
    manager = MenuManager()
    manager.run()


if __name__ == "__main__":
    main()
