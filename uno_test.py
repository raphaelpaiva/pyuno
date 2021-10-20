import unittest
import re
from uno import PLAYER_HAND_SIZE, Card, VALUES, SUITS, Deck, Game, Player

class CardTest(unittest.TestCase):
  def testCardConstructor_okValue_okSuit(self):
    card = Card('0', 'red')

    self.assertEqual(card.value, '0')
    self.assertEqual(card.suit,  'red')
  
  def testCardConstructor_wrongValue(self):
    self.assertRaises(ValueError, Card, 'a', 'red')
  
  def testCardConstructor_wrongSuit(self):
    self.assertRaises(ValueError, Card, '0', 'rede')
  
  def testCard_isSkipCard_plus2(self):
    card = Card('+2', 'red')
    self.assertTrue(card.is_skip_card(), f"Card {card.value} should be a skip card")
  
  def testCard_isSkipCard_skip(self):
    card = Card('skip', 'red')
    self.assertTrue(card.is_skip_card(), f"Card {card.value} should be a skip card")
  
  def testCard_isSkipCard_skip(self):
    card = Card('3', 'red')
    self.assertFalse(card.is_skip_card(), f"Card {card.value} should be a skip card")
class DeckTest(unittest.TestCase):
  def testConstructDeck(self):
    decks = [Deck(half=False), Deck(half=True)]
    
    for deck in decks:
      self._test_deck(deck)

  def _test_deck(self, deck):
      expected_deck_cards = 56 if deck.half else 108
      self.assertEqual(len(deck.cards), expected_deck_cards, f"There should be {expected_deck_cards} cards in a {'half' if deck.half else 'full'} deck")
      
      for suit, suit_cards in deck.cards_by_suit.items():
        if suit != 'wild':
          number_of_cards          = len(suit_cards)
          number_of_zero_cards     = len(list(filter(lambda x: x.value == '0', suit_cards)))
          number_of_reverse_cards  = len(list(filter(lambda x: x.value == 'reverse', suit_cards)))
          number_of_draw_two_cards = len(list(filter(lambda x: x.value == '+2', suit_cards)))
          number_of_skip_cards     = len(list(filter(lambda x: x.value == 'skip', suit_cards)))

          number_of_number_cards  = len(list(filter(lambda x: re.match(r'[0-9]', x.value), suit_cards)))
          
          expected_suit_cards    = 13 if deck.half else 25
          expected_number_cards  = 10 if deck.half else 19
          expected_special_cards = 1 if deck.half else 2
          expected_zero_cards    = 1
          
          self.assertEqual(number_of_cards,          expected_suit_cards,    f"There should be 25 cards in {suit} suit")
          self.assertEqual(number_of_zero_cards,     expected_zero_cards,    f"There should be 1 '0' card in {suit} suit")
          self.assertEqual(number_of_number_cards,   expected_number_cards,  f"There should be 19 number cards in {suit} suit")
          self.assertEqual(number_of_draw_two_cards, expected_special_cards, f"There should be 2 +2 cards in {suit} suit")
          self.assertEqual(number_of_reverse_cards,  expected_special_cards, f"There should be 2 reverse cards in {suit} suit")
          self.assertEqual(number_of_skip_cards,     expected_special_cards, f"There should be 2 skip cards in {suit} suit")
        else:
          number_of_cards           = len(suit_cards)
          number_of_wild_cards      = len(list(filter(lambda x: x.value == 'wild', suit_cards)))
          number_of_draw_four_cards = len(list(filter(lambda x: x.value == '+4', suit_cards)))

          expected_suit_cards      = 4 if deck.half else 8
          expected_wild_cards      = 2 if deck.half else 4
          expected_draw_four_cards = 2 if deck.half else 4
          
          self.assertEqual(number_of_cards,           expected_suit_cards,      f"There should be 8 cards in {suit} suit")
          self.assertEqual(number_of_wild_cards,      expected_wild_cards,      f"There should be 4 cards in {suit} suit")
          self.assertEqual(number_of_draw_four_cards, expected_draw_four_cards, f"There should be 8 cards in {suit} suit")
    
  def test_getHand(self):
    deck = Deck()

    hand = deck.get_hand()
    hand_size = len(hand)
    
    expected_deck_size = 108 - PLAYER_HAND_SIZE

    self.assertEqual(hand_size,   PLAYER_HAND_SIZE,   f"Expected hand size to be {PLAYER_HAND_SIZE}")
    self.assertEqual(deck.size(), expected_deck_size, f"Expected new deck size to be {expected_deck_size}")

PLAYERS = [
  Player('Player 1', 'red'),
  Player('Player 2', 'green'),
  Player('Player 3', 'blue'),
]

class GameTest(unittest.TestCase):
  def test_init_twoPlayers(self):
    # Must be half deck
    game = Game(PLAYERS[:2])
    self.assertEquals(len(game.players), 2)
    self.assertTrue(game.deck.half, "Expected a two player game to be half deck.")
    DeckTest()._test_deck(game.deck)
  
  def test_init_threePlayers(self):
    # Must be full deck
    game = Game(PLAYERS)
    self.assertEqual(len(game.players), 3)
    self.assertFalse(game.deck.half, "Expected a two player game to be full deck.")
    DeckTest()._test_deck(game.deck)