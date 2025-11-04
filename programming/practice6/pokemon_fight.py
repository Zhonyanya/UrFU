import requests

class Pokemon:
    def __init__(self, pokemon_name: str):
        self.name = pokemon_name
        self.pokeresponse = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}").json()
    def info(self):
        types = [type["type"]['name'] for type in self.pokeresponse["types"]]
        abilities = [ability["ability"]["name"] for ability in self.pokeresponse["abilities"]]
        height = self.pokeresponse["height"]
        weight = self.pokeresponse["weight"]
        name = self.name
        return f"Покемон: {name}, типы: {types}, способности: {abilities}, рост: {height}, вес: {weight}"
    def __str__(self):
        return self.info()
squirtle = Pokemon("squirtle")
print(squirtle)
