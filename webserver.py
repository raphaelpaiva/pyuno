from typing import Dict
from flask import Flask, request, abort

from uno import Game, Player

app = Flask('pyuno')
GAMES_BY_ID = {}

def get_players(request):
  content = request.json

  players = []
  for player_content in content['players']:
    players.append(
      Player(player_content['name'], player_content['color'])
    )

  return players

@app.route('/')
def hello():
  result = {}
  for game in GAMES_BY_ID.values():
    result[game.id] = get_game_public_info(game.id)

  return result

@app.route('/game/<game_id>/')
def get_game_public_info(game_id):
  if game_id not in GAMES_BY_ID:
    abort(404) 

  game = GAMES_BY_ID[game_id]
  
  return {
    'finished': game.finished,
    'started': len(game.discard_pile) > 0,
    'players': [p.as_dict() for p in game.players],
    'players_hands': [{'id': p.id, 'hand': len(p.hand)} for p in game.players],
    'discard_top': game.get_discard_top().as_dict(),
    'current_player': game.get_current_player().id
  }

@app.route('/game/<game_id>/start', methods = ['POST'])
def start_game(game_id: str):
  players = get_players(request)
  if not game_id in GAMES_BY_ID:
    GAMES_BY_ID[game_id] = Game(players, game_id)
  
  game = GAMES_BY_ID[game_id]
  game.start()

  return "OK"