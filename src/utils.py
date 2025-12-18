def sign_eq(a: (int | float), b: (int | float)) -> bool:
    """
    Returns whether a and b have the same sign.
    """
    return (a >= 0 and b >= 0) or (a < 0 and b < 0)

class Point:
    """
    A point in the plane.
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
