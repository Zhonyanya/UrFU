import requests
response = requests.get("https://pokeapi.co/api/v2/pokemon")
responselist = response.json()["results"]
pokedict = dict()
for pokemon in responselist:
    pokedict[pokemon['name']] = pokemon['url'] 
def get_pokemon_stats(pokemon_name: str):
    """
    Выдаёт данные покемона: имя, тип, вес, рост, !имена! способностей

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

    moves = get_poke["moves"]
    movelist = []
    for move in moves:
        movelist.append(move["move"]["name"])
    return {"name": pokemon_name, "types": types, "weight": weight,
            "height": height, "moves": movelist}
