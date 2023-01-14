import typing
from dijkstra2 import DijkstraHelper
import flood
import functions


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
  curr_health = my_snake["health"]

  opponents = []
  for snake in snakes:
    if snake["id"] != my_snake["id"]:
      opponents.append(snake)

  # Calculate paths and distances
  dijkstra = DijkstraHelper(my_snake, snakes, board_height, board_width)
  safe_moves = dijkstra.get_safe_moves()

  if game_state["turn"] < 3:
    next_move = dijkstra.find_move_to_closest_food(food)
  else:
    if len(safe_moves) == 1:
      next_move = safe_moves[0]
    elif len(safe_moves) > 0:
      print("SUPER EVALUATING")
      next_move = functions.super_evaluator(safe_moves, my_snake, opponents, food, board_height, board_width)
    else:
      # shit
      next_move = "down"
  # next_move = safe_moves[0]
  
  # print("My snake:")
  # print(my_snake["body"])
  # print("Simulated Snake:")
  # print(functions.simulate_move(my_snake["body"], food, ate_food))

  #create a flood board to make flood assessments
  # flood_board = flood.FloodBoard(snakes, board_width, board_height)

  # # Decide our next move
  # if len(my_snake) == 1:
  #   next_move = dijkstra.find_move_to_closest_food(food)
  # else:
  #   #give each safe move a score
  #   move_scores = []
  #   for move in safe_moves:
  #     move_score = 0
  #     if dijkstra.path_exists(my_tail):
  #       print("will find my tail if I go:" + str(move))
  #       move_score += 69
  #     if dijkstra.find_move_to_closest_food(food) is not None \
  #       and move == dijkstra.find_move_to_closest_food(food):
  #       print("will find closest food if I go: " + str(move))
  #       move_score += 10
  #     flood_score = flood_board.make_assessment(move)
  #     print("My flood score for " + str(move) + " is: " + str(flood_score))
  #     move_score += flood_score

  #     move_scores.append([move, move_score])

  #   highest_score = 0
  #   best_move = "down"
  #   for move in move_scores:
  #     score = move[1]
  #     if score > highest_score:
  #       highest_score = score
  #       best_move = move[0]

  #   next_move = best_move

  # print("my snake")
  # print(my_snake["body"])
  # print("simulated snake")
  # print(functions.get_new_snake_given_move(my_snake["body"], next_move, foods))

  # Send our decision
  print(f'MOVE {game_state["turn"]}: {next_move}')
  return {"move": next_move}


if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
