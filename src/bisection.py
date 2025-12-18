import math
from typing import Callable
from utils import sign_eq

def bisection_min_iterations(delta_max: float, a: float, b: float) -> int:
    """
    Calculates the minimum number of iterations required to obtain an
    error less than `delta_max` using the bisection method on an
    interval [`a`, `b`].
    """
    if a > b:
        a, b = b, a
    
    return int((math.log(b - a, math.e) - math.log(delta_max, math.e)) / math.log(2, math.e))

def bisection(f: Callable[[float], float], n: int, a: float, b: float) -> (float | None):
    """
    Applies the bisection method on a function `f`, in the
    interval [`a`, `b`].

    If this method cannot be applied, returns `None`.
    """
    if a > b:
        a, b = b, a

    if f(a) == 0:
        return a
    if f(b) == 0:
        return b
    if sign_eq(f(a), f(b)) or n <= 0:
        return None
    
    while n > 0:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        if sign_eq(f(a), f(c)):
            a = c
        else:
            b = c
        n -= 1

    return c

if __name__ == "__main__":
    #################
    # Usage example #
    #################

    # Equation: tan(x) = x <=> tan(x) - x = 0

    f = lambda x: math.tan(x) - x
    a = 4.49
    b = 4.5
    n = Bisection.bisection_min_iterations(0.0000000001, a, b)
    print(Bisection.bisection(f, n, a, b))
