
import random
import uuid
from typing import List

SUITS        = ['red', 'green', 'blue', 'yellow', 'wild']
VALUES       = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', '+4', 'skip', 'reverse', 'wild']
SUIT_CHOICES = list(SUITS)
SUIT_CHOICES.remove('wild')
PLAYER_HAND_SIZE = 7

class UnoObject(object):
  def __init__(self, id: str = None) -> None:
    if id is None:
      self.id = str(uuid.uuid4())
    else:
      self.id = id
  
  def as_dict(): raise NotImplementedError()

class Card(UnoObject):
  def __init__(self, value: str, suit: str, id: str = None) -> None:
    super().__init__(id)
    if value not in VALUES:
      raise ValueError(f"Value must be one of {VALUES}. Was {value}.")

    if suit not in SUITS:
      raise ValueError(f"Suit must be one of {SUITS}. Was {suit}.")
    
    self.value = value
    self.suit  = suit
  
  def is_skip_card(self) -> bool:
    return self.value in ['+2', 'skip']
  
  def is_reverse_card(self) -> bool:
    return self.value == 'reverse'

  def is_choose_color_card(self) -> bool:
    return self.value in ['+4', 'wild']
  
  def is_draw_card(self) -> bool:
    return self.value in ['+2', '+4']

  def draw_how_many(self) -> bool:
    how_many = 0
    if self.value == '+2':
      how_many = 2
    elif self.value == '+4':
      how_many = 4
    
    return how_many
  
  def as_dict(self):
    return {
      'id': self.id,
      'value': self.value,
      'suit': self.suit
    }
  
  @staticmethod
  def from_dict(card_dict: dict):
    return Card(
      id    = card_dict['id'],
      value = card_dict['value'],
      suit  = card_dict['suit']
    )

  def __str__(self):
    return f"Card({self.value}, {self.suit}, {self.id})"
  
  def __repr__(self) -> str:
      return str(self)
class Deck(UnoObject):
  def __init__(self, half: bool = False, id: str = None) -> None:
    super().__init__(id)
    self.cards = []
    self.cards_by_suit = {}
    self.half = half
    
    for suit in SUITS:
      self.cards_by_suit[suit] = []
      self._makedeck(suit)
  
  def _makedeck(self, suit: str):
    if suit != 'wild':
      zero_card = Card('0', suit)
      self.cards.append(zero_card)
      self.cards_by_suit[suit].append(zero_card)
      for j in range(2 if not self.half else 1):
        for i in range(1, 10):
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

  def get_hand(self) -> List[Card]:
    hand = []
    for _ in range(PLAYER_HAND_SIZE):
      hand.append(self.cards.pop())
    
    return hand
  
  def draw(self, num_cards = 1) -> List[Card]:
    cards = []
    for i in range(num_cards):
      cards.append(self.cards.pop())
    
    return cards

  def size(self) -> int:
    return len(self.cards)

class Player(UnoObject):
  def __init__(self, name: str, color: str, id: str = None) -> None:
    super().__init__(id)
    self.name = name
    self.color = color
    self.hand = []
  
  def as_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'color': self.color,
      'hand': [c.as_dict() for c in self.hand]
    }
  
  @staticmethod
  def from_dict(player_dict : dict):
    player = Player(
      id    = player_dict['id'],
      name  = player_dict['name'],
      color = player_dict['color']
    )

    if 'hand' in player_dict:
      player.hand = [Card.from_dict(c_dict) for c_dict in player_dict['hand']]
    
    return player

class Play(UnoObject):
  def __init__(self, player: Player, action: str, card: Card = None, suit: str = None, id: str = None) -> None:
    super().__init__(id)
    self.player = player
    self.action = action
    self.card   = card
    self.suit   = suit

    if self.action == 'play':
      if self.card is None:
        raise ValueError(f"Play argument must be a card. It is {self.card}")
      
      if self.card.is_choose_color_card() and self.suit not in SUIT_CHOICES:
        raise ValueError(f"For {self.card.value} cards, suit choice must be one of {SUIT_CHOICES}")

  def get_card(self) -> Card:
    return self.card
  
  def get_suit(self) -> str:
    return self.suit

def is_card_playable(card: Card, discard_top: Card) -> bool:
  return card.value == discard_top.value \
    or card.suit == discard_top.suit \
    or card.suit == 'wild'

class Game(UnoObject):
  def __init__(self, players: List[Player], id: str = None) -> None:
    super().__init__(id)
    
    self.deck = Deck(half=True)
    self.discard_pile   = []
    self.players        = players
    self._players_by_id = {p.id: p for p in self.players}
    self.started        = False
    self.finished       = False
    self.direction      = +1
    self.winner         = None
    
    self.current_player_index = 0
    
  def start(self):
    if not self.started:
      self.deck.shuffle()
      
      for player in self.players:
        player.hand = self.deck.get_hand()

      self._draw_discard()
      self.started = True

  def get_current_player(self) -> Player:
    return self.players[self.current_player_index]   

  def get_player_by_id(self, player_id):
    return self._players_by_id[player_id]

  def progress(self, play: Play):
    if self.get_current_player() != play.player:
      raise ValueError(f"Current player should be {self.get_current_player()}")    
    
    if play.action == 'play':
      self.play(play)
    elif play.action == 'draw':
      self.draw(play)
    elif play.action == 'pass':
      self.skip()

  def draw(self, play: Play, player: Player = None) -> List[Card]:
    if player is None:
      player = self.get_current_player()

    if play.get_card() is not None and play.get_card().is_draw_card():
      player.hand.extend(self.deck.draw(play.get_card().draw_how_many()))
    elif play.action == 'draw':
      player.hand.extend(self.deck.draw())
    
  def play(self, play: Play):
    if play.get_card() is None or not is_card_playable(play.get_card(), self.get_discard_top()):
      raise ValueError(f"Play card is invalid: {play.get_card()}")

    self.get_current_player().hand.remove(play.get_card())
    self.discard_pile.append(play.get_card())

    if len(self.get_current_player().hand) < 1:
      self.finish(self.get_current_player())
    
    if play.get_card().is_reverse_card():
      self.direction = -1
    
    skip = 0
    if play.get_card().is_skip_card():
      skip = 1
    

    if play.get_card().is_draw_card():
      self.draw(play, self.players[self._get_next_player_index(0)])

    if play.get_card().is_choose_color_card():
      self.get_discard_top().suit = play.get_suit()
    
    self._set_next_player(skip)
  
  def skip(self):
    self._set_next_player()

  def _set_next_player(self, skip: int = 0):
    self.current_player_index = self._get_next_player_index(skip)

  def _get_next_player_index(self, skip) -> int:
      return (self.current_player_index + (1 + skip) * self.direction) % len(self.players)

  def get_discard_top(self) -> Card:
    return self.discard_pile[-1]
  
  def finish(self, winner: Player = None):
    self.finished = True
    self.winner = winner

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