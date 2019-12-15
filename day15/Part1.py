import math;

def opcodeSplit(instruction):
    strInstruction = str(instruction);
    for i in range(5 - len(strInstruction)):
        strInstruction = "0" + strInstruction;
    #print((strInstruction[3], strInstruction[:3]));
    return (strInstruction[3:], strInstruction[:3]);

def binEnoughParameters(fullInput, currentExecutePointer, countParamRequired):
    if ((len(fullInput) - currentExecutePointer - countParamRequired) < 1):
        return False;
    return True;

def retrieve(memory, param, mode, relativeBase):
    #print(param, mode)
    if mode == "0":
        return accessMemory(memory, param);
    elif mode == "1":
        return param;
    elif mode == "2":
        return int(accessMemory(memory, param)) + relativeBase;
    return None;

def retrieveAllParams(memory, currentExecutePointer, fullMode, countParamRequired, relativeBase):
    paramList = []
    for i in range(countParamRequired):
        paramList.append(retrieve(memory, int(currentExecutePointer) + 1 + i, fullMode[-1 - i], relativeBase))
    return tuple(paramList);

def inputToMemory(fullInput):
    memory = {}
    for i in range(0, len(fullInput)):
        memory[i] = str(fullInput[i]);
    return memory;

def writeToMemory(memory, location, value):
    memory[int(location)] = str(value);
    return memory;

def accessMemory(memory, location):
    if int(location) not in memory:
        memory[int(location)] = "0";
    return memory[int(location)];


def isAdjacentUnexplored(position):
    global robotAreaGrid;

    if robotAreaGrid[(position[0], position[1] + 1)] == 0:
        return (position[0], position[1] + 1);
    elif robotAreaGrid[(position[0] + 1, position[1])] == 0:
        return (position[0] + 1, position[1]);
    elif robotAreaGrid[(position[0], position[1] - 1)] == 0:
        return (position[0], position[1] - 1);
    elif robotAreaGrid[(position[0] - 1, position[1])] == 0:
        return (position[0] - 1, position[1]);
    else:
        return False;

def returnSurrounding(position):
    global robotAreaGrid;
    surrounding = []
    if robotAreaGrid[(position[0], position[1] + 1)] != 2:
        surrounding.append((position[0], position[1] + 1));
    if robotAreaGrid[(position[0] + 1, position[1])] != 2:
        surrounding.append((position[0] + 1, position[1]));
    if robotAreaGrid[(position[0], position[1] - 1)] != 2:
        surrounding.append((position[0], position[1] - 1));
    if robotAreaGrid[(position[0] - 1, position[1])] != 2:
        surrounding.append((position[0] - 1, position[1]));
    #if position == (-7, 4):
        #print(surrounding)
        #input();
    return surrounding;

def isPositionAdjacent(positionFrom, positionTo):
    global robotAreaGrid;
    if (positionFrom[0], positionFrom[1] + 1) == positionTo or (positionFrom[0], positionFrom[1] - 1) == positionTo or (positionFrom[0] - 1, positionFrom[1]) == positionTo or (positionFrom[0] + 1, positionFrom[1]) == positionTo:
        return True;
    else:
        return False;

def searchForUnexplored(traversePosition, maxMovementToFind, positionFrom):
    global robotAreaGrid;

    adjCheckVar = isAdjacentUnexplored(traversePosition);

    #print(traversePosition, maxMovementToFind, adjCheckVar)
    #if maxMovementToFind > 20:
        #print(maxMovementToFind, traversePosition);

    if adjCheckVar != False:
        unxSearchVar = []
        unxSearchVar.append(adjCheckVar);
        unxSearchVar.append(traversePosition);
        return unxSearchVar;

    if maxMovementToFind != 0:
        for i in returnSurrounding(traversePosition):
            if i != positionFrom:
                unxSearchVar = searchForUnexplored(i, maxMovementToFind - 1, traversePosition);
            else:
                unxSearchVar = None;
            if unxSearchVar != False and unxSearchVar != None:
                unxSearchVar.append(traversePosition);
                #print(unxSearchVar);
                return unxSearchVar;
    else:
        return False;


