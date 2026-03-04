import math


def calculate_relativistic(v, t0):
    """
    Returns gamma and t (dilated time) for given v (velocity in a fraction of c) and t (proper_time).
    Assuming v is 0 <= v <= 1.
    """

    gamma = 1 / math.sqrt(1 - v**2)
    t = gamma * t0
    return gamma, t


def calculate_gravitational(t0, factor):
    """
    Calculates gravitational time dilation. It takes t0 (proper time) and factor of (gravitational time dilation multiplier) assuming (0 < factor <=1)
    """
    return t0 * factor
