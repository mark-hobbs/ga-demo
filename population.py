import numpy as np
import matplotlib.pyplot as plt


class Population:

    def __init__(self, individuals):
        self.individuals = individuals
        self.fitness = []
        self.parents = []

    def evaluate(self):
        self.fitness = [individual.fitness() for individual in self.individuals]

    def select_parents(self, num_parents):
        sorted_individuals = sorted(
            self.individuals, key=lambda x: x.fitness(), reverse=True
        )
        self.parents = sorted_individuals[:num_parents]

    def plot(self):
        fig, axes = plt.subplots(5, 5, figsize=(12, 12))
        for individual, ax in zip(self.individuals, axes.flatten()):
            individual.plot(ax)
        plt.tight_layout()
        return fig
