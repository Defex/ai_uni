#IFF 4/1 Lukas Vanagas

import os
import operator
import math

INPUT_PATH = os.path.join(os.getcwd(), 'input.txt')

def read_file(file_name):
    with open(file_name) as f:
        return f.read()

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.dx = float(x)
        self.dy = float(y)
        self.distance = 0

    def get_distance(self, x1, y1):
        self.distance = math.hypot(self.x - x1, self.y - y1)

    def __str__(self):
        return 'x: {}, y: {}'.format(self.x, self.y)

    def __repr__(self):
        return 'x: {} y: {} distance: {}'.format(self.x, self.y, self.distance)

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

class SunnyMountains:
    def __init__(self):
        self.points = []
    @staticmethod
    def get_data(text):
        data = []
        lines = text.splitlines()
        test_cases = int(lines[0])
        lines = lines[1:]
        for x in range(0, test_cases):
            rows = int(lines[0])
            data.append([xx.strip() for xx in lines[1:rows+1]])
            lines = lines[rows+1:]
        return data

    def get_points(self, points_data):
        for line in points_data:
            point = line.split()
            self.points.append(Point(point[0], point[1]))

    def sort_points(self):
        self.points.sort(key=operator.attrgetter('x'))

    def remove_lower_points(self):
        r_points = reversed(self.points[:-1])
        filtered_points = []
        compare_point = self.points[-1]
        filtered_points.append(compare_point)
        for point in r_points:
            if point > compare_point:
                filtered_points.append(point)
                compare_point = point
        self.points = filtered_points

    def calc_each_point(self):
        prev_point = self.points[0]
        for point in self.points[1:]:
            point.get_distance(prev_point.x, prev_point.y)
            prev_point = point

    def get_total_length(self):
        return sum(point.distance for point in self.points)

if __name__ == '__main__':
    data = SunnyMountains.get_data(read_file(INPUT_PATH))
    for item in data:
        sm = SunnyMountains()
        sm.get_points(item)
        sm.sort_points()
        sm.remove_lower_points()
        sm.calc_each_point()
        # print(sm.points)
        print(sm.get_total_length())
    # print(data)
