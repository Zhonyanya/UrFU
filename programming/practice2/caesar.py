engalph = "abcdefghijklmnopqrstuvwxyz"
rusalph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
skiplist = ' 1234567890_-+=/*!@#$%^&*()[]{}":;<>,.?`~\|'

def define_lang(word):
    """
    Определяет язык переданной фразы

    Args:
        word (str): Введённая фраза

    Returns: 
        lang (str): Определённый язык
    """
    word = word.lower()
    lang = "rus"
    flag = True
    for letter in word:
        if letter in skiplist:
            continue
        if not letter in engalph:
            flag = False
    if flag:
        lang = "eng"
    for letter in word:
        if letter in skiplist:
            continue
        if not letter in rusalph:
            lang = "none"
    return lang

def cipher(word, key=3):
    """
    Зашифровывает фразу шифром Цезаря
    
    Args:
        word (str): Фраза, которую надо зашифровать
        key (int): Ключ шифрования
    
    Returns:
        str: Зашифрованная фраза
    """
    lang = define_lang(word)
    if lang == "none":
        return "Фраза введена некорректно"
    else:
        newword = list(word)
        if lang == "rus":
            for i in range(len(word)):
                if word[i] in skiplist:
                    continue
                letter_number = rusalph.find(word[i].lower())
                # Прибавляем сдвиг к номеру буквы и находим остаток от деления на длину русского алфавита для шифрования
                encrypted_letter = rusalph[(letter_number + key) % 33]
                if word[i].isupper():
                    newword[i] = encrypted_letter.upper()
                else:
                    newword[i] = encrypted_letter
        else:
            for i in range(len(word)):
                letter_number = engalph.find(word[i].lower())
                # Прибавляем сдвиг к номеру буквы и находим остаток от деления на длину английского алфавита для шифрования
                encrypted_letter = engalph[(letter_number + key) % 26]
                if word[i].isupper():
                    newword[i] = encrypted_letter.upper()
                else:
                    newword[i] = encrypted_letter
        return "".join(newword)

def decipher(word, key=3):
    """
    Расшифровывает фразу, зашифрованную шифром Цезаря
    
    Args:
        word (str): Зашифрованная фраза
        key (int): Ключ шифрования
    
    Returns:
        str: Расшифрованная фраза
    """
    lang = define_lang(word)
    if lang == "none":
        return "Фраза введено некорректно"
    else:
        newword = list(word)
        if lang == "rus":
            for i in range(len(word)):
                if word[i] in skiplist:
                    continue
                letterNum = rusalph.find(word[i].lower())
                # Вычитаем сдвиг и находим остаток от деления на длину русского алфавита для расшифровки
                decrypted_letter = rusalph[(letterNum - key) % 33]
                if word[i].isupper():
                    newword[i] = decrypted_letter.upper()
                else:
                    newword[i] = decrypted_letter
        else:
            for i in range(len(word)):
                letter_number = engalph.find(word[i].lower())
                # Вычитаем сдвиг и находим остаток от деления на длину английского алфавита для расшифровки
                decrypted_letter = engalph[(letter_number - key) % 26]
                if word[i].isupper():
                    newword[i] = decrypted_letter.upper()
                else:
                    newword[i] = decrypted_letter
        return "".join(newword)
