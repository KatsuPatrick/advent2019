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

def retrieve(fullInput, param, mode):
    #print(param, mode)
    if mode == "0":
        return fullInput[param];
    elif mode == "1":
        return param;
    return None;

def retrieveAllParams(fullInput, currentExecutePointer, fullMode, countParamRequired):
    paramList = []
    for i in range(countParamRequired):
        paramList.append(retrieve(fullInput, currentExecutePointer + 1 + i, fullMode[-1 - i]))
    return tuple(paramList);


def amplifier(memory, phase, inputValue, variableSave, name):
    #print(memory, phase, inputValue, variableSave)
    #print(inputValue);
    fullInput = memory.copy();
    currentExecutePointer = variableSave;
    exitCode = 0;
    phaseSet = False;
    returnValue = None;
    loopCount = -1
    while exitCode == 0:
        loopCount += 1;
        variableSave = (currentExecutePointer);
        toPrint = 0
        for i in fullInput:
            if i > toPrint:
                toPrint = i;
        print(toPrint);
        #a = input();
        if name == "E":
            print(fullInput[-2]);
        if ((len(fullInput) - currentExecutePointer) > 0): #if anywhere for instruction
            currentInstruction = opcodeSplit(fullInput[currentExecutePointer]);
            if currentInstruction[0] == "01": # ADD
                if not binEnoughParameters(fullInput, currentExecutePointer, 3):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 3);
                fullInput[params[2]] = int(fullInput[params[0]]) + int(fullInput[params[1]]);
                currentExecutePointer += 4;


            elif currentInstruction[0] == "02": # MULTIPLY
                if not binEnoughParameters(fullInput, currentExecutePointer, 3):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 3);
                fullInput[params[2]] = int(fullInput[params[0]]) * int(fullInput[params[1]]);
                currentExecutePointer += 4;


            elif currentInstruction[0] == "03": # INPUT
                if not returnValue == None:
                    return((returnValue, None, fullInput, variableSave));
                if not binEnoughParameters(fullInput, currentExecutePointer, 1):
                    exitCode = 3;
                    break;
                if phaseSet == False and phase != None:
                    userInput = phase;
                    phaseSet = True;
                else:
                    userInput = inputValue;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 1);
                fullInput[params[0]] = int(userInput);

                #else:
                    #exitCode = 5;
                    #break;
                currentExecutePointer += 2;


            elif currentInstruction[0] == "04": # OUTPUT
                if not binEnoughParameters(fullInput, currentExecutePointer, 1):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 1);
                returnValue = fullInput[params[0]];
                currentExecutePointer += 2;

            elif currentInstruction[0] == "05": # JMP IF TRUE
                if not binEnoughParameters(fullInput, currentExecutePointer, 2):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 2);
                if fullInput[params[0]] != 0:
                    currentExecutePointer = fullInput[params[1]];
                else:
                    currentExecutePointer += 3

            elif currentInstruction[0] == "06": # JMP IF FALSE
                if not binEnoughParameters(fullInput, currentExecutePointer, 2):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 2);
                if fullInput[params[0]] == 0:
                    currentExecutePointer = fullInput[params[1]];
                else:
                    currentExecutePointer += 3

            elif currentInstruction[0] == "07": # LESS THAN
                if not binEnoughParameters(fullInput, currentExecutePointer, 3):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 3);
                if fullInput[params[0]] < fullInput[params[1]]:
                    fullInput[params[2]] = 1;
                else:
                    fullInput[params[2]] = 0;
                currentExecutePointer += 4

            elif currentInstruction[0] == "08": # EQUAL TO
                if not binEnoughParameters(fullInput, currentExecutePointer, 3):
                    exitCode = 3;
                    break;
                params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 3);
                if fullInput[params[0]] == fullInput[params[1]]:
                    fullInput[params[2]] = 1;
                else:
                    fullInput[params[2]] = 0;
                currentExecutePointer += 4

            elif currentInstruction[0] == "99": # HALT
                exitCode = 1;
                break;
            else:
                exitCode = 2;
                break;
        else:
            exitCode = 4;
    return((returnValue, exitCode, fullInput, variableSave));
    if exitCode == 1:
        #print(fullInput);
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

def intcodeHalted(thrustExitMemory):
    if thrustExitMemory[1] != None:
        return True;
    return False;

constInput = [3,8,1001,8,10,8,105,1,0,0,21,38,55,64,89,114,195,276,357,438,99999,3,9,101,3,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,101,5,9,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,101,5,9,9,1002,9,5,9,101,5,9,9,102,3,9,9,4,9,99,3,9,101,3,9,9,1002,9,4,9,101,5,9,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99];

