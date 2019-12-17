import math;
import re;

inputStream = open("./input", "r");
listInput = inputStream.readlines();
fftInput = listInput[0][:-1]
#print(sanitisedInput);
#print();
#fftInput = "80871224585914546619083218645595";
basePattern = (0, 1, 0, -1);

def singleEfficientOutputValue(inputIndex, fullInput):
    sum = 0
    fullOneLoops = math.ceil((len(fullInput) - inputIndex) / ((inputIndex + 1) * 4)) - 1
    for i in range(fullOneLoops): #loops as many times as sections of 1's in effective basePattern, aside from the last section
        for j in range(inputIndex + 1)
            sum += int(fullInput[inputIndex + j + (i * 4 * (inputIndex + 1))])
    for j in range(min(   len(fullInput[inputIndex + (fullOneLoops * 4 * (inputIndex + 1)):])    , inputIndex + 1)):
        sum += int(fullInput[inputIndex + j + (fullOneLoops * 4 * (inputIndex + 1))]);



def singleOutputValue(inputIndex, fullInput):
    global basePattern;

    patternIndex = 0
    modifiedBasePattern = [];
    for i in range(len(fullInput) + 1):
        patternIndex = patternIndex % 4;
        for i in range(inputIndex + 1):
            modifiedBasePattern.append(basePattern[patternIndex]);
        patternIndex += 1;
    modifiedBasePattern.pop(0);

    sum = 0;
    for i in range(len(fullInput)):
        sum += int(fullInput[i]) * modifiedBasePattern[i];

    return abs(sum) % 10;

def fftLoop(fullInput):

    output = "";
    for i in range(len(fullInput)):
        output += str(singleOutputValue(i, fullInput));
        if fullInput[i] == "0":
            if output[-1] != "0":
                print(fullInput, output, i);
                input();
    return output;

def multipleFFT(fftInput, loops):
    fullInput = fftInput;
    for i in range(loops):
        print(i);
        fullInput = fftLoop(fullInput);
    return fullInput;

print(len(fftInput));
print(multipleFFT(fftInput, 100));
