from utils import Point

def newton_interpolation(points: list[Point]) -> list[float]:
    if len(points) == 0:
        raise ValueError("Points list cannot be empty")

    coefficients = [points[0].y]
    matrix = []

    for i in range(len(points) - 1):
        matrix.append([None for _ in range(len(points) - 1)])

    for i in range(0, len(points) - 1):
        for j in range(i, len(points) - 1):
            matrix[i][j] = _recursive(points, matrix, i, j)
            if i == j:
                coefficients.append(matrix[i][j])

    return coefficients

def _recursive(points: list[Point], matrix: list[list[float]], k: int, t: int) -> float:
    if t == 0:
        return (points[k + 1].y - points[k].y) / (points[k + 1].x - points[k].x)

    if matrix[k][t] is not None:
        return matrix[k][t]

    return (_recursive(points, matrix, k, t - 1) - _recursive(points, matrix, k - 1, t - 1)) / (points[k + 1].x - points[k - t].x)

class NewtonInterpolator:
    _points: list[Point]
    _coefficients: list[float]
    _modified: bool

    def __init__(self, points: list[Point] = None):
        self._points = points if points is not None else []
        self._modified = True

    def add_point(self, point: Point) -> None:
        if not isinstance(point, Point):
            raise ValueError("Point must be an instance of Point")
        if point in self._points:
            return
        self._points.append(point)
        self._modified = True

    def remove_point(self, point: Point) -> None:
        if not isinstance(point, Point):
            raise ValueError("Point must be an instance of Point")
        if point not in self._points:
            return
        self._points.remove(point)
        self._modified = True

    def clear(self) -> None:
        self._points.clear()
        self._modified = True

    def interpolate(self, x: float) -> float:
        if not isinstance(x, (int, float)):
            raise ValueError("x must be a number")
        if self._modified:
            self._modified = False
            self._coefficients = newton_interpolation(self._points)

        result = self._coefficients[0]
        for i in range(1, len(self._coefficients)):
            product = self._coefficients[i]
            for j in range(i):
                product *= (x - self._points[j].x)
            result += product
        
        return result

    def get_coefficients(self) -> list[float]:
        if self._modified:
            self._modified = False
            self._coefficients = newton_interpolation(self._points)
        return self._coefficients.copy()

    def get_string(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if self._modified:
            self._modified = False
            self._coefficients = newton_interpolation(self._points)
        
        result = f'{self._coefficients[0] :.4f}'
        for i in range(1, len(self._coefficients)):
            if self._coefficients[i] != 0:
                if self._coefficients[i] > 0:
                    result += ' + '
                else:
                    result += ' - '
                result += f'{abs(self._coefficients[i]) :.4f} '
                for j in range(i):
                    if self._points[j].x >= 0:
                        result += f'(x - {self._points[j].x :.4f})'
                    else:
                        result += f'(x + {abs(self._points[j].x) :.4f})'

        return result

####################################################################################################

if __name__ == "__main__":
    #################
    # Usage example #
    #################

    points = [Point(-1, -1), Point(0, 3), Point(2, 11), Point(3, 27)]
    interp = NewtonInterpolator(points)
    
    print(interp.get_coefficients())                # [-1.0, 4.0, 0.0, 1.0]
    print(f'P(x) = ' + interp.get_string())         # P(x) = -1 + 4 (x + 1) + 1 (x + 1)(x - 0)(x - 2)
    print(f'P(1) = {interp.interpolate(1)}')        # P(1) = 5
