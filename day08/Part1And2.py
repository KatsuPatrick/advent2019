import math;

inputStream = open("./input", "r");
seperatedInput = inputStream.readlines();
sanitisedInput = str(seperatedInput)[2:-4];
#print(sanitisedInput);
image = {};
layerName = 0;
for i in range(0, len(sanitisedInput)//150):
    image[layerName] = sanitisedInput[150 * i:150 * (i + 1)];
    layerName += 1;
minZeroCount = math.inf;
oneTwoStore = None;
for i in image:
    #print(i)
    #print(len(image[i]));
    zeroCount = 0;
    oneCount = 0;
    twoCount = 0
    for j in image[i]:
        #print(j);
        if j == "0":
            zeroCount += 1;
            #print(zeroCount);
        elif j == "1":
            oneCount += 1;
        elif j == "2":
            twoCount += 1
    #print(zeroCount);
    if zeroCount < minZeroCount:
        minZeroCount = zeroCount;
        oneTwoStore = twoCount * oneCount;
#print(image);
#print(oneTwoStore);
decodedImage = {}
currentLayer = 0
while len(decodedImage) < 150:
    currentIndex = 0
    while currentIndex < 150:
        if not currentIndex in decodedImage:
            if image[currentLayer][currentIndex] != "2":
                decodedImage[currentIndex] = image[currentLayer][currentIndex];
        currentIndex += 1
    currentLayer += 1
for i in decodedImage:
    if decodedImage[i] == "0":
        decodedImage[i] = " ";
    else:
        decodedImage[i] = "@";
for i in range(0, 6):
    currentString = ""
    for j in range(0, 25):
        currentString = currentString + decodedImage[(25 * i) + j];
    print(currentString)
