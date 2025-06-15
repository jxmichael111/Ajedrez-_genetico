# ai/genetic_algorithm.py
import random
import copy
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np  

class Individual:
    def __init__(self, layer_sizes=None):
        self.layer_sizes = layer_sizes or [769, 64, 32, 1]
        self.weights = []
        self.biases = []
        self.fitness = 0.0

        for i in range(len(self.layer_sizes) - 1):
            input_size = self.layer_sizes[i]
            output_size = self.layer_sizes[i + 1]
            w = np.random.randn(output_size, input_size) * 0.1
            b = np.random.randn(output_size) * 0.1
            self.weights.append(w)
            self.biases.append(b)

    def evaluate(self, input_vector):
        x = input_vector
        for w, b in zip(self.weights, self.biases):
            x = np.tanh(np.dot(w, x) + b)
        return x[0]  # Output final: escalar

    def mutate(self, mutation_rate=0.1):
        for l in range(len(self.weights)):
            mutation_mask = np.random.rand(*self.weights[l].shape) < mutation_rate
            self.weights[l] += mutation_mask * np.random.uniform(-1.0, 1.0, self.weights[l].shape)

            mutation_mask_b = np.random.rand(*self.biases[l].shape) < mutation_rate
            self.biases[l] += mutation_mask_b * np.random.uniform(-1.0, 1.0, self.biases[l].shape)

    def crossover(self, other):
        child = Individual(self.layer_sizes)
        for i in range(len(self.weights)):
            mask = np.random.rand(*self.weights[i].shape) < 0.5
            child.weights[i] = np.where(mask, self.weights[i], other.weights[i])

            mask_b = np.random.rand(*self.biases[i].shape) < 0.5
            child.biases[i] = np.where(mask_b, self.biases[i], other.biases[i])
        return child

    def get_activations(self, input_vector):
        activations = []
        x = input_vector
        for w, b in zip(self.weights, self.biases):
            x = np.tanh(np.dot(w, x) + b)
            activations.append(x)
        return activations

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, fitness_function, save_path, layer_sizes=None):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.fitness_function = fitness_function
        self.save_path = save_path
        self.layer_sizes = layer_sizes or [769, 64, 32, 1]

        self.population = []
        self.generation = 0
        self.best_fitness_history = []

        self._load_or_initialize()

    def _load_or_initialize(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "rb") as f:
                data = pickle.load(f)
                self.population = data["population"]
                self.generation = data["generation"]
                self.best_fitness_history = data["fitness_history"]
                print(f"Continuando desde generación {self.generation}")
        else:
            self.population = [Individual(layer_sizes=self.layer_sizes) for _ in range(self.population_size)]

    def save_state(self):
        data = {
            "population": self.population,
            "generation": self.generation,
            "fitness_history": self.best_fitness_history,
        }
        with open(self.save_path, "wb") as f:
            pickle.dump(data, f)

        # También guardar el mejor individuo
        best = self.get_best_individual()
        best_path = self.save_path.replace(".pkl", "_best.pkl")
        with open(best_path, "wb") as f:
            pickle.dump(best, f)

        # Guardar el gráfico
        self.plot_progress()

    def evaluate_fitness(self):
        for individual in self.population:
            individual.fitness = self.fitness_function(individual)

    def select_parents(self):
        weights = [ind.fitness for ind in self.population]
        total = sum(weights)
        if total == 0:
            return random.sample(self.population, 2)
        return random.choices(self.population, weights=weights, k=2)

    def evolve(self):
        self.evaluate_fitness()
        new_population = []

        best = self.get_best_individual()
        new_population.append(copy.deepcopy(best))
        self.best_fitness_history.append(best.fitness)

        print(f"Generación {self.generation} - Mejor fitness: {best.fitness:.4f}")

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            if random.random() < self.crossover_rate:
                child = parent1.crossover(parent2)
            else:
                child = copy.deepcopy(random.choice([parent1, parent2]))
            child.mutate(self.mutation_rate)
            new_population.append(child)

        self.population = new_population
        self.generation += 1
        self.save_state()

    def get_best_individual(self):
        return max(self.population, key=lambda ind: ind.fitness)

    def get_fitness_history(self):
        return self.best_fitness_history

    def plot_progress(self):
        if not self.best_fitness_history:
            return
        plt.figure(figsize=(8, 4))
        plt.plot(self.best_fitness_history, label='Mejor Fitness')
        plt.title(f'Progreso del Fitness hasta la generación {self.generation}')
        plt.xlabel('Generación')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        graph_path = self.save_path.replace(".pkl", "_fitness.png")
        plt.savefig(graph_path)
        plt.close()
