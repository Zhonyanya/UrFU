class Employee:
    def __init__(self, workhours, money_per_hour):
        """
        Класс работника

        Args:
            workhours (int): рабочие часы
            money_per_hour (float): зарплата в час
        """
        self.workhours = workhours
        self.money_per_hour = money_per_hour
    def info(self):
        """
        Возвращает зарплату

        Returns:
            (float): зарплата
        """
        return self.workhours * self.money_per_hour
class Manager(Employee):
    def __init__(self, workhours, money_per_hour, developers_fired, money_per_dev):
        """
        Класс манагера

        Args:
            workhours (int): рабочие часы
            money_per_hour (float): зарплата в час
            developers_fired (int): количество ликвидированных разработчиков
            money_per_dev (float): премия за девелопера
        """
        self.workhours = workhours
        self.money_per_hour = money_per_hour
        self.developers_fired = developers_fired
        self.money_per_dev = money_per_dev
    def info(self):
        """
        Возвращает зарплату

        Returns:
            (float): зарплата
        """
        return self.workhours * self.money_per_hour + self.money_per_dev * self.developers_fired
class Developer(Employee):
    def __init__(self, workhours, money_per_hour, lines_written, money_per_line):
        """
        Класс разработчика

        Args:
            workhours (int): рабочие часы
            money_per_hour (float): зарплата в час
            lines_written (int): количество написанных строчек кода
            money_per_line (float): премия за строчку
        """
        self.workhours = workhours
        self.money_per_hour = money_per_hour
        self.lines_written = lines_written
        self.money_per_line = money_per_line
    def info(self):
        """
        Возвращает зарплату

        Returns:
            (float): зарплата
        """
        return self.workhours * self.money_per_hour + self.money_per_line * self.lines_written
