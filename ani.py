
import turtle
import time
import math

screen = turtle.Screen()
screen.title("Walking Dog Animation")
screen.bgcolor("lightblue")
screen.setup(800, 500)
screen.tracer(0)

dog = turtle.Turtle()
dog.speed(0)
dog.shape("circle")
dog.color("saddlebrown")
dog.penup()

# Draw the dog
def draw_dog(x, leg_angle):
    dog.clear()
    dog.goto(x, -40)

    # Body
    dog.color("saddlebrown")
    dog.dot(100)

    # Head
    dog.goto(x + 65, 15)
    dog.dot(65)

    # Ears
    dog.goto(x + 45, 45)
    dog.dot(25)

    # Eyes
    dog.color("black")
    dog.goto(x + 78, 25)
    dog.dot(6)

    # Nose
    dog.goto(x + 95, 5)
    dog.dot(10)

    # Legs
    dog.color("saddlebrown")
    for offset in [-30, 10]:
        dog.goto(x + offset, -85)
        dog.setheading(leg_angle)
        dog.pendown()
        dog.pensize(9)
        dog.forward(30)
        dog.penup()

    # Tail
    dog.goto(x - 45, -20)
    dog.setheading(150 + leg_angle)
    dog.pensize(8)
    dog.pendown()
    dog.forward(35)
    dog.penup()

# Animation loop
x = -350
frame = 0

while True:
    angle = 25 * math.sin(frame * 0.3)
    draw_dog(x, angle)

    screen.update()

    x += 5
    if x > 350:
        x = -350

    frame += 1
    time.sleep(0.04)
