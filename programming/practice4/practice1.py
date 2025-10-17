class Employee:
    def __init__(self, workhours, money_per_hour):
        self.workhours = workhours
        self.money_per_hour = money_per_hour
    def info(self):
        return self.workhours * self.money_per_hour
class Manager(Employee):
    def __init__(self, workhours, money_per_hour, developers_fired, money_per_dev):
        self.workhours = workhours
        self.money_per_hour = money_per_hour
        self.developers_fired = developers_fired
        self.money_per_dev = money_per_dev
    def info(self):
        return self.workhours * self.money_per_hour + self.money_per_dev * self.developers_fired
class Developer(Employee):
    def __init__(self, workhours, money_per_hour, lines_written, money_per_line):
        self.workhours = workhours
        self.money_per_hour = money_per_hour
        self.lines_written = lines_written
        self.money_per_line = money_per_line
    def info(self):
        return self.workhours * self.money_per_hour + self.money_per_line * self.lines_written
