import random
import numpy as np

from polygon import Polygon
from animation import Animation


class GeneticAlgorithm:
    def __init__(self, population, num_generations=50):
        self.population = population
        self.num_generations = num_generations
        self.generations = []
        self.animation = Animation()

    def generate_offspring(self):
        new_population = []
        for _ in range(len(self.population.individuals)):
            parent_a, parent_b = random.sample(self.population.parents, 2)
            child = self.crossover(parent_a, parent_b)
            self.mutation(child)
            new_population.append(child)

        self.population.individuals = new_population

    def crossover(self, parent_a, parent_b):
        """
        Partially mapped crossover (PMX)

        Returns
        -------
        child
        """
        size = len(parent_a.points)
        child = [-1] * size
        a, b = sorted(np.random.choice(range(size), size=2, replace=False))

        for i in range(a, b):
            child[i] = parent_a.points[i]

        for i in range(size):
            if i < a or i >= b:
                value = parent_b.points[i]
                while value in child:
                    idx = child.index(parent_a.points[child.index(value)])
                    value = parent_b.points[idx]
                child[i] = value

        return Polygon(child)

    def mutation(self, child):
        """
        Mutation: Swap mutation
        """
        if np.random.rand() < 0.05:  # Mutation probability
            idx1, idx2 = np.random.randint(0, len(child.points), 2)
            child.points[idx1], child.points[idx2] = (
                child.points[idx2],
                child.points[idx1],
            )

    def evolutionary_cycle(self, i):
        self.population.evaluate()
        self.population.select_parents()
        self.generate_offspring()
        self.generations.append(self.population.individuals.copy())
        # self.population.plot()
        # plt.savefig(f'figures/generation-{i}.png')
        self.animation.save_frame(self.population)

    def evolve(self):
        for i in range(self.num_generations):
            self.evolutionary_cycle(i)

        self.animation.generate()
