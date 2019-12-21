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

def recieveInput():
    global firstCoordSent;
    global tractorCheckPosition;

    if not firstCoordSent:
        firstCoordSent = True;
        return tractorCheckPosition[0];
    else:
        firstCoordSent = False;
        return tractorCheckPosition[1];

def recieveOutput(output):
    return output

def mainCode():

    fullInput = [109,424,203,1,21101,11,0,0,1105,1,282,21101,0,18,0,1106,0,259,1202,1,1,221,203,1,21101,0,31,0,1105,1,282,21102,1,38,0,1106,0,259,20101,0,23,2,22102,1,1,3,21101,1,0,1,21101,0,57,0,1106,0,303,1202,1,1,222,21002,221,1,3,21001,221,0,2,21102,1,259,1,21101,80,0,0,1105,1,225,21102,1,117,2,21102,1,91,0,1105,1,303,1202,1,1,223,20102,1,222,4,21101,0,259,3,21101,0,225,2,21101,225,0,1,21101,118,0,0,1105,1,225,21001,222,0,3,21101,20,0,2,21102,1,133,0,1105,1,303,21202,1,-1,1,22001,223,1,1,21101,0,148,0,1106,0,259,2101,0,1,223,20102,1,221,4,21001,222,0,3,21101,0,16,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,195,1,0,105,1,108,20207,1,223,2,21002,23,1,1,21102,-1,1,3,21101,0,214,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1201,-4,0,249,22102,1,-3,1,22101,0,-2,2,21202,-1,1,3,21102,1,250,0,1106,0,225,22102,1,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,21202,-2,1,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21201,-2,0,3,21101,343,0,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21101,0,384,0,1105,1,303,1105,1,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22101,0,1,-4,109,-5,2105,1,0];

    currentExecutePointer = 0;
    relativeBase = 0;
    memory = inputToMemory(fullInput);
    exitCode = 0;

    tractorReturn = None;

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

            memory = writeToMemory(memory, params[0], userInput);
            currentExecutePointer += 2;


        elif currentInstruction[0] == "04": # OUTPUT
            params = retrieveAllParams(memory, currentExecutePointer, currentInstruction[1], 1, relativeBase);

            tractorReturn = recieveOutput(accessMemory(memory, params[0])) #Modified from std

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
        #print("Exited Successfully");
        return tractorReturn;
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
        return None;

def pointInTractorBeam(position):
    global tractorCoordGrid;
    global firstCoordSent;
    global tractorCheckPosition;

    firstCoordSent = False;
    tractorCheckPosition = position;

    if position not in tractorCoordGrid:
        tractorCoordGrid[position] = mainCode();
    if tractorCoordGrid[position] == "1":
        return True;
    else:
        return False;

# Globul btw
tractorCoordGrid = {}
firstCoordSent = False;
allChecked = False;
tractorCheckPosition = None;

found100Space = False;

currentMinimumX = 5
currentTestingY = 12

while not found100Space:
    currentTestingY += 1;
    currentCheckClosest = (currentMinimumX, currentTestingY);
    if pointInTractorBeam(currentCheckClosest) == False:
        tempPos = currentCheckClosest;
        while pointInTractorBeam(tempPos) == False:
            tempPos = (tempPos[0] + 1, tempPos[1]);
            if tempPos[0] > currentCheckClosest[0] + 10:
                print("o no");
                input();
        currentCheckClosest = tempPos;
        currentMinimumX = currentCheckClosest[0];
    while pointInTractorBeam((currentCheckClosest[0] + 99, currentCheckClosest[1])):
        if pointInTractorBeam((currentCheckClosest[0], currentCheckClosest[1] + 99)):
            print(currentCheckClosest);
            found100Space = True;
        currentCheckClosest = (currentCheckClosest[0] + 1, currentCheckClosest[1]);
