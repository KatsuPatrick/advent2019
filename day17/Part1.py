import math;
import re;

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



def addAdditionalCorner(lineCornerSet, allLines, allPOI):
    newLineCornerLineSet = set();
    for i in lineCornerSet:
        for j in range(len(i[0]) - 1):
            if (i[0][j], i[0][j + 1]) not in allLines or (i[0][j + 1], i[0][j]) not in allLines:
                print("aaaaaaah", i);

        for j in allLines:
            if j[0] == i[0][-1] and (i[0][-2][0] != i[0][-1][0] or i[0][-1][0] != j[1][0]) and (i[0][-2][1] != i[0][-1][1] or i[0][-1][1] != j[1][1]):
                firstHorDif = i[0][-1][0] - i[0][-2][0]; # +ve = left to right
                firstVerDif = i[0][-1][1] - i[0][-2][1]; # +ve = top to bottom
                secHorDif = j[-1][0] - j[-2][0];
                secVerDif = j[-1][1] - j[-2][1];
                newPoints = [];
                for k in i[0]:
                    newPoints.append(k);
                newPoints.append(j[1]);
                tupleNewPoints = tuple(newPoints);
                if firstHorDif != 0: # hor then ver
                    if firstHorDif == 0 or secVerDif == 0:
                        print(i[0], j);
                        input();
                    if (firstHorDif > 0 and secVerDif > 0) or (firstHorDif < 0 and secVerDif < 0): # right
                        newLineCornerLineSet.add((tupleNewPoints, str(i[1]) + ",R," + str(abs(secVerDif))));
                    else:
                        newLineCornerLineSet.add((tupleNewPoints, str(i[1]) + ",L," + str(abs(secVerDif))));
                else:
                    if firstVerDif == 0 or secHorDif == 0:
                        print(i, j);
                        input();
                    if (firstVerDif > 0 and secHorDif > 0) or (firstVerDif < 0 and secHorDif < 0): # Left
                        newLineCornerLineSet.add((tupleNewPoints, str(i[1]) + ",L," + str(abs(secHorDif))));
                    else:
                        newLineCornerLineSet.add((tupleNewPoints, str(i[1]) + ",R," + str(abs(secHorDif))));
    return newLineCornerLineSet;




def recieveInput():

    "R,4,R,12,R,10,L,4"

    return input()[0];

def recieveOutput(output):
    global asciiRecieved;
    global fullMap;
    global lineCount;
    #variablesRecieved.append(output);
    #print("Output: " + str(output));
    #print(asciiRecieved);
    if int(output) == 10:
        currentLine = "";
        for i in range(len(asciiRecieved)):
            #print(asciiRecieved[i]);
            currentLine = currentLine + chr(int(asciiRecieved[i]));
            if int(asciiRecieved[i]) != 46:
                fullMap[(i, lineCount)] = chr(int(asciiRecieved[i]));
        print(currentLine);
        lineCount += 1;
        asciiRecieved = [];
    else:
        asciiRecieved.append(int(output));

# Globul btw
asciiRecieved = [];
fullMap = {};
lineCount = 0

inputStream = open("./input", "r");
seperatedInput = inputStream.readlines();
stringInput = seperatedInput[0][:-1];
stringList = re.split(",", stringInput)
fullInput = []
for i in stringList:
    fullInput.append(int(i))
