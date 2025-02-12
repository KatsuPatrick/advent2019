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

fullInput = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,78,5,225,1,166,139,224,101,-74,224,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1002,136,18,224,101,-918,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1001,83,84,224,1001,224,-139,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,55,20,225,1101,53,94,225,2,217,87,224,1001,224,-2120,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,102,37,14,224,101,-185,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1101,8,51,225,1102,46,15,225,1102,88,87,224,1001,224,-7656,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1101,29,28,225,1101,58,43,224,1001,224,-101,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,1101,93,54,225,101,40,191,224,1001,224,-133,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1101,40,79,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,226,677,224,1002,223,2,223,1005,224,329,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,344,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,389,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,419,101,1,223,223,107,677,226,224,1002,223,2,223,1006,224,434,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,449,101,1,223,223,1107,226,226,224,1002,223,2,223,1005,224,464,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,479,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,494,101,1,223,223,107,677,677,224,102,2,223,223,1005,224,509,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,539,1001,223,1,223,108,677,226,224,102,2,223,223,1006,224,554,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,569,1001,223,1,223,8,677,677,224,1002,223,2,223,1005,224,584,1001,223,1,223,7,677,677,224,1002,223,2,223,1005,224,599,101,1,223,223,1108,226,226,224,102,2,223,223,1006,224,614,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,629,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,644,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,674,101,1,223,223,4,223,99,226];

#fullInput = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

#fullInput = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9];

currentExecutePointer = 0;
exitCode = 0;
while exitCode == 0:
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
            if not binEnoughParameters(fullInput, currentExecutePointer, 1):
                exitCode = 3;
                break;
            params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 1);
            print(">>> ");
            userInput = input();
            if userInput == "0" or userInput == "1" or userInput == "2" or userInput == "3" or userInput == "4" or userInput == "5" or userInput == "6" or userInput == "7" or userInput == "8" or userInput == "9":
                fullInput[params[0]] = int(userInput);
            else:
                exitCode = 5;
                break;
            currentExecutePointer += 2;


        elif currentInstruction[0] == "04": # OUTPUT
            if not binEnoughParameters(fullInput, currentExecutePointer, 1):
                exitCode = 3;
                break;
            params = retrieveAllParams(fullInput, currentExecutePointer, currentInstruction[1], 1);
            print(fullInput[params[0]]);
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