#fullInput = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

#constInput = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5];
phase = "55555";
setCheck = set();
maxThrusterSignal = 0;
maxAll = 0;
while int(phase) < 100000:
    setCheck = set();
    setCheck.add(phase[0]);
    setCheck.add(phase[1]);
    setCheck.add(phase[2]);
    setCheck.add(phase[3]);
    setCheck.add(phase[4]);
    firstLoop = True;
    codeHalted = False;
    memoryA = []
    memoryB = []
    memoryC = []
    memoryD = []
    memoryE = []
    prevEThrust = None;
    if len(setCheck) == 5 and "0" not in setCheck and "1" not in setCheck and "2" not in setCheck and "3" not in setCheck and "4" not in setCheck:
        while not codeHalted:
            if firstLoop:
                # A FIRST RUN
                thrustExitMemory = amplifier(constInput, phase[0], 0, 0, "A");
                memoryA = (thrustExitMemory[2].copy(), thrustExitMemory[3]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;
                # B FIRST RUN
                thrustExitMemory = amplifier(constInput, phase[1], thrustExitMemory[0], 0, "B");
                memoryB = (thrustExitMemory[2].copy(), thrustExitMemory[3]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # C FIRST RUN
                thrustExitMemory = amplifier(constInput, phase[2], thrustExitMemory[0], 0, "C");
                memoryC = (thrustExitMemory[2].copy(), thrustExitMemory[3]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # D FIRST RUN
                thrustExitMemory = amplifier(constInput, phase[3], thrustExitMemory[0], 0, "D");
                memoryD = (thrustExitMemory[2].copy(), thrustExitMemory[3]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # E FIRST RUN
                thrustExitMemory = amplifier(constInput, phase[4], thrustExitMemory[0], 0, "E");
                memoryE = (thrustExitMemory[2].copy(), thrustExitMemory[3]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;
                else:
                    prevEThrust = thrustExitMemory[0]



                #print(thrustExitMemory[0])



                if codeHalted:
                    if thrustExitMemory[0] > maxThrusterSignal:
                        maxThrusterSignal = thrustExitMemory[0];
                firstLoop = False;
            else:
                # A SUBSEQUENT RUNS
                thrustExitMemory = amplifier(memoryA[0], None, thrustExitMemory[0], memoryA[1], "A");
                memoryA = (thrustExitMemory[2].copy(), thrustExitMemory[3], thrustExitMemory[0]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # B SUBSEQUENT RUNS
                thrustExitMemory = amplifier(memoryB[0], None, thrustExitMemory[0], memoryB[1], "B");
                memoryB = (thrustExitMemory[2].copy(), thrustExitMemory[3], thrustExitMemory[0]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # C SUBSEQUENT RUNS
                thrustExitMemory = amplifier(memoryC[0], None, thrustExitMemory[0], memoryC[1], "C");
                memoryC = (thrustExitMemory[2].copy(), thrustExitMemory[3], thrustExitMemory[0]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # D SUBSEQUENT RUNS
                thrustExitMemory = amplifier(memoryD[0], None, thrustExitMemory[0], memoryD[1], "D");
                memoryD = (thrustExitMemory[2].copy(), thrustExitMemory[3], thrustExitMemory[0]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;

                # E SUBSEQUENT RUNS
                thrustExitMemory = amplifier(memoryE[0], None, thrustExitMemory[0], memoryE[1], "E");
                memoryE = (thrustExitMemory[2].copy(), thrustExitMemory[3], thrustExitMemory[0]);
                if intcodeHalted(thrustExitMemory):
                    codeHalted = True;
                else:
                    prevEThrust = thrustExitMemory[0];

                if memoryA != None:
                    if memoryA[2] > maxAll:
                        maxAll = memoryA[2];

                if memoryB != None:
                    if memoryB[2] > maxAll:
                        maxAll = memoryB[2];

                if memoryC != None:
                    if memoryC[2] > maxAll:
                        maxAll = memoryC[2];

                if memoryD != None:
                    if memoryD[2] > maxAll:
                        maxAll = memoryD[2];

                if memoryE != None:
                    if memoryE[2] > maxAll:
                        maxAll = memoryE[2];


        if codeHalted:
            if prevEThrust > maxThrusterSignal:
                maxThrusterSignal = prevEThrust;

    phase = str(int(phase) + 1);
    while len(phase) < 5:
        phase = "0" + phase;
#print(maxThrusterSignal);
