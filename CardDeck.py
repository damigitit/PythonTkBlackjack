# Title: CardDeck.py
# Author: Damian Archer
# Date: 2-7-2021
# Purpose: CIS 120 Programming Project 3

"""
    A simple implementation of a card deck.
    
    Requirements: 
      1) Capable of dealing out cards randomly.
      2) Deck class should contain a list of 52 unique Card objects.
      3) deal() method "pops" card choosen from random location in card list.
      4) cardsLeft() method tells how many cards are left in the deck.
"""

import random

class Deck:

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        """ post: self.shuffle is shuffled list of 52 unique Card objects. """
        self.cards = [Card(i) for i in range(52)]
        random.shuffle(self.cards)
        
    def deal(self):
        """ post: returns a card from a random location in the deck. """
        return self.cards.pop(random.randrange(0, len(self.cards)))

    def cardsLeft(self):
        """ post: returns int amount of cards remaining in deck. """
        return len(self.cards)

class Card:
    SUITS = ["\u2663", "\u2666", "\u2665", "\u2660"]
    RANKS = ["A", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self, card_id):
        """ pre: card id is an integer between 0 and 51"""
        self.card_id = card_id

    def get_rank(self):
        """ post: returns rank of card according to card_id"""
        return self.RANKS[self.card_id%13]

    def get_suit(self):
        """ post: returns suit of card according to card_id"""
        return self.SUITS[self.card_id%4]

    def get_blackjack_value(self):
        """ post:  Returns 11 for Aces, 10 for Faces or Ten card,
                   or appropriate value in range 2-9, according to card_id.
        """
        if self.card_id%13 == 0: return 11
        elif self.card_id%13 > 8: return 10
        else: return self.card_id%13 + 1

    def __str__(self):
        return f"{self.get_rank()} of {self.get_suit()}"

    def draw(self, gfx, x, y):
        w, h = gfx.winfo_width()/9, gfx.winfo_height()/5
        if self.get_suit() in ["\u2666","\u2665"]: fontcolor = "red"
        else: fontcolor = "black"
        gfx.create_rectangle(x, y, w+x, h+y, fill="white")
        gfx.create_text(x+24, y+16, text=self.get_rank()+" "+self.get_suit(), font=["jokerman", 16], fill=fontcolor)
        gfx.create_text((x+w)-24, (y+h)-16, text=self.get_suit()+" "+self.get_rank(),font=["jokerman", 16], fill=fontcolor)

        

    
