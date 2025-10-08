from random import choices
choice_list = ["Верхний регистр", "Нижний регистр", "Специальные символы", "Цифры"]
choice_dict = {"Верхний регистр": "QWERTYUIOPASDFGHJKLZXCVBNM", "Нижний регистр": "qwertyuiopasdfghjklzxcvbnm",
               "Специальные символы": "!@#$%^&*_", "Цифры": "0123456789"}
char_list = ""
password_length = int(input("Введите желаемую длину пароля: "))
choice = 1
flag = True
if password_length > 0:
    while choice != 0:
        print("==================================")
        # Для вывода вариантов ответа
        for i in range(len(choice_list)):
            print(f"{i + 1}. {choice_list[i]}")
        print("0. Закончить работу")
        print("==================================")
        choice = int(input("Пожалуйста, введите номер настройки: "))
        if choice == 0:
            print("Спасибо за использование!")
            break   
        elif len(str(choice)) != 1 or choice > len(choice_list):
            print("Ошибка!")
        else:
            # Добавляет список символов текущей настройки к общему списку, из которого составляется пароль
            char_list += choice_dict[choice_list[choice - 1]]
            choice_list.pop(choice - 1)
    if len(char_list) != 0:
        # Случайно выбирает символы (с возможностью повторений) из строчки char_list
        end_password = ''.join(choices(char_list, k=password_length))
        print(f"Ваш пароль: {end_password}")
else:
    print("Респект")
print("==================================")
