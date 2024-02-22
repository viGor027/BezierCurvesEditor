import math
import numpy as np


def calc_distance(control_points: list) -> float:
    """
    Calculates distance from first to last control point going through every control point.
    :param control_points: list of control points.
    :return: float
    """
    dist = 0
    for i in range(len(control_points) - 1):
        x1, y1 = control_points[i]
        x2, y2 = control_points[i + 1]
        dist += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def get_optimized_moments(control_points: list) -> np.array:
    """
    Returns an array of moments for sampling the curve.
    :param control_points: list of control points.
    :return: np.array
    """
    return np.linspace(0, 1, num=int(calc_distance(control_points)//10 * 5))


def calc_distances_experimental(control_points: list) -> list[float]:
    """
    Calculates distance from first to last control point going through every control point.
    :param control_points: list of control points.
    :return: table of distances such that i'th element is distance between i'th and i+1 control point.
    """
    dist = []
    for i in range(len(control_points) - 1):
        x1, y1 = control_points[i]
        x2, y2 = control_points[i + 1]
        dist.append(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    return dist


def get_optimized_moments_experimental(control_points: list) -> np.array:
    """
    Returns an array of moments for sampling the curve.
    :param control_points: list of control points.
    :return: np.array of moments.
    """
    distances = calc_distances_experimental(control_points)
    moments = np.array([])
    total_dist = sum(distances)
    total_n_points = int(total_dist*0.5)
    prefix_sum = 0
    for i in range(len(control_points) - 1):
        start = prefix_sum / total_dist
        stop = (prefix_sum + distances[i]) / total_dist
        moments = np.append(moments,
                            np.linspace(start, stop, num=int((distances[i])/total_dist * total_n_points)
                                        )
                            )
        prefix_sum += distances[i]
    return moments


if __name__ == "__main__":
    random_points = [(0, 0), (10, 0), (100, 0)]
    print(get_optimized_moments(random_points) == get_optimized_moments_experimental(random_points))
