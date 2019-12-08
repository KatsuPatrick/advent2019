import math
import sys

inpInput = open("./input", "r")
sepInput = inpInput.readlines()
sanitised = []
for i in sepInput:
    sanitised.append(int(i[:-1]))
sumTotal = 0
for j in sanitised:
    sumTotal += (j//3) - 2
print(sumTotal)
