from typing import Dict
from flask import Flask, request, abort

from uno import Game, Play, Player

app = Flask('pyuno')
GAMES_BY_ID = {}

def get_game(game_id : str) -> Game:
  if game_id not in GAMES_BY_ID:
    abort(404)
  
  return GAMES_BY_ID[game_id]

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

@app.route('/game/<game_id>')
def get_game_public_info(game_id):
  game = get_game(game_id)

  player_dicts = [p.as_dict() for p in game.players]

  for player_info in player_dicts:
    player_info['hand_size'] = len(player_info['hand'])
    del player_info['hand']
  
  return {
    'finished': game.finished,
    'started': game.started,
    'players': player_dicts,
    'discard_top': game.get_discard_top().as_dict(),
    'current_player': game.get_current_player().id
  }

@app.route('/game/<game_id>/player/<player_id>')
def get_player_data(game_id, player_id):
  try:
    game   = get_game(game_id)
    player = game.get_player_by_id(player_id)

    player_dict = player.as_dict()

    return player_dict
  except KeyError:
    abort(404)


@app.route('/game/<game_id>/start', methods = ['POST'])
def start_game(game_id: str):
  players = get_players(request)
  game_existed = True
  if not game_id in GAMES_BY_ID:
    GAMES_BY_ID[game_id] = Game(players, game_id)
    game_existed = False
  
  game = get_game(game_id)

  game.start()

  return {"status": "ok"} if game_existed else {"status": "created"}

@app.route('/game/<game_id>/play', methods = ['POST'])
def play(game_id: str):
  game = get_game(game_id)
  current_player = game.get_current_player()
  content = request.json
  player_cards_by_id = {c.id: c for c in current_player.hand}

  if content['player_id'] != current_player.id:
    abort(403)
  if not content['card_id'] in player_cards_by_id:
    print(f"Card {content['card_id']} not present on player's hand")
    abort(400)
  
  game.progress(
    Play(
      player = current_player,
      action = content['action'],
      card   = player_cards_by_id[content['card_id']],
      suit   = content['suit']
    )
  )

  return {"status": "ok"}
