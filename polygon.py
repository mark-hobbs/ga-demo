import numpy as np
import matplotlib.pyplot as plt

from individual import Individual

class Polygon(Individual):
    def __init__(self, points):
        """
        The polygon is defined by the order of the points.
        """
        super().__init__(points)

    @property
    def points(self):
        return self.genes

    @points.setter
    def points(self, value):
        self.genes = value

    def calculate_area(self):
        n = len(self.points)
        if n < 3:
            return 0  # Not a polygon
        x = np.array([p.x for p in self.points])
        y = np.array([p.y for p in self.points])
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        return area

    def calculate_perimeter(self):
        n = len(self.points)
        perimeter = 0
        for i in range(n):
            x_diff = self.points[i].x - self.points[(i + 1) % n].x
            y_diff = self.points[i].y - self.points[(i + 1) % n].y
            perimeter += np.sqrt(x_diff**2 + y_diff**2)
        return perimeter

    def fitness(self):
        area = self.calculate_area()
        perimeter = self.calculate_perimeter()
        if perimeter == 0:
            return 0
        return area / (perimeter**2)
    
    def crossover(self, partner):
        return Polygon(super().crossover(partner))

    def mutate(self, mutation_probability):
        super().mutate(mutation_probability)

    def plot(self, ax=None):
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 6))

        x = [p.x for p in self.points]
        y = [p.y for p in self.points]
        x.append(x[0])
        y.append(y[0])
        ax.plot(x, y, "o")
        ax.plot(x, y, "k-", label="Polygon")
        ax.fill(x, y, "c", alpha=0.3, label="Polygon Area")
        ax.axis("off")
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            top=False,
            left=False,
            right=False,
            labelbottom=False,
            labelleft=False,
        )
