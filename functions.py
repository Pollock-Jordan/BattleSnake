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
  if my_head["x"] > (board_width - 2):
    print("right edge detected")
    is_move_safe["right"] = False
  if my_head["x"] < 1:
    print("left edge detected")
    is_move_safe["left"] = False
  if my_head["y"] > (board_height - 2):
    print("top edge detected")
    is_move_safe["up"] = False
  if my_head["y"] < 1:
    is_move_safe["down"] = False

