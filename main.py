from model.model import *
from common.constants import *
from common import globals
from genetics.genetics import *

from time import time


def read_file(path: str) -> tuple[list, list[Lesson]]:
    lessons: list[Lesson] = []
    with open(path) as f:
        classrooms: list = f.readline()
        classrooms = list(map(str.strip, classrooms.split("rooms:")[1].split(",")))
        f.readline()
        for line in f.readlines():
            subject, duration = line.split(",")
            lessons.append(Lesson(subject.strip(), int(duration)))
    
    return classrooms, lessons


def print_stats(population: list[Schedule]) -> None:
    i: int = 0
    score_sum: int = 0
    for chromosome in population:
        score = optimal_criterion(chromosome)
        print(f"Chromosome:{i} Score:{score}")
        score_sum += score
        i += 1
    print(f"Average:{score_sum / POPULATION_SIZE}")
    

def main() -> None:
    rooms, lessons = read_file("./ata_timetable.txt")
    globals.lesson_count = len(lessons)

    population: list[Schedule] = generate_population(rooms, lessons)
    
    print("Start population:")
    print_stats(population)

    p = time()
    it = 1
    
    for _ in range(GENERATIONS):
        parents = roulette_selection(population)
        children = crossover(parents)
        mutate(children)
        population = elitism(population, children)

        it += 1

    best_schedule = population[0]
    best_score = optimal_criterion(best_schedule)
    for chromosome in population:
        if optimal_criterion(chromosome) > best_score:
            best_schedule = chromosome
            best_score = optimal_criterion(chromosome)
    
    print("\nNew population")
    print_stats(population)
    print(f"Best schedule: \n{best_schedule}")
    print(f"Best score: {best_score}.")
    print(f"Program took {time()-p} seconds.")

if __name__ == "__main__":
    main()