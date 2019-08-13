from collections import namedtuple

Point = namedtuple('Point', 'x y')
p1 = Point(2, 3)
p2 = Point(5, 7)
p3 = Point(7, 6)
p4 = Point(10, 10)
p5 = Point(4, 5)
p6 = Point(12, 8)

WIDTH = 16
HEIGHT = 16


class Canvas:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.buffer = list(' ' * self.width * self.height)

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.buffer[j + i * self.height], end='')
            print()

    def paint_dot(self, x, y):
        self.buffer[x + y * self.height] = '*'

    def paint_row(self, row, num):
        for i in range(self.width):
            self.buffer[i + num * self.height] = row[i]


def rect(p1, p2, cnv):
    w = abs(p1.x - p2.x)
    h = abs(p1.y - p2.y)
    for j in range(h):
        for i in range(w):
            cnv.paint_dot(i + p1.x, j + p1.y)


def rect_no_fill(p1, p2, cnv):
    w = abs(p1.x - p2.x)
    h = abs(p1.y - p2.y)
    for j in range(h):
        for i in range(w):
            if j == 0 or j == h-1:
                cnv.paint_dot(i + p1.x, j + p1.y)
            elif i == 0 or i == w-1:
                cnv.paint_dot(i + p1.x, j + p1.y)
            else:
                continue


canvas = Canvas(WIDTH, HEIGHT)
rect(p1, p2, canvas)
canvas.show()
print('=' * WIDTH)
rect(p3, p4, canvas)
canvas.show()
print('=' * WIDTH)
rect_no_fill(p5, p6, canvas)
canvas.show()