import sys
from queue import PriorityQueue, SimpleQueue
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
  # https://docs.python.org/3/library/queue.html#queue.PriorityQueue
  priority: int
  item: Any = field(compare=False)


class DijkstraHelper:

  def __init__(self, my_snake, snakes, height, width):
    self.my_snake_id = my_snake["id"]
    self.my_head = my_snake["head"]
    self.my_body = my_snake["body"]
    self.my_tail = my_snake["body"][-1]
    self.snakes = snakes
    self.height = height
    self.width = width

    self.graph = self.__create_graph()
    self.dist, self.paths = self.__dijkstra()

  def find_move_to_closest_food(self, foods):
    if len(foods) == 0:
      return None

    closest = foods[0]
    for food in foods:
      closest_dist = self.distance_to(closest)
      curr_dist = self.distance_to(food)

      if curr_dist < closest_dist:
        closest = food

    if not self.path_exists(closest):
      # Should only happen if no food is reachable
      return None

    return self.get_next_move_towards(closest)

  def path_exists(self, dest):
    return self.paths[dest["y"]][dest["x"]] is not None

  def get_next_move_towards(self, dest):
    # Only call this method is path_exists() == True
    next = dest
    temp = self.paths[next["y"]][next["x"]]

    while temp != self.my_head and temp is not None:
      next = temp
      temp = self.paths[next["y"]][next["x"]]

    # Paths go from dest -> src, so to go from src -> dest
    # we need to follow the path in reverse
    if self.my_head["y"] > next["y"]:
      return "down"

    if self.my_head["y"] < next["y"]:
      return "up"

    if self.my_head["x"] > next["x"]:
      return "left"

    if self.my_head["x"] < next["x"]:
      return "right"

    # Should never happen
    return None

  def distance_to(self, point):
    return self.dist[point["y"]][point["x"]]

  def get_safe_moves(self):
    safe_moves = []
    open_spaces = self.__get_neighbours(self.my_head, self.graph)

    for space in open_spaces:
      if self.my_head["y"] > space["y"]:
        safe_moves.append("down")
      elif self.my_head["y"] < space["y"]:
        safe_moves.append("up")
      elif self.my_head["x"] > space["x"]:
        safe_moves.append("left")
      elif self.my_head["x"] < space["x"]:
        safe_moves.append("right")

    return safe_moves

  def flood_fill(self, node):
    visited = []
    vertices = SimpleQueue()
    vertices.put(node)

    count = 0
    while not vertices.empty():
      curr = vertices.get()

      if self.path_exists(curr):
        count = count + 1
        visited.append(curr)
        neighbours = self.__get_neighbours(curr)

        for neighbour in neighbours:
          if neighbour not in visited:
            vertices.put(neighbour)

    return count

  def two_areas_exist(self, safe_spaces):
    if len(safe_spaces) != 2:
      return False
    
    # Up and down are open, left and right are blocked
    if "up" in safe_spaces and "down" in safe_spaces:
      return True
    
    # Left and right are open, up and down are blocked
    if "left" in safe_spaces and "right" in safe_spaces:
      return True

    return False

  def three_areas_exist(self, safe_spaces):
    if len(safe_spaces) != 3:
      return False

    last_move = self.my_body[1]
    

  def __create_graph(self):
    graph = [["O" for row in range(self.height)] for col in range(self.width)]

    for snake in self.snakes:
      for section in snake["body"]:
        row = section["y"]
        col = section["x"]
        graph[row][col] = "X"

    # Mark all potential enemy moves as dangerous
    for snake in self.snakes:
      if snake["id"] == self.my_snake_id:
        continue

      enemy_head = snake["head"]
      enemy_head_neighbours = self.__get_neighbours(enemy_head, graph)

      for neighbour in enemy_head_neighbours:
        row = neighbour["y"]
        col = neighbour["x"]
        graph[row][col] = "X"

    my_head_row = self.my_head["y"]
    my_head_col = self.my_head["x"]
    graph[my_head_row][my_head_col] = "H"

    my_tail_row = self.my_tail["y"]
    my_tail_col = self.my_tail["x"]
    graph[my_tail_row][my_tail_col] = "O"

    return graph

  def __dijkstra(self):
    dist = [[sys.maxsize for row in range(self.height)] for col in range(self.width)]
    paths = [[None for row in range(self.height)] for col in range(self.width)]

    dist[self.my_head["y"]][self.my_head["x"]] = 0
    paths[self.my_head["y"]][self.my_head["x"]] = "H"

    vertices = PriorityQueue()
    vertices.put(PrioritizedItem(0, self.my_head))

    while not vertices.empty():
      prioritized_item = vertices.get()
      min_dist = prioritized_item.priority
      min = prioritized_item.item

      neighbours = self.__get_neighbours(min, self.graph)

      for neighbour in neighbours:
        neighbour_dist = dist[neighbour["y"]][neighbour["x"]]

        if neighbour_dist > min_dist + 1:
          dist[neighbour["y"]][neighbour["x"]] = min_dist + 1
          paths[neighbour["y"]][neighbour["x"]] = min
          vertices.put(PrioritizedItem(min_dist + 1, neighbour))

    return dist, paths

  def __get_neighbours(self, node, graph):
    neighbours = []

    # Up
    if node["y"] < self.height - 1 and graph[node["y"] + 1][node["x"]] == "O":
      neighbours.append({"x": node["x"], "y": node["y"] + 1})

    # Down
    if node["y"] > 0 and graph[node["y"] - 1][node["x"]] == "O":
      neighbours.append({"x": node["x"], "y": node["y"] - 1})

    # Right
    if node["x"] < self.width - 1 and graph[node["y"]][node["x"] + 1] == "O":
      neighbours.append({"x": node["x"] + 1, "y": node["y"]})

    # Left
    if node["x"] > 0 and graph[node["y"]][node["x"] - 1] == "O":
      neighbours.append({"x": node["x"] - 1, "y": node["y"]})

    return neighbours

  def print_distances(self):
    print()
    for row in reversed(range(self.height)):
      for col in range(self.width):
        if self.dist[row][col] == sys.maxsize:
          print(f'{"X": <2}', end=" ")
        else:
          print(f'{self.dist[row][col]: <2}', end=" ")
      print()
    print()

  def print_paths(self):
    print()
    for row in reversed(range(self.height)):
      for col in range(self.width):
        if self.paths[row][col] is None:
          print("█████", end=" ")
        elif self.paths[row][col] == "H":
          print("HHHHH", end=" ")
        else:
          next = self.paths[row][col]
          print("({},{})".format(next["x"], next["y"]), end=" ")
      print()
    print()
