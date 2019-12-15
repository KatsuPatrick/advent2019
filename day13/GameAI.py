import os
import math

aiInput = [];
for i in range(1000):
    aiInput.append(0);
i = 0;
currentMaxScore = 0
while i < 1000000000:
    index = 0;
    aiInput[0] += 1;
    while aiInput.count(3) != 0:
        aiInput[aiInput.index(3) + 1] += 1
        aiInput[aiInput.index(3)] = 0
    #print(aiInput);
    i += 1
    #input();
    score = os.system("Part1And2.py " + str(aiInput))
    if score > currentMaxScore:
        currentMaxScore = score;
        print(currentMaxScore);
