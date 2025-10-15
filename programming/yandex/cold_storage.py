from datetime import datetime as dt
from decimal import Decimal
goods = {}
def add(items, title, amount, expiration_date=None):
    if expiration_date != None:
        date_as_string = dt.strptime(expiration_date, "%Y-%m-%d")
        expiration_date = dt.date(date_as_string)
    if not title in items:
        items[title] = [
            {"amount": Decimal(amount), "expiration_date": expiration_date}
        ]
    else:
        items[title].append({"amount": Decimal(amount), "expiration_date": expiration_date})

def add_by_note(items, note):
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

def find(items, needle):
    needle = needle.lower()
    keys = list(items.keys())
    found_list = []
    for key in keys:
        if needle in key.lower():
            found_list.append(key)
    return found_list

def amount(items, needle):
    needle = needle.lower()
    found = find(items, needle)
    quantity = Decimal("0")
    for key in found:
        for batch in items[key]:
            quantity += Decimal(batch["amount"])
    return quantity
