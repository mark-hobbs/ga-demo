import numpy as np
import matplotlib.pyplot as plt


class Population:

    def __init__(self, individuals, num_parents=4):
        self.individuals = individuals
        self.num_parents = num_parents
        self.fitness = []
        self.parents = []

    def evaluate(self):
        self.fitness = [individual.fitness() for individual in self.individuals]

    def select_parents(self):
        sorted_individuals = sorted(
            self.individuals, key=lambda x: x.fitness(), reverse=True
        )
        self.parents = sorted_individuals[: self.num_parents]

    def plot(self):
        _, axes = plt.subplots(5, 5, figsize=(12, 12))
        for individual, ax in zip(self.individuals, axes.flatten()):
            individual.plot(ax)
        plt.tight_layout()
