import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from polygon import Polygon
# from population import Population

class GeneticAlgorithm:
    def __init__(self, points, population_size=25, num_generations=50, num_parents=4):
        self.points = points
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_parents = num_parents
        self.population = self.initial_population()
        self.generations = []

    def initial_population(self):
        """
        Return an initial population of polygons of size `population_size`
        """
        population = []
        for _ in range(self.population_size):
            individual = np.random.permutation(self.points)
            population.append(Polygon(individual))
        return population

    def selection(self, fitness_scores):
        """
        Return the top `num_parents` polygons from the population based on
        their fitness scores.
        """
        sorted_indices = np.argsort(fitness_scores)[-self.num_parents :]
        return [self.population[i] for i in sorted_indices]

    def crossover(self, parents):
        offspring = []
        num_parents = len(parents)
        for k in range(self.population_size - self.num_parents):
            parent1 = parents[k % num_parents]
            parent2 = parents[(k + 1) % num_parents]
            cut_point = np.random.randint(1, len(parent1.points))
            child_points = list(parent1.points[:cut_point]) + list(
                parent2.points[cut_point:]
            )
            unique_points = []
            seen = set()
            for point in child_points:
                if (point.x, point.y) not in seen:
                    unique_points.append(point)
                    seen.add((point.x, point.y))
            missing_points = set(self.points) - seen
            unique_points.extend(missing_points)
            offspring.append(Polygon(unique_points))
        return offspring

    def mutation(self, offspring):
        for individual in offspring:
            if np.random.rand() < 0.1:  # mutation probability
                swap_indices = np.random.choice(
                    len(individual.points), size=2, replace=False
                )
                (
                    individual.points[swap_indices[0]],
                    individual.points[swap_indices[1]],
                ) = (
                    individual.points[swap_indices[1]],
                    individual.points[swap_indices[0]],
                )

    def evolve(self):
        for generation in range(self.num_generations):
            fitness_scores = np.array(
                [individual.fitness() for individual in self.population]
            )
            parents = self.selection(fitness_scores)
            offspring = self.crossover(parents)
            self.mutation(offspring)
            self.population = parents + offspring
            best_individual = max(self.population, key=lambda x: x.fitness())
            print(
                f"Generation {generation}: Best Fitness = {best_individual.fitness()}"
            )
            self.generations.append(
                self.population[:]
            )  # Save current population for animation
        best_individual = max(self.population, key=lambda x: x.fitness())
        return best_individual
    
    # def evolve(self):
    #     population.initialise()
    #     for generation in range(self.num_generations):
    #         population.evaluate()
    #         population.select_parents()

    def plot_population(self):
        _, axes = plt.subplots(5, 5, figsize=(12, 12))
        for individual, ax in zip(self.population, axes.flatten()):
            individual.plot(ax)
        plt.tight_layout()
