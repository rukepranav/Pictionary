"""
Represents a round of the game, storing things like
word, time, skips, drawing player and more.
"""
import time as t
from _thread import *
from .game import Game
from .chat import Chat


class Round(object):

    def __init__(self, word, player_drawing, players, game):
        """
                init object
                :param word: str
                :param player_drawing: Player
                :param players: Player[]
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.time = 75
        self.game = game
        self.chat = Chat(self)
        self.player_scores = {player:0 for player in players}
        start_new_thread(self.time_thread, ())

    def skip(self):
        """
        returns true is round skipped threshold met
        :return: bool
        """
        self.skip += 1
        if self.skips > len(self.game.players) - 2:
            return True
        return False

    def get_scores(self):
        """
        :returns all the players scores
        :return:
        """
        return self.scores

    def get_score(self, player):
        """
        get specific player score
        :param player:
        :return:
        """
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            return Exception("player not in score list")

    def time_thread(self):
        """
        Runs in thread to keep track of time
        :return: None
        """
        while self.time > 0:
            t.sleep(1)
            self.time -= 1

        self.end_round("Time's up!!!!")


    def guess(self, player, wrd):
        """
                :returns bool if player got guess correct
                :param word: str
                :param player: Player
                :return bool
        """
        correct = wrd == self.word
        if correct:
            self.player_guessed.append(player)
            #TODO implement scoring system here

    def player_left(self, player):

        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove((player))

        if player == self.player_drawing:
            self.end_round("Drawing Player Left!!!")

    def end_round(self, msg):
        #TODO implement end_round functionality
        for player in self.players:
            player.update_score(self.player_scores[player])
        self.game.round_ended()



