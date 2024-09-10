from model.lesson import Lesson
from typing import Any

def read_file(path: str) -> tuple[list, list[Lesson]]:
    lessons: list[Lesson] = []
    with open(path) as f:
        classrooms: list[Any] = list(map(str.strip, f.readline().split("rooms:")[1].split(",")))
        f.readline()
        for line in f.readlines():
            subject, duration = line.split(",")
            lessons.append(Lesson(subject.strip(), int(duration)))
    
    return classrooms, lessons

