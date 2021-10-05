from rich import print
from uno import Card, Game, Play, Player, is_card_playable

INPUTS = [ 'exit', 'buy' ]

SYMBOLS = {
  'reverse': "🔄",
  'skip': "🚫"
}


def get_players():
  return [
    Player('Raphael', 'red'),
    Player('Jessica', 'blue')
  ]

def get_suit_style(suit):
  if suit != 'wild':
    return suit
  else:
    return 'bold white'

def get_card_str(card: Card):
  suit_style = get_suit_style(card.suit)
  card_sign  = SYMBOLS.get(card.value, card.value)
  return f"[{suit_style}]|{card_sign}|[/{suit_style}]"

def print_card(card: Card):
  print(get_card_str(card))

def print_player_hand(player: Player, discard_top: Card):
  print(f"[{player.color}]{player.name}'s hand:[/{player.color}]")
  hand_str = ""
  for card in player.hand:
    additional_str = ''
    if is_card_playable(card, discard_top):
      additional_str = '*'
    hand_str += get_card_str(card) + f"{additional_str} "
  print(hand_str)

def validate_input(input: str):
  return input in INPUTS

def main():
  players = get_players()

  game = Game(players)
  game.start()
  discard_top = game.get_discard_top()

  while not game.finished:
    player = game.get_current_player()
    print(f"[bold grey] Discard: {get_card_str(discard_top)}[/bold grey]")
    print(f"{player.name}'s turn")
    print_player_hand(player, discard_top)
    
    valid_input = False
    while not valid_input:
      player_input = input("> ")
      valid_input = validate_input(player_input)
      
    
    if player_input == 'exit':
      game.finish()
    else:
      game.progress(Play(
        player,
        'buy',
        None
      ))


    if game.is_finished(): break

    

if __name__ == "__main__":
  main()