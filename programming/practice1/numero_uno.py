cels = float(input("Введите температуру в Цельсиях: "))
fahr = (cels * 1.8) + 32
kelv = cels + 273.15
print(f"Температура в Фаренгейтах: {round(fahr, 2)}, температура в Кельвинах: {round(kelv, 2)}")
