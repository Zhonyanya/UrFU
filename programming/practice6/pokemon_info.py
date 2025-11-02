import requests
response = requests.get("https://pokeapi.co/api/v2/pokemon")
responselist = response.json()["results"]
pokedict = dict()
for pokemon in responselist:
    pokedict[pokemon['name']] = pokemon['url']
def get_pokemon_stats(pokemon_name: str):
    """
    Выдаёт данные покемона: имя, типы, вес, рост, названия способностей

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
# print(get_pokemon_stats("beedrill")["abilities"])
