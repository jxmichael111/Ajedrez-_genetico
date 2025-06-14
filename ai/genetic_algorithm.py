# ai/genetic_algorithm.py
import random
import copy
import pickle
import os
import matplotlib.pyplot as plt

class Individual:
    def __init__(self, weights):
        self.weights = weights  # Lista de pesos
        self.fitness = 0.0

    def evaluate(self, input_vector):
        return sum(w * x for w, x in zip(self.weights, input_vector))

    def mutate(self, mutation_rate=0.1):
        for i in range(len(self.weights)):
            if random.random() < mutation_rate:
                self.weights[i] += random.uniform(-1.0, 1.0)

    def crossover(self, other):
        child_weights = []
        for w1, w2 in zip(self.weights, other.weights):
            child_weights.append(random.choice([w1, w2]))
        return Individual(child_weights)

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, gene_length, fitness_function, save_path):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.gene_length = gene_length
        self.fitness_function = fitness_function
        self.population = []
        self.generation = 0
        self.best_fitness_history = []
        self.save_path = save_path
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
            self.population = [Individual([random.uniform(-1, 1) for _ in range(self.gene_length)]) for _ in range(self.population_size)]

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
