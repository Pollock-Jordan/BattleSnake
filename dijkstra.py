# Based on code from https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
# Originally by Divyanshu Mehta and Pranav Singh Sambyal
import sys


class Graph():

  def __init__(self, vertices, board_width):
    self.V = vertices
    self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
    self.board_width = board_width

  def print_solution(self, dist):
    print("Dijkstra", end="")
    for node in range(self.V):
      if (node % self.board_width == 0):
        print()

      if dist[node] == sys.maxsize:
        print(f'{"X": <2}', " ", end="")
      else:
        print(f'{dist[node]: <2}', " ", end="")

  def print_prev(self, prev):
    print("prev")
    for x in range(self.board_width):
      for y in range(self.board_width):
        print(f'{"(0,1)": <7}'.format(prev[x][y]["x"], prev[x][y]["y"]),
              end=" ")
      print()

  # A utility function to find the vertex with
  # minimum distance value, from the set of vertices
  # not yet included in shortest path tree
  def min_distance(self, dist, sptSet):
    min = sys.maxsize
    min_index = -1

    # Search for nearest vertex not in the
    # shortest path tree
    for u in range(self.V):
      if dist[u] < min and sptSet[u] == False:
        min = dist[u]
        min_index = u

    return min_index

  def print(self):
    for row in range(self.V):
      print(row, end=' ')
      for col in range(self.V):
        print(self.graph[row][col], end='')
      print("")

  # Function that implements Dijkstra's single source
  # shortest path algorithm using an adjaceny matrix
  def dijkstra(self, src):
    dist = [sys.maxsize] * self.V
    prev = [[-1 for x in range(self.board_width)]
            for y in range(self.board_width)]
    dist[src] = 0
    sptSet = [False] * self.V

    for _ in range(self.V):
      # Pick the minimum distance vertex from
      # the set of vertices not yet processed.
      # x is always equal to src in first iteration
      x = self.min_distance(dist, sptSet)

      # Put the minimum distance vertex in the
      # shortest path tree
      sptSet[x] = True

      # Update dist value of the adjacent vertices
      # of the picked vertex only if the current
      # distance is greater than new distance and
      # the vertex in not in the shortest path tree
      for y in range(self.V):
        if (self.graph[x][y] == sys.maxsize):
          dist[y] = sys.maxsize
        elif self.graph[x][y] > 0 and sptSet[y] == False and \
              dist[y] > dist[x] + self.graph[x][y]:
          dist[y] = dist[x] + 1
          s1 = int_to_coords(y, self.board_width)
          s2 = int_to_coords(x, self.board_width)
          prev[s1["x"]][s1["y"]] = s2

    dist[src] = 0
    self.print_prev(prev)


def int_to_coords(num, board_width):
  if num < board_width:
    x = num
    y = 0
  else:
    x = num % board_width
    y = num // board_width

  return {'x': x, 'y': y}


def coords_to_int(coords, board_width):
  x = coords['x']
  y = coords['y']

  return x + board_width * y


# Generates an Adjacency Matrix for a square board
def generate_graph(my_head, board_width, foods, snakes):
  num_vertices = board_width * board_width
  graph = Graph(num_vertices, board_width)

  for vertex in range(num_vertices):
    if (vertex + 1 < num_vertices):
      graph.graph[vertex][vertex + 1] = 1
    if (vertex % board_width != 0):
      graph.graph[vertex][vertex - 1] = 1
    if (vertex + board_width < num_vertices):
      graph.graph[vertex][vertex + board_width] = 1
    if (vertex - board_width >= 0):
      graph.graph[vertex][vertex - board_width] = 1

    for snake in snakes:
      if int_to_coords(vertex + 1, board_width) in snake['body']:
        graph.graph[vertex][vertex + 1] = sys.maxsize
      if int_to_coords(vertex - 1, board_width) in snake['body']:
        graph.graph[vertex][vertex - 1] = sys.maxsize
      if int_to_coords(vertex + board_width, board_width) in snake['body']:
        graph.graph[vertex][vertex + board_width] = sys.maxsize
      if int_to_coords(vertex - board_width, board_width) in snake['body']:
        graph.graph[vertex][vertex - board_width] = sys.maxsize

  graph.graph[my_head["x"]][my_head["y"]] = 0

  return graph
