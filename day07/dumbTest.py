import math;
import sys;
import re;

inputStream = open("./dumbTest.txt", "r");
seperatedInput = inputStream.readlines();
sanitisedInput = []
for i in seperatedInput:
    sanitisedInput.append(i[:-1])
print(sanitisedInput)
max = 0
for i in sanitisedInput:
    if int(i) > max:
        max = int(i);
print(max);
