
import random
from typing import List, Union

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
  
  def is_skip_card(self):
    return self.value in ['+2', 'skip']
  
  def is_reverse_card(self):
    return self.value == 'reverse'

  def is_choose_color_card(self):
    return self.value in ['+4', 'wild']
  
  def is_draw_card(self):
    return self.value in ['+2', '+4']

  def draw_how_many(self):
    how_many = 0
    if self.value == '+2':
      how_many = 2
    elif self.value == '+4':
      how_many = 4
    
    return how_many

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
  
  def draw(self, num_cards = 1):
    cards = []
    for i in range(num_cards):
      cards.append(self.cards.pop())
    
    return cards

  def size(self):
    return len(self.cards)

class Player():
  def __init__(self, name: str, color: str) -> None:
    self.name = name
    self.color = color
    self.hand = []

class Play():
  def __init__(self, player: Player, action: str, args: Union[Card, int]) -> None:
    self.player = player
    self.action = action
    self.args   = args

    if self.action == 'play' and not isinstance(self.args, Card):
      raise ValueError(f"Play argument must be a card. It is {self.args}")
    
    if self.action == 'draw':
      if self.args is None:
        self.args = 0
      elif not isinstance(self.args, int):
        raise ValueError(f"Draw argument must be int or None. It is: {self.args}")

  def get_card(self) -> Card:
    if isinstance(self.args, Card):
      return self.args

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
    self.direction = +1
    
    self.current_player_index = 0
    
  def start(self):
    self.deck.shuffle()
    
    for player in self.players:
      player.hand = self.deck.get_hand()

    self._draw_discard()

  def get_current_player(self):
    return self.players[self.current_player_index]   

  def progress(self, play: Play):
    if self.get_current_player() != play.player:
      raise ValueError(f"Current player should be {self.get_current_player()}")    
    
    if play.action == 'play':
      self.play(play)
    elif play.action == 'draw':
      self.draw(play)
    elif play.action == 'pass':
      self.skip()

  def draw(self, play) -> List[Card]:
    if play.get_card() is not None and play.get_card().is_draw_card():
      self.get_current_player().hand.extend(self.deck.draw(play.get_card().draw_how_many()))
    elif play.action == 'draw':
      self.get_current_player().hand.extend(self.deck.draw())
    

  def play(self, play: Play):
    if play.get_card() is None or not is_card_playable(play.get_card(), self.get_discard_top()):
      raise ValueError(f"Play card is invalid: {play.get_card()}")
    
    self.get_current_player().hand.remove(play.get_card())
    self.discard_pile.append(play.get_card())
    
    if play.get_card().is_reverse_card():
      self.direction = -1
    
    skip = 0
    if play.get_card().is_skip_card():
      skip = 1
    
    self._set_next_player(skip)

    if play.get_card().is_draw_card():
      self.draw(play)
  
  def skip(self):
    self._set_next_player()

  def _set_next_player(self, skip: int = 0):
    self.current_player_index = (self.current_player_index + (1 + skip) * self.direction) % len(self.players)


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