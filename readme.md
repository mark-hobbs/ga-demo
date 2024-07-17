# ga-demo

This repository demonstrates a basic implementation of a Genetic Algorithm (GA).

## Problem statement

Given a set of points in 2D space, determine the polygon that maximises the ratio of its area to the square of its perimeter $(\text{Area}/\text{Perimeter}^2)$. This ratio serves as a measure of compactness, which is often desirable in various fields such as materials science, biology, and urban planning. Compact shapes can lead to more efficient designs, reduced material usage, and optimised spatial arrangements.

## Example Solutions

The following animations demonstrate the evolution of the polygon shapes over many generations.

![Evolution Animation](figures/animation-1.gif)

![Evolution Animation](figures/animation-2.gif)

## Usage

### 1. Generate random points

Start by generating 10 random points.

```python
n_points = 10
points = [Point(np.random.rand(), np.random.rand()) for _ in range(n_points)]
```

### 2. Generate the initial population of polygons

Create an initial population of 25 polygons using the generated points.

```python
population_size = 25
individuals = [Polygon(np.random.permutation(points)) for _ in range(population_size)]
population = Population(individuals)
```

### 3. Initiate the Genetic Algorithm

Set up the Genetic Algorithm with the initial population, number of generations, number of parents, and mutation probability. You can also enable animation.

```python
ga = GeneticAlgorithm(
    population=population,
    num_generations=100,
    num_parents=4,
    mutation_probability=0.05,
    animate=True,
)
```

### 4. Perform the Evolution

Run the genetic algorithm to evolve the population towards optimal solutions.

```python
ga.evolve()
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.