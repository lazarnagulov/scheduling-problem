from common.constants import BEST_STREAK_TO_EXIT_ON, GENERATIONS, POPULATION_SIZE
from common.globals import lesson_count

from model.lesson import Lesson
from model.schedule import Schedule
from genetics import genetics

from util import file_utils
from time import time

PRINT_GENERATIONS = True

def print_all_stats(population: list[Schedule]) -> None:
    i: int = 0
    score_sum: int = 0
    same: int = 0
    score = genetics.optimal_criterion(population[0])
    for chromosome in population:
        prev_score, score = score, genetics.optimal_criterion(chromosome)
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
    i: int = 0
    score_sum: int = 0
    for chromosome in population:
        score = genetics.optimal_criterion(chromosome)
        score_sum += score
        i += 1
    print(f"Average score: {score_sum / POPULATION_SIZE}")
    best_schedule, best_score = find_best(population)
    print(f"Best score: {best_score}.")

def find_best(population: list[Schedule]) -> tuple[Schedule, float]:
    best_schedule = population[0]
    best_score = genetics.optimal_criterion(best_schedule)
    for chromosome in population:
        if genetics.optimal_criterion(chromosome) > best_score:
            best_schedule = chromosome
            best_score = genetics.optimal_criterion(chromosome)
    return best_schedule, best_score

def main() -> None:
    rooms, lessons = file_utils.read_file("../data_timetable.txt")
    lesson_count = len(lessons)

    population: list[Schedule] = genetics.generate_population(rooms, lessons)
    
    print("Start population:")
    print_all_stats(population)

    p = time()
    it = 1
    
    prev_best_score = 0
    best_score = 0
    same = 1

    for _ in range(GENERATIONS):
        parents = genetics.roulette_selection(population)
        children = genetics.crossover(parents)
        genetics.mutate(children)
        population = genetics.elitism(population, children)

        if BEST_STREAK_TO_EXIT_ON != -1:
            prev_best_score, best_score = best_score, find_best(population)[1]
            if prev_best_score == best_score:
                same += 1
            else:
                same = 1
            if same == BEST_STREAK_TO_EXIT_ON:
                print(f"Exiting on iteration {it}...")
                break

        if PRINT_GENERATIONS and it%10 == 0:
            print(f"Generation {it}")
            print_stats(population)
            print()

        it += 1

    best_schedule, best_score = find_best(population)
    
    print("\nNew population")
    print_all_stats(population)
    print(f"Best schedule: \n{best_schedule}")
    print(f"Best score: {best_score}.")
    print(f"Program took {time()-p} seconds.")

if __name__ == "__main__":
    main()