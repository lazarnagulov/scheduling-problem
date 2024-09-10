from dataclasses import dataclass
from .classroom import Classroom

@dataclass
class Day:
    name: str
    classrooms: list[Classroom]
    
    def __str__(self) -> str:
        string = self.name + ": \n"
        for cr in self.classrooms:
            string += str(cr) + '\n'
        return string
