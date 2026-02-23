from __future__ import annotations
from typing import Tuple
import math

PointXY = Tuple[float, float]


class LinEq:
    """Simple class representing a linear equation or line"""
    
    def __init__(self, slope: float, intercept: float):
        self.slope = slope
        self.intercept = intercept

    def get_y(self, x: float) -> float:
        """Get the y associated to a given x"""
        return self.slope * x + self.intercept
    
    def get_x(self, y: float) -> float:
        """Get the x associated to a given y. Returns NaN if ``slope == 0``."""
        if math.isclose(self.slope, 0):
            return float('nan')
        return (y - self.intercept) / self.slope
    
    def intersection(self, other: LinEq) -> PointXY:
        """Returns the intersection ``(x, y)`` between two LinEq. Raises a 
        ValueError if the lines are parallel or congruent. """
        if math.isclose(self.slope, other.slope):
            if math.isclose(self.intercept, other.intercept):
                raise ValueError('Infinite interceptions: linear equations are identical.')
            else:
                raise ValueError('No interception: linear equations are parallel.')
        x = (self.intercept - other.intercept) / (other.slope - self.slope)
        y = self.get_y(x)
        return x, y

    __call__ = get_y

    @classmethod
    def from_2points(cls, pnt0: PointXY, pnt1: PointXY) -> LinEq:
        x0, y0 = pnt0
        x1, y1 = pnt1
        if math.isclose(x1, x0):
            raise ValueError('Vertical lines are not supported.')
        slope = (y1 -y0) / (x1 - x0)
        intercept = y0 - x0 * slope
        return cls(slope, intercept)


def intersection(p0: PointXY, p1: PointXY, q0: PointXY, q1: PointXY) -> PointXY:
    """Calculates the intersection between two lines, defined by two points each."""
    g = LinEq.from_2points(p0, p1)
    h = LinEq.from_2points(q0, q1)
    return g.intersection(h)