def findFastestPath(positionFrom, positionTo, lessStepsThan, prevPosition):
    global robotAreaGrid;

    if lessStepsThan != 0:
        ipaCheckVar = isPositionAdjacent(positionFrom, positionTo);
        if ipaCheckVar == True:
            return 1;
        for i in returnSurrounding(positionFrom):
            if positionFrom == (0, 0):
                print(i);
            if i != prevPosition:
                ffpVar = findFastestPath(i, positionTo, lessStepsThan - 1, positionFrom);
                #print(positionFrom, i, lessStepsThan);
            else:
                ffpVar = False;
            if ffpVar != False and ffpVar != None:
                return ffpVar + 1;
        return False;
    else:
        return False;



def closestUnexploredMovement():
    global robotPosition;
    global robotAreaGrid;

    traversePosition = robotPosition;
    foundUnexplored = False;
    maxMovementToFind = 0;
    while True:
        maxMovementToFind += 1;
        adjCheckVar = isAdjacentUnexplored(traversePosition);
        if adjCheckVar != False:
            return [adjCheckVar];
        unxSearchVar = searchForUnexplored(traversePosition, maxMovementToFind, traversePosition);
        #print(unxSearchVar, unxSearchVar == None);
        if unxSearchVar != False and unxSearchVar != None:
            #print(unxSearchVar);
            unxSearchVar.pop()
            return unxSearchVar;

def relativeSpace(robotPosition, direction):
    if direction == 1:
        return (robotPosition[0], robotPosition[1] + 1);
    elif direction == 2:
        return (robotPosition[0], robotPosition[1] - 1);
    elif direction == 3:
        return (robotPosition[0] - 1, robotPosition[1]);
    elif direction == 4:
        return (robotPosition[0] + 1, robotPosition[1]);
    print("Direction unrecognised");
    return False;

def recieveInput():
    global robotPosition;
    global robotCommandHistory;
    global robotMovementHistory;
    global robotPositionHistory;
    global robotAreaGrid;
    global plannedMovement;
    global oxygenPosition;
    global maxOxygenSteps;
    global fullyExplored;
    global turnAround;

    if fullyExplored == False:
        newGridUnexploredPositions = [];
        for i in robotAreaGrid:
            if robotAreaGrid[i] == 1 or robotAreaGrid[i] == 3: # 0 Unexplored, 1 Explored (Clear), 2 Explored (Wall), 3 Explored (OxygenSystem; Clear)
                if (i[0], i[1] + 1) not in robotAreaGrid:
                    newGridUnexploredPositions.append((i[0], i[1] + 1));
                if (i[0] + 1, i[1]) not in robotAreaGrid:
                    newGridUnexploredPositions.append((i[0] + 1, i[1]));
                if (i[0], i[1] - 1) not in robotAreaGrid:
                    newGridUnexploredPositions.append((i[0], i[1] - 1));
                if (i[0] - 1, i[1]) not in robotAreaGrid:
                    newGridUnexploredPositions.append((i[0] - 1, i[1]));
        for i in newGridUnexploredPositions:
            robotAreaGrid[i] = 0;
    foundAnyUnexplored = False;
    for i in robotAreaGrid:
        if robotAreaGrid[i] == 0:
            foundAnyUnexplored = True;
    if foundAnyUnexplored == False:
        fullyExplored = True;
        #print(fullyExplored);

    if fullyExplored == False:
        if plannedMovement == []:
            plannedMovement = closestUnexploredMovement();
        if len(robotMovementHistory) > 200 and turnAround == False:
            turnAround = True;
            plannedMovement = robotPositionHistory;
            plannedMovement.pop();
                #print(plannedMovement[-1], robotPosition)
                #print(plannedMovement, robotPosition);
        if robotPosition == (0, 0):
            turnAround = False
            robotPositionHistory = []
            robotMovementHistory = []
            #print(robotMovementHistory);
            print("ORIGIN!");
        #if turnAround:
            #print(plannedMovement[-1], robotPosition);

        if plannedMovement[-1] == (robotPosition[0], robotPosition[1] + 1):
            robotCommandHistory.append(1);
            plannedMovement.pop();
            return 1;
        elif plannedMovement[-1] == (robotPosition[0], robotPosition[1] -1):
            robotCommandHistory.append(2);
            plannedMovement.pop();
            return 2;
        elif plannedMovement[-1] == (robotPosition[0] - 1, robotPosition[1]):
            robotCommandHistory.append(3);
            plannedMovement.pop();
            return 3;
        elif plannedMovement[-1] == (robotPosition[0] + 1, robotPosition[1]):
            robotCommandHistory.append(4);
            plannedMovement.pop();
            #if turnAround:
                #print("a");
                #print(plannedMovement[-1], robotPosition);
            return 4;
        else:
            print("? Fuckup pathing.", plannedMovement[-1], robotPosition);
            return 0;

    else:
        currentFastest = maxOxygenSteps[0];
        #print(currentFastest, currentFastest[0], len(currentFastest[1]));
        foundFastest = False;
        while not foundFastest:
            print(currentFastest);
            ffpVar = findFastestPath((0, 0), oxygenPosition, 500, (0, 0));
            if ffpVar == False or ffpVar == None:
                foundFastest = True;
            else:
                currentFastest = ffpVar;
        print(currentFastest);
        input();
    print("?")
    return 0;



