"""
MAIN THREAD
Handles all of the connections, creating new games and
requests from the client(s).
"""


import socket
from _thread import *
import threading
import time
from player import Player
from game import Game
import json


class Server(object):
    PLAYERS = 4
    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self,conn,player):
        while True:
            try:
                #Receive request
                data = conn.recv(1024)
                data = json.loads(data)

                #player is not part of the game
                keys = [key for key in data.keys()]
                send_msg = {key:[] for key in keys}

                for key in keys:
                    if key == -1:  # get game, returns a list of players
                        if player.game:
                            send_msg[-1] = player.game.players
                        else:
                            send_msg[-1] = []
                    if player.game:
                        if key == 0: #guess
                            correct = player.game.player_guess(player, data[0][0])
                            send_msg[0] = correct
                        elif key ==1:   #skip
                            skip = player.game.skip()
                            send_msg[1] = skip

                        elif key == 2:   #Get Chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content

                        elif key == 3:   #Get Board
                            brd = player.game.board.get_board()
                            send_msg[3] = brd

                        elif key ==4:   #Get Score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores

                        elif key == 5:   #Get Round
                            rnd = player.game.round_count
                            send_msg[5] = rnd

                        elif key == 6:   #Get Word
                            word = player.game.round.word
                            send_msg[6] = word

                        elif key == 7:   #Get Skips
                            skips = player.game.round.skips
                            send_msg[7] = skips

                        elif key == 8:   #Update Board
                            x,y,color = data[8][:3]
                            self.game.update_board(x,y,color)

                        elif key ==9:   #Get Round Time
                            t = self.game.round.time
                            send_msg[9] = t

                        else:
                            raise Exception("Not a valid request")




                conn.sendall(json.dumps(send_msg))


            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()} disconnected", e)
                conn.close()

    def handle_queue(self, player):
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.connection_queue[:], self.game_id)

            for p in self.connection_queue:
                p.set_game(game)

            self.game_id +=1
            self.connection_queue = []



    def authentication(self,conn,addr):
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception("No Name Received")

            conn.sendall("1".encode())
            player = Player(addr,name)
            self.handle_queue(player)
            threading.Thread(target=self.player_thread, args=(conn, player))

        except Exception as e:
            print("[EXCEPTION",e)
            conn.close()
    def connection_thread(self):
        server = "localhost"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server,port))
        except socket.error as e:
            str(e)

        s.listen()
        print("Waiting for a connection, Server Started")

        while True:
            conn, addr = s.accept()
            print("[CONNECT] New Connection!!")

            self.authentication(conn, addr)


if __name__ == "__main__":
    s=Server()
    threading.Thread(target=s.connection_thread)
