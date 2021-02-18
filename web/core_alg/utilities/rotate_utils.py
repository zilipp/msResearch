import math


def rotate(point, degree):
    rad = math.radians(degree)
    x = point[0]
    y = point[1]
    new_x = math.cos(rad)*x - math.sin(rad)*y
    new_y = math.sin(rad)*x + math.cos(rad)*y
    return [new_x, new_y]