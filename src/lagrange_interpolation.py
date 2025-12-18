from utils import Point

class LagrangeInterpolator:
    _points: list[Point]
    _modified: bool
    _coefficients: list[float]

    def __init__(self, points: list[Point] = None):
        self._points = points if points is not None else []
        self._modified = True

    def add_point(self, point: Point) -> None:
        if not isinstance(point, Point):
            raise ValueError("Point must be an instance of Point")
        if point in self._points:
            return
        for p in self._points:
            if p.x == point.x:
                raise ValueError("Points must have distinct x coordinates")
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
        if self._modified:
            self._coefficients = self._calculate_coefficients()
            self._modified = False
        
        result = 0.0
        for i in range(len(self._points)):
            val = self._coefficients[i]
            for j in range(len(self._points)):
                if i != j:
                    val *= (x - self._points[j].x)
            result += val
        
        return result

    def _calculate_coefficients(self) -> list[float]:
        result = []
        for i in range(len(self._points)):
            val = self._points[i].y
            div = 1
            for j in range(len(self._points)):
                if i != j:
                    div *= (self._points[i].x - self._points[j].x)
            result.append(val / div)
            
        return result

    def get_short_string(self) -> str:
        if self._modified:
            self._coefficients = self._calculate_coefficients()
            self._modified = False

        ret = ''
        for i in range(len(self._points)):
            if self._coefficients[i] != 0:
                if i > 0:
                    ret += ' + ' if self._coefficients[i] >= 0 else ' - '
                elif self._coefficients[i] < 0:
                    ret += '-'
                ret += f'{abs(self._coefficients[i]) :.4f} * '
                for j in range(len(self._points)):
                    if i != j:
                        sign = '-' if self._points[j].x >= 0 else '+'
                        ret += f'(x {sign} {abs(self._points[j].x)})'

        return ret

    def get_string(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if len(self._points) == 0:
            return ''

        ret = f'{self._points[0].y :.4f} * (A0 / B0)'
        for i in range(1, len(self._points)):
            ret += f' + {self._points[i].y :.4f} * (A{i} / B{i})'
        ret += '\n'

        for i in range(len(self._points)):
            a = f'A{i} = '
            b = f'B{i} = '
            for j in range(len(self._points)):
                if i != j:
                    sign = '-' if self._points[j].x >= 0 else '+'
                    a += f'(x {sign} {abs(self._points[j].x)})'
                    b += f'({self._points[i].x} {sign} {abs(self._points[j].x)})'
            ret += f'{a}\n{b}'
            if i < len(self._points) - 1:
                ret += '\n'

        return ret

####################################################################################################

if __name__ == "__main__":
    #################
    # Usage example #
    #################

    points = [Point(-1, -1), Point(0, 3), Point(2, 11), Point(3, 27)]
    interp = LagrangeInterpolator(points)
    
    print(f'P(x) = ' + interp.get_string())
    print(f'P(x) = ' + interp.get_short_string())
    print(f'P(1) = {interp.interpolate(1)}')            # P(1) = 5.0
