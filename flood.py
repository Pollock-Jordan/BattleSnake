#used python function from: https://plainenglish.io/blog/a-python-example-of-the-flood-fill-algorithm-bced7f96f569


class FloodBoard():

  def __init__(self, snakes, width, height):
    #create a width*height board of all 0s
    self.board = [[0 for x in range(width)] for y in range(height)]
    self.snakes = snakes
    self.width = width
    self.height = height

    #add all the snakes
    for snake in snakes:
      #make each section of the body a 6
      for section in snake["body"]:
        x = section["x"]
        y = section["y"]
        self.board[x][y] = 6

    #add danger spots beside heads of opponents
    for i in range(1, (len(snakes) - 1)):
      head_x = snakes[i][0]["x"]
      head_y = snakes[i][0]["y"]

      if (head_x + 1) < (width - 1):
        self.board[head_x + 1][head_y] = 6
      if (head_x - 1) > -1:
        self.board[head_x - 1][head_y] = 6
      if (head_y + 1) < (height - 1):
        self.board[head_x][head_y + 1] = 6
      if (head_y - 1) > -1:
        self.board[head_x][head_y - 1] = 6

  #this will be called on a move to make sure the move is safe w.r.t getting stuck
  def make_assessment(self, move):
    head_x = self.snakes[0]["head"]["x"]
    head_y = self.snakes[0]["head"]["y"]

    tail_x = self.snakes[0]["body"][-1]["x"]
    tail_y = self.snakes[0]["body"][-1]["y"]

    if move == "right":
      head_x = head_x + 1
    elif move == "left":
      head_x = head_x - 1
    elif move == "up":
      head_y = head_y + 1
    elif move == "down":
      head_y = head_y - 1

    new_position = {"x": head_x, "y": head_y}

    self.board[tail_x][tail_y] = 0

    old = 0
    new = 1
    self.flood_fill(head_x, head_y, old, new)

    #total count
    count = 0
    for row in self.board:
      for item in row:
        if item == 1:
          count += 1

    return count

  def flood_fill(self, x, y, old, new):
    # firstly, make sure the x and y are inbounds
    if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0]):
      return
    # secondly, check if the current position equals the old value
    if self.board[x][y] != old:
      return
    # thirdly, set the current position to the new value
    self.board[x][y] = new

    # fourthly, attempt to fill the neighboring positions
    self.flood_fill(x + 1, y, old, new)
    self.flood_fill(x - 1, y, old, new)
    self.flood_fill(x, y + 1, old, new)
    self.flood_fill(x, y - 1, old, new)

  def print(self):
    for x in range(self.width):
      for y in range(self.height):
        print(f'{self.board["x"]["y"]:<2}')
      print()
