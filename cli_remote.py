import json
import requests
from rich.console import Console
from rich.json import JSON
from cli_local import print_player_hand

from uno import Card, Player

class MyException(Exception): pass

console = Console()

GAME_ID        = 'abc'
BASE_URL       = 'http://localhost:5000'
GAME_URL       = f"{BASE_URL}/game/{GAME_ID}"
START_GAME_URL = f"{GAME_URL}/start"
PLAYER_URL     = f"{GAME_URL}/player"

PLAYERS = {
  'players': [
    {
      'name': 'Raphael',
      'color': 'red'
    },
    {
      'name': 'Jessica',
      'color': 'blue'
    }
  ]
}

def post(url : str, data : dict) -> dict:
  response = requests.post(url, json=data)
  if response.status_code > 400:
    console.log(
      f"Got status [yellow]{response.status_code}[/yellow] while posting to [blue]{url}[/blue]",
      response.text
    )
    
    raise MyException()
  else:
    return response.json()

def get(url : str) -> dict:
  response = requests.get(url)
  if response.status_code > 400:
    console.log(
      f"Got status [yellow]{response.status_code}[/yellow] while getting to [blue]{url}[/blue]",
      response.text
    )
    
    raise MyException()
  else:
    return response.json()

def print_table(current_player : Player, discard_top : Card, players_data : dict):
  for player_data in players_data.values():
    player = Player.from_dict(player_data)
    
    if player.id != current_player.id:
      console.print(f"[{player.color}]{player.name}'s hand: [bold]{player_data['hand_size']}[/bold][/{player.color}]")
  
  print_player_hand(current_player, discard_top)

try:
  post(START_GAME_URL, PLAYERS)
  game_data = get(GAME_URL)

  console.log('Got game data.', game_data)

  game_players = {p['id']: p for p in game_data['players']}

  current_player_id = game_data['current_player']
  current_player = game_players[current_player_id]

  console.log(f"Current player is {current_player['name']}.")

  current_player_data = get(f"{PLAYER_URL}/{current_player_id}")
 
  player = Player.from_dict(current_player_data)
  discard_top = Card.from_dict(game_data['discard_top'])
  
  print_table(player, discard_top, game_players)
except MyException:
  console.log('Exiting.')