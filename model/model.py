from dataclasses import dataclass
from common.constants import *

@dataclass
class Lesson:
    subject: str
    length: int
    
    def __str__(self) -> str:
        return "    " + self.subject + " [" + str(self.length) + " min]"
    
    def __hash__(self) -> int:
        return hash(self.subject)

@dataclass
class Classroom:
    name: str
    start_time: int
    total_time: int
    lessons: list[Lesson]
    
    def __str__(self) -> str:
        if self.total_time != 0:
            string = "  " + self.name + f": (start: {self.start_time//60:02d}:{self.start_time%60:02d}," + \
                                        f" end: {(self.start_time + self.total_time)//60:02d}:{(self.start_time + self.total_time)%60:02d}," + \
                                        f" total: {self.total_time//60}h {self.total_time%60:02d}min)\n"
        else:
            string = "  " + self.name + ":\n    Empty\n"
            return string
        for lesson in self.lessons:
            string += str(lesson) + '\n'
        return string
    
    def remove_lesson(self, lesson: Lesson):
        self.lessons.remove(lesson)
        if len(self.lessons) == 0:
            self.total_time = 0
        else:
            self.total_time -= lesson.length + BREAK
        self.start_time = START_TIME + (MAX_TIME - self.total_time) // 2
    
    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)
        if len(self.lessons) == 1:
            self.total_time = lesson.length
        else:
            self.total_time += lesson.length + BREAK
        self.start_time = START_TIME + (MAX_TIME - self.total_time) // 2
    

@dataclass
class Day:
    name: str
    classrooms: list[Classroom]
    
    def __str__(self) -> str:
        string = self.name + ": \n"
        for cr in self.classrooms:
            string += str(cr) + '\n'
        return string

@dataclass
class Schedule:
    lesson_map: dict[Lesson,tuple[Day,Classroom]]
    days: list[Day]
    
    def __str__(self) -> str:
        string = ""
        for day in self.days:
            string += str(day) + '\n'
        return string