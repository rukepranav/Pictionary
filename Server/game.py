"""
Handles operations related to game and connections
between, player, board, chat and round
"""
from .player import Player
from .board import Board
from .round import Round


class Game(object):

    def __init__(self, id, players,thread):
        """
        init the game! once player threshold is met
        :param id: int
        :param players: Player[]
        """
        self.id = id
        self.players = players
        self.words_used = []
        self.round = None
        self.player_draw_ind = 0
        self.board = Board()
        self.connected_thread = thread
        self.start_new_round()

    def start_new_round(self):
        self.round = Round(self.get_word(), self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind +=1

        if self.player_draw_ind >= len(self.players):
            self.end_round()
            self.end_game()


    def player_guess(self, player, guess):
        return self.round.guess(player,guess)

    def player_disconnected(self, players):
        pass

    def skip(self):
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
        else:
            raise Exception("No round started yet")

    def round_ended(self):
        self.start_new_round()
        self.board.clear()


    def update_board(self, x, y, color):
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def end_game(self):
        pass

    def get_word(self):
        #todo get a list of words
        pass