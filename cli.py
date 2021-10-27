from typing import Any, Callable
from rich.console import Console

from uno import Card, Player, is_card_playable

COMMANDS = [ 'exit', 'draw', 'play', 'pass' ]

SYMBOLS = {
  'reverse': "r",
  'skip': "s",
  'wild': "w"
}

console = Console()

def get_input(prompt: str = '> ', validator: Callable = lambda x: True) -> Any:
  while True:
    try:
      value = input(prompt)
      if validator(value):
        return value
    except Exception as e:
      console.print(e)

def parse_input(player_input):
  player_input = player_input.strip()
  input_parts = player_input.split(' ')
  
  command = input_parts.pop(0)
  args = ' '.join(input_parts)
  return command,args

def validate_commands(input: str):
  return input.split(' ')[0] in COMMANDS

def get_command():
  player_input = get_input(validator=validate_commands)
  command, args = parse_input(player_input)
  return command,args

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
  console.print(get_card_str(card))

def print_player_hand(player: Player, discard_top: Card):
  console.print(f"[{player.color}]{player.name}'s hand:[/{player.color}]")
  hand_str = ""
  for card in player.hand:
    card_str = get_card_str(card)
    if is_card_playable(card, discard_top):
      card_str = f"[underline]{card_str}[/underline]"
    
    hand_str += card_str + " "
  console.print(hand_str)
  index_str = ""
  for i in range(len(player.hand)):
    index_str += f"|{i}| "
  console.print(index_str)

def print_discard(discard_top):
  console.print(f"[bold grey]Discard: {get_card_str(discard_top)}[/bold grey]")

def print_other_player_hands(current_player, players_data):
  for player_data in players_data.values():
    player = Player.from_dict(player_data)
  
    if player.id != current_player.id:
      if 'hand_size' in player_data:
        hand_size = player_data['hand_size']
      else:
        hand_size = len(player.hand)
    
      console.print(f"[{player.color}]{player.name}'s hand: [bold]{hand_size}[/bold][/{player.color}]")

def print_table(current_player : Player, discard_top : Card, players_data : dict):
  print_other_player_hands(current_player, players_data)
  print_discard(discard_top)
  print_player_hand(current_player, discard_top)
