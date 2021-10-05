import unittest
from uno import Card, VALUES, SUITS

class UnoTest(unittest.TestCase):
  def testCardConstructor_okValue_okSuit(self):
    card = Card('0', 'red')

    self.assertEqual(card.value, '0')
    self.assertEqual(card.suit,  'red')
  
  def testCardConstructor_wrongValue(self):
    self.assertRaises(ValueError, Card, 'a', 'red')
  
  def testCardConstructor_wrongSuit(self):
    self.assertRaises(ValueError, Card, '0', 'rede')
