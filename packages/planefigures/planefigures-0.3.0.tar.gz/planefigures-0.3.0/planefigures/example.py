import turtle
import planefigures as figures

import random

def triangle():
    figures.polygon(3,200)

def square():
    figures.polygon(4,200)

def rectangle():
    figures.rectangle(200,150)

def hexagon():
    figures.polygon(6,100)

def circle():
    figures.circle(100)

shapes = [triangle, square, rectangle, hexagon, circle]
colors = ['red','orange','yellow','green','blue','indigo','violet']

screen = turtle.Screen()
screen.screensize(800,800)

turtle.title('Planefigures - @OthnielDona') # - shown in the titlebar of the turtle graphics window
turtle.shape('turtle')
turtle.fillcolor('pink')
turtle.pensize(3)

# Number of figures to be drawn
n = 10

turtle.begin_fill()
for i in range(n):
    # Choose a random color from the list of colors
    color = random.choice(colors)
    # Choose a random shape from the list shapes
    shape = random.choice(shapes)

    turtle.pencolor(color)
    shape() # - draw the selected shape
    turtle.right(360/n)
turtle.end_fill()

turtle.exitonclick()