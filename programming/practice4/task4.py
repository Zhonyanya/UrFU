from datetime import datetime
from abc import ABC, abstractmethod
class Printable(ABC):
    @abstractmethod
    def print_info(self, info):
        pass

class Book(Printable):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year


    def info(self) -> str:
        return f"Книга {self.title} написана автором {self.author} и выпущена в {self.year} году"
    
    def print_info(self):
        print(self.info())
    

    @classmethod
    def from_string(cls, data):
        title, author, year = data.split(";")
        return cls(title, author, int(year))
    

    @property
    def age(self) -> int:
        return datetime.now().year - self.year
    
    @age.setter
    def age(self, value):
        self.year = datetime.now().year - value


    def __str__(self) -> str:
        return self.info()
    

    def __eq__(self, other) -> bool:
        return isinstance(other, Book) and self.title == other.title
