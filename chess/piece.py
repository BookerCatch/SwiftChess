import enum
import os
import pathlib
import pygame

from pygame.sprite import Sprite

from utils.constants import scalar


def generate_set(board, player):
    """Generates a standard chess piece set"""
    pieces = [Rook(board, player), Knight(board, player), Bishop(board, player), Queen(board, player),
              King(board, player), Bishop(board, player), Knight(board, player), Rook(board, player)]
    pawns = []

    if player.number == 2:
        pieces = list(reversed(pieces))
    for i in range(8):
        pawns.append(Pawn(board, player))

    return pieces, pawns


class Colors(enum.Enum):
    Red = 'red'
    Blue = 'blue',
    White = 'white'

    #def load_pieces(self, game):
        #players = (game.player1, game.player2)
        #for player in players:
            #color_dir = 'data/assets/pieces/' + player.color
            #for image in os.listdir(color_dir):
                #if pathlib.Path(image).suffix == '.png':
                    #name = image.split('.').pop(0)
                    #self.sprites[player.color][name] = p.transform.scale(p.image.load(
                        #color_dir + '/' + image), tuple(i * self.scalar for i in self.piece_size))


class PieceCursor(Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        sprite_dir = 'assets/gui/'
        for image in os.listdir('assets/gui/'):
            if pathlib.Path(image).suffix == '.png':
                asset = pygame.image.load(f'{sprite_dir}/{image}')
                sprite = pygame.transform.scale(asset, (asset.get_width() * scalar, asset.get_height() * scalar))
                self.sprites.append(sprite)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.anim_speed_mult = 2

    def update(self, delta_time):
        self.current_sprite += delta_time * self.anim_speed_mult
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]


class Piece(Sprite):
    """Base class for chess pieces"""

    def __init__(self, board, player, shortname=None, name=None, color=None, position=None, rank=None, file=None):
        super().__init__()
        if board is None:
            raise TypeError("board may not be None")

        if not shortname:
            raise TypeError("shortname must be non-empty")

        if not name:
            raise TypeError("name must be non-empty")

        if not player:
            raise TypeError("player must be non-empty")

        if player.number == 1:
            self.facing = 'Back'
        else:
            self.facing = 'Front'

        self.board = board
        self.player = player
        self.shortname = shortname
        self.color = player.color
        self.name = name
        sprite = pygame.image.load(
            f'assets/pieces/{player.color}/{self.name.lower()}{self.facing}' + '.png')
        self.image = pygame.transform.scale(sprite, (sprite.get_width() * scalar, sprite.get_height() * scalar))
        self.rect = self.image.get_rect()
        self.can_castle = False
        self.square = None

        if position is None:
            self.rank = rank
            self.file = file
            self.position = (file, rank)
        else:
            self.rank, self.file = board.parse_position(position)

        # board.place_piece(self.rank, self.file, self)
        self.color = color

    def full_name(self):
        return str(self.color).capitalize() + ' ' + self.name.capitalize()


class Pawn(Piece):
    def __init__(self, board, player):
        super().__init__(board, player=player, shortname='P', name='Pawn')
        self.color = player.color


class Rook(Piece):
    def __init__(self, board, player):
        super().__init__(board, player=player, shortname='R', name='Rook')
        self.color = player.color


class Knight(Piece):
    def __init__(self, board, player):
        super().__init__(board, player=player, shortname='N', name='Knight')
        self.color = player.color


class Bishop(Piece):
    def __init__(self, board, player):
        super().__init__(board, player=player, shortname='B', name='Bishop')
        self.color = player.color


class Queen(Piece):
    def __init__(self, board, player):
        super().__init__(board, player=player, shortname='Q', name='Queen')
        self.color = player.color


class King(Piece):
    def __init__(self, board, player):
        super().__init__(board, player=player, shortname='K', name='King')
        self.color = player.color
        self.can_castle = True
