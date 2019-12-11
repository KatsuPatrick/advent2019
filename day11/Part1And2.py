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
    global robotPosition;
    global facing;
    global robotPanelGrid;
    global variablesRecieved;

    if variablesRecieved != []:
        if variablesRecieved[-2] == "0":
            robotPanelGrid[robotPosition] = False;
        else:
            robotPanelGrid[robotPosition] = True;
        if variablesRecieved[-1] == "0":
            facing = (facing + 3) % 4;
        else:
            facing = (facing + 1) % 4;
        if facing == 0:
            newPos = (robotPosition[0], robotPosition[1] + 1)
            if newPos not in robotPanelGrid:
                robotPanelGrid[newPos] = False;
            robotPosition = newPos;

        if facing == 1:
            newPos = (robotPosition[0] + 1, robotPosition[1])
            if newPos not in robotPanelGrid:
                robotPanelGrid[newPos] = False;
            robotPosition = newPos;

        if facing == 2:
            newPos = (robotPosition[0], robotPosition[1] - 1)
            if newPos not in robotPanelGrid:
                robotPanelGrid[newPos] = False;
            robotPosition = newPos;

        if facing == 3:
            newPos = (robotPosition[0] - 1, robotPosition[1])
            if newPos not in robotPanelGrid:
                robotPanelGrid[newPos] = False;
            robotPosition = newPos;
        variablesRecieved = []

    if robotPanelGrid[robotPosition] == True:
        return 1;
    return 0;

def recieveOutput(output):
    global variablesRecieved;
    #variablesRecieved.append(output);
    #print("Output: " + str(output));
    variablesRecieved.append(output);

# Globul btw
robotPosition = (0, 0);
robotPanelGrid = {}
robotPanelGrid[robotPosition] = True; # black false, white true
facing = 0; # 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
variablesRecieved = [];


fullInput = [3,8,1005,8,298,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,28,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,51,1006,0,37,1006,0,65,1,4,9,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,83,2,3,9,10,1006,0,39,1,1,0,10,1,104,11,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,120,2,104,13,10,1,1007,18,10,1006,0,19,1,107,2,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,157,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,179,2,108,16,10,2,1108,14,10,1006,0,70,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,211,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,234,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,256,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,278,101,1,9,9,1007,9,957,10,1005,10,15,99,109,620,104,0,104,1,21101,387508441896,0,1,21101,0,315,0,1105,1,419,21101,666412880532,0,1,21102,1,326,0,1106,0,419,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,106341436456,0,1,21101,373,0,0,1106,0,419,21101,46211886299,0,1,21101,384,0,0,1106,0,419,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,838433923860,1,21102,1,407,0,1105,1,419,21102,1,988224946540,1,21102,1,418,0,1106,0,419,99,109,2,21201,-1,0,1,21101,40,0,2,21102,1,450,3,21101,440,0,0,1105,1,483,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,445,446,461,4,0,1001,445,1,445,108,4,445,10,1006,10,477,1101,0,0,445,109,-2,2105,1,0,0,109,4,1201,-1,0,482,1207,-3,0,10,1006,10,500,21101,0,0,-3,21201,-3,0,1,21202,-2,1,2,21101,1,0,3,21102,1,519,0,1105,1,524,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,547,2207,-4,-2,10,1006,10,547,22102,1,-4,-4,1106,0,615,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21102,1,566,0,1105,1,524,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,585,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,607,22101,0,-1,1,21102,1,607,0,105,1,482,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

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
    max0 = 0;
    max1 = 0;
    min0 = 0;
    min1 = 0;
    for i in robotPanelGrid:
        if i[0] > max0:
            max0 = i[0];
        elif i[0] < min0:
            min0 = i[0];
        if i[1] > max1:
            max1 = i[1];
        elif i[1] < min1:
            min1 = i[1];
    output = []
    for i in range(min1, max1 + 1):
        outputLine = ""
        #print(i)
        for j in range(min0, max0 + 1):
            if (j, i) in robotPanelGrid:
                if robotPanelGrid[(j, i)] == True:
                    outputLine = outputLine + "█";
                if robotPanelGrid[(j, i)] == False:
                    outputLine = outputLine + " ";
            else:
                outputLine = outputLine + " ";
        output.append(outputLine);
    for i in range(len(output)):
        print(output[len(output) - i - 1]);
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
