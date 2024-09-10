from dataclasses import dataclass

from .lesson import Lesson
from .classroom import Classroom
from .day import Day

@dataclass
class Schedule:
    lesson_map: dict[Lesson,tuple[Day,Classroom]]
    days: list[Day]
    
    def __str__(self) -> str:
        string = ""
        for day in self.days:
            string += str(day) + '\n'
        return string