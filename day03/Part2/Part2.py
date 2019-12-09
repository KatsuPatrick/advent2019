import math;
import re;
import collections;

def dictConnect(currentWire, point1, point2):
    if point1 != point2:
        if not point1 in currentWire:
            currentWire[point1] = set();
        if not point2 in currentWire:
            currentWire[point2] = set();
        currentWire[point1].add(point2);
        currentWire[point2].add(point1);
    return currentWire;

def moveDirectional(currentWire, previousCorner, instructionInt, intHori, intVert, wireOrder, orderPointer):
    previousStep = previousCorner;
    j = 0
    while j < instructionInt:
        currentLocation = (previousStep[0] + intHori, previousStep[1] + intVert);
        currentWire = dictConnect(currentWire, previousStep, currentLocation);
        if currentLocation not in wireOrder:
            wireOrder[currentLocation] = orderPointer + j + 1;
        previousStep = currentLocation;
        j += 1;
    orderPointer += j;
    returnTuple = (currentWire, previousStep, wireOrder, orderPointer);
    return returnTuple;

def move(currentWire, previousCorner, instruction, wireOrder, orderPointer):
    if instruction[0] == "U":
        return moveDirectional(currentWire, previousCorner, int(instruction[1:]), 0, 1, wireOrder, orderPointer);
    elif instruction[0] == "D":
        return moveDirectional(currentWire, previousCorner, int(instruction[1:]), 0, -1, wireOrder, orderPointer);
    elif instruction[0] == "R":
        return moveDirectional(currentWire, previousCorner, int(instruction[1:]), 1, 0, wireOrder, orderPointer);
    elif instruction[0] == "L":
        return moveDirectional(currentWire, previousCorner, int(instruction[1:]), -1, 0, wireOrder, orderPointer);
    return None;

def mapWire(wirePath, startCoord, wireInstructions, wireOrder):
    previousCorner = startCoord
    pointer = 0;
    orderPointer = 0
    while pointer < len(wireInstructions):
        returnTuple = move(wirePath, previousCorner, wireInstructions[pointer], wireOrder, orderPointer);
        if returnTuple == None:
            continue;
        wirePath = returnTuple[0];
        previousCorner = returnTuple[1];
        wireOrder = returnTuple[2];
        orderPointer = returnTuple[3];
        pointer += 1;
    returnTuple = (wirePath, wireOrder);
    return returnTuple;

def mergeAndIntersectWires(wire1, wire2, excludedFromIntersectPoints):
    combinedWire = {};
    intersectPoints = set();
    for i in wire1:
        combinedWire[i] = set();
        for j in wire1[i]:
            combinedWire[i].add(j);
        if i in wire2:
            if i not in excludedFromIntersectPoints:
                intersectPoints.add(i);
            for j in wire2[i]:
                combinedWire[i].add(j);
    for i in wire2:
        if i not in wire1:
            combinedWire[i] = set();
            for j in wire2[i]:
                combinedWire[i].add(j);
    returnTuple = (combinedWire, intersectPoints);
    return returnTuple;

