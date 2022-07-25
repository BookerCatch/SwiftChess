import sys

import pygame as p


def menu():
    # General setup
    p.init()
    screen_dim = (1920, 1080)
    clock = p.time.Clock()
    max_fps = 60
    screen = p.display.set_mode(screen_dim, p.RESIZABLE)

    # ========== MAIN LOOP ========== #
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

        p.display.flip()
        clock.tick(max_fps)


class BoardScreen:
    def __init__(self):
        self.screen_dim = (1920, 1080)
        self.max_fps = 60
        self.bg_color = (77, 34, 51)

        self.bg = p.image.load('assets/board/blackWhite.png')
        self.bg_size = self.bg.get_size()
        self.scalar = 4
        self.bg_x = self.bg_size[0] * self.scalar
        self.bg_y = self.bg_size[1] * self.scalar
        self.sq_size = self.bg_y // 8

        self.b_offset_x = ((self.screen_dim[0] - self.bg_x) / 2)
        self.b_offset_y = ((self.screen_dim[1] - self.bg_y) / 2)

        self.piece_size = (16, 48)
        self.bg_trim = p.image.load('assets/board/board_trim_blackWhite.png')
        self.trim_size = self.bg_trim.get_size()
        self.trim_x = self.trim_size[0] * self.scalar
        self.trim_y = self.trim_size[1] * self.scalar

    def render(self, game):

        # General setup
        p.init()
        clock = p.time.Clock()

        # Game screen
        screen = p.display.set_mode(self.screen_dim, p.RESIZABLE)
        p.display.set_caption('Swift Chess')
        p.display.set_icon(p.image.load('assets/icon.png'))
        screen.fill(p.Color(self.bg_color))

        # ========== MAIN LOOP ========== #

        while True:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()

            p.display.flip()
            clock.tick(self.max_fps)
