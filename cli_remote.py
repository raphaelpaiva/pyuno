
import requests
from rich.console import Console
from cli import get_command, get_input, print_table, print_player_hand

from uno import Card, Play, Player

class MyException(Exception): pass

console = Console()

GAME_ID        = 'abc'
BASE_URL       = 'http://localhost:5000'
GAME_URL       = f"{BASE_URL}/game/{GAME_ID}"
START_GAME_URL = f"{GAME_URL}/start"
PLAYER_URL     = f"{GAME_URL}/player"
PLAY_URL       = f"{GAME_URL}/play"

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
  console.log(f"Posting {data} to {url}")
  response = requests.post(url, json=data)
  if response.status_code >= 400:
    console.log(
      f"Got status [yellow]{response.status_code}[/yellow] while posting to [blue]{url}[/blue]",
      response.text
    )
    
    raise MyException()
  else:
    return response.json()

def get(url : str) -> dict:
  console.log(f"Getting {url}")
  response = requests.get(url)
  if response.status_code > 400:
    console.log(
      f"Got status [yellow]{response.status_code}[/yellow] while getting to [blue]{url}[/blue]",
      response.text
    )
    
    raise MyException()
  else:
    return response.json()

try:
  game_staus = post(START_GAME_URL, PLAYERS)
  console.log(f"Game status: {game_staus['status']}")
  
  game_data = get(GAME_URL)
  
  while not game_data['finished']:
    console.log('Got game data.')
    game_players = {p['id']: p for p in game_data['players']}
    players_by_name = {p['name']: p for p in game_players.values()}
    player_names = list(players_by_name.keys())

    player_name  = get_input(f"Who are you? {player_names}> ", validator=lambda x: x in player_names)
    local_player = Player.from_dict(players_by_name[player_name])

    current_player_id = game_data['current_player']
    current_player = game_players[current_player_id]

    console.log(f"Current player is {current_player['name']}.")

    if current_player_id == local_player.id:
      current_player_data = get(f"{PLAYER_URL}/{current_player_id}")

      player = Player.from_dict(current_player_data)
      discard_top = Card.from_dict(game_data['discard_top'])
      print_table(player, discard_top, game_players)
      command, args = get_command()

      if command == 'play':
        args_list = args.split(' ')
        card_index = int(args_list[0].strip())
        card = player.hand[card_index]
      
        suit = args_list[1].strip() if len(args_list) > 1 else None

        play = {
          'player_id': player.id,
          'action': 'play',
          'card_id': card.id,
          'suit': suit
        }

        play_status = post(PLAY_URL, play)
        console.log(play_status)
    else:
      console.log("Not your turn")
    
    game_data = get(GAME_URL)
  
except MyException:
  console.log('Exiting.')