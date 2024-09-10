from common.constants import POPULATION_SIZE
from model.schedule import Schedule

from time import time

def print_final_results(population: list[Schedule], start_time: float) -> None:
    best_schedule, best_score = find_best(population)
    
    print("\nNew population")
    print_all_stats(population)
    print(f"Best schedule: \n{best_schedule}")
    print(f"Best score: {best_score}.")
    print(f"Program took {time() - start_time} seconds.")

def print_all_stats(population: list[Schedule]) -> None:
    from genetics.genetics import optimal_criterion
    i: int = 0
    score_sum: int = 0
    same: int = 0
    score = optimal_criterion(population[0])
    for chromosome in population:
        prev_score, score = score, optimal_criterion(chromosome)
        if score != prev_score:
            if same != 1:
                print(f"Chromosome:[{i-same}-{i-1}] Score:{score}")
            else:
                print(f"Chromosome: {i-1}      Score:{score}")
            same = 1
        else:
            same += 1
        score_sum += score
        i += 1
    if same != 1:
        print(f"Chromosome:[{i-same}-{i-1}] Score:{score}")
    else:
        print(f"Chromosome: {i-1}      Score:{score}")
    print(f"Average score: {score_sum / POPULATION_SIZE}")
    
def print_stats(population: list[Schedule]) -> None:
    from genetics.genetics import optimal_criterion
    i: int = 0
    score_sum: int = 0
    for chromosome in population:
        score = optimal_criterion(chromosome)
        score_sum += score
        i += 1
    print(f"Average score: {score_sum / POPULATION_SIZE}")
    _, best_score = find_best(population)
    print(f"Best score: {best_score}.")

def find_best(population: list[Schedule]) -> tuple[Schedule, int]:
    from genetics.genetics import optimal_criterion
    best_schedule = population[0]
    best_score = optimal_criterion(best_schedule)
    for chromosome in population:
        if optimal_criterion(chromosome) > best_score:
            best_schedule = chromosome
            best_score = optimal_criterion(chromosome)
    return best_schedule, best_score