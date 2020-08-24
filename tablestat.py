import logging
import re
from pokergame import Player, Game


re_hand = re.compile('Hand #(?P<hand>\d+-\d+) - (?P<hand_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
re_seat = re.compile('Seat (?P<seat>\d): (?P<player>\S+) \((?P<stack>\d+)\)')
re_holecards = re.compile('\*\* Hole Cards \*\* \[(?P<players>\d) players\]')
re_fold = re.compile('(?P<player>\S+) folds')
re_flop = re.compile('\*\* Flop \*\*')
re_turn = re.compile('\*\* Turn \*\*')
re_river = re.compile('\*\* River \*\*')
re_winspot = re.compile('(?P<player>\S+) wins Pot \((?P<potsize>\d+\))')
re_showdown = re.compile('\*\* Pot Show Down \*\*')

game = Game()



for line in open('HandHistory_20200821.txt', 'r'):
    m = re_hand.search(line)
    if m:
        game.handcount+=1
        game.gamestate = Game.PREFLOP

    m = re_seat.search(line)
    if m:
        player = m.groupdict()['player']
        if player not in game.players:
            logging.info(f'Player {player} not in players!')
            p = Player(player, startstack=int(m.groupdict()['stack']))
            game.players[player] = p

        game.players[player].handcount +=1 

    m = re_holecards.search(line)
    if m:
        game.gamestate = Game.HOLECARDS
    
    m = re_flop.search(line)
    if m:
        game.gamestate = Game.FLOP

    m = re_turn.search(line)
    if m:
        game.gamestate = Game.TURN

    m = re_river.search(line)
    if m:
        game.gamestate = Game.RIVER

    m = re_showdown.search(line)
    if m:
        game.gamestate = Game.SHOWDOWN

    m = re_fold.search(line)
    if m:
        pass

    m = re_winspot.search(line)
    if m:
        player = m.groupdict()['player']
        game.players[player].wins +=1 



    playertest = line.split(' ')
    player = playertest[0]
    if player in list(game.players) and playertest[1] in ['calls', 'checks', 'raises', 'bets', 'shows']:
        if game.gamestate == Game.FLOP:
            game.players[player].flops+=1
        if game.gamestate == Game.TURN:
            game.players[player].turns+=1
        if game.gamestate == Game.RIVER:
            game.players[player].rivers+=1
        if game.gamestate == Game.SHOWDOWN:
            game.players[player].showdowns+=1

print('Player Summary')
for player in game.players:
    p = game.players[player]
    print(f"{p.player} - Hands: {p.handcount} Flops: {p.flops}  Turns: {p.turns} Rivers: {p.rivers} Showdowns: {p.showdowns} Wins: {p.wins}" )
    print(f'Win Ratio {p.wins / p.handcount:.3f} Flop Win Ratio {p.wins / p.flops:.3f}')
    print()
    