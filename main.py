import typing
from dijkstra2 import DijkstraHelper
import functions

food_last_turn = []


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

  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  food = game_state['board']['food']
  snakes = game_state['board']['snakes']

  ate_food = my_head in food_last_turn
  
  opponents = []
  for snake in snakes:
    if snake["id"] != my_snake["id"]:
      opponents.append(snake)

  # Calculate paths and distances
  dijkstra = DijkstraHelper(my_snake, snakes, board_height, board_width, ate_food)
  safe_moves = dijkstra.get_safe_moves()

  if game_state["turn"] < 3:
    next_move = dijkstra.find_move_to_closest_food(food)
  else:
    if len(safe_moves) == 1:
      next_move = safe_moves[0]
    elif len(safe_moves) > 0:
      ate_food = my_head in food_last_turn
      next_move = functions.super_evaluator(safe_moves, my_snake, opponents,
                                            food, board_height, board_width,
                                            ate_food)
    else:
      # Returns "down" if no safe moves
      next_move = functions.simple_evaluator(my_snake, my_head, snakes,
                                             board_width, board_height)

  food_last_turn.clear()
  food_last_turn.extend(food)

  # Send our decision
  print(f'MOVE {game_state["turn"]}: {next_move}\n')
  return {"move": next_move}


if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
