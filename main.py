import random
import typing
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
  is_move_safe = {"up": True, "down": True, "left": True, "right": True}

  my_head = game_state["you"]["body"][0]
  my_body = game_state['you']['body']

  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  opponents = game_state['board']['snakes']

  # Avoid hazards
  functions.avoid_walls(my_head, board_width, board_height, is_move_safe)
  functions.avoid_body(my_head, my_body, is_move_safe)

  for snake in opponents:
    functions.avoid_body(my_head, snake["body"], is_move_safe)

  # Are there any safe moves left?
  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  if len(safe_moves) == 0:
    print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
    return {"move": "down"}

  # Choose a random move from the safe ones
  next_move = random.choice(safe_moves)

  # TODO: Step 4 - Move towards food instead of random, to regain health
  # food = game_state['board']['food']

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
