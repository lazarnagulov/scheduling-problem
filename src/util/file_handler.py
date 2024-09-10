from model.lesson import Lesson

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

