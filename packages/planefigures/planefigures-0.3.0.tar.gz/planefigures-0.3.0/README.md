# planefigures
`planefigures` is a python package based on the [turtle library](https://docs.python.org/3.5/library/turtle.html). It takes the pain out of drawing plain shapes.

## Installation
```bash
pip install planefigures
```
Python 3 is supported.

## Example
Try out this little peace of code and be amazed.
```python
import planefigures as figures
import turtle

figures.color('red','yellow')

figures.begin_fill()

for n in range(8):
    figures.polygon(8, 80)
    turtle.right(360/8)

figures.end_fill()
```

Or better still ...
```python
python -m planefigures.example
```
and enjoy.

## Road map
At this stage, only [regular polygons](https://en.wikipedia.org/wiki/Regular_polygon) are supported. The aim however, is to support regular as well as irregular shapes.

- [x] Circle
- [ ] Scalene triangle
- [ ] Isosceles triangle
- [x] Right triangle
- [ ] Obtuse triangle
- [x] Rectangle
- [x] Parallelogram
- [ ] Trapezium