def shortestPathFromTo(wire, pointsFrom, pointTo):
    #takes a wire, a set of points to check from, and a point to check to, then finds the shortest path from any single one of the pointsFrom, and returns it as a list of points.
    # RTFQ btw
    currentShortestPaths = {};
    currentShortestPathsLengths = {};
    if pointTo not in wire:
        return None;
    if pointTo in pointsFrom:
        return [pointTo];
    for startPoint in pointsFrom:
        currentShortestPaths[startPoint] = [];
        currentShortestPathsLengths[startPoint] = math.inf;
        enteredPathsOnCurrentTree = {}; # keys of points in the current path; values of the nodes traversed from there
        travellingForwards = True;
        finishedCurrentPoint = False;
        currentPath = [];
        currentPath.append(startPoint);

        # don't go to a point in the current path when going forwards
        # when coming back to a node already visited in the current path, do not take a node already taken; if all already have been, go back another point
        # when reaching goal, stop, note the list and distance if shortest, then go back.
        # don't explore further than the current shortest path.
        # stop when that algo has nowhere to go

        while not finishedCurrentPoint:
            if len(currentPath) == 0: # if finished (on this point)
                finishedCurrentPoint = True;
            else:
                currentLocation = currentPath[-1];
                branchList = list(wire[currentLocation]);
                if travellingForwards:
                    enteredPathsOnCurrentTree[currentLocation] = set();
                if currentLocation == pointTo:
                    if len(currentPath) < currentShortestPathsLengths[startPoint]:
                        currentShortestPaths[startPoint] = currentPath.copy();
                        currentShortestPathsLengths[startPoint] = len(currentPath);
                if len(currentPath) > 1: # if there is a point behind to check
                    branchList.remove(currentPath[-2]);
                if not travellingForwards: # if just came backwards (i.e. there are other branches to remove)
                    for i in enteredPathsOnCurrentTree[currentLocation]:
                        branchList.remove(i);
                for j in branchList:
                    if j in currentPath:
                        branchList.remove(j);
                if len(branchList) > 0 and len(currentPath) < currentShortestPathsLengths[startPoint]: # if still any branches remain, go to one, unless would exceed current shortest. (FORWARDS)
                    travellingForwards = True;
                    nextLocation = branchList[0];
                    currentPath.append(nextLocation);
                    enteredPathsOnCurrentTree[currentLocation].add(nextLocation);
                else: # (BACKWARDS)
                    travellingForwards = False;
                    currentPath.pop();
                    enteredPathsOnCurrentTree.pop(currentLocation);
    shortestStartPoint = None;
    shortestStartPointLength = math.inf;
    for i in currentShortestPaths:
        if len(i) < shortestStartPointLength:
            shortestStartPoint = i;
            shortestStartPointLength = len(i);
    return currentShortestPaths[shortestStartPoint];

def sanitiseInstr(instructions):
    instructions = re.split(",", instructions);
    return instructions;

def findClosestCircuitIntersect(intersectPoints, wireOrder1, wireOrder2):
    smallestCircuitIntersect = None;
    smallestCircuitDistance = math.inf;
    for i in intersectPoints:
        if wireOrder1[i] + wireOrder2[i] < smallestCircuitDistance:
            smallestCircuitIntersect = i;
            smallestCircuitDistance = wireOrder1[i] + wireOrder2[i];
    returnTuple = (smallestCircuitIntersect, smallestCircuitDistance);
    return returnTuple;

