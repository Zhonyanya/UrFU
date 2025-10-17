class Car:
    def __init__(self, speed, mass):
        self.speed = speed
        self.mass = mass
    def info(self):
        return f"Это обыкновенная машина массой {self.mass} и максимальной скоростью {self.speed}"

class Racecar(Car):
    def info(self):
        return f"Это гоночная машина массой {self.mass} и максимальной скоростью {self.speed}"

class Bike(Car):
    def info(self):
        return f"Это велосипед массой {self.mass} и максимальной скоростью {self.speed}"

class Autobus(Car):
    def __init__(self, speed, mass, number_of_people):
        super().__init__(speed, mass)
        self.number_of_people = number_of_people
    def info(self):
        return f"Это автобус массой {self.mass}, максимальной скоростью {self.speed}, а вмещает в себя он аж {self.number_of_people} человек"

def get_info(car):
    return car.info()
