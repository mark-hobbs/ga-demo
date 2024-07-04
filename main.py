import numpy as np
import matplotlib.pyplot as plt


from point import Point
from polygon import Polygon
from population import Population
from ga import GeneticAlgorithm


def main():
    n_points = 10
    points = [Point(np.random.rand(), np.random.rand()) for _ in range(n_points)]

    population_size = 25
    individuals = [
        Polygon(np.random.permutation(points)) for _ in range(population_size)
    ]
    population = Population(individuals)

    ga = GeneticAlgorithm(
        population,
        num_generations=100,
        num_parents=4,
        mutation_probability=0.05,
        animate=True,
    )
    ga.evolve()


main()
