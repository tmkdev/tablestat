import csv

class Card_EV(object):
    def __init__(self, lookuptable='ev.tsv'):
        self.lookuptable = lookuptable
        self.hands = {}

        self._loadfile()

    def _loadfile(self):
        with open(self.lookuptable, ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                self.hands[row['hand']] = float(row['ev'])
  
    def evalhand(self, hand):
        #Hand in the format of 7c Td 
        cards = hand.split(' ')
        card0 = cards[0][:-1]
        card1 = cards[1][:-1] 

        suit0 = cards[0][-1]
        suit1 = cards[1][-1]

        hand = f'{card0}{card1}'

        hand = ''.join(sorted(hand))

        if hand not in self.hands:
            hand = hand[::-1]

        suited = ''
        if suit0 == suit1:
            suited = ' s'

        hand = f"{hand}{suited}"  

        ev = self.hands[hand]

        return hand, ev 


if __name__ == '__main__':
    c = Card_EV()

    print(c.evalhand('Qc Qd'))