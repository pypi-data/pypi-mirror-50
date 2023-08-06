"""
planefigures is a python package based on the turtle library.
It takes the pain out of drawing plain shapes.

Example

    import figures
    import turtle

    figures.color('red','yellow')

    figures.begin_fill()

    for n in range(8):
        figures.polygon(8, 80)
        turtle.right(360/8)

    figures.end_fill()

Functions

    polygon(sides:int, length:int) -- Draw a regular polygon of given sides with each side of given length.
    rectangle(length:int, breadth:int) -- Draw a rectangle of given length and breadth.
    circle(radius, extent=None, steps=None) -- Draw a circle of given radius. This function works exactly like turtle.circle().
    color(*args) -- Return or set pencolor and fillcolor. This function works exactly like turtle.color().
    begin_fill() -- To be called just before drawing a shape to be filled.
    end_fill() -- Fill the shape drawn after the last call to begin_fill().
"""

import turtle
import math

def polygon(sides:int, length:int):
    """Draw a regular polygon of given sides with each side of given length.
    
    Arguments:
        sides {int} -- The number of sides of the polygon
        length {int} -- The length of each side of the polygon in pixels
    """
    
    # Make sure the arguments are of type int
    if not isinstance(sides, int):
        raise TypeError('Please provide an int argument')
    if not isinstance(length, int):
        raise TypeError('Please provide an int argument')
    
    # (sides - 2) * 180 -- defines sum of angles in any polygon
    angle = ((sides - 2) * 180) / sides

    for x in range(sides):
        turtle.forward(length)
        turtle.left(180 - angle)
        

def rectangle(length:int, breadth:int):
    """Draw a rectangle of given length and breadth.
    
    Arguments:
        length {int} -- The length of the quadrilateral in pixels
        breadth {int} -- The breadth of the quadrilateral in pixels
    """
    
    # Make sure the arguments are of type int
    if not isinstance(length, int):
        raise TypeError('Please provide an int argument')
    if not isinstance(breadth, int):
        raise TypeError('Please provide an int argument')
    
    for x in range(2):
        turtle.forward(length)
        turtle.right(90)
        turtle.forward(breadth)
        turtle.right(90)


def parallelogram(length:int, breadth:int, angle:float):
    """Draw a parallelogram of given length and breadth and a given pair of opposite angle
    
    Arguments:
        length {int} -- The length of the parallelogram
        breadth {int} -- The breadth of the parallelogram
        angle {float} -- A pair of opposite angles
    """
    
    # Make sure the arguments are of the right type
    if not isinstance(length, int):
        raise TypeError('Please provide an int argument')
    if not isinstance(breadth, int):
        raise TypeError('Please provide an int argument')
    if not isinstance(angle, float) or not isinstance(angle, int):
        raise TypeError('Please provide a float argument')
    
    turtle.forward(length)
    turtle.left(angle)
    turtle.forward(breadth)
    turtle.left(180-angle)
    turtle.forward(length)
    turtle.left(angle)
    turtle.forward(breadth)
    turtle.left(180-angle)


def righttriangle(a=None, b=None, c=None):
    """Draw a right-angle triangle.
    You can provide just two sides out of three or all three sides.
    
    Keyword Arguments:
        a {float} -- the vertical side (default: {None})
        b {float} -- the horizontal side (default: {None})
        c {float} -- the hypotenus (default: {None})
    """
    
    # Calculate  the third side from the two given sides
    if a and b and not c:
        c = math.hypot(a,b)
    elif a and c and not b:
        b = math.sqrt(c**c - a**a)
    elif b and c and not a:
        a = math.sqrt(c**c - b**b)
    elif a and b and c:
        # Make sure the hypotenus c is the longest side
        try:
            assert math.hypot(a,b) is c
        except AssertionError:
            text = 'The three given sides do not satisfy the Pythagorean theorem.'
    else:
        return print('You must provide at least two out of the three sides.')
    
    # Calculate angle A opposite side a
    x = math.degrees(math.asin(a/c))

    turtle.forward(b)
    turtle.left(180-x)
    turtle.forward(c)
    turtle.left(90+x)
    turtle.forward(a)
    turtle.left(90)

    if text:
        turtle.penup()
        # Print the text below the diagram
        # Use c since it's the highest value of the diagram
        turtle.goto(0,c+10)
        turtle.write(text, align="center", font=("Arial",12,"bold"))
        turtle.home()
        turtle.pendown()