n = int(input())
primelist = [i for i in range(2, n + 1)]
for num in primelist:
    for num2 in primelist:
        if num2 % num == 0 and num2 != num:
            primelist.remove(num2)
print(primelist)
