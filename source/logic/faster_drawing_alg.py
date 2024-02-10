from typing import Callable


def p(t: float, W: list, w: list) -> tuple:
    n = len(W) - 1
    u = 1 - t
    b = n
    p = W[0] * w[0]
    d = t
    for i in range(1, n + 1):
        p = (
            p[0] * u + b * W[i][0] * d * w[i],
            p[1] * u + b * W[i][1] * d * w[i]
        )
        d *= t
        b *= (n - i) / (i + 1)
    nwp = get_nwp(t, w)
    return p[0] / nwp, p[1] / nwp


def get_nwp(t: float, w: list) -> float:
    n = len(w) - 1
    u = 1 - t
    b = n
    p = w[0]
    d = t
    for i in range(1, n + 1):
        p = p * u + b * d * w[i]
        d *= t
        b *= (n - i) / (i + 1)
    return p


def bezier(W: list, w: list) -> Callable:
    return lambda t: p(t, W, w)
