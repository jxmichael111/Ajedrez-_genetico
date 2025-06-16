from ai.genetic_algorithm import GeneticAlgorithm
from ai.evaluation import evaluate_board
from game.board import Board
from utils.fen import generate_random_fen, load_fen

import pickle
from multiprocessing import Process

# Arquitectura de la red neuronal: 769 entradas → 64 → 32 → 1 salida
LAYER_SIZES = [769, 64, 32, 1]

def fitness_function_white(individual):
    total_score = 0.0
    samples = 5

    for _ in range(samples):
        fen = generate_random_fen()
        piece_placement, turn = fen.split()[0], fen.split()[1]

        board = Board()
        board.board = load_fen(piece_placement)
        board.current_turn = 'white'

        total_score += evaluate_board(board, individual)

    return total_score / samples

def fitness_function_black(individual):
    total_score = 0.0
    samples = 5

    for _ in range(samples):
        fen = generate_random_fen()
        piece_placement, turn = fen.split()[0], fen.split()[1]

        board = Board()
        board.board = load_fen(piece_placement)
        board.current_turn = 'black'

        total_score += evaluate_board(board, individual)

    return total_score / samples

def train_ai(fitness_fn, save_name, color_label):
    print(f"Entrenando IA {color_label}...")
    ga = GeneticAlgorithm(
        population_size=50,
        mutation_rate=0.1,
        crossover_rate=0.7,
        fitness_function=fitness_fn,
        save_path=save_name,
        layer_sizes=LAYER_SIZES
    )
    generations = 100
    for gen in range(generations):
        ga.evolve()
        best = ga.get_best_individual()
        print(f"[{color_label}] Gen {gen}: Mejor Fitness = {best.fitness:.4f}")

    with open(save_name.replace(".pkl", "_best.pkl"), "wb") as f:
        pickle.dump(best, f)

def main():
    print("Iniciando entrenamiento paralelo...")

    process_white = Process(
        target=train_ai,
        args=(fitness_function_white, "best_individual_white.pkl", "BLANCAS")
    )

    process_black = Process(
        target=train_ai,
        args=(fitness_function_black, "best_individual_black.pkl", "NEGRAS")
    )

    process_white.start()
    process_black.start()

    process_white.join()
    process_black.join()

    print("Entrenamiento de ambas IAs finalizado.")

if __name__ == "__main__":
    main()
