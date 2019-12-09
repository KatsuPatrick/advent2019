import math;
import sys;

inputStream = open("./input", "r");
seperatedInput = inputStream.readlines();
sanitisedInput = [];
for i in seperatedInput:
    sanitisedInput.append(i[:-1])
wire = {}
for j in sanitisedInput:
    wire[j[4:]] = j[:3];
totalOrbits = 0
for k in wire:
    totalOrbits += 1;
    prevObject = k;
    currentlyOrbiting = wire[prevObject];
    while currentlyOrbiting != "COM":
        totalOrbits += 1;
        prevObject = currentlyOrbiting;
        currentlyOrbiting = wire[prevObject];
print(totalOrbits)

mySubObjects = []
prevObject = "YOU";
currentlyOrbiting = wire[prevObject];
while currentlyOrbiting != "COM":
    mySubObjects.append(currentlyOrbiting);
    prevObject = currentlyOrbiting;
    currentlyOrbiting = wire[prevObject];

sanSubObjects = []
prevObject = "SAN";
currentlyOrbiting = wire[prevObject];
while currentlyOrbiting != "COM":
    sanSubObjects.append(currentlyOrbiting);
    prevObject = currentlyOrbiting;
    currentlyOrbiting = wire[prevObject];

for i in mySubObjects:
    if i in sanSubObjects:
        print(mySubObjects.index(i) + sanSubObjects.index(i));
        break;
