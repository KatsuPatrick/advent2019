import math;
import re;
import sys;

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
    global currentDisplay;
    global variablesRecieved;
    global playerScore;
    global aiInput;
    global inputIndex;
    global paddleIncrementIndex;
    global ballExitDifference;
    global exitIndex;

    #print(variablesRecieved);

    while len(variablesRecieved) > 2:
        triplet = []
        for i in range(3):
            triplet.append(variablesRecieved[i])
        if triplet[0] == '-1' and triplet[1] == '0':
            playerScore = int(triplet[2]);
        else:
            currentDisplay[(int(triplet[1]), int(triplet[0]))] = triplet[2];
            #print(currentDisplay)
        for i in range(len(triplet)):
            variablesRecieved.pop(0);

    maxY = 0
    for i in currentDisplay:
        if int(i[0]) > maxY:
            maxY = int(i[1]);
    currentLine = ""
    currentLineIndex = 0;
    for i in range(maxY + 1):
        for j in currentDisplay:
            if j[0] == currentLineIndex:
                while int(j[1]) > len(currentLine):
                    currentLine += " ";
                currentLine = currentLine[:j[1]] + currentDisplay[j] + currentLine[j[1] + 1:];
                #print(currentLine)

        for k in range(len(currentLine)):
            if currentLine[k] == "0":
                currentLine = currentLine[:k] + " " + currentLine[k + 1:];
            elif currentLine[k] == "1":
                currentLine = currentLine[:k] + "█" + currentLine[k + 1:];
            elif currentLine[k] == "2":
                currentLine = currentLine[:k] + "X" + currentLine[k + 1:];
            elif currentLine[k] == "3":
                currentLine = currentLine[:k] + "=" + currentLine[k + 1:];
            elif currentLine[k] == "4":
                currentLine = currentLine[:k] + "O" + currentLine[k + 1:];
        if i == maxY - 2:
            if currentLine.count("O") > 0:
                paddleIncrementIndex.append(inputIndex)
                ballExitDifference[inputIndex] = 0
        if i == maxY - 1:
            if currentLine.count("O") > 0:
                ballExitDifference[inputIndex - 1] = currentLine.index("O") - currentLine.index("=");
        currentLineIndex += 1
        if inputIndex == exitIndex:
            print(currentLine + " " + str(playerScore) + " " + str(inputIndex));
        #input()
    #print(playerScore);
    #input()



    playerInput = aiInput[inputIndex]
    inputIndex += 1;

    if playerInput == 0:
        return 0
    elif playerInput == 1:
        return 1;
    else:
        return -1;

def recieveOutput(output):
    global currentDisplay;
    global variablesRecieved;
    variablesRecieved.append(output);

def runGame(aiInput):
    inputStream = open("./input", "r");
    seperatedInput = inputStream.readlines();
    fullInput = re.split(",", seperatedInput[0]);
    for i in range(len(fullInput)):
        fullInput[i] = int(fullInput[i]);
    fullInput[0] = 2;

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
        #print(variablesRecieved);
        count = 0
        for i in range(int(len(variablesRecieved)/3)):
            if variablesRecieved[(i * 3) + 2] == '2':
                count+=1

        #print(count);
        #print("Exited Successfully");
        #print(aiInput);
        #input();
        #print(playerScore)
        return playerScore;
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

aiInput = [];
discardInputs = {};
discardInputs[0] = set();
for i in range(5000):
    aiInput.append(0);
