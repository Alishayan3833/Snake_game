# -------------------------------------------- module ----------------------------------------------

from tkinter import *
from random import randint
import os
import sys

# -------------------------------------------- classes -----------------------------------------


class Snake:
    """
    This class is defined for the body of the snake and has attributes and methods
    """
    def __init__(self):
        """
        Body size determines the initial value of the snake at the start of the game, which is fixed = 2
        squares and coordinates store the coordinates of the snake.
        """
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for _ in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=COLOR_SNAKE)
            self.squares.append(square)

class Food:
    def __init__(self):
        """
        This class is for food, which is selected from the canvas method, circle option, you can also use rectangle
        """
        x = randint(0, (GAME_WIDTH // SPACE_SIZE)-1)*SPACE_SIZE
        y = randint(0, (GAME_HEIGHT // SPACE_SIZE)-1)*SPACE_SIZE
        self.coordinates = [x, y]
        square = canvas.create_oval(
            x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=COLOR_FOOD, tags="food")


# -------------------------------------------- functions -------------------------------------------


def next_turn(snake, food):
    """
    Direction keys are defined in this function
    """
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(
        x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=COLOR_SNAKE)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        """
        The condition causes that if the food is eaten, it will be erased and appear somewhere else, and the lunch points will be added
        """
        global score
        score += 10
        label.config(text=f"score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_game_over(snake):
        game_over()
    else:
        window.after(slowness, next_turn, snake, food)


def check_game_over(snake):
    """
    As its name suggests, this function checks when the player loses
    """
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        """
        The condition causes the game to stop if the player collides with the walls
        """
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for sq in snake.coordinates[1:]:
        """
        This for checks the collision of the snake's head with its own body or tail
        """
        if x == sq[0] and y == sq[1]:
            return True

    return False


def game_over():
    """
    If you lose, this function will stop the game and game over!!! prints the
    """
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2,
                       canvas.winfo_height() / 2, font=("terminal", 30), text="GAME OVER!!!", fill="red", tags="gameover")


def change_direction(new_dir):
    """
    The direction of the snake's movement is determined
    """
    global direction

    if new_dir == "left":
        if direction != "right":
            direction = new_dir
    elif new_dir == "right":
        if direction != "left":
            direction = new_dir
    elif new_dir == "up":
        if direction != "down":
            direction = new_dir
    elif new_dir == "down":
        if direction != "up":
            direction = new_dir


def restart_program():
    """
    The os and sys packages are only used here.
    """
    path = sys.executable
    os.execl(path, path, *sys.argv)


# -------------------------------------------- varibles ----------------------------------------------

slowness = input("please enter speed game:(10-900)")
BODY_SIZE = 2
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 30
COLOR_SNAKE = "blue"
COLOR_FOOD = "red"
BACKGROUND_COLOR = "black"
score = 0
direction = "down"

# ------------------------------------------ designed ---------------------------------------------

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"score:{score}", font=("Courier", 25))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR,
                height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

restart = Button(window, text="RESTART", fg="red", command=restart_program)
restart.pack()

window.update()

# ------------------------------------------ geometry -------------------------------------------

"""
In geometry, the opening location of the game screen is determined and fixed
"""

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

w = int((screen_width/2)-(window_width/2))

window.geometry(f"{window_width}x{window_height}+{w}+{100}")

# ------------------------------------------- snake ----------------------------------------------

snake = Snake()

# ------------------------------------------- Food -----------------------------------------------

food = Food()

# ------------------------------------------- move ----------------------------------------------

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# ------------------------------------------ shift ---------------------------------------------

next_turn(snake, food)

# ---------------------------------------------------------------------------------------------


window.mainloop()
