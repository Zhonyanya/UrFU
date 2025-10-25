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

class Ebook(Book):
    def __init__(self, title, author, year, format):
        """
        Класс электронной книги

        Args:
            title (str): Название
            author (str): Автор
            year (int): Год выхода
            format (str): Формат выхода
        """
        self.title = title
        self.author = author
        self.year = year
        self.format = format


    def info(self) -> str:
        """
        Возвращает инфу
        """
        return f"Книга {self.title} написана автором {self.author} и выпущена в {self.year} году. Формат: {self.format}"
    
    def __str__(self) -> str:
        """
        Позволяет принтовать нормально
        """
        return self.info()
