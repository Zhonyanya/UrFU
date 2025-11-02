import requests
response = requests.get("https://pokeapi.co/api/v2/pokemon")
responselist = response.json()["results"]
pokedict = dict()
pokenamelist = []
for pokemon in responselist:
    pokedict[pokemon['name']] = pokemon['url']
    pokenamelist.append(pokemon["name"])
print(pokenamelist)

def get_pokemon_stats(pokemon_name: str):
    """
    Выдаёт данные покемона: имя, тип, вес, рост, названия способностей

    Args:
        pokemon_name (str): Имя покемона на английском
    """
    get_poke = requests.get(pokedict[pokemon_name]).json()
    weight = get_poke["weight"]

    this_poketypes = get_poke["types"]
    #их оказца несколько может быть у одного покемона, поэтому список
    types = []
    for type in this_poketypes:
        types.append(type["type"]["name"])

    height = get_poke["height"]
    abilities = get_poke["abilities"]
    abilist = []
    for abi in abilities:
        abilist.append(abi["ability"]["name"])
    return {"name": pokemon_name, "types": types, "weight": weight,
             "height": height, "abilities": abilist}
pokename = input("Имя покемона: ")
pokestats = get_pokemon_stats(pokename)
print(f"Имя: {pokestats['name']}")
print(f"Типы: {pokestats['types']}")
print(f"Вес: {pokestats['weight']}")
print(f"Рост: {pokestats['height']}")
print(f"Способности: {pokestats['abilities']}")