currentMaxScore = 0;
paddleIncrementIndexMax = 0;
firstUnlockedInputIndex = 0;
paddleApproach = {};
exitIndex = 0;
paddleModifiers = [];
prevExitIndex = 0;
testRun = True;
ballExitDifference = {}
while True:
    index = 0;
    for i in range(firstUnlockedInputIndex, 1000):
        aiInput[i] = 0;
    if firstUnlockedInputIndex != 0:
        nextInputIndex = firstUnlockedInputIndex;
        for i in range(len(modifiedPaddleIndex)):
            #print(modifiedPaddleIndex)
            currentPaddle = modifiedPaddleIndex[- i - 1]
            for i in range(abs(ballExitDifference[currentPaddle])):
                #print(i)
                if ballExitDifference[currentPaddle] > 0:
                    aiInput[nextInputIndex + i] = 1;
                else:
                    aiInput[nextInputIndex + i] = 2;
            if ballExitDifference[currentPaddle] > 0:
                if paddleApproach[currentPaddle] == 0:
                    aiInput[nextInputIndex + abs(ballExitDifference[currentPaddle])] = 1
                elif paddleApproach[currentPaddle] == 1:
                    aiInput[currentPaddle - 1] = 1
                else:
                    aiInput[nextInputIndex + abs(ballExitDifference[currentPaddle])] = 1
                    aiInput[nextInputIndex + abs(ballExitDifference[currentPaddle]) + 1] = 1
                    aiInput[currentPaddle + 1] = -1
            else:
                if paddleApproach[currentPaddle] == 0:
                    aiInput[nextInputIndex + abs(ballExitDifference[currentPaddle])] = -1
                elif paddleApproach[currentPaddle] == 1:
                    aiInput[currentPaddle - 1] = -1
                else:
                    aiInput[nextInputIndex + abs(ballExitDifference[currentPaddle])] = -1
                    aiInput[nextInputIndex + abs(ballExitDifference[currentPaddle]) + 1] = -1
                    aiInput[currentPaddle + 1] = 1
            nextInputIndex = currentPaddle + 1;
        for i in range(4999):
            if aiInput[999 - i] != 0:
                #print(str(999 - i));
                break;

    #print(aiInput[:100]);
    print(paddleApproach);

    #print(aiInput);
    #input();

    # Globul btw
    inputIndex = 0;
    variablesRecieved = [];
    currentDisplay = {};
    playerScore = 0;
    paddleIncrementIndex = []
    modifiedPaddleIndex = [];


    #print(aiInput);
    score = runGame(aiInput);
    prevExitIndex = exitIndex;
    exitIndex = inputIndex;
    print(exitIndex);

    #for i in range(999):
        #if aiInput[999 - i] != 0:
            #if 999 - i != exitIndex - 1:
                #print("!!!", 999 - i, exitIndex - 1);
                #input();
            #break;

    if exitIndex != prevExitIndex:
        paddleModifiers = [];
        toPop = []
        for i in paddleApproach:
            if i > exitIndex:
                toPop.append(i)
        for i in toPop:
            paddleApproach.pop(i);

    for i in paddleIncrementIndex:
        if i not in paddleApproach:
            paddleApproach[i] = 0;
    #input();

    if score > currentMaxScore:
        currentMaxScore = score;
        print("NEW MAX SCORE! Score: " + str(currentMaxScore));
    elif testRun == True:
        testRun = False;
    else: # 0: stationary 1: from std 2: opposite
        if paddleModifiers == []:
            paddleModifiers.append(paddleApproach[paddleIncrementIndex[-1]] + 1);
        else:
            paddleModifiers[0] += 1
        testRun = True;

    while paddleModifiers.count(3) > 0:
        if paddleModifiers.index(3) < len(paddleModifiers) - 1:
            paddleModifiers[paddleModifiers.index(3) + 1] += 1;
        else:
            paddleModifiers.append(paddleApproach[paddleIncrementIndex[- len(paddleModifiers)]] + 1);
        paddleModifiers[paddleModifiers.index(3)] = 0
        
    for i in range(len(paddleModifiers)):
        paddleApproach[paddleIncrementIndex[-i - 1]] = paddleModifiers[i]
        modifiedPaddleIndex.append(paddleIncrementIndex[- i -1]);
    if len(paddleIncrementIndex) > paddleIncrementIndexMax:
        paddleIncrementIndexMax = len(paddleIncrementIndex)
        #print(aiInput);
        firstUnlockedInputIndex = paddleIncrementIndex[-2] + 1;
    firstUnlockedInputIndex = paddleIncrementIndex[- len(paddleModifiers) - 1] + 1
