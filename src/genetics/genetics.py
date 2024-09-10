from model.lesson import Lesson
from model.schedule import Schedule
from model.day import Day
from model.classroom import Classroom
from common.globals import lesson_count
from time import time

from common.constants import *
from util import file_handler, stats

from copy import deepcopy
import random

def run() -> None:
    global lesson_count
    rooms, lessons = file_handler.read_file(TEST_DATA_FILE)
    lesson_count = len(lessons)
    population: list[Schedule] = generate_population(rooms, lessons)
    
    print("Start population:")
    stats.print_all_stats(population)
    start_time: float = time()
    population = run_generation(population, 1)
    stats.print_final_results(population, start_time)
    
def run_generation(population: list[Schedule], iteration: int) -> list[Schedule]:
    prev_best_score: int = 0
    best_score: int = 0
    same: int = 1

    for _ in range(GENERATIONS):
        parents: list[tuple[Schedule, Schedule]] = roulette_selection(population)
        children: list[Schedule] = crossover(parents)
        mutate(children)
        population = elitism(population, children)

        if BEST_STREAK_TO_EXIT_ON != -1:
            prev_best_score, best_score = best_score, stats.find_best(population)[1]
            if prev_best_score == best_score:
                same += 1
            else:
                same = 1
            if same == BEST_STREAK_TO_EXIT_ON:
                print(f"Exiting on iteration {iteration}...")
                break

        if PRINT_GENERATIONS and iteration%10 == 0:
            print(f"Generation {iteration}")
            stats.print_stats(population)
            print()

        iteration += 1
        
    return population

def generate_population(classrooms: list[str], lessons: list[Lesson]) -> list[Schedule]:
    random.shuffle(lessons)
    population: list[Schedule] = []

    for _ in range(POPULATION_SIZE):
        schedule = Schedule({}, [])
        schedule.days = [Day(name, [Classroom(cr, START_TIME, 0, []) for cr in classrooms]) for name in DAY_NAMES]
        
        lesson_idx = 0
        while lesson_idx < len(lessons):
            lesson = lessons[lesson_idx]
            day = random.choice(schedule.days)
            classroom_idx = random.randint(0, len(day.classrooms) - 1)
            classroom = day.classrooms[classroom_idx]
            if classroom.total_time + lesson.length + BREAK <= MAX_TIME:
                if classroom.total_time != 0:
                    classroom.total_time += BREAK
                classroom.total_time += lesson.length
                classroom.lessons.append(lesson)
                schedule.lesson_map[lesson] = (day, classroom)
            else:
                end_idx = classroom_idx
                classroom_idx += 1
                if classroom_idx >= len(day.classrooms):
                    classroom_idx = 0
                success = False
                while classroom_idx != end_idx:
                    if day.classrooms[classroom_idx].total_time + lesson.length + BREAK <= MAX_TIME:
                        day.classrooms[classroom_idx].total_time += lesson.length + BREAK
                        day.classrooms[classroom_idx].lessons.append(lesson)
                        schedule.lesson_map[lesson] = (day, day.classrooms[classroom_idx])
                        success = True
                        break
                    classroom_idx += 1
                    if classroom_idx >= len(day.classrooms):
                        classroom_idx = 0
                if not success:
                    continue
            lesson_idx += 1
        for day in schedule.days:
            for classroom in day.classrooms:
                leftover_time = MAX_TIME - classroom.total_time
                classroom.start_time += random.randint(0, leftover_time)
        population.append(schedule)
    return population

def optimal_criterion(schedule: Schedule) -> int:
    score = 0
    for day in schedule.days:
        for classroom in day.classrooms:
            if classroom.total_time == 0:
                score  += MAX_TIME * MAX_TIME
                continue
            else:
                end_time = classroom.start_time + classroom.total_time
                score += (classroom.start_time - START_TIME) * (END_TIME - end_time)
    return score

