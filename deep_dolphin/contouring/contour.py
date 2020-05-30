import os

class Contour(object):

    def __init__(self, points=[]):
        self.points = points

    def __repr__(self):
        return str(self.points)

    def __str__(self):
        return str(self.points)

    def first_point(self):
        if len(self.points) > 0:
            return self.points[0]
        else:
            return None

    def last_point(self):
        if len(self.points) > 1:
            return self.points[-1]
        else:
            return None

    def previous_point(self):
        if len(self.points) > 1:
            return self.points[-2]
        else:
            return None

    def add(self, point):
        self.points.append(point)
        return self


if __name__ == '__main__':
    a = Contour()
    print(a.first_point())
    print(a.last_point())
    print(a.previous_point())
    print(a.add((1, 1)))
