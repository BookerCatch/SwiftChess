import pygame
import pandas


class Square(pygame.sprite.Sprite):
    letter_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    white = pygame.image.load('assets/board/square_white.png')
    black = pygame.image.load('assets/board/square_black.png')

    def __init__(self, col, row):
        super().__init__()
        self.x = col
        self.y = row
        self.image = None
        self.piece = None
        self.threats = []

        if self.x % 2 == 0 and self.y % 2 == 0:
            self.image = pygame.transform.scale(self.white, (self.white.get_width() * 4, self.white.get_height() * 4))
        elif self.x % 2 != 0 and self.y % 2 == 0:
            self.image = pygame.transform.scale(self.black, (self.black.get_width() * 4, self.black.get_height() * 4))
        elif self.x % 2 != 0 and self.y % 2 != 0:
            self.image = pygame.transform.scale(self.white, (self.white.get_width() * 4, self.white.get_height() * 4))
        else:
            image = pygame.image.load('assets/board/square_black.png')
            self.image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_id(self):
        return self.x, self.y

    def chess_notation(self):
        return self.letter_map[self.y] + str(abs(self.x - 7) + 1)

    def has_piece(self):
        return self.piece is not None


class Board:
    def __init__(self):
        self.squares = self.generate_squares(8)

    def get_row(self, rank):
        return self.squares[rank]

    def get_column(self, file):
        return self.squares.iloc[file]

    def get_pieces(self):
        pieces = []
        for col in self.squares.iteritems():
            for square in col[1]:
                if square.has_piece():
                    pieces.append(square.piece)
        return pieces

    def display(self):
        localized_board = {}
        for column in self.squares.iteritems():
            col = []
            for element in column[1]:
                if element.has_piece():
                    col.append(element.piece.shortname)
                else:
                    col.append(element.chess_notation())
            localized_board.update({column[0]: col})
        print(pandas.DataFrame(localized_board).transpose())

    @staticmethod
    def generate_squares(dimensions):
        """ Generates specified number of squares """
        squares = {}
        for col in range(dimensions):
            cells = []
            for row in range(dimensions):
                cells.append(Square(col, row))
                squares[col] = cells
        return pandas.DataFrame(squares)

    @staticmethod
    def parse_position(position):
        pos_x = position[0]
        pos_y = position[1]
        return Square.letter_map[pos_y] + str(abs(pos_x - 7) + 1)

    @staticmethod
    def place_piece(piece, square):
        """ Place piece on the board. Check for collisions, update threats, etc. """
        pos = square.get_id()
        piece.square = square
        piece.position = pos
        piece.file = pos[0]
        piece.rank = pos[1]
        square.piece = piece
        piece.update()
