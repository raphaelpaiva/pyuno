from uno import Deck, Card
from rich import print

deck = Deck()
for suit in deck.cards_by_suit.keys():
  cards = deck.cards_by_suit[suit]
  suit_str = ""
  for card in cards:
    suit_str += f"|{card.value}| "

  print(f"[{suit}]{suit_str}[/{suit}]")