from chess.player import Player
from states.gameplay import GameState
from states.state import State


class Title(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta_time, actions):
        if actions['start']:
            player1 = Player(1, "white")
            player2 = Player(2, "blue")
            game_state = GameState(self.game, player1, player2)
            game_state.enter_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill(self.game.bg_color)
        self.game.draw_text(display, "Swift Chess", (251, 229, 190), self.game.GAME_W/2, self.game.GAME_H/2 - 200)
        self.game.draw_text(display, "Press Enter to Start Game", (251, 229, 190), self.game.GAME_W/2, self.game.GAME_H/2)
