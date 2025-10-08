def find_all(where_to_find, what_to_find):
    """
    Находит все индексы букв в строке

    Args:
        where_to_find (str): Строка, где надо искать
        what_to_find (str): Строка, которую надо искать
    Returns:
        found_indexes (list): Список найденных индексов
    Example:
        >>>> find_all("бибки", "б")
        [0, 2]
    """
    where_to_find = where_to_find.lower()
    found_indexes = []
    for i in range(len(where_to_find)):
        if where_to_find[i] == what_to_find:
            found_indexes.append(i)
    return found_indexes
def replace(list_to_replace, word, index_list):
    """
    Заменяет элементы списка на соответствующие им буквы из слова
    
    Args:
        list_to_replace (list): Список символов, где надо заменить
        word (str): Слово, из которого надо брать символы и вставлять в список
        index_list (list): Список индексов
    Returns:
        list_to_replace (list): Изменённый список
    Example:
        >>>> replace(["_", "_", "_", "_"], "муха", "[1, 2]")
        ["_", "у", "х", "_"]
    """
    for index in index_list:
        list_to_replace[index] = word[index]
    return list_to_replace
# Словарь картинок для виселицы. Делал до смешного долго
hanged_pictures = {10: 
""""|
    |
    |
    |""",
                    9: 
""""   ————
    |
    |
    |
    |    """,
                    8:
""""   ————
    |/
    |
    |
    |    """,
                    7:
""""   ————
    |/ |
    |
    |
    |    """,
                     6:
""""   ————
    |/ |
    |  °
    |
    |    """,
                    5:
""""   ————
    |/ |
    |  °
    |  |
    |    """,
                    4:
""""   ————
    |/ |
    |  °
    |  |\\
    |       """,
                    3:
""""   ————
    |/ |
    |  °
    | /|\\
    |       """,
                    2:
""""   ————
    |/ |
    |  °
    | /|\\
    |   \    """,
                    1:
""""   ————
    |/ |
    |  °
    | /|\\
    | / \    """,
                    0:
"Вы проиграли!"    }
  
word = "Галлюциноген"
mistakes = 10
guessed_word = ["_"] * len(word)
# Пока не потратили все ошибки и не угадали слово
while mistakes != 0 and "".join(guessed_word) != word:
    guess = input("Введите букву: ")
    if len(guess) != 1:
        print("Пожалуйста, введите одну букву")
    if guess in word:
        #Ищем индексы и меняем список с подчёркиваниями по ним
        found_indexes = find_all(word, guess)
        guessed_word = replace(guessed_word, word, found_indexes)
        print(''.join(guessed_word))
    else:
        mistakes -= 1
        print(hanged_pictures[mistakes])
        print(f"Ошибка! Ошибок осталось {mistakes} штук")
if mistakes != 0:
    print("Поздравляю, вы победил!")
