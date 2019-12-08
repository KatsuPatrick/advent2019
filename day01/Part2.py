import math
import sys

inpInput = open("./input", "r")
sepInput = inpInput.readlines()
sanitised = []
for i in sepInput:
    sanitised.append(int(i[:-1]))
sumTotal = 0
for j in sanitised:
    sumOf = 0
    temp = 0
    while j > 0:
        sumOf += temp
        temp = (j//3) - 2
        j = temp
    sumTotal += sumOf
print(sumTotal)
