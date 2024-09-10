from common.constants import BEST_STREAK_TO_EXIT_ON, GENERATIONS, POPULATION_SIZE
from common.globals import lesson_count

from model.lesson import Lesson
from model.schedule import Schedule
from genetics import genetics

from util import file_handler
from util import stats
from time import time

PRINT_GENERATIONS = True

def main() -> None:
    global lesson_count
    rooms, lessons = file_handler.read_file("./data_timetable.txt")
    lesson_count = len(lessons)

    population: list[Schedule] = genetics.generate_population(rooms, lessons)
    
    print("Start population:")
    stats.print_all_stats(population)

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
            prev_best_score, best_score = best_score, stats.find_best(population)[1]
            if prev_best_score == best_score:
                same += 1
            else:
                same = 1
            if same == BEST_STREAK_TO_EXIT_ON:
                print(f"Exiting on iteration {it}...")
                break

        if PRINT_GENERATIONS and it%10 == 0:
            print(f"Generation {it}")
            stats.print_stats(population)
            print()

        it += 1

    best_schedule, best_score =  stats.find_best(population)
    
    print("\nNew population")
    stats.print_all_stats(population)
    print(f"Best schedule: \n{best_schedule}")
    print(f"Best score: {best_score}.")
    print(f"Program took {time()-p} seconds.")

if __name__ == "__main__":
    main()