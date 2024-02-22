def de_casteljau(t: float, points: list[tuple]) -> tuple:
    """
    Performs the De Casteljau's algorithm for Bézier curve evaluation.
    This recursive function calculates the Bézier curve point at a specific parameter t
    using the De Casteljau's algorithm.
    :param t: Parameter value between 0.0 and 1.0 representing the position on the curve.
    :param points: List of control points, each represented as a tuple (x, y).
    :return: tuple
    """
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((x, y))
        return de_casteljau(t, new_points)
