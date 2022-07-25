import pygame
import pygame as p

from chess.board import Board
from chess.piece import generate_set, PieceCursor, Pawn, Knight, King, Queen
from states.state import State
from utils.constants import scalar


class GameState(State):
    def __init__(self, game, player1, player2):
        # ===== Initialization ===== #
        State.__init__(self, game)
        self.game = game
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.init()

        # ===== Sample Squares ===== #
        self.sq_top_left, self.sq_bot_right = self.board.squares.iloc[0, 0], self.board.squares.iloc[7, 7]

        # ===== Rendering ===== #
        self.bg = p.image.load('assets/board/blackWhite.png')

        self.canvas_dim = (game.game_canvas.get_width(), game.game_canvas.get_height())
        self.bg_size = self.bg.get_size()
        self.bg_x = self.bg_size[0] * scalar
        self.bg_y = self.bg_size[1] * scalar

        # Handle square sprites
        self.sq_size_x = self.board.squares.iloc[0, 0].rect.width
        self.sq_size_y = self.board.squares.iloc[0, 0].rect.height

        self.square_sprites = pygame.sprite.Group()
        self.player1_sprites = pygame.sprite.Group()
        self.player2_sprites = pygame.sprite.Group()
        self.cursor = pygame.sprite.Group()
        self.load_sprites()

        # Selection Manager
        self.sq_selected = None
        self.player_clicks = 0

        self.piece_selected = None
        self.board.display()

    def init(self):
        players = (self.player2, self.player1)
        for i, player in enumerate(players):
            pieces = generate_set(self, player)
            for j, square in enumerate(self.board.get_row(i + (i * 6))):  # Row always 0 or 7
                self.board.place_piece(pieces[0][j], square)
            for j, square in enumerate(self.board.get_row(1 + (i * 5))):  # Row always 1 or 6
                self.board.place_piece(pieces[1][j], square)

    def update(self, delta_time, actions):
        self.cursor.update(delta_time)
        if actions['left_click']:
            self.left_click()
        self.game.reset_keys()

    def render(self, display):
        # display.fill(self.game.bg_color)
        display.fill(pygame.Color('black'))
        self.render_squares(display)
        self.render_pieces(display)

    def load_sprites(self):
        # Add squares to their sprite group
        # board_dim = self.sq_size_x * 8, self.sq_size_y * 8
        # b_offset_x = ((self.canvas_dim[0] - board_dim[0]) / 2)
        # b_offset_y = ((self.canvas_dim[1] - board_dim[1]) / 2)
        b_offset_x = ((self.canvas_dim[0] - self.bg_x) / 2)
        b_offset_y = ((self.canvas_dim[1] - self.bg_y) / 2)

        for col, row, in self.board.squares.iteritems():
            for element in row:
                element.rect.y = element.x * element.image.get_width() + b_offset_x
                element.rect.x = element.y * element.image.get_width() + b_offset_y
                element.add(self.square_sprites)

        # Add pieces to their sprite group
        for piece in self.board.get_pieces():
            piece.rect.centerx = piece.square.rect.centerx
            piece.rect.bottom = piece.square.rect.bottom - (piece.square.rect.height / 3)
            if piece.color == self.player1.color:
                piece.add(self.player1_sprites)
            else:
                piece.add(self.player2_sprites)

        PieceCursor().add(self.cursor)

    def render_squares(self, display):
        self.square_sprites.draw(display)

    def render_pieces(self, display):
        self.player1_sprites.draw(display)
        self.player2_sprites.draw(display)

        if self.piece_selected is not None:
            cursor = self.cursor.sprites().__getitem__(0)
            piece_class = self.piece_selected.__class__
            if issubclass(piece_class, Pawn):
                cursor.rect.x = self.piece_selected.rect.x
                cursor.rect.y = self.piece_selected.rect.y + 4
                self.cursor.draw(display)
            elif issubclass(piece_class, Knight):
                cursor.rect.x = self.piece_selected.rect.x
                cursor.rect.y = self.piece_selected.rect.y - 24
                self.cursor.draw(display)
            elif issubclass(piece_class, Queen):
                cursor.rect.x = self.piece_selected.rect.x
                cursor.rect.y = self.piece_selected.rect.y - 32
                self.cursor.draw(display)
            elif issubclass(piece_class, King):
                cursor.rect.x = self.piece_selected.rect.x
                cursor.rect.y = self.piece_selected.rect.y - 28
                self.cursor.draw(display)
            else:
                cursor.rect.x = self.piece_selected.rect.x
                cursor.rect.y = self.piece_selected.rect.y - 12
                self.cursor.draw(display)

    def left_click(self):
        sq = self.get_selection()
        if sq is not None:
            print(sq.chess_notation())
            if sq.has_piece():
                if sq.piece == self.piece_selected:
                    self.clear_selection()
                else:
                    self.player_clicks += 1
                    self.piece_selected = sq.piece
                    print(f'There is a {self.piece_selected.full_name()} '
                          f'belonging to {self.piece_selected.player.color}')
            else:
                self.player_clicks += 1
            if self.player_clicks == 2:
                piece = self.piece_selected
                self.clear_selection()
                self.piece_selected = piece

    def calculate_offsets(self):
        off_x = (self.game.screen.get_width() - self.game.game_canvas.get_width()) // 2
        off_y = (self.game.screen.get_height() - self.game.game_canvas.get_height()) // 2
        return off_x, off_y

    def get_selection(self):
        location = p.mouse.get_pos()
        mx = location[0]
        my = location[1]

        offsets = self.calculate_offsets()

        if self.hovering_board():
            col = int((mx - (self.sq_top_left.rect.left + offsets[0])) // self.sq_size_x)
            row = int((my - (self.sq_top_left.rect.top + offsets[1])) // self.sq_size_x)
            if row > 7:
                row = 7
            self.sq_selected = self.board.squares.iloc[col, row]
            return self.sq_selected

    def hovering_board(self):
        location = p.mouse.get_pos()
        mx = location[0]
        my = location[1]

        # Range using Squares
        sq_top_left = self.board.squares.iloc[0, 0]
        sq_bot_right = self.board.squares.iloc[7, 7]

        offsets = self.calculate_offsets()

        x_min, y_min = sq_top_left.rect.left + offsets[0], sq_top_left.rect.top + offsets[1]
        x_max, y_max = sq_bot_right.rect.right + offsets[0], sq_bot_right.rect.bottom + offsets[1]

        return x_min <= mx <= x_max and y_min <= my <= y_max

    def clear_selection(self):
        self.sq_selected = ()
        self.player_clicks = 0
        self.piece_selected = None
        print('Selections cleared')
