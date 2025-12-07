import math


def calculate_relativistic(v, t0):
    """
    Returns gamma and t (dilated time) for given v (velocity in a fraction of c) and t (proper_time).
    Assuming v is validated in models.py file.
    """

    gamma = 1 / math.sqrt(1 - v**2)
    t = gamma * t0
    return gamma, t
