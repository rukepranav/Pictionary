"""
Represents a player object on the server side
"""

class Player(object):
    def __init__(self, ip, name):
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def set_game(self, game):
        """
        sets the players game associtations
        :param game: Game
        :return: None
        """
        self.game = game

    def update_score(self, x):
        self.score += x

    def guess(self, wrd):
        self.game.player_guess(self,wrd)

    def disconnect(self):
        self.game.player_disconnected(self)

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score