def recieveOutput(output):
    global robotAreaGrid;
    global robotPosition;
    global robotCommandHistory;
    global robotMovementHistory;
    global robotPositionHistory;
    global oxygenPosition;
    global maxOxygenSteps;
    global turnAround;

    testedSpace = relativeSpace(robotPosition, robotCommandHistory[-1]);
    #print(output);
    #input();
    #if testedSpace == (-11, -7):
        #input();
    if int(output) == 0:
        robotAreaGrid[testedSpace] = 2;
    elif int(output) == 1:
        robotPosition = testedSpace;
        robotMovementHistory.append(robotCommandHistory[-1]);
        if turnAround == False:
            robotPositionHistory.append(robotPosition)
        robotAreaGrid[robotPosition] = 1;
    elif int(output) == 2:
        robotPosition = testedSpace;
        robotMovementHistory.append(robotCommandHistory[-1]);
        robotPositionHistory.append(robotPosition);
        robotAreaGrid[robotPosition] = 3;
        if oxygenPosition == None:
            oxygenPosition = testedSpace;
            maxOxygenSteps = [len(robotMovementHistory), robotMovementHistory.copy()];
            print(len(robotMovementHistory), len(robotCommandHistory));
            #print(robotMovementHistory);
            #input();

def printArea(robotAreaGrid):
    maxX = 0;
    maxY = 0;
    minX = 0;
    minY = 0;
    for i in robotAreaGrid:
        if i[0] > maxX:
            maxX = i[0];
        if i[0] < minX:
            minX = i[0];
        if i[1] > maxY:
            maxY = i[1];
        if i[1] < minY:
            minY = i[1];
    print(minX, maxX);
    print(minY, maxY);
    input();
    defaultLine = ""
    for i in range(maxX - minX + 1):
        defaultLine += "?";
    print(len(defaultLine));
    currentLineNumber = maxY;
    while currentLineNumber >= minY:
        currentLine = ""
        for i in range(maxX - minX + 1):
            #print((i + minX, currentLineNumber));
            if tuple((i + minX, currentLineNumber)) in robotAreaGrid:
                currentLine = currentLine + str(robotAreaGrid[(i + minX, currentLineNumber)]);
            else:
                currentLine = currentLine + "?";
                #print(len(currentLine[:minX + i[0]]), len(str(robotAreaGrid[i])), len(currentLine[minX + i[0] + 1:]));
                #if len(currentLine) != len(defaultLine):
                    #currentLine = currentLine[:-1];
                    #input();
        for i in range(len(currentLine)):
            if currentLine[i] == "0":
                currentLine = currentLine[:i] + "!" + currentLine[i + 1:];
            elif currentLine[i] == "1":
                currentLine = currentLine[:i] + " " + currentLine[i + 1:];
            elif currentLine[i] == "2":
                currentLine = currentLine[:i] + "█" + currentLine[i + 1:];
            elif currentLine[i] == "3":
                currentLine = currentLine[:i] + "O" + currentLine[i + 1:];
            if currentLineNumber == 0:
                #print(i, minX);
                if i + minX == 0:
                    currentLine = currentLine[:i] + "X" + currentLine[i + 1:];
        #print(len(currentLine));
        print(currentLine + " =" + str(currentLineNumber));
        print
        #print(currentLineNumber, minY)
        currentLineNumber -= 1;
        #input();


