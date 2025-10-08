def print_pack_report(number):
    """
    Определяет, будем ли мы фасовать по 3 или по 5, по 5, по 3 или не будем вовсе

    Args:
        number (int): Число, от которого идёт отсчёт назад
    """
    for n in range(number, 0, -1):
        if n % 15 == 0:
            print(f"{n} - расфасуем по 3 или по 5")
        elif n % 5 == 0 and n % 3 != 0:
            print(f"{n} - расфасуем по 5")
        elif n % 3 == 0:
            print(f"{n} - расфасуем по 3")
        else:
            print(f"{n} - не заказываем!")
