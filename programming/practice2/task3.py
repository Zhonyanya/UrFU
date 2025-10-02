def print_pack_report(number):
    for n in range(number, 0, -1):
        if n % 15 == 0:
            print(f"{n} - расфасуем по 3 или по 5")
        elif n % 5 == 0 and n % 3 != 0:
            print(f"{n} - расфасуем по 5")
        elif n % 3 == 0:
            print(f"{n} - расфасуем по 3")
        else:
            print(f"{n} - не заказываем!")