# Globul btw
robotPosition = (0, 0);
oxygenPosition = None;
maxOxygenSteps = None;
robotAreaGrid = {}
robotAreaGrid[robotPosition] = 1; # 0 Unexplored, 1 Explored (Clear), 2 Explored (Wall), 3 Explored (OxygenSystem; Clear)
robotCommandHistory = []; # 1 = NORTH, 2 = SOUTH, 3 = WEST, 4 = EAST
robotMovementHistory = [];
robotPositionHistory = [];
robotPositionHistory.append(robotPosition);
plannedMovement = [];
fullyExplored = False;
turnAround = False;



fullInput = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,102,1,1034,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1001,1034,0,1039,102,1,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,1002,1037,1,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1001,1035,0,1040,1001,1038,0,1043,1002,1037,1,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,7,1032,1006,1032,165,1008,1040,33,1032,1006,1032,165,1101,2,0,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,60,1044,1105,1,224,1101,0,0,1044,1106,0,224,1006,1044,247,101,0,1039,1034,101,0,1040,1035,1002,1041,1,1036,1002,1043,1,1038,101,0,1042,1037,4,1044,1105,1,0,92,17,17,33,88,37,85,63,23,14,79,46,37,69,8,6,63,55,61,21,86,19,37,78,49,15,54,28,54,94,91,14,11,40,56,96,20,20,82,28,12,91,68,43,18,63,16,82,71,8,83,88,25,79,67,26,55,33,51,74,68,59,64,58,78,30,65,64,9,48,87,26,85,32,82,92,21,34,99,1,20,66,34,85,65,58,87,12,21,13,51,90,54,19,12,85,3,88,47,31,93,95,49,70,95,55,7,67,2,92,42,80,88,42,24,91,2,59,41,41,70,89,42,83,43,92,44,93,62,26,63,99,81,35,98,70,71,79,8,90,26,66,94,22,47,55,90,93,6,87,92,88,40,73,40,97,14,73,90,31,92,16,35,93,36,27,69,57,97,80,34,58,42,95,34,9,93,22,94,45,79,32,33,90,72,77,58,29,63,56,95,37,61,58,51,57,8,25,86,75,25,63,64,93,57,7,79,85,57,53,97,16,63,40,71,52,23,33,75,13,56,65,90,26,12,66,93,26,36,64,30,10,75,18,77,76,86,33,98,4,23,52,64,66,82,38,90,17,63,94,24,97,20,92,70,63,80,19,73,8,74,93,16,98,77,52,38,90,46,49,76,84,53,50,22,93,19,16,61,47,54,67,56,78,21,77,52,88,4,64,91,90,10,97,10,51,89,15,57,97,22,79,59,92,17,84,71,30,96,58,82,52,93,48,20,62,4,89,64,53,85,37,92,52,89,43,80,86,2,41,81,53,53,82,77,31,66,92,31,44,81,14,49,96,66,42,91,2,61,82,36,32,90,8,61,32,67,52,25,81,15,63,27,59,61,1,15,88,87,62,10,85,47,75,24,46,63,24,77,34,73,34,45,71,10,96,46,43,75,31,23,72,37,87,57,88,63,30,6,86,91,16,53,16,89,81,11,32,75,22,82,69,50,88,53,67,50,65,67,26,81,83,20,14,23,89,98,57,64,3,79,7,69,89,57,1,61,65,14,52,76,66,83,3,57,90,82,53,13,72,94,37,26,97,77,32,53,43,78,22,36,65,83,98,55,82,58,48,24,68,92,18,22,90,65,28,81,33,63,79,3,31,65,92,53,46,74,7,80,37,79,79,83,42,82,84,33,21,79,79,21,81,55,4,95,10,53,84,14,25,86,65,24,74,53,26,61,47,19,66,86,58,99,37,83,35,46,3,11,89,27,66,53,33,67,8,95,44,45,70,71,65,59,49,77,25,3,56,83,39,91,3,52,86,67,57,99,86,40,39,3,99,25,69,94,93,62,36,37,91,17,26,80,98,77,15,5,90,25,40,69,11,85,66,56,40,83,61,10,85,33,28,86,26,41,61,4,86,78,20,71,78,47,94,39,92,26,61,91,52,69,20,47,45,99,38,96,39,98,76,58,28,94,27,47,97,2,45,54,64,94,98,27,69,54,23,72,89,96,22,58,21,16,79,28,45,55,78,75,15,92,67,10,81,80,64,61,13,30,98,65,57,35,4,22,96,72,92,47,51,87,33,78,26,83,20,5,93,22,73,83,68,24,17,61,69,39,62,53,20,95,84,53,83,36,48,99,33,13,42,90,97,87,9,55,64,34,94,7,78,62,42,43,83,54,82,57,24,36,98,95,54,63,75,52,15,40,92,87,77,5,13,93,48,82,71,65,97,96,1,3,68,49,97,9,77,88,99,25,78,4,84,97,77,4,92,91,76,53,71,58,64,55,68,97,96,48,99,2,86,51,69,15,72,42,72,44,86,55,73,0,0,21,21,1,10,1,0,0,0,0,0,0]

