
from unittest.case import skip


SUITS  = ['red', 'green', 'blue', 'yellow', 'wild']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', '+4', 'skip', 'reverse', 'color']

class Card():
  def __init__(self, value: str, suit: str) -> None:
    if value not in VALUES:
      raise ValueError(f"Value must be one of {VALUES}. Was {value}.")

    if suit not in SUITS:
      raise ValueError(f"Suit must be one of {SUITS}. Was {suit}.")
    
    self.value = value
    self.suit  = suit

class Deck():
  def __init__(self):
    self.cards = []
    self.cards_by_suit = {}
    for suit in SUITS:
      self.cards_by_suit[suit] = []
      self._makedeck(suit)
  
  def _makedeck(self, suit: str):
    if suit != 'wild':
      for i in range(0, 10):
        card = Card(str(i), suit) 
        self.cards.append(card)
        self.cards_by_suit[suit].append(card)
      
      for i in range(2):
        plus2_card = Card('+2', suit)
        reverse_card = Card('reverse', suit)
        skip_card = Card('skip', suit)

        self.cards.append(plus2_card)
        self.cards.append(reverse_card)
        self.cards.append(skip_card)
        self.cards_by_suit[suit].append(plus2_card)
        self.cards_by_suit[suit].append(reverse_card)
        self.cards_by_suit[suit].append(skip_card)


  