#print(fullInput);
#print();

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
    intersections = set();
    corners = set();
    deadEnds = set();
    for i in fullMap:
        totalSurrounding = 0

        if (i[0], i[1] + 1) in fullMap:
            totalSurrounding += 1;
        if (i[0] + 1, i[1]) in fullMap:
            totalSurrounding += 1;
        if (i[0], i[1] - 1) in fullMap:
            totalSurrounding += 1;
        if (i[0] - 1, i[1]) in fullMap:
            totalSurrounding += 1;
        if totalSurrounding == 4:
            intersections.add(i);
        elif totalSurrounding == 1:
            deadEnds.add(i);
        elif totalSurrounding == 2 and (((i[0], i[1] + 1) in fullMap and (i[0] + 1, i[1]) in fullMap) or
        ((i[0], i[1] - 1) in fullMap and (i[0] - 1, i[1]) in fullMap) or ((i[0], i[1] + 1) in fullMap and (i[0] - 1, i[1]) in fullMap) or
        ((i[0], i[1] - 1) in fullMap and (i[0] + 1, i[1]) in fullMap)):
            corners.add(i);

    allPOI = set();
    allPOI = deadEnds.union(corners);
    allPOI = allPOI.union(intersections);

    allLines = {};

    #for i in corners:      # for non-duplicate, can use only corners
    for i in allPOI:
        currentSpace = i;
        while currentSpace in fullMap: #North
            currentSpace = (currentSpace[0], currentSpace[1] + 1);
            if currentSpace in allPOI and (i, currentSpace) not in allLines: #and (currentSpace, i) not in allLines: #Will duplicate
                allLines[(i, currentSpace)] = (currentSpace[1] - i[1]);

        currentSpace = i;
        while currentSpace in fullMap: #South
            currentSpace = (currentSpace[0], currentSpace[1] - 1);
            if currentSpace in allPOI and (i, currentSpace) not in allLines: #and (currentSpace, i) not in allLines:
                allLines[(i, currentSpace)] = (i[1] - currentSpace[1]);

        currentSpace = i;
        while currentSpace in fullMap: #East
            currentSpace = (currentSpace[0] + 1, currentSpace[1]);
            if currentSpace in allPOI and (i, currentSpace) not in allLines: #and (currentSpace, i) not in allLines:
                allLines[(i, currentSpace)] = (currentSpace[0] - i[0]);

        currentSpace = i;
        while currentSpace in fullMap: #North
            currentSpace = (currentSpace[0] - 1, currentSpace[1]);
            if currentSpace in allPOI and (i, currentSpace) not in allLines: #and (currentSpace, i) not in allLines:
                allLines[(i, currentSpace)] = (i[0] - currentSpace[0]);

    allLineCornerLine = set();

    for i in allLines:
        if (i[1], i[0]) not in allLines:
            print("aaah", i);

        for j in allLines:
            if j[0] == i[1] and (i[0][0] != i[1][0] or i[1][0] != j[1][0]) and (i[0][1] != i[1][1] or i[1][1] != j[1][1]):
                firstHorDif = i[1][0] - i[0][0]; # +ve = left to right
                firstVerDif = i[1][1] - i[0][1]; # +ve = top to bottom
                secHorDif = j[1][0] - j[0][0];
                secVerDif = j[1][1] - j[0][1];
                if firstHorDif != 0: # hor then ver
                    if firstHorDif == 0 or secVerDif == 0:
                        print(i, j);
                        input();
                    if (firstHorDif > 0 and secVerDif > 0) or (firstHorDif < 0 and secVerDif < 0): # right
                        allLineCornerLine.add(((i[0], i[1], j[1]), str(abs(firstHorDif)) + ",R," + str(abs(secVerDif))));
                    else:
                        allLineCornerLine.add(((i[0], i[1], j[1]), str(abs(firstHorDif)) + ",L," + str(abs(secVerDif))));
                else:
                    if firstVerDif == 0 or secHorDif == 0:
                        print(i, j);
                        input();
                    if (firstVerDif > 0 and secHorDif > 0) or (firstVerDif < 0 and secHorDif < 0): # Left
                        allLineCornerLine.add(((i[0], i[1], j[1]), str(abs(firstVerDif)) + ",L," + str(abs(secHorDif))));
                    else:
                        allLineCornerLine.add(((i[0], i[1], j[1]), str(abs(firstVerDif)) + ",R," + str(abs(secHorDif))));

    for i in allLineCornerLine:
        #print(i[0]);
        None;

    threeLCL = addAdditionalCorner(allLineCornerLine, allLines, allPOI);
    fourLCL = addAdditionalCorner(threeLCL, allLines, allPOI);
    fiveLCL = addAdditionalCorner(fourLCL, allLines, allPOI);
    #print(threeLCL);


    finalLCL = fiveLCL.copy();
    finalLCL = finalLCL.union(fourLCL);
    finalLCL = finalLCL.union(threeLCL);


    finalLCLSet = set();
    finalLCLCount = {};
    for i in finalLCL:
        finalLCLSet.add(i[1]);
        if i[1] not in finalLCLCount:
            finalLCLCount[i[1]] = 1;
        else:
            finalLCLCount[i[1]] += 1;

    totalMax = math.inf;
    sortedLCLCount = [];
    while len(sortedLCLCount) != len(finalLCLCount):
        currentMax = 0;
        for i in finalLCLCount:
            if (i, finalLCLCount[i]) not in sortedLCLCount:
                if finalLCLCount[i] == totalMax:
                    sortedLCLCount.append((i, finalLCLCount[i]));
                elif finalLCLCount[i] > currentMax and finalLCLCount[i] < totalMax:
                    currentMax = finalLCLCount[i];
        #print(len(sortedLCLCount));
        totalMax = currentMax;
    usefulLCLs = {};
    for i in range(len(sortedLCLCount)):
        #print(sortedLCLCount[i]);
        if sortedLCLCount[i][1] > 1:
            saveDirections = sortedLCLCount[i][0];
            subLCLs = set();
            for j in finalLCL:
                if j[1] == sortedLCLCount[i][0]:
                    subLCLs.add(j[0]);
            subLCLLines = {};
            for line in subLCLs: # add every line pair in each lcl example to a dictionary
                subLCLLines[line] = []
                for j in line:
                    for k in line:
                        if j != k:
                            subLCLLines[line].append((j, k));
            toRemove = set();
            for j in subLCLLines: # compare
                if j not in toRemove:
                    for segmentIndex in range(len(j)):
                        for k in range(len(j)):
                            if segmentIndex != k:
                                if j[segmentIndex] == j[k]:
                                    toRemove.add(j);
                    for k in subLCLLines:
                        if j != k:
                            for segment in j:
                                if segment in k:
                                    toRemove.add(k);
            for j in toRemove:
                subLCLLines.pop(j);
            if len(subLCLLines) > 1:
                workingLCLs = [];
                for i in subLCLLines:
                    workingLCLs.append(i);
                usefulLCLs[saveDirections] = tuple(workingLCLs);
                #print(sortedLCLCount[i][0], subLCLLines.keys(), len(subLCLLines));
                #input();
    #focusLCL = "12,L,4,R,10,L,4,L,10";
    focusLCL = "12,L,8,R,10,R,4,R,10"
    #print(usefulLCLs[focusLCL]);
    focusLCLLines = set();
    for i in range(len(usefulLCLs[focusLCL])):
        for j in range(len(usefulLCLs[focusLCL][i]) - 1):
            maxJ = len(usefulLCLs[focusLCL][i]) - 1;
            focusLCLLines.add((usefulLCLs[focusLCL][i][j], usefulLCLs[focusLCL][i][j + 1]));
            focusLCLLines.add((usefulLCLs[focusLCL][i][maxJ - j], usefulLCLs[focusLCL][i][maxJ - j - 1]));
    reallyUsefulLCLs = {};
    for i in usefulLCLs: # lcl
        count = 0;
        if len(usefulLCLs[i]) > 2:
            noClash = True;
            for j in usefulLCLs[i]: # ind continuous line
                for k in range(len(j) - 1): #pairs
                    #print((j[k], j[k + 1]) in focusLCLLines);
                    count += 1;
                    if tuple([j[k], j[k + 1]]) in focusLCLLines:
                        noClash = False;
            if noClash == True:
                #print(count);
                reallyUsefulLCLs[i] = usefulLCLs[i];
    #print(reallyUsefulLCLs);
    #reallyUsefulLCLs = usefulLCLs.copy();
    rULCLLines = {}
    for i in reallyUsefulLCLs:
        rULCLLines[i] = set();
        for j in range(len(reallyUsefulLCLs[i])):
            for k in range(len(reallyUsefulLCLs[i][j]) - 1):
                maxK = len(reallyUsefulLCLs[i][j]) - 1;
                rULCLLines[i].add((reallyUsefulLCLs[i][j][k], reallyUsefulLCLs[i][j][k + 1]));
                rULCLLines[i].add((reallyUsefulLCLs[i][j][maxK - k], reallyUsefulLCLs[i][j][maxK - k - 1]));
    noMatch = {};
    for i in rULCLLines:
        noMatch[i] = set();
        for j in rULCLLines:
            if i != j:
                for k in rULCLLines[i]:
                    if k in rULCLLines[j]:
                        noMatch[i].add(j);
    superReallyUsefulLCLs = {};
    for i in rULCLLines:
        if len(noMatch[i]) < len(reallyUsefulLCLs) - 1:
            superReallyUsefulLCLs[i] = reallyUsefulLCLs[i];
            #print(len(i), len(reallyUsefulLCLs[i]), len(noMatch[i]), i, );
    #print(superReallyUsefulLCLs);
    usefulPointsSRULCL = {};
    for i in superReallyUsefulLCLs:
        usefulPointsSRULCL[i] = set();
        for j2 in superReallyUsefulLCLs[i]:
            for j in j2:
                #print(j2);
                if j in deadEnds or j == usefulLCLs[focusLCL][0][0] or j == usefulLCLs[focusLCL][0][0] or j == usefulLCLs[focusLCL][0][0] or j == usefulLCLs[focusLCL][0][0]:
                    usefulPointsSRULCL[i].add(j);
                for k in range(len(usefulLCLs[focusLCL])):
                    if j == usefulLCLs[focusLCL][k][0] or j == usefulLCLs[focusLCL][k][-1]:
                        usefulPointsSRULCL[i].add(j);
    for i in superReallyUsefulLCLs:
        print(len(i), len(usefulPointsSRULCL[i]), len(noMatch[i]), usefulPointsSRULCL[i], i, usefulLCLs[i]);
        print();

    test2 = "10,R,4,R,10,L,4";
    test3 = "2,L,8,L,2,R,4";
    input();
    print();
    #print(noMatch);
    input();
    #print(intersections);
    #print(deadEnds);
    #print(corners);
    #print(fullMap);
    print();
    sum = 0;
    for i in intersections:
        sum += (i[0]) * (i[1]);
    print(sum);
    print();
    print("Exited Successfully");
else:
    if exitCode == 2:
        print("Unrecognised command; commands must be suffixed with 01, ... , 09, or 99.");
    elif exitCode == 3:
        print("End of program reached searching for parameters.");
    elif exitCode == 4:
        print("End of program reached searching for opcode");
        print(fullInput);
    elif exitCode == 5:
        print("Unrecognised input; only enter single integers.");
    else:
        print("Unknown Error");
