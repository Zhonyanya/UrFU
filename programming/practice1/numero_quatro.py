import random
charcount = 0
numcount = 0
symbcount = 0
charlist = "QWERTYUIOPASDFGHJKLZXCVBNM"
numlist = "0123456789"
symblist = "!@#$%^&*"
password = []
for _ in range(3):
    password.append(random.choice(charlist))
for _ in range(3):
    password.append(random.choice(numlist))
for _ in range(2):
    password.append(random.choice(symblist))
random.shuffle(password)
print("".join(password))
