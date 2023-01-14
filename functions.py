import sys
from copy import deepcopy
from dijkstra2 import DijkstraHelper


def get_new_snake_given_move(snake, move, foods):
  new_head = get_new_head_given_move(snake[0], move)
  will_eat_food = new_head in foods
  snake.insert(0, new_head)

  if not will_eat_food:
    snake.pop()

  return snake


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


def super_evaluator(safe_moves, my_snake, opponents, foods, height, width):
  results = []
  for move in safe_moves:
    my_new_snake = deepcopy(my_snake)
    my_new_snake["body"] = get_new_snake_given_move(my_snake["body"], move, foods)
    my_new_tail = my_new_snake["body"][-1]
    snakes = [my_new_snake] + opponents

    dijkstra = DijkstraHelper(my_new_snake, snakes, height, width)
    closest_food = dijkstra.get_closest_food(foods)

    if closest_food is None:
      distance_to_closest_food = sys.maxsize
    else:
      distance_to_closest_food = dijkstra.distance_to(closest_food)

    results.append({
      "move": move,
      "distance_to_closest_food": distance_to_closest_food,
      "path_to_tail_exists": dijkstra.path_exists(my_new_tail),
      "flood_score": dijkstra.get_flood_score()
    })

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
        print("flood score low -- going to tail")
        return result["move"]
    print("flood score low -- going to largest space")
    return results[highest_flood_score_index]["move"]

  # Go to the closest food
  closest_food = sys.maxsize
  closest_food_index = 0
  for i, result in enumerate(results):
    if result["distance_to_closest_food"] < closest_food:
      closest_food = result["distance_to_closest_food"]
      closest_food_index = i

  return results[closest_food_index]["move"]
