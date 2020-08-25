import logging

class Player(object):

    def __init__(self, player, startstack=0):
        self.player = player
        self.startstack = startstack

        self.stack = 0
        self.handcount = 0
        self.flops = 0 
        self.turns = 0
        self.rivers = 0 
        self.showdowns =0
        self.folds = 0 
        self.wins = 0 
        self.rebuys = 0
        self.rebuychips = 0
        


class Game(object):
    PREFLOP = 0
    HOLECARDS = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5

    def __init__(self):
        self.players = {}
        self.handcount = 0
        self.flops = 0 
        self.turns = 0
        self.rivers = 0
        self.showdowns = 0

        self.gamestate = Game.PREFLOP