s = input().lower()
squantity = dict()
for symb in s:
    if not symb in squantity:
        squantity[symb] = 1
    else:
        squantity[symb] += 1
sorted_values = sorted(squantity.items(), key=lambda item: item[1], reverse=True)
print(sorted_values[0][0], sorted_values[1][0], sorted_values[2][0])
