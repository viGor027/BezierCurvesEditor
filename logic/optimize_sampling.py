import math
import numpy as np


def calc_distance(control_points: list):
    """
    Calculates distance from first to last control point going through every control point
    :param control_points: list of control points
    :return:
    """
    dist = 0
    for i in range(len(control_points) - 1):
        x1, y1 = control_points[i]
        x2, y2 = control_points[i + 1]
        dist += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def get_optimized_moments(control_points: list):
    """
    Returns an array of moments for sampling the curve
    :param control_points: list of control points
    :return: np.array
    """
    print(int(calc_distance(control_points)))
    return np.linspace(0, 1, num=int(calc_distance(control_points)//10 * 5))
