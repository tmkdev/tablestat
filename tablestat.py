import logging
import re
from pokergame import Player, Game
from ev_eval import Card_EV

import tkinter as tk
from tkinter import filedialog

chipval = 0.20

re_hand = re.compile('Hand #(?P<hand>\d+-\d+) - (?P<hand_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
re_seat = re.compile('Seat (?P<seat>\d): (?P<player>\S+) \((?P<stack>\d+)\)')
re_holecards = re.compile('\*\* Hole Cards \*\* \[(?P<players>\d) players\]')
re_fold = re.compile('(?P<player>\S+) folds')
re_flop = re.compile('\*\* Flop \*\*')
re_turn = re.compile('\*\* Turn \*\*')
re_river = re.compile('\*\* River \*\*')
re_winspot = re.compile('(?P<player>\S+) wins Pot \((?P<potsize>\d+\))')
re_showdown = re.compile('\*\* Pot Show Down \*\*')
re_rebuy = re.compile('(?P<player>\S+) adds (?P<chips>\d+) chips')
re_dealtcard = re.compile('Dealt to (?P<player>\S+) \[(?P<cards>\S{2} \S{2})\]')


def processgame():
    game = Game()
    ev = Card_EV()

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    for line in open(file_path, 'r'):
        m = re_hand.search(line)
        if m:
            game.handcount+=1
            game.gamestate = Game.PREFLOP
            game.reset_playerstate()

        m = re_seat.search(line)
        if m:
            player = m.groupdict()['player']
            if player not in game.players:
                logging.info(f'Player {player} not in players!')
                p = Player(player, startstack=int(m.groupdict()['stack']))
                game.players[player] = p
                game.startingchips += int(m.groupdict()['stack'])

            game.players[player].stack = int(m.groupdict()['stack']) 
            game.players[player].handcount +=1 

        m = re_holecards.search(line)
        if m:
            game.gamestate = Game.HOLECARDS
        
        m = re_flop.search(line)
        if m:
            game.gamestate = Game.FLOP
            game.flops += 1

        m = re_turn.search(line)
        if m:
            game.gamestate = Game.TURN
            game.turns += 1

        m = re_river.search(line)
        if m:
            game.gamestate = Game.RIVER
            game.rivers += 1

        m = re_showdown.search(line)
        if m:
            game.gamestate = Game.SHOWDOWN
            game.showdowns += 1

        m = re_fold.search(line)
        if m:
            player = m.groupdict()['player']
            game.players[player].folds +=1 

        m = re_winspot.search(line)
        if m:
            player = m.groupdict()['player']
            game.players[player].wins +=1 
            if game.gamestate == Game.SHOWDOWN:
                game.players[player].showdownwins +=1 

        m = re_rebuy.search(line)
        if m: 
            player = m.groupdict()['player']
            game.players[player].rebuys +=1
            game.players[player].rebuychips += int(m.groupdict()['chips'])

            game.rebuychips += int(m.groupdict()['chips'])

        m = re_dealtcard.search(line)
        if m: 
            player = m.groupdict()['player']
            h, e = ev.evalhand(m.groupdict()['cards'])
            game.players[player].card_ev_sum += e
            game.players[player].hand = m.groupdict()['cards']

        playertest = line.split(' ')
        player = playertest[0]
        if player in list(game.players) and playertest[1] in ['calls', 'checks', 'raises', 'bets', 'shows']:
            if game.gamestate == Game.FLOP and game.players[player].state != Game.FLOP: 
                game.players[player].state = Game.FLOP
                game.players[player].flops+=1
                if game.players[player].hand:
                    h, e = ev.evalhand(game.players[player].hand)
                    game.players[player].flop_ev_sum += e
            
            if game.gamestate == Game.TURN and game.players[player].state != Game.TURN:
                game.players[player].state == Game.TURN
                game.players[player].turns+=1

            if game.gamestate == Game.RIVER and game.players[player].state != Game.RIVER:
                game.players[player].state == Game.RIVER
                game.players[player].rivers+=1
            
            if game.gamestate == Game.SHOWDOWN and game.players[player].state != Game.SHOWDOWN:
                game.players[player].state == Game.SHOWDOWN
                game.players[player].showdowns+=1

    return game

def gameoutput(game):
    print('GAMESTATS')
    print(f'Hands Played: {game.handcount}')
    print(f'Initial Buyin chips: {game.startingchips} - ${game.startingchips * chipval:.2f}')
    print(f'Rebuy Chips chips: {game.rebuychips}')
    print(f'Total Table Chips: {game.rebuychips + game.startingchips}')


def output(game):
    print('Player Summary')
    for player in game.players:
        p = game.players[player]
        print(f'********** {p.player} ***********')
        print(f" Hands: {p.handcount} Flops seen: {p.flops} Turns seen: {p.turns} Rivers seen: {p.rivers} Showdowns: {p.showdowns} Wins: {p.wins} Folds: {p.folds}" )
        print(f' Hands Played%: {100.0 * p.flops / p.handcount:.1f}%')
        try:
            print(f' %Pots Won: {100.0 * p.wins / p.flops:.1f}%')
        except ZeroDivisionError:
            print(' %Pots Won: N/A')
        print(f' Overall Win%: {100.0 * p.wins / p.handcount:.1f}%')
        try:
            print(f' Showdown Win%: {100.0 * p.showdownwins / p.showdowns:.1f}%')
        except ZeroDivisionError:
            print(f' Showdown Win%: N/A')
        print()
        print(' ---- STACK INFO ----')
        print(f' Start Stack: {p.startstack} for ${p.startstack*0.2:.2f}')
        print(f' Rebuys: {p.rebuys} for {p.rebuychips} chips ${p.rebuychips*0.2:.2f}')
        print(f' Final Stack: {p.stack} chips ${p.stack*0.2:.2f}')
        print(f' Net Earnings: {p.stack - (p.rebuychips + p.startstack)} chips ${(p.stack - (p.rebuychips + p.startstack)) * 0.2:.2f}')
        print()
        print(' ---- Card Expected Values ----')
        try:
            print(f' Avg Card EV: {p.card_ev_sum / p.handcount:.2f}')
            print(f' Avg Flop Card EV: {p.flop_ev_sum / p.flops:.2f}')
        except ZeroDivisionError:
            print('EV Stats not available.')
        print()
    
if __name__ == '__main__':
    game = processgame()
    output(game)
    gameoutput(game)