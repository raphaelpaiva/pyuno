from typing import List
from cli import get_command, get_input, print_table, console
from uno import Game, Play, Player

def get_players() -> List[Player]:
  num_players = get_input("How many players? [2-10] > ", lambda x: int(x) > 1 and int(x) <= 10)
  
  players = []
  for i in range(int(num_players)):
    player_number = i + 1
    player_name = get_input(f"Player {player_number} name > ")
    player_color = get_input(f"Player {player_number} color > ", lambda x: x in ['blue', 'green', 'yellow', 'red', 'cyan', 'magenta', 'white', 'gray'])

    players.append(Player(player_name, player_color))

  return players

def main():
  players = get_players()

  game = Game(players)
  game.start()

  while not game.finished:
    player = game.get_current_player()
    discard_top = game.get_discard_top()
    
    print_table(player, discard_top, {p.id: p.as_dict() for p in game.players})
    
    command, args = get_command()
    
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
        console.print(f"[red reverse]ERROR[/red reverse]: {ie}")
        continue
      except ValueError as ve:
        console.print(f"[red reverse]ERROR[/red reverse]: {ve}")
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
    console.print(f"[{game.winner.color} reverse]{game.winner.name} WON![/{game.winner.color} reverse]")    

if __name__ == "__main__":
  main()