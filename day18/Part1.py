import math;
import re;

inputStream = open("./input", "r");
seperatedInput = inputStream.readlines();
sanitisedInput = [];
for i in range(len(seperatedInput)):
    sanitisedInput.append(seperatedInput[i][:-1]);
#print(sanitisedInput);

gridInitialValues = {};
availableKeys = {};
lockedDoors = {};
start = None;
for i in range(len(sanitisedInput)):
    for j in range(len(sanitisedInput[i])):
        if sanitisedInput[i][j] != '#':
            gridInitialValues[(j, i)] = sanitisedInput[i][j];
            if sanitisedInput[i][j].isalpha():
                if sanitisedInput[i][j].islower():
                    availableKeys[(j, i)] = sanitisedInput[i][j];
                else:
                    lockedDoors[(j, i)] = sanitisedInput[i][j];
            if sanitisedInput[i][j] == '@':
                start = (j, i)

#print(availableKeys, lockedDoors);
adjacentTuple = ((0, 1), (1, 0), (0, -1), (-1, 0));

linkedGrid = {}; # every coord has a list of coordinates-modifier pairs they can move to; modifier None or the key that needs to have been visited

for i in gridInitialValues:
    linkedGrid[i] = [];
    for j in adjacentTuple:
        checkCoord = (i[0] + j[0], i[1] + j[1]);
        if checkCoord in gridInitialValues:
            if checkCoord in lockedDoors:
                toUnlock = lockedDoors[checkCoord].lower();
                linkedGrid[i].append((checkCoord, toUnlock));
            else:
                linkedGrid[i].append(tuple([checkCoord]));
keysVisited = set();
keysVisitedUnique = "";
keysOrderForUnique = {};
count = 0;
for i in availableKeys:
    keysVisitedUnique += "0";
    keysOrderForUnique[i] = count;
    count += 1;
currentPath = [];
currentShortest = math.inf;
currentLocation = start;
deadEndList = {}; # keys are keysVisitedUnique's
deadEndList[keysVisitedUnique] = set();
fromDeadEnd = False; #might be un-needed
completedSearch = False;
leashed = False;
while completedSearch == False:
    print(currentPath, currentLocation);
    actualLinks = []; # connected squares that aren't previous square, or a square that leads to dead end
    if len(currentPath) + 1 < currentShortest and len(keysVisited) != len(availableKeys):
        for i in linkedGrid[currentLocation]:
            if len(i) == 2: #door
                if i[1] in keysVisited:
                    actualLinks.append(i[0]);
            elif i[0] not in currentPath and i[0] not in deadEndList[keysVisitedUnique]:
                print(i[0], currentLocation, currentPath);
                input();
                actualLinks.append(i[0]);
    else:
        leashed = True;
    #print(actualLinks);
    if len(actualLinks) == 0: # if no viable connections, reverse
        if not leashed:
            fromDeadEnd = True;
            deadEndList[keysVisitedUnique] = currentLocation;
        if len(currentPath) == 0: # nowhere to reverse; completed search
            completedSearch = True;
        else:
            if currentLocation in availableKeys:
                localKey = availableKeys[currentLocation]
                keysVisited.pop(localKey);
                localKeyUnique = keysOrderForUnique[localKey];
                keysVisitedUnique = keysVisitedUnique[:localKeyUnique] + "0" + keysVisitedUnique[localKeyUnique + 1:];
            currentLocation = currentPath[-1];
            currentPath.pop();
    else: # somewhere to go
        #if len(actualLinks) == 0 and fromDeadEnd == True: #no choice in direction (previous on line isn't in actualLinks), reversing # shouldn't be needed
            #deadEndList.add(currentLocation)
        if fromDeadEnd == True: # first split after reversing
            fromDeadEnd = False;

        currentPath.append(currentLocation);
        currentLocation = actualLinks[0];
        if currentLocation in availableKeys:
            localKey = availableKeys[currentLocation];
            keysVisited.add(localKey);
            localKeyUnique = keysOrderForUnique[localKey];
            keysVisitedUnique = keysVisitedUnique[:localKeyUnique] + "1" + keysVisitedUnique[localKeyUnique + 1:];
            if keysVisitedUnique not in deadEndList:
                deadEndList[keysVisitedUnique] = set();
            if len(keysVisited) == len(availableKeys):
                if len(currentPath) + 1 < currentShortest:
                    currentShortest = len(currentPath) + 1;
                    print(currentShortest);
print(currentShortest);
print("Exited Successfully");