#fullInput = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

#fullInput = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99];

currentExecutePointer = 0;
relativeBase = 0;
memory = inputToMemory(fullInput);
exitCode = 0;
while exitCode == 0:

    currentInstruction = opcodeSplit(accessMemory(memory, currentExecutePointer));

    #print("Mem: " + str(memory) + " Pointer: " + str(currentExecutePointer) + " Instruction: " + str(currentInstruction)  + " RelativeBase: " + str(relativeBase));

    if currentInstruction[0] == "01": # ADD
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 3, relativeBase);
        memory = writeToMemory(memory, params[2], int(accessMemory(memory, params[0])) + int(accessMemory(memory, params[1])));
        currentExecutePointer += 4;


    elif currentInstruction[0] == "02": # MULTIPLY
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 3, relativeBase);
        memory = writeToMemory(memory, params[2], int(accessMemory(memory, params[0])) * int(accessMemory(memory, params[1])));
        currentExecutePointer += 4;


    elif currentInstruction[0] == "03": # INPUT
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 1, relativeBase);
        #print(">>> ");

        userInput = recieveInput(); #Modified from std
        #print(userInput);

        memory = writeToMemory(memory, params[0], userInput);
        currentExecutePointer += 2;


    elif currentInstruction[0] == "04": # OUTPUT
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 1, relativeBase);

        recieveOutput(accessMemory(memory, params[0])) #Modified from std

        #print(accessMemory(memory, params[0]));

        currentExecutePointer += 2;


    elif currentInstruction[0] == "05": # JMP IF TRUE
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 2, relativeBase);
        if accessMemory(memory, params[0]) != "0":
            currentExecutePointer = int(accessMemory(memory, params[1]));
        else:
            currentExecutePointer += 3


    elif currentInstruction[0] == "06": # JMP IF FALSE
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 2, relativeBase);
        if accessMemory(memory, params[0]) == "0":
            currentExecutePointer = int(accessMemory(memory, params[1]));
        else:
            currentExecutePointer += 3


    elif currentInstruction[0] == "07": # LESS THAN
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 3, relativeBase);
        if int(accessMemory(memory, params[0])) < int(accessMemory(memory, params[1])):
            memory = writeToMemory(memory, params[2], 1)
        else:
            memory = writeToMemory(memory, params[2], 0)
        currentExecutePointer += 4


    elif currentInstruction[0] == "08": # EQUAL TO
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 3, relativeBase);
        if int(accessMemory(memory, params[0])) == int(accessMemory(memory, params[1])):
            memory = writeToMemory(memory, params[2], 1)
        else:
            memory = writeToMemory(memory, params[2], 0)
        currentExecutePointer += 4


    elif currentInstruction[0] == "09": # ADJUST RELATIVE BASE
        params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 1, relativeBase);
        relativeBase = relativeBase + int(accessMemory(memory, params[0]));
        currentExecutePointer += 2;


    elif currentInstruction[0] == "99": # HALT
        exitCode = 1;
        break;
    else:
        exitCode = 2;
        break;

if exitCode == 1:
    #print(len(robotPanelGrid));

    print("Exited Successfully");

else:
    if exitCode == 2:
        print("Unrecognised command; commands must be suffixed with 01, ... , 08, or 99.");
    elif exitCode == 3:
        print("End of program reached searching for parameters.");
    elif exitCode == 4:
        print("End of program reached searching for opcode");
        print(fullInput);
    elif exitCode == 5:
        print("Unrecognised input; only enter single integers.");
    else:
        print("Unknown Error");
