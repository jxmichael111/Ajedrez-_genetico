# train.py
from ai.genetic_algorithm import GeneticAlgorithm
from ai.evaluation import evaluate_board
from game.board import Board
import pickle

# Arquitectura de la red neuronal: 769 entradas → 64 → 32 → 1 salida
LAYER_SIZES = [769, 64, 32, 1]

def fitness_function_white(individual):
    board = Board()
    board.current_turn = 'white'
    return evaluate_board(board, individual)

def fitness_function_black(individual):
    board = Board()
    board.current_turn = 'black'
    return evaluate_board(board, individual)

def train_ai(fitness_fn, save_name, color_label):
    print(f"Entrenando IA {color_label}...")
    ga = GeneticAlgorithm(
        population_size=50,
        mutation_rate=0.1,
        crossover_rate=0.7,
        fitness_function=fitness_fn,
        save_path=save_name,
        layer_sizes=LAYER_SIZES  # ✅ Red multicapa en lugar de gene_length
    )

    generations = 100
    for gen in range(generations):
        ga.evolve()
        best = ga.get_best_individual()
        print(f"Gen {gen}: Mejor Fitness = {best.fitness:.4f}")

    with open(save_name.replace(".pkl", "_best.pkl"), "wb") as f:
        pickle.dump(best, f)

def main():
    print("Entrenando IA Blanca...")
    train_ai(fitness_function_white, "best_individual_white.pkl", "BLANCAS")
    
    print("\nEntrenando IA Negra...")
    train_ai(fitness_function_black, "best_individual_black.pkl", "NEGRAS")

if __name__ == "__main__":
    main()
