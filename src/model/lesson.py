from dataclasses import dataclass

@dataclass
class Lesson:
    subject: str
    length: int
    
    def __str__(self) -> str:
        return "    " + self.subject + " [" + str(self.length) + " min]"
    
    def __hash__(self) -> int:
        return hash(self.subject)
