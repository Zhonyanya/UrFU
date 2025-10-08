def arabic_to_roman(number):
    """
    Переводит арабское число в римское

    Args:
        number (int): Арабское число, которое нужно перевести в римское
    Returns:
        result (str): Римское число 
    Example:
        >>>> arabic_to_roman(14)
        "XIV"
    """
    # Словарь соответствия арабских чисел римским
    roman_dict = {1000: "M", 900: "CM", 500: "D", 400: "CD",
                  100: "C", 90: "XC", 50: "L", 
                  40: "XL", 10: "X", 9: "IX", 
                     5: "V", 4: "IV", 1: "I"}
    
    result = ""
    remainder = number

    for num in roman_dict:
        if remainder > 0:
            multiplier = num
            roman_digit = roman_dict[num]
            # Количество раз, которое должна повториться римская цифра
            times = remainder // multiplier
            remainder = remainder % multiplier
            result += roman_digit * times
    return result

def roman_to_arabic(numeral):
    """
    Переводит римское число в арабское

    Args:
        number (str): Римское число, которое нужно перевести в арабское
    Returns:
        value (int): Арабское число 
    Example:
        >>>> roman_to_arabic("XIV")
        14
    """
    roman_dict = {"M": 1000, "CM": 900, "D": 500, "CD": 400,
                  "C": 100, "XC": 90, "L": 50,
                  "XL": 40, "X": 10, "IX": 9,
                  "V": 5, "IV": 4, "I": 1}
    value = 0
    last_digit = 0

    for roman_digit in numeral[::-1]:
        digit_value = roman_dict[roman_digit]
        # грубо говоря чекает там XI или IX и работает с этим
        if digit_value >= last_digit:
            value += digit_value
            last_digit = digit_value
        else:
            value -= digit_value
    return value
