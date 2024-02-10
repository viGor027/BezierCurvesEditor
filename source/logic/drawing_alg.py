def de_casteljau(t: float, points: list[tuple]) -> tuple:
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((x, y))
        return de_casteljau(t, new_points)
