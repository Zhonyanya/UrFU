class Book:
    def __init__(self, title, author, year):
        """
        Класс книги

        Args:
            title (str): Название
            author (str): Автор
            year (int): Год выхода
        """
        self.title = title
        self.author = author
        self.year = year
    def info(self) -> str:
        """
        Возвращает инфу
        """
        return f"Книга {self.title} написана автором {self.author} и выпущена в {self.year} году"
