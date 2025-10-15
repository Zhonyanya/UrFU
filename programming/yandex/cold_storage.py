from datetime import datetime as dt
from decimal import Decimal
goods = {}
def add(items: dict, title: str, amount: Decimal, expiration_date=None):
    """
    Добавляет в заданный список заданный продукт заданного количества и заданного срока годности

    Args:
        items (dict): Словарь, куда добавляем объекты
        title (str): Название продукта
        amount (Decimal): Количество продукта
        expiration_date (str): Срок годности
    
    Example:
        >>>> add(goods, 'Пельмени Универсальные', Decimal('2'), '2023-10-28')
        goods = {'Пельмени Универсальные': [{'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 10, 28)}]} 
    """
    if expiration_date != None:
        date_as_string = dt.strptime(expiration_date, "%Y-%m-%d")
        expiration_date = dt.date(date_as_string)
    if not title in items:
        items[title] = [
            {"amount": amount, "expiration_date": expiration_date}
        ]
    else:
        items[title].append({"amount": amount, "expiration_date": expiration_date})

def add_by_note(items: dict, note: str):
    """
    Добавляет в заданный список заданный продукт заданного количества и заданного срока годности через строчку

    Args:
        items (dict): Словарь, куда добавляем объекты
        note (str): Строка, из которой достаём параметры
    
    Example:
        >>>> add_by_note(goods, 'Яйца гусиные 4 2023-07-15')
        goods = {'Яйца гусиные': [{'amount': Decimal('4'), 'expiration_date': datetime.date(2023, 7, 15)}]} 
    """
    splitted_note = note.split()
    if "-" in splitted_note[-1]:
        amount = splitted_note[-2]
        expiration_date = splitted_note[-1]
        title = " ".join(splitted_note[:-2])
    else:
        amount = splitted_note[-1]
        expiration_date = None
        title = "".join(splitted_note[:-2])
    add(items, title, amount, expiration_date)

def find(items: dict, needle: str):
    """
    Ищет среди ключей словаря заданную подстроку

    Args:
        items (dict): Словарь, где ищем объекты
        needle (str): Подстрока, которую ищем
    
    Returns:
        found_list (list): Список найденных ключей
    
    Example:
        goods = {
    'Яйца': [{'amount': Decimal('1'), 'expiration_date': datetime.date(2023, 6, 24)}],
    'Яйца гусиные': [{'amount': Decimal('4'), 'expiration_date': datetime.date(2023, 7, 15)}],
    'Морковь': [{'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 6)}]
}
        >>>> find(goods, 'йц')
        ["Яйца", "Яйца гусиные"]
    """
    needle = needle.lower()
    keys = list(items.keys())
    found_list = []
    for key in keys:
        if needle in key.lower():
            found_list.append(key)
    return found_list

def amount(items: dict, needle: str):
    """
    Считает количество продуктов с таким же названием

    Args:
        items (dict): Словарь, где считаем количество продуктов
        needle (str): Подстрока, по которой ищем ключи и потом считаем

    Returns:
        quantity (Decimal): Количество продуктов
    
    Example:
        goods = {
    'Яйца': [{'amount': Decimal('1'), 'expiration_date': None}],
    'Морковь': [
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
        {'amount': Decimal('3'), 'expiration_date': datetime.date(2023, 8, 6)}
    ],
    'Вода': [{'amount': Decimal('2.5'), 'expiration_date': None}]
}
        >>>> amount(goods, "морковь")
        5
    """
    needle = needle.lower()
    found = find(items, needle)
    quantity = Decimal("0")
    for key in found:
        for batch in items[key]:
            quantity += Decimal(batch["amount"])
    return quantity
