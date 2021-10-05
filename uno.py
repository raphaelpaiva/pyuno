
import random

SUITS  = ['red', 'green', 'blue', 'yellow', 'wild']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', '+4', 'skip', 'reverse', 'wild']

class Card():
  def __init__(self, value: str, suit: str) -> None:
    if value not in VALUES:
      raise ValueError(f"Value must be one of {VALUES}. Was {value}.")

    if suit not in SUITS:
      raise ValueError(f"Suit must be one of {SUITS}. Was {suit}.")
    
    self.value = value
    self.suit  = suit

class Deck():
  def __init__(self, half: bool = False):
    self.cards = []
    self.cards_by_suit = {}
    self.half = half
    
    for suit in SUITS:
      self.cards_by_suit[suit] = []
      self._makedeck(suit)
  
  def _makedeck(self, suit: str):
    if suit != 'wild':
      for j in range(2 if not self.half else 1):
        for i in range(0, 10):
          card = Card(str(i), suit) 
          self.cards.append(card)
          self.cards_by_suit[suit].append(card)
      
      for i in range(2 if not self.half else 1):
        plus2_card = Card('+2', suit)
        reverse_card = Card('reverse', suit)
        skip_card = Card('skip', suit)

        self.cards.append(plus2_card)
        self.cards.append(reverse_card)
        self.cards.append(skip_card)
        self.cards_by_suit[suit].append(plus2_card)
        self.cards_by_suit[suit].append(reverse_card)
        self.cards_by_suit[suit].append(skip_card)
    else:
      for i in range(4 if not self.half else 2):
        draw4_card = Card('+4', 'wild')
        wild_card = Card('wild', 'wild')
        self.cards.append(draw4_card)
        self.cards.append(wild_card)
        self.cards_by_suit['wild'].append(draw4_card)
        self.cards_by_suit['wild'].append(wild_card)
  
  def shuffle(self):
    random.shuffle(self.cards)

  def get_hand(self):
    hand = []
    for i in range(7):
      hand.append(self.cards.pop())
    
    return hand
  
  def size(self):
    return len(self.cards)

class Player():
  def __init__(self, name: str, color: str) -> None:
    self.name = name
    self.color = color
    self.hand = []

class Play():
  def __init__(self, player: Player, action: str, card: Card) -> None:
    self.player = player
    self.action = action
    self.card   = card

def is_card_playable(card: Card, discard_top: Card):
  return card.value == discard_top.value \
    or card.suit == discard_top.suit \
    or card.suit == 'wild'

class Game():
  def __init__(self, players: list) -> None:
    self.deck = Deck(half=True)
    self.discard_pile = []
    self.players = players
    self.finished = False
    
    self.current_player_index = 0
    
  def start(self):
    self.deck.shuffle()
    
    for player in self.players:
      player.hand = self.deck.get_hand()

    self._draw_discard()

  def get_current_player(self):
    return self.players[self.current_player_index]

  def progress(self, play: Play):
    if play.player.name != self.get_current_player().name:
      raise ValueError
    else:
      self.current_player_index = (self.current_player_index + 1) % len(self.players)

  def get_discard_top(self):
    return self.discard_pile[-1]
  

  def finish(self):
    self.finished = True

  def is_finished(self):
    return self.finished

  def _draw_discard(self):
    card = self.deck.cards.pop()
    while not self._validate_discard_top(card):
      self.deck.cards.insert(0, card)
      card = self.deck.cards.pop()
    
    self.discard_pile.append(card)

  def _validate_discard_top(self, card: Card):
    return card.value not in ['+2', '+4', 'skip', 'reverse', 'wild']