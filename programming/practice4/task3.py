from datetime import datetime
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
    

    @classmethod
    def from_string(cls, data):
        """
        Генерирует объект класса Book через строку
        
        Args:
            cls: Название класса
            data (str): Строка через которую создаётся класс
        Returns:
            cls (Book): Объект класса Book
        """
        title, author, year = data.split(";")
        return cls(title, author, int(year))
    

    @property
    def age(self) -> int:
        """
        Геттер
        """
        return datetime.now().year - self.year
    
    @age.setter
    def age(self, value):
        """
        Сеттер
        """
        self.year = datetime.now().year - value


    def __str__(self) -> str:
        """
        Позволяет принтовать нормально
        """
        return self.info()
    

    def __eq__(self, other) -> bool:
        """
        Позволяет сравнивать две книги
        """
        return isinstance(other, Book) and self.title == other.title
