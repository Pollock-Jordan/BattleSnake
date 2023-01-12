import typing
import functions
import dijkstra
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
  is_move_safe = {"up": True, "down": True, "left": True, "right": True}

  my_head = game_state["you"]["body"][0]
  my_body = game_state['you']['body']
  my_tail = game_state["you"]["body"][len(game_state["you"]["body"]) - 1]

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

  # Move towards food or random
  food = game_state['board']['food']
  next_move = functions.find_closest_food(my_head, food, safe_moves)

  # Generate an adjacency matrix for the given board -A
  g = dijkstra.generate_graph(my_head, board_width, [], opponents)
  # g.print()

  # Run Dijkstra's algo. from head location -A
  int_head_location = dijkstra.coords_to_int(my_head, board_width)
  # g.dijkstra(int_head_location)

  #Doing flood assessments to prevent getting stuck in corners or in self
  #my own body is included in oppoents
  #only bother checking if there is more than one safe move to check
  #only bother checking if there is more than one safe move to check
  if len(safe_moves) > 1:
    flood_board = flood.FloodBoard(opponents, board_width, board_height)
    safety_value = flood_board.make_assessment(next_move)

    if safety_value < 121:
      next_move = functions.find_closest_food(my_head, [my_tail], safe_moves)
      safety_value = flood_board.make_assessment(next_move)

      if safety_value < 121:
        move_safety_values = []
        for move in safe_moves:
          safety_value = flood_board.make_assessment(move)
          move_safety_values.append([move, safety_value])

        highest_index = 0
        highest = 0
        for i in range(len(move_safety_values)):
          if move_safety_values[i][1] > highest:
            highest_index = i

        next_move = move_safety_values[highest_index][0]

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
