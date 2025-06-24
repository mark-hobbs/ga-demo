import numpy as np

from pyga import Individual, blended, gaussian


class Star(Individual):

    _crossover_method = staticmethod(blended)
    _mutate_method = staticmethod(gaussian)

    target_shape = None

    def __init__(self, genes):
        super().__init__(genes)

    @classmethod
    def set_target_shape(cls, points):
        if cls.target_shape is not None:
            raise AttributeError("Target shape already set")
        cls.target_shape = points

    def evaluate_fitness(self):
        """
        Lower distance -> higher fitness
        """
        if Star.target_shape is None:
            raise ValueError("Target shape not set")
        distances = np.linalg.norm(
            np.array(self.genes).reshape(-1, 2)
            - np.array(Star.target_shape).reshape(-1, 2),
            axis=1,
        )
        self._fitness = 1 / (1 + np.mean(distances))

    def plot(self, ax):
        points = np.array(self.genes).reshape(-1, 2)
        x = np.append(points[:, 0], points[0, 0])
        y = np.append(points[:, 1], points[0, 1])
        ax.plot(x, y, "k-")
        ax.fill(x, y, "c", alpha=0.3)
        ax.set_aspect("equal")
        ax.axis("off")
