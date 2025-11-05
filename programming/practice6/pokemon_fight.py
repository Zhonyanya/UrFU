import requests
class Pokemon:
    """Класс покемона"""

    def __init__(self, pokemon_name: str):
        """
        Инициализация класса покемона
        
        Args:
            pokemon_name (str): Имя покемона
        """

        self.name = pokemon_name
        self.pokeresponse = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}").json()
        self.hp = self.pokeresponse["stats"][0]["base_stat"]
        self.attack = self.pokeresponse["stats"][1]["base_stat"]

    def info(self):
        """Выдаёт имя, типы, способности, рост, вес, текущее здоровье и силу атаки"""

        types = [type["type"]['name'] for type in self.pokeresponse["types"]]
        abilities = [ability["ability"]["name"] for ability in self.pokeresponse["abilities"]]
        height = self.pokeresponse["height"]
        weight = self.pokeresponse["weight"]
        name = self.name
        return f"""
Покемон: {name}, типы: {types}, способности: {abilities}, рост: {height}, вес: {weight}
Текущее здоровье: {round(self.hp, 1)}
Сила атаки: {self.attack}"""
    
    def fight(self, other):
        """
        Устраивает битву между двумя покемонами.
        Покемоны сражаются в цикле нанося урон друг другу.
        Побеждает тот, кто раньше снесёт противника.

        Args:
            other (Pokemon): Покемон-противник
        """

        current_turn = self.name
        while self.hp > 0 and other.hp > 0:
            if current_turn == self.name:
                damage = round(self.attack * 0.2, 1)
                other.hp -= damage
                print(f"{current_turn} нанёс {other.name} {damage} урона. У того осталось: {round(other.hp, 1)} хп.")
            else:
                damage = round(other.attack * 0.2, 1)
                self.hp -= damage
                print(f"{current_turn} нанёс {self.name} {damage} урона. У того осталось: {round(self.hp, 1)} хп.")
            current_turn = self.name if current_turn == other.name else other.name
        if self.hp > 0:
            winner = self.name
        else:
            winner = other.name
        print(f'В поединке победил {winner}!')
    def __str__(self):
        """Превращает класс в человекочитаемый вид"""

        return self.info()
    
class Team:
    """Класс команды покемонов"""
    def __init__(self):
        """Инициализация команды покемонов"""

        self.team = []

    def add(self, pokemon: Pokemon):
        """
        Добавляет покемона в команду

        Args:
            pokemon (Pokemon): Покемон, которого надо добавить
        """

        if pokemon in self.team:
            print("Этот покемон уже есть в команде!")
        elif len(self.team) == 6:
            print("Достигнут максимальный размер команды!")
        else:
            self.team.append(pokemon)

    def remove(self, pokemon_name: str):
        """
        Удаляет покемона из команды

        Args:
            pokemon_name (str): Имя покемона, которого надо удалить
        """

        flag = True
        for pokemon in self.team:
            if pokemon.name == pokemon_name:
                self.team.remove(pokemon)
                flag = False
        if flag:
            print("Такого покемона нет в команде!")

    def get_pokemon(self, pokemon_name: str):
        """
        Возвращает покемона из команды по его имени

        Args:
            pokemon_name (str): Имя покемона, которого надо вернуть
        """

        for pokemon in self.team:
            if pokemon.name == pokemon_name:
                return pokemon
        print("Такого покемона нет в команде!")
    
    def info(self):
        """Возвращает инфу о каждом покемоне в команде"""

        teaminfo = [str(pokemon) for pokemon in self.team]
        return "\n".join(teaminfo)
    
    def __str__(self):
        """Превращает класс в человекочитаемый вид"""

        return self.info()

squirtle = Pokemon("squirtle")
charmander = Pokemon("charmander")
team = Team()
team.add(charmander)
team.add(squirtle)
print(team)
team.remove("squirtle")
print(team)
