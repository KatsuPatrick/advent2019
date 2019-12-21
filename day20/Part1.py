import math;
import re;
import random;

def adjacentTraversablePoints(point):
    global traversableSet;
    returnVar = []
    if (point[0] + 1, point[1]) in traversableSet:
        returnVar.append((point[0] + 1, point[1]));
    if (point[0] - 1, point[1]) in traversableSet:
        returnVar.append((point[0] - 1, point[1]));
    if (point[0], point[1] + 1) in traversableSet:
        returnVar.append((point[0], point[1] + 1));
    if (point[0], point[1] - 1) in traversableSet:
        returnVar.append((point[0], point[1] - 1));
    return returnVar;

def adjacentTraversablePointFromTwo(point1, point2):
    global traversableSet;
    if (point1[0] + 1, point1[1]) in traversableSet:
        return (point1[0] + 1, point1[1]);
    elif (point1[0] - 1, point1[1]) in traversableSet:
        return (point1[0] - 1, point1[1]);
    elif (point1[0], point1[1] + 1) in traversableSet:
        return (point1[0], point1[1] + 1);
    elif (point1[0], point1[1] - 1) in traversableSet:
        return (point1[0], point1[1] - 1);
    elif (point2[0] + 1, point2[1]) in traversableSet:
        return (point2[0] + 1, point2[1]);
    elif (point2[0] - 1, point2[1]) in traversableSet:
        return (point2[0] - 1, point2[1]);
    elif (point2[0], point2[1] + 1) in traversableSet:
        return (point2[0], point2[1] + 1);
    elif (point2[0], point2[1] + 1) in traversableSet:
        return (point2[0], point2[1] + 1);
    else:
        return None;

inputStream = open("./input", "r");

#inputStream = open("./testInput", "r");

seperatedInput = inputStream.readlines();
traversableSet = set();
letterDict = {};
for j in range(len(seperatedInput)):
    for i in range(len(seperatedInput[j])):
        var = seperatedInput[j][i];
        if var != " " and var != "#" and var != "\n":
            if var == ".":
                traversableSet.add((i, j));
            else:
                letterDict[(i, j)] = var;

portalsDict = {};

for i in letterDict:
    # each pair read only once by only checking down and right
    skip = False;
    j = None;
    if (i[0] + 1, i[1]) in letterDict:
        j = (i[0] + 1, i[1]);
    elif (i[0], i[1] + 1) in letterDict:
        j = (i[0], i[1] + 1);
    else:
        skip = True;
    if not skip:
        portalPoint = adjacentTraversablePointFromTwo(i, j);
        portalID = str(letterDict[i] + letterDict[j]);
        if portalID not in portalsDict:
            portalsDict[portalID] = [];
        portalsDict[portalID].append(portalPoint);
        if len(portalsDict[portalID]) > 2:
            print("o no", portalID, portalsDict[portalID]);
            input();

linkedMaze = {}

for i in portalsDict:
    if len(portalsDict[i]) == 2:
        for j in portalsDict[i]:
            if j not in linkedMaze:
                linkedMaze[j] = set();
        linkedMaze[portalsDict[i][0]].add(portalsDict[i][1]);
        linkedMaze[portalsDict[i][1]].add(portalsDict[i][0]);

for i in traversableSet:
    if i not in linkedMaze:
        linkedMaze[i] = set();
    connectedPoints = adjacentTraversablePoints(i);
    for j in connectedPoints:
        linkedMaze[i].add(j);


startPoint = portalsDict["AA"][0];
endPoint = portalsDict["ZZ"][0];

currentPoint = startPoint;
currentPath = [];

pathsTaken = {};

currentLowestTraversal = math.inf;
completedTraversal = False;

count = 0

while not completedTraversal:
    movedForwards = False;
    #print(currentPath, currentLowestTraversal, linkedMaze[currentPoint], pathsTaken, movedForwards)
    if len(currentPath) < currentLowestTraversal:
        branchesAvailable = linkedMaze[currentPoint].copy();
        if len(currentPath) > 0:
            if currentPath[-1] in branchesAvailable:
                branchesAvailable.remove(currentPath[-1]);
        if currentPoint not in pathsTaken:
            pathsTaken[currentPoint] = set();
        for i in pathsTaken[currentPoint]:
            if i in branchesAvailable:
                branchesAvailable.remove(i);
        toPop = set();
        for i in branchesAvailable:
            if i in currentPath:
                toPop.add(i);
        for i in toPop:
            branchesAvailable.remove(i);
        if len(branchesAvailable) > 0:
            newPoint = random.choice(tuple(branchesAvailable));
            pathsTaken[currentPoint].add(newPoint);
            currentPath.append(currentPoint);
            currentPoint = newPoint;
            movedForwards = True;
            if currentPoint == endPoint:
                count += 1
                if len(currentPath) < currentLowestTraversal:
                    currentLowestTraversal = len(currentPath);
                currentPoint = currentPath[-1];
                currentPath.pop();
    if not movedForwards:
        if currentPoint in pathsTaken:
            pathsTaken.pop(currentPoint);
        if len(currentPath) > 0:
            currentPoint = currentPath[-1];
            currentPath.pop();
        else:
            completedTraversal = True;
print(currentLowestTraversal);
