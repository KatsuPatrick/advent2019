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
    global newDiscardInputs;
    global paddleIncrementIndex;

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

        currentLineIndex += 1
        #print(currentLine + " " + str(playerScore));
        #input()
    #print(playerScore);



    playerInput = aiInput[inputIndex]
    newDiscardInputs.append(aiInput[inputIndex])
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
for i in range(1000):
    aiInput.append(0);
currentMaxScore = 0;
paddleIncrementIndexMax = 0;
firstUnlockedInputIndex = 0;
while True:
    index = 0;

    discardCheck = False;
    while aiInput.count(3) != 0 or discardCheck == False:
        while aiInput.count(3) != 0:
            aiInput[aiInput.index(3) + 1] += 1;
            aiInput[aiInput.index(3)] = 0;


        while discardCheck == False:
            #print(discardInputs);
            restartDiscard = False
            if tuple(aiInput[firstUnlockedInputIndex:]) in discardInputs[firstUnlockedInputIndex]:
                aiInput[firstUnlockedInputIndex] += 1
                restartDiscard = True
            if restartDiscard == False:
                discardCheck = True;


    #print(aiInput);
    #input();

    # Globul btw
    inputIndex = 0;
    variablesRecieved = [];
    currentDisplay = {};
    playerScore = 0;
    newDiscardInputs = []
    paddleIncrementIndex = []

    #print(aiInput);
    score = runGame(aiInput);
    #print(score)
    if score > currentMaxScore:
        currentMaxScore = score;
    if len(paddleIncrementIndex) > paddleIncrementIndexMax:
        paddleIncrementIndexMax = len(paddleIncrementIndex)
        print(aiInput);
        print("NEW MAX PADDLE HITS! Score: " + str(currentMaxScore));
    if len(paddleIncrementIndex) > 1:
        if paddleIncrementIndex[-2] + 1 > firstUnlockedInputIndex:
            firstUnlockedInputIndex = paddleIncrementIndex[-2] + 1;
            discardInputs[firstUnlockedInputIndex] = set()
            aiInput[paddleIncrementIndex[-2] + 1] += 1;
            print(firstUnlockedInputIndex);
            print("to ~" + str(paddleIncrementIndex[-1]));
    #print(paddleIncrementIndex);
    #print(discardInputs);
    #print(firstUnlockedInputIndex);
    #print(newDiscardInputs[firstUnlockedInputIndex:])
    #input()
    if tuple(newDiscardInputs[firstUnlockedInputIndex:]) in discardInputs[firstUnlockedInputIndex]:
        firstUnlockedInputIndex += -1;
        discardInputs[firstUnlockedInputIndex] = set()
        discardInputs[firstUnlockedInputIndex].add(tuple(aiInput[firstUnlockedInputIndex + 1]))
        print(firstUnlockedInputIndex);
        print("to ~" + str(paddleIncrementIndex[-1]));
    else:
        discardInputs[firstUnlockedInputIndex].add(tuple(newDiscardInputs[firstUnlockedInputIndex:]));
    aiInput[firstUnlockedInputIndex] += 1;
