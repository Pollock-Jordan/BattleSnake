import typing
from dijkstra2 import DijkstraHelper
import flood


def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "planesnake",
    "color": "#F1F1F1",
    "head": "trans-rights-scarf",
    "tail": "beach-puffin",
  }


def start(game_state: typing.Dict):
  print("GAME START")


def end(game_state: typing.Dict):
  print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
  print(f'TURN {game_state["turn"]}')
  
  # Game state
  my_snake = game_state["you"]
  my_head = my_snake["head"]
  my_tail = my_snake["body"][-1]

  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  food = game_state['board']['food']
  snakes = game_state['board']['snakes']
  curr_health = my_snake[""]

  # Calculate paths and distances
  dijkstra = DijkstraHelper(my_snake, snakes, board_height, board_width)
  safe_moves = dijkstra.get_safe_moves
  
  # Decide our next move
  next_move = safe_moves[0]
  
  # if three areas exist, evaluate each
  
  # elif two areas exist, evaluate each
  
  #if safe path to food and safe path to tail
    #go to food
  #elif 
  #elif one has safe path to tail
  #else choose largest space
  
  # elif we are in open space
  
  #if health > 50:
    #if path_exists(tail):
 		 #get_next_move_towards(tail)
    #else:
 		#find_move_to_closest_food
  #else:
 	  #find_move_to_closest_food

  # Send our decision
  print(f'MOVE {game_state["turn"]}: {next_move}')
  return {"move": next_move}


if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
