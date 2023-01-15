import sys
import math
from copy import deepcopy
from dijkstra2 import DijkstraHelper


def get_new_snake_given_move(snake, move, foods, ate_food):
  new_head = get_new_head_given_move(snake[0], move)
  snake.insert(0, new_head)

  if not ate_food:
    snake.pop()

  return new_head, snake


def get_new_head_given_move(my_head, move):
  if move == "up":
    return {"x": my_head["x"], "y": my_head["y"] + 1}
  elif move == "down":
    return {"x": my_head["x"], "y": my_head["y"] - 1}
  elif move == "right":
    return {"x": my_head["x"] + 1, "y": my_head["y"]}
  elif move == "left":
    return {"x": my_head["x"] - 1, "y": my_head["y"]}
  else:
    return my_head


def super_evaluator(safe_moves, my_snake, opponents, foods, height, width,
                    ate_food):
  results = []
  for move in safe_moves:
    my_new_snake = deepcopy(my_snake)
    my_new_snake["head"], my_new_snake["body"] = get_new_snake_given_move(my_new_snake["body"], move, foods, ate_food)
    my_new_tail = my_new_snake["body"][-1]
    my_new_snake["length"] = len(my_new_snake["body"])
    snakes = [my_new_snake] + opponents

    dijkstra = DijkstraHelper(my_new_snake, snakes, height, width, ate_food)
    closest_food = dijkstra.get_closest_food(foods)

    if closest_food is None:
      distance_to_closest_food = sys.maxsize
    else:
      distance_to_closest_food = dijkstra.distance_to(closest_food)

    results.append({
      "move": move,
      "distance_to_closest_food": distance_to_closest_food,
      "path_to_tail_exists": dijkstra.path_exists(my_new_tail),
      "flood_score": dijkstra.get_flood_score(),
      "will_eat_food": my_new_snake["head"] in foods
    })

  print("Super evaluator results:")
  for result in results:
    print(result)

  # Evaluate how much space is available
  highest_flood_score = -1
  highest_flood_score_index = 0
  for i, result in enumerate(results):
    if result["flood_score"] > highest_flood_score:
      highest_flood_score = result["flood_score"]
      highest_flood_score_index = i

  # Potential danger, try to move to safety
  if highest_flood_score < 10:
    for result in results:
      if result["path_to_tail_exists"]:
        return result["move"]
    return results[highest_flood_score_index]["move"]

  # Eat food if we can
  for result in results:
    if result["will_eat_food"]:
      return result["move"]

  # Otherwise move towards the closest food
  closest_food = sys.maxsize
  curr_flood_score = 0
  best_move_index = 0
  for i, result in enumerate(results):
    if my_snake["length"] > 10:
      enough_space = math.ceil(0.5 * my_snake["length"])
    else:
      enough_space = math.ceil(0.25 * my_snake["length"])

    if not enough_space and not result["path_to_tail_exists"]:
      continue

    if result["distance_to_closest_food"] < closest_food:
      closest_food = result["distance_to_closest_food"]
      curr_flood_score = result["flood_score"]
      best_move_index = i
    elif result["distance_to_closest_food"] == closest_food and result[
        "flood_score"] > curr_flood_score:
      # If two foods are equidistant, break the tie using flood score
      curr_flood_score = result["flood_score"]
      best_move_index = i

  return results[best_move_index]["move"]


def avoid_body(my_head, body, is_move_safe):
  up = {"x": my_head["x"], "y": my_head["y"] + 1}
  down = {"x": my_head["x"], "y": my_head["y"] - 1}
  right = {"x": my_head["x"] + 1, "y": my_head["y"]}
  left = {"x": my_head["x"] - 1, "y": my_head["y"]}

  if up in body:
    is_move_safe["up"] = False
  if down in body:
    is_move_safe["down"] = False
  if right in body:
    is_move_safe["right"] = False
  if left in body:
    is_move_safe["left"] = False


def avoid_walls(my_head, board_width, board_height, is_move_safe):
  if my_head["x"] == 0:
    is_move_safe["left"] = False
  elif my_head["x"] >= board_width - 1:
    is_move_safe["right"] = False

  if my_head["y"] == 0:
    is_move_safe["down"] = False
  elif my_head["y"] >= board_height - 1:
    is_move_safe["up"] = False


def simple_evaluator(my_snake, my_head, snakes, board_width, board_height):
  is_move_safe = {"up": True, "down": True, "left": True, "right": True}

  avoid_walls(my_head, board_width, board_height, is_move_safe)
  for snake in snakes:
    avoid_body(my_head, snake["body"], is_move_safe)

  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  if len(safe_moves) > 0:
    return safe_moves[0]
  else:
    return "down"
