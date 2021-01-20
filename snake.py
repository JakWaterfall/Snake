import random
import time


class Snake:
    """Snake Class"""
    def __init__(self, canvas, screenWidth, screenHeight, tileSize, gameOver):
        self.canvas = canvas
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileSize = tileSize
        self.gameOver = gameOver
        self.__xVel = self.tileSize
        self.__yVel = 0
        self.__score = 0
        self.__bodys = []
        self.__hasMoved = False
        # add two elements to the snake body.
        self.addBody()
        self.addBody()

    @property
    def score(self):
        """Getter for score. Returns the score as an int."""
        return self.__score

    @property
    def bodys(self):
        """Getter for snake body. Returns list of elements that makes up the snake."""
        return self.__bodys

    def addScore(self):
        """Increments the score by one."""
        self.__score += 1

    def addBody(self):
        """Adds an element to the snake's body / Increases the snake's size by 1."""
        self.__bodys.insert(1, Element(80000, 80000, self.tileSize))

    def draw(self):
        """Draws the snake to screen."""
        colourNum = 901000
        for body in self.__bodys:
            # Adds 100 to the Hex RGB value to cause a colour gradient from red to yellow as the snake gets larger
            colourNum += 100
            fillHex = str(colourNum)
            # Makes the tail of the snake invisible so that you may start with 2 elements of the snake to move
            if body == self.__bodys[-1]:
                continue
            self.canvas.create_rectangle(body.x1, body.y1, body.x2, body.y2, fill="#" + fillHex)

    def tick(self):
        """Updates the snakes position by removing the tail and adding it to where the head should be."""
        head = self.__bodys.pop(-1)
        head.x1 = self.__bodys[0].x1 + self.__xVel
        head.y1 = self.__bodys[0].y1 + self.__yVel
        head.x2 = self.__bodys[0].x2 + self.__xVel
        head.y2 = self.__bodys[0].y2 + self.__yVel
        self.__bodys.insert(0, head)

        self.__hasMoved = False  # Flag to force only one input per tick to stop button mashing
        self.__wallCheck()

    def __wallCheck(self):
        """Checks if the snake has hit the wall and moves the snake to the corresponding position on the over side."""
        W = self.screenWidth
        H = self.screenHeight
        TS = self.tileSize
        # RIGHT SIDE
        if self.__bodys[0].x2 > W:
            self.__bodys[0].x1 = 0
            self.__bodys[0].x2 = TS
        # LEFT SIDE
        if self.__bodys[0].x1 < 0:
            self.__bodys[0].x1 = (W - TS)
            self.__bodys[0].x2 = W
        # TOP SIDE
        if self.__bodys[0].y1 < 0:
            self.__bodys[0].y1 = (H - TS)
            self.__bodys[0].y2 = H
        # BOTTOM SIDE
        if self.__bodys[0].y2 > H:
            self.__bodys[0].y1 = 0
            self.__bodys[0].y2 = TS

    def hitSelfCheck(self):
        """Checks if snake has hit itself and returns flag to end the game."""
        i = 1
        # len -1 so that the head cannot collide with the invisible tail
        while i < len(self.__bodys) - 1:
            if self.__bodys[0].x1 == self.__bodys[i].x1 and self.__bodys[0].y1 == self.__bodys[i].y1:
                self.__xVel = 0
                self.__yVel = 0
                return True
            i = i + 1
        return False

    def leftKey(self, event):
        """Turns snake left if moving on vertical plane."""
        if self.__hasMoved:  # Flag to force only one input per tick to stop button mashing
            return
        else:
            self.__hasMoved = True
        if self.__yVel != 0:  # Checks snake is moving vertically
            self.__yVel = 0
            self.__xVel = -self.tileSize

    def rightKey(self, event):
        """Turns snake right if moving on vertical plane."""
        if self.__hasMoved:  # Flag to force only one input per tick to stop button mashing
            return
        else:
            self.__hasMoved = True
        if self.__yVel != 0:  # Checks snake is moving vertically
            self.__yVel = 0
            self.__xVel = self.tileSize

    def upKey(self, event):
        """Turns snake up if moving on horizontal plane."""
        if self.__hasMoved:  # Flag to force only one input per tick to stop button mashing
            return
        else:
            self.__hasMoved = True
        if self.__xVel != 0:  # Checks snake is moving horizontally
            self.__xVel = 0
            self.__yVel = -self.tileSize

    def downKey(self, event):
        """Turns snake down if moving on horizontal plane."""
        if self.__hasMoved:  # Flag to force only one input per tick to stop button mashing
            return
        else:
            self.__hasMoved = True
        if self.__xVel != 0:  # Checks snake is moving horizontally
            self.__xVel = 0
            self.__yVel = self.tileSize

    def spaceKey(self, event):
        """Space keyboard Key Debug to add Elements of snake body."""
        self.addBody()


class Element:
    """Element data structure for snake and food body."""
    def __init__(self, x1, y1, tileSize):
        self.x1 = x1
        self.x2 = x1 + tileSize
        self.y1 = y1
        self.y2 = y1 + tileSize


class Food:
    """Food Class"""
    def __init__(self, canvas, width, height, tileSize, snake):
        self.__food = None
        self.canvas = canvas
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.snake = snake
        self.addFood()

    def addFood(self):
        """Adds food to a random location on screen within the tile bounds and not within the snake."""
        x = random.randint(0, (self.width / self.tileSize) - 1) * self.tileSize
        y = random.randint(0, (self.height / self.tileSize) - 1) * self.tileSize
        self.__food = Element(x, y, self.tileSize)
        for body in self.snake.bodys:
            if x == body.x1 and y == body.y1:
                try:
                    self.addFood()
                except RecursionError:
                    print("Screen Full")  # DEBUG MESSAGE
                    global gameOver
                    gameOver = True  # Forces game over if screen is full

    def drawFood(self):
        """Draws food to the screen."""
        if self.__food is None:
            return
        self.canvas.create_oval(self.__food.x1, self.__food.y1, self.__food.x2, self.__food.y2, fill="blue")

    def foodCheck(self, tickRate):
        """Checks if the snake ate the food and speeds up the snake if it did."""
        if self.__food.x1 == self.snake.bodys[0].x1 and self.__food.y1 == self.snake.bodys[0].y1:
            self.addFood()
            self.snake.addScore()
            self.snake.addBody()
            if tickRate > 0.001:
                tickRate -= 0.001
                return tickRate
        return tickRate


def play(root, canvas, tileSize, width, height):
    """Starts the gameplay loop of snake."""
    # Variables
    tickRate = 0.05
    gameOver = False

    # Instantiates Snake, food and binds controls
    snake = Snake(canvas, width, height, tileSize, gameOver)
    food = Food(canvas, width, height, tileSize, snake)
    root.bind('<Left>', snake.leftKey)
    root.bind('<Right>', snake.rightKey)
    root.bind('<Up>', snake.upKey)
    root.bind('<Down>', snake.downKey)
    root.bind('<space>', snake.spaceKey)

    # Game loop
    while not gameOver:
        snake.tick()
        gameOver = snake.hitSelfCheck()
        snake.draw()
        tickRate = food.foodCheck(tickRate)
        food.drawFood()
        canvas.create_text((width / 2), 20, fill="black", font="Times 15", text="Score: " + str(snake.score))
        root.update_idletasks()
        root.update()
        canvas.delete("all")
        time.sleep(tickRate)

    return snake.score
