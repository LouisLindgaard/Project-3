import math
import random

import numpy as np

np.set_printoptions(suppress=True)

def orientationTest(p1, p2, p3):
    # p1, p2, p3 are points in the form of (x, y)
    # returns 1 if p1, p2, p3 are counterclockwise
    # returns 0 if p1, p2, p3 are collinear
    # returns -1 if p1, p2, p3 are clockwise
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return -1


def INC_CH(points):
    #Graham scan
    pointsByX = sorted(points, key=lambda x: x[0])

    upperHull = []
    upperHull.append(pointsByX[0])
    upperHull.append(pointsByX[1])
    for i in range(2, len(pointsByX)):
        upperHull.append(pointsByX[i])
        while len(upperHull) > 2 and orientationTest(upperHull[-3], upperHull[-2], upperHull[-1]) != 1:
            upperHull.pop(-2)

    lowerHull = []
    lowerHull.append(pointsByX[-1])
    lowerHull.append(pointsByX[-2])
    for i in range(len(pointsByX)-3, -1, -1):
        lowerHull.append(pointsByX[i])
        while len(lowerHull) > 2 and orientationTest(lowerHull[-3], lowerHull[-2], lowerHull[-1]) != 1:
            lowerHull.pop(-2)

    lowerHull.pop(0)
    lowerHull.pop(-1)
    hull = upperHull + lowerHull
    return hull


def GIFT_CH(points):
    #Jarvis march (gift wrapping)
    leftmost = min(points, key=lambda x: x[0])
    hull = []
    pointOnHull = leftmost
    i = 0
    while True:
        hull.append(pointOnHull)
        endpoint = points[0]
        for j in range(1, len(points)):
            if endpoint == pointOnHull or orientationTest(pointOnHull, endpoint, points[j]) == -1:
                endpoint = points[j]
        i += 1
        pointOnHull = endpoint
        if endpoint == leftmost:
            break
    return hull

def MBC_CH(points):
    #Marriage before conquest

    #pick a random vertical line to seperate the points
    xmin = min(points, key=lambda x: x[0])[0]
    xmax = max(points, key=lambda x: x[0])[0]
    xm = 0

    # The "bridge" between two sets of points P1 and P2, is the line y = ax+ b that satisfies the following:
    #   1) Passes above all points
    #   2) Has the highest intersection point with the line seperating P1 and P2.
    # This equates to finding a line such that
    #   1) y_i <= ax_i + b for every point i
    #   2) y_m = ax_m + b is minimized
    # This is a linear program which we can solve with a randomized incremental algorithm
    def bridge(points, xm):
        import scipy.optimize as opt
        #objective function coefs
        c = np.array([xm, 1])
        #inequality coefficients
        A_ub = np.array([[-p[0], -1] for p in points])
        b_ub = np.array([-p[1] for p in points])
        #solve the linear program
        res = opt.linprog(c, A_ub, b_ub)
        a, b = res.x

        print(a)
        print(b)
        print(res.status)
        return (a, b)

    bridge = bridge(points, xm)

    #plot xm as a vertical line
    plt.axvline(x=xm, color="black")

    #plot the bridge
    x = np.linspace(xmin, xmax, 100)
    y = bridge[0] * x + bridge[1]
    plt.plot(x, y, "green")


def generatePointsInASquare(n):
    import random
    points = []
    for i in range(n):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        points.append((x, y))
    return points

def generatePointsInACircle(n):
    import random
    points = []
    for i in range(n):
        r = math.sqrt(random.uniform(0, 100))
        theta = random.uniform(0, 2*math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))
    return points

def generatePointsOnYEqualsXsquared(n):
    import random
    points = []
    for i in range(n):
        x = random.randint(0, 100)
        y = x**2
        points.append((x, y))
    return points

def generatePointsOnYEqualsMinusXsquared(n):
    points = []
    for i in range(n):
        x = random.randint(0, 100)
        y = -x**2
        points.append((x, y))
    return points

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    points = generatePointsInACircle(400)
    for point in points:
        plt.plot(point[0], point[1], 'ro')

    MBC_CH(points)
    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
