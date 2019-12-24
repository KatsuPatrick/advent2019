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

#inputStream = open("./testInput2", "r");

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
maxX = 0
minX = math.inf;
maxY = 0
minY = math.inf;

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
        if portalPoint[0] < minX:
            minX = portalPoint[0];
        if portalPoint[0] > maxX:
            maxX = portalPoint[0];
        if portalPoint[1] < minY:
            minY = portalPoint[1];
        if portalPoint[1] > maxY:
            maxY = portalPoint[1];
        portalID = str(letterDict[i] + letterDict[j]);
        if portalID not in portalsDict:
            portalsDict[portalID] = [];
        portalsDict[portalID].append(portalPoint);
        if len(portalsDict[portalID]) > 2:
            print("o no", portalID, portalsDict[portalID]);
            input();

linkedMaze = {}

for i in portalsDict:
    if len(portalsDict[i]) == 2: # non entrance/exit marked points
        firstPointOutside = False;
        if portalsDict[i][0][0] == minX or portalsDict[i][0][0] == maxX or portalsDict[i][0][1] == minY or portalsDict[i][0][1] == maxY:
            firstPointOutside = True;
        for j in portalsDict[i]:
            if j not in linkedMaze:
                linkedMaze[j] = set();
        if firstPointOutside:
            linkedMaze[portalsDict[i][0]].add((portalsDict[i][1], -1));
            linkedMaze[portalsDict[i][1]].add((portalsDict[i][0], 1));
        else:
            linkedMaze[portalsDict[i][0]].add((portalsDict[i][1], 1));
            linkedMaze[portalsDict[i][1]].add((portalsDict[i][0], -1));

for i in traversableSet:
    if i not in linkedMaze:
        linkedMaze[i] = set();
    connectedPoints = adjacentTraversablePoints(i);
    for j in connectedPoints:
        linkedMaze[i].add((j, 0));



startPoint = portalsDict["AA"][0];
endPoint = portalsDict["ZZ"][0];

currentPoint = (startPoint, 0);
currentPath = [];
layerPath = [];

multiPathsTaken = {};
multiPathsTaken[0] = {};

currentLowestTraversal = 5500;
completedTraversal = False;

layeredTraversedPoints = {};
layeredTraversedPoints[0] = set();
layeredTraversedPoints[0].add(startPoint);

currentLayer = 0;

count = 0;
maxCount = 0;

while not completedTraversal:
    movedForwards = False;
    if currentPoint[1] not in layeredTraversedPoints:
        layeredTraversedPoints[currentPoint[1]] = set();
    if len(currentPath) < currentLowestTraversal:
        tempBranches = linkedMaze[currentPoint[0]].copy();
        # currentPoint is (coord, layer)
        branchesAvailable = set(); # format of: (coordTuple, layer of coord)
        sanitisedBranches = set(); # format of: coordTuple
        for i in tempBranches:
            branchesAvailable.add((i[0], currentPoint[1] + i[1]));
        for i in branchesAvailable:
            sanitisedBranches.add(i[0]);
        if len(currentPath) > 0:
            if currentPath[-1] in branchesAvailable:
                sanitisedBranches.remove(currentPath[-1][0]);
        if currentPoint[1] not in multiPathsTaken:
            multiPathsTaken[currentPoint[1]] = {};
        if currentPoint[0] not in multiPathsTaken[currentPoint[1]]:
            multiPathsTaken[currentPoint[1]][currentPoint[0]] = set();
        toRemove = set();
        for i in multiPathsTaken[currentPoint[1]][currentPoint[0]]:
            if i in sanitisedBranches:
                    toRemove.add(i);
        for i in toRemove:
            sanitisedBranches.remove(i);
        toPop = set();
        for i in branchesAvailable:
            if i[1] in layeredTraversedPoints:
                if i[0] in layeredTraversedPoints[i[1]]:
                    toPop.add(i);
            if i[1] == -1 or i[1] > 30: # ai is ez guys is fine
                toPop.add(i);
            if (i[0] == startPoint or i[0] == endPoint) and i[1] != 0:
                toPop.add(i);
        for i in toPop:
            if i[0] in sanitisedBranches:
                sanitisedBranches.remove(i[0]);



        #print(currentPoint, currentLayer, sanitisedBranches, branchesAvailable);
        #input();



        if len(sanitisedBranches) > 0:
            count += 1
            layeredTraversedPoints[currentPoint[1]].add(currentPoint[0]);

            newPoint = (random.choice(tuple(sanitisedBranches)));
            for i in branchesAvailable:
                if i[0] == newPoint:
                    newPoint = i;
            if len(newPoint) == 1:
                print("aaa");
                input();

            multiPathsTaken[currentPoint[1]][currentPoint[0]].add(newPoint[0]);
            currentPath.append((currentPoint[0], currentPoint[1]));
            currentPoint = newPoint;
            movedForwards = True;
            if newPoint[1] != currentPoint[1]:
                layerPath.append(currentPoint[1]);
                #print(currentLayer);
            #layeredTraversedPoints[currentLayer].add(currentPoint[0]);

            if currentPoint[0] == endPoint:
                if len(currentPath) < currentLowestTraversal:
                    currentLowestTraversal = len(currentPath);
                currentPoint = currentPath[-1];
                currentPath.pop();
    if not movedForwards:
        count -= 1;
        if currentPoint[0] in multiPathsTaken[currentPoint[1]]:
            if len(multiPathsTaken[currentPoint[1]]) == 0:
                layerPath.pop();
            multiPathsTaken[currentPoint[1]].pop(currentPoint[0]);
        if len(currentPath) > 0:
            currentPoint = currentPath[-1];
            currentPath.pop();
            layeredTraversedPoints[currentPoint[1]].remove(currentPoint[0]);
        else:
            completedTraversal = True;
    if count > maxCount:
        maxCount = count
print(currentLowestTraversal);
#print(maxCount);
#manage deletion of sub dicts? still need to make going backwards across layers update layer value
