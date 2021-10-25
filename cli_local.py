from typing import Any, Callable, List
from rich import print
from uno import Card, Game, Play, Player, is_card_playable

COMMANDS = [ 'exit', 'draw', 'play', 'pass' ]

SYMBOLS = {
  'reverse': "r",
  'skip': "s",
  'wild': "w"
}

def get_input(prompt: str = '> ', validator: Callable = lambda x: True) -> Any:
  while True:
    try:
      value = input(prompt)
      if validator(value):
        return value
    except Exception as e:
      print(e)

def get_players() -> List[Player]:
  num_players = get_input("How many players? [2-10]> ", lambda x: int(x) > 1 and int(x) <= 10)
  
  players = []
  for i in range(int(num_players)):
    player_number = i + 1
    player_name = get_input(f"Player {player_number} Name> ")
    player_color = get_input(f"Player {player_number} Name> ", lambda x: x in ['blue', 'green', 'yellow', 'red', 'cyan', 'magenta', 'white', 'gray'])

    players.append(Player(player_name, player_color))

  return players

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

      try:
        args_list = args.split(' ')
        card_index = int(args_list[0].strip())
        card = player.hand[card_index]
      
        suit = args_list[1].strip() if len(args_list) > 1 else None
        
        game.progress(Play(
          player,
          'play',
          card=card,
          suit=suit
        ))
      except IndexError as ie:
        print(f"[red reverse]ERROR[/red reverse]: {ie}")
        continue
      except ValueError as ve:
        print(f"[red reverse]ERROR[/red reverse]: {ve}")
        continue

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

  if game.winner is not None:
    print(f"[{game.winner.color} reverse]{game.winner.name} WON![/{game.winner.color} reverse]")

def parse_input(player_input):
  player_input = player_input.strip()
  input_parts = player_input.split(' ')
  
  command = input_parts.pop(0)
  args = ' '.join(input_parts)
  return command,args

    

if __name__ == "__main__":
  main()