firstWireInstructions = "R991,U77,L916,D26,R424,D739,L558,D439,R636,U616,L364,D653,R546,U909,L66,D472,R341,U906,L37,D360,L369,D451,L649,D521,R2,U491,R409,U801,R23,U323,L209,U171,L849,D891,L854,U224,R476,D519,L937,U345,R722,D785,L312,D949,R124,U20,R677,D236,R820,D320,L549,D631,R42,U621,R760,U958,L925,U84,R914,U656,R598,D610,R397,D753,L109,U988,R435,U828,R219,U583,L317,D520,L940,D850,R594,D801,L422,U292,R883,U204,L76,U860,L753,U483,L183,U179,R441,U163,L859,U437,L485,D239,R454,D940,R689,D704,R110,D12,R370,D413,L192,D979,R990,D651,L308,U177,R787,D717,R245,U689,R11,D509,L680,U228,L347,D179,R508,D40,L502,U689,L643,U45,R884,D653,L23,D918,L825,D312,L691,U292,L285,D183,R997,U427,L89,U252,R475,U217,R16,U749,L578,D931,L273,U509,L741,U97,R407,U275,L605,U136,L558,U318,R478,U505,R446,U295,R562,D646,R988,D254,L68,U645,L953,U916,L442,D713,R978,U540,R447,U594,L804,U215,R95,D995,R818,D237,R212,U664,R455,D684,L338,U308,R463,D985,L988,D281,R758,U510,L232,U509,R289,D90,R65,D46,R886,D741,L327,U755,R236,U870,L764,U60,R391,U91,R367,U587,L651,D434,L47,U954,R707,D336,L242,D387,L410,D19,R203,D703,L228,U292,L19,U916,R411,U421,L726,U543,L240,U755,R157,U836,L397,U71,L125,D934,L723,D145,L317,D229,R863,U941,L926,D55,L2,D452,R895,D670,L216,U504,R66,U696,L581,U75,L235,U88,L609,U415,L850,U21,L109,U416,R408,D367,R823,D199,L718,U136,L860,U780,L308,D312,R230,D671,R477,D672,L94,U307,R301,D143,L300,D792,L593,D399,R840,D225,R680,D484,L646,D917,R132,D213,L779,D143,L176,U673,L772,D93,L10,D624,L244,D993,R346";
secondWireInstructions = "L997,U989,L596,U821,L419,U118,R258,D239,R902,D810,R553,D271,R213,D787,R723,D57,L874,D556,R53,U317,L196,D813,R500,U151,R180,D293,L415,U493,L99,U482,R517,U649,R102,U860,R905,D499,R133,D741,R394,U737,L903,U800,R755,D376,L11,U751,R539,U33,R539,U30,L534,D631,L714,U190,L446,U409,R977,D731,R282,U244,R29,D212,L523,D570,L89,D327,R178,U970,R435,U250,R213,D604,R64,D348,R315,D994,L508,D261,R62,D50,L347,U183,R410,D627,L128,U855,L803,D695,L879,U857,L629,D145,L341,D733,L566,D626,L302,U236,L55,U428,R183,U254,R226,D228,R616,U137,L593,U204,R620,U624,R605,D705,L263,D568,R931,D464,R989,U621,L277,U274,L137,U768,L261,D360,L45,D110,R35,U212,L271,D318,L444,D427,R225,D380,L907,D193,L118,U741,L101,D298,R604,D598,L98,U458,L733,U511,L82,D173,L644,U803,R926,D610,R24,D170,L198,U766,R656,D474,L393,D934,L789,U92,L889,U460,L232,U193,L877,D380,L455,D526,R899,D696,R452,U95,L828,D720,R370,U664,L792,D204,R84,D749,R808,U132,L152,D375,R19,U164,L615,D121,R644,D289,R381,U126,L304,U508,L112,D268,L572,D838,L998,U127,R500,D344,R694,U451,L846,D565,R158,U47,L430,U214,R571,D983,R690,D227,L107,U109,L286,D66,L544,U205,L453,U716,L36,U672,L517,U878,L487,U936,L628,U253,R424,D409,R422,U636,R412,U553,R59,D332,R7,U495,L305,D939,L428,D821,R749,D195,R531,D898,R337,D303,L398,D625,R57,D503,L699,D553,L478,U716,R897,D3,R420,U903,R994,U864,L745,U205,R229,U126,L227,D454,R670,U605,L356,U499,R510,U238,L542,D440,R156,D512,L237,D341,L439,U642,R873,D650,R871,D616,R322,U696,R248,D746,R990,U829,R812,U294,L462,U740,R780";

#TESTING (USE THESE BTW THIS TAKES A LONG TIME ON ACC DATA)
#firstWireInstructions = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
#secondWireInstructions = "U62,R66,U55,R34,D71,R55,D58,R83"

#firstWireInstructions = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
#secondWireInstructions = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

#firstWireInstructions = "R8,U5,L5,D3"
#secondWireInstructions = "U7,R6,D4,L4"
#TESTING

firstSanitised = sanitiseInstr(firstWireInstructions);
secondSanitised = sanitiseInstr(secondWireInstructions);

firstWirePath = {};
secondWirePath = {};
origin = (0, 0);

firstWireOrder = {origin: 0};
secondWireOrder = {origin: 0};

firstWireReturn = mapWire(firstWirePath, origin, firstSanitised, firstWireOrder);
secondWireReturn = mapWire(secondWirePath, origin, secondSanitised, secondWireOrder);

firstWirePath = firstWireReturn[0];
secondWirePath = secondWireReturn[0];

firstWireOrder = firstWireReturn[1];
secondWireOrder = secondWireReturn[1];

excludedPoints = set();
excludedPoints.add(origin);

mergeAndIntersect = mergeAndIntersectWires(firstWirePath, secondWirePath, excludedPoints);
unionWire = mergeAndIntersect[0];
intersectPoints = mergeAndIntersect[1];

circuitDistanceAndIntersect = findClosestCircuitIntersect(intersectPoints, firstWireOrder, secondWireOrder);
print(circuitDistanceAndIntersect);
#shortestIntersectToOriginPath = shortestPathFromTo(unionWire, intersectPoints, origin);
#print(shortestIntersectToOriginPath);
#print(len(shortestIntersectToOriginPath));
