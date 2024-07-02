import numpy as np
import matplotlib.pyplot as plt

# Step 1: Define the points
points = np.random.rand(5, 2)  # 5 points in 2D space


def calculate_area_and_perimeter(polygon):
    polygon = np.vstack([polygon, polygon[0]])  # Ensure the polygon is closed
    perimeter = np.sum(np.sqrt(np.sum(np.diff(polygon, axis=0) ** 2, axis=1)))
    area = 0.5 * np.abs(
        np.dot(polygon[:-1, 0], polygon[1:, 1])
        - np.dot(polygon[1:, 0], polygon[:-1, 1])
    )
    return area, perimeter


def fitness(polygon):
    area, perimeter = calculate_area_and_perimeter(polygon)
    if perimeter == 0:
        return 0
    return area / (perimeter**2)


# Step 2: Initial Population
def initial_population(points, population_size):
    population = []
    for _ in range(population_size):
        individual = np.random.permutation(points)
        population.append(individual)
    return np.array(population)


# Step 3: Selection
def selection(population, fitness_scores, num_parents):
    sorted_indices = np.argsort(fitness_scores)[-num_parents:]
    return population[sorted_indices]


# Step 4: Crossover
def crossover(parents, offspring_size):
    offspring = []
    num_parents = len(parents)
    for k in range(offspring_size):
        parent1_idx = k % num_parents
        parent2_idx = (k + 1) % num_parents
        cut_point = np.random.randint(1, len(parents[0]))
        child = np.vstack(
            (parents[parent1_idx][:cut_point], parents[parent2_idx][cut_point:])
        )
        unique_points, indices = np.unique(child, return_index=True, axis=0)
        missing_points = set(map(tuple, points)) - set(map(tuple, unique_points))
        if missing_points:
            missing_points = np.array(list(missing_points))
            child = np.vstack((child[indices], missing_points))
        else:
            child = child[indices]
        offspring.append(child)
    return np.array(offspring)


# Step 5: Mutation
def mutation(offspring):
    for individual in offspring:
        if np.random.rand() < 0.1:  # mutation probability
            swap_indices = np.random.choice(len(individual), size=2, replace=False)
            individual[swap_indices[0]], individual[swap_indices[1]] = (
                individual[swap_indices[1]],
                individual[swap_indices[0]],
            )
    return offspring


# Step 6: Evolution
def genetic_algorithm(points, population_size, num_generations, num_parents):
    population = initial_population(points, population_size)
    best_individual = None
    best_fitness = -np.inf

    for generation in range(num_generations):
        fitness_scores = np.array([fitness(individual) for individual in population])
        parents = selection(population, fitness_scores, num_parents)
        offspring_size = population_size - len(parents)
        offspring = crossover(parents, offspring_size)
        offspring = mutation(offspring)
        population = np.vstack((parents, offspring))
        generation_best_individual = population[np.argmax(fitness_scores)]
        generation_best_fitness = np.max(fitness_scores)

        if generation_best_fitness > best_fitness:
            best_individual = generation_best_individual
            best_fitness = generation_best_fitness

        print(f"Generation {generation}: Best Fitness = {generation_best_fitness}")

    return best_individual, best_fitness


# Running the genetic algorithm
best_shape, best_fitness = genetic_algorithm(
    points, population_size=100, num_generations=500, num_parents=4
)
print("Best Shape:", best_shape)
print("Best Fitness:", best_fitness)


# Visualization
def plot_polygon(points, best_shape):
    plt.plot(points[:, 0], points[:, 1], "o", label="Initial Points")
    plt.plot(
        np.append(best_shape[:, 0], best_shape[0, 0]),
        np.append(best_shape[:, 1], best_shape[0, 1]),
        "k-",
        label="Best Shape",
    )
    plt.fill(
        np.append(best_shape[:, 0], best_shape[0, 0]),
        np.append(best_shape[:, 1], best_shape[0, 1]),
        "c",
        alpha=0.3,
    )
    plt.title("Best Shape")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.legend()
    plt.show()


plot_polygon(points, best_shape)
