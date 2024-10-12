from email.header import SPACE
from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "#C0A9BD"
FOOD_COLOUR = "#FF0000"
BACKGROUND_COLOUR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x +SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOUR, tag = "snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1)* SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE))-1 ) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOUR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0] # head of snake

    #adjust coords according to the direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x-= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #Insert the new snake
    snake.coordinates.insert(0, (x, y))

    #Create the new snake
    square = canvas.create_rectangle(x,y, x+SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOUR)

    #add the new snake to the already existing snake
    snake.squares.insert(0, square)

    #Check if head of snake is at the food coordinate
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score +=1
        #Change score
        label.config(text="Score:{}".format(score))

        canvas.delete("food")
        food = Food()
    else:
        #Delete the end of the snake
        #Appears it is now moving
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]
    if check_Collissions(snake):
        game_over()
    else:
        #Keep calling itself
        window.after(SPEED, next_turn, snake, food)
def change_Direction(new_direction):
    #Make direction a global variable
    global direction

    if new_direction == 'left':
        if direction != 'right':#Dont want 180 turn as mess with snake tail
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':#Dont want 180 turn as mess with snake tail
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':#Dont want 180 turn as mess with snake tail
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':#Dont want 180 turn as mess with snake tail
            direction = new_direction
def check_Collissions(snake):
    #Get coordinates of the snakes head
    x, y = snake.coordinates[0]

    #Check if snake head is past game borders
    if x < 0 or x>= GAME_WIDTH:
        return True
    elif y <0 or y>= GAME_HEIGHT:
        return True
    #check if body part collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False
def game_over():
    #Delete things
    canvas.delete(ALL)
    #Create the words game over.
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ('consolas', 70), text = "GAME OVER", fill ="red", tag = 'gameover')

window = Tk()
window.title("Snek game")
#window.resizable(False, False)
score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font = ('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#CONTROLS
window.bind('<Left>', lambda event: change_Direction('left'))
window.bind('<Right>', lambda event: change_Direction('right'))
window.bind('<Up>', lambda event: change_Direction('up'))
window.bind('<Down>', lambda event: change_Direction('down'))

snake = Snake()
food = Food()

next_turn(snake,food)
window.mainloop()