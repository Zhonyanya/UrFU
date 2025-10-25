class Car:
    def __init__(self, speed, mass):
        """
        Класс машины

        Args:
            speed (float): скорость
            mass (float): масса
        """
        self.speed = speed
        self.mass = mass
    def info(self):
        """
        Возвращает описание машины

        Returns:
            (str): описание машины
        """
        return f"Это обыкновенная машина массой {self.mass} и максимальной скоростью {self.speed}"

class Racecar(Car):
    def info(self):
        """
        Возвращает описание гоночной машины

        Returns:
            (str): описание гоночной машины
        """
        return f"Это гоночная машина массой {self.mass} и максимальной скоростью {self.speed}"

class Bike(Car):
    def info(self):
        """
        Возвращает описание велосипеда

        Returns:
            (str): описание велосипеда
        """
        return f"Это велосипед массой {self.mass} и максимальной скоростью {self.speed}"

class Autobus(Car):
    def __init__(self, speed, mass, number_of_people):
        """
        Класс автобуса

        Args:
            speed (float): скорость
            mass (float): масса
            number_of_people (int): максимальная вместимость
        """
        super().__init__(speed, mass)
        self.number_of_people = number_of_people
    def info(self):
        """
        Возвращает описание автобуса

        Returns:
            (str): описание автобуса
        """
        return f"Это автобус массой {self.mass}, максимальной скоростью {self.speed}, а вмещает в себя он аж {self.number_of_people} человек"

def get_info(car):
    """
    Возвращает описание средства передвижения

    Returns:
        (str): описание средства
    """
    return car.info()
