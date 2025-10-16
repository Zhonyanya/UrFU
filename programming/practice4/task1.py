class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    def info(self) -> str:
        return f"Книга {self.title} написана автором {self.author} и выпущена в {self.year} году"