def crossover(parents: list[tuple[Schedule, Schedule]]) -> list[Schedule]:
    global lesson_count
    children: list[Schedule] = []
    for pair in parents:
        parent_0 = deepcopy(pair[0])
        parent_1 = deepcopy(pair[1])
        to_cross = lesson_count // 2
        for _ in range(to_cross):
            day_0 = random.choice(parent_0.days)
            old_classroom_0 = random.choice(day_0.classrooms)
            while len(old_classroom_0.lessons) == 0:
                day_0 = random.choice(parent_0.days)
                old_classroom_0 = random.choice(day_0.classrooms)
            lesson = random.choice(old_classroom_0.lessons)

            day_1, old_classroom_1 = parent_1.lesson_map[lesson]

            if old_classroom_0 == old_classroom_1:
                continue

            new_classroom_1: Classroom = __find_classroom(parent_1, day_0.name, old_classroom_0.name)
            new_classroom_0: Classroom = __find_classroom(parent_0, day_1.name, old_classroom_1.name)

            if new_classroom_0.total_time + lesson.length + BREAK > MAX_TIME:
                continue
            if new_classroom_1.total_time + lesson.length + BREAK > MAX_TIME:
                continue

            old_classroom_0.remove_lesson(lesson)
            old_classroom_1.remove_lesson(lesson)

            new_classroom_0.add_lesson(lesson)
            parent_0.lesson_map[lesson] = (day_0, new_classroom_0)
            new_classroom_1.add_lesson(lesson)
            parent_1.lesson_map[lesson] = (day_1, new_classroom_1)

        children.append(parent_0)
        children.append(parent_1)
            
    return children

def mutate(population: list[Schedule]) -> None:
    for chromosome in population:
        chance = random.random()
        if chance <= MUTATION_RATE:
            to_move = random.randint(1, MUTATION_WIDTH)
            for _ in range(to_move):
                day = random.choice(chromosome.days)
                classroom = random.choice(day.classrooms)
                while len(classroom.lessons) == 0:
                    day = random.choice(chromosome.days)
                    classroom = random.choice(day.classrooms)
                lesson = random.choice(classroom.lessons)
                new_day = random.choice(chromosome.days)
                new_classroom = random.choice(new_day.classrooms)
                if new_classroom.total_time + lesson.length + BREAK <= MAX_TIME:
                    new_classroom.add_lesson(lesson)
                    classroom.remove_lesson(lesson)
                    chromosome.lesson_map[lesson] = (new_day, new_classroom)

            to_swap = random.randint(1, MUTATION_WIDTH)
            for _ in range(to_swap):
                lesson_A = random.choice(list(chromosome.lesson_map.keys()))
                lesson_B = random.choice(list(chromosome.lesson_map.keys()))

                while lesson_A == lesson_B:
                    lesson_B = random.choice(list(chromosome.lesson_map.keys()))

                day_A, classroom_A = chromosome.lesson_map[lesson_A]
                day_B, classroom_B = chromosome.lesson_map[lesson_B]

                if classroom_A.total_time + (lesson_B.length - lesson_A.length) <= MAX_TIME and \
                   classroom_B.total_time + (lesson_A.length - lesson_B.length) <= MAX_TIME:
                    classroom_A.remove_lesson(lesson_A)
                    classroom_B.remove_lesson(lesson_B)
                    classroom_A.add_lesson(lesson_B)
                    classroom_B.add_lesson(lesson_A)
                    chromosome.lesson_map[lesson_B] = (day_A, classroom_A)
                    chromosome.lesson_map[lesson_A] = (day_B, classroom_B)

def roulette_selection(population: list[Schedule]) -> list[tuple[Schedule,Schedule]]: 
    weights: list[tuple[float, Schedule]] = []
    scores: list[int] = [optimal_criterion(chromosome) for chromosome in population]
    parents: list[tuple[Schedule, Schedule]] = []
    for _ in range(0, len(population), 2):
        weights = []
        for i in range(len(population)):
            weights.append((scores[i] * random.random(), population[i]))
        weights.sort(reverse=True)
        parents.append((weights[0][1], weights[1][1]))
    return parents

def elitism(population: list[Schedule], children: list[Schedule]) -> list[Schedule]:
    population = sorted(population, key = optimal_criterion, reverse=True)
    children = sorted(children, key = optimal_criterion, reverse=True)
    elitism_size: int = int(round(POPULATION_SIZE * ELITISM_RATE))
    return population[:elitism_size] + children[:(POPULATION_SIZE - elitism_size)]

def __find_classroom(schedule: Schedule, day_name: str, classroom_name: str) -> Classroom:
    for day in schedule.days:
        if day.name == day_name:
            for classroom in day.classrooms:
                if classroom.name == classroom_name:
                    return classroom 
    
    raise Exception("Unreachable...")            