from rich import print
from uno import Card, Game, Play, Player, is_card_playable

COMMANDS = [ 'exit', 'draw', 'play', 'pass' ]

SYMBOLS = {
  'reverse': "r",
  'skip': "s",
  'wild': "w"
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
    card_str = get_card_str(card)
    if is_card_playable(card, discard_top):
      card_str = f"[underline]{card_str}[/underline]"
    
    hand_str += card_str + " "
  print(hand_str)
  index_str = ""
  for i in range(len(player.hand)):
    index_str += f"|{i}| "
  print(index_str)

def validate_input(input: str):
  return input in COMMANDS

def main():
  players = get_players()

  game = Game(players)
  game.start()

  while not game.finished:
    player = game.get_current_player()
    discard_top = game.get_discard_top()
    
    print(f"[bold grey] Discard: {get_card_str(discard_top)}[/bold grey]")
    print(f"{player.name}'s turn")
    print_player_hand(player, discard_top)
    
    valid_input = False
    while not valid_input:
      player_input = input("> ")
      command, args = parse_input(player_input)
      valid_input = validate_input(command)
    

    if command == 'exit':
      game.finish()
    elif command == 'play':
      card_index = int(args.strip())

      card = player.hand[card_index]
      
      game.progress(Play(
        player,
        'play',
        card
      ))
    elif command == 'draw':
      game.progress(Play(
        player,
        'draw',
        None
      ))
    elif command == 'pass':
      game.progress(Play(
        player,
        'pass',
        None
      ))


    if game.is_finished(): break

def parse_input(player_input):
    player_input = player_input.strip()
    input_parts = player_input.split(' ')
    
    command = input_parts.pop(0)
    args = ' '.join(input_parts)
    return command,args

    

if __name__ == "__main__":
  main()