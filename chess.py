import os
import time
import pygame

from states.title import Title
from utils.input_handler import handle_events


class Chess:
    scalar = 4

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Swift Chess')
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))

        self.GAME_W, self.GAME_H = 1080, 1080
        self.SCREEN_W, self.SCREEN_H = 1920, 1080
        self.bg_color = (77, 34, 51)
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), pygame.RESIZABLE)
        self.running, self.playing = True, True
        self.actions = {"left": False, "right": False, "up": False, "down": False,
                        "action1": False, "action2": False, "start": False, 'left_click': False}
        self.dt, self.prev_time = 0, 0
        self.clock = pygame.time.Clock()
        self.fps = 144
        self.state_stack = []
        self.assets_dir = None
        self.sprite_dir = None
        self.font_dir = None
        self.font = None
        self.font_dir = None
        self.load_assets()
        self.load_states()

    def game_loop(self):
        while self.playing:
            self.clock.tick(self.fps)
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            handle_events(self, event)

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.screen.fill(self.bg_color)
        self.state_stack[-1].render(self.game_canvas)
        offset_x = (self.screen.get_width() - self.game_canvas.get_width()) // 2
        offset_y = (self.screen.get_height() - self.game_canvas.get_height()) // 2
        self.screen.blit(self.game_canvas, (offset_x, offset_y))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        # Create pointers to directories
        self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "monogram.ttf"), 80)

    def load_states(self):
        title_screen = Title(self)
        self.state_stack.append(title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


if __name__ == "__main__":
    g = Chess()
    while g.running:
        g.game_loop()
