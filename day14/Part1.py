import math;
import re;

def addMaterial(requiredMaterial, countAndMaterial):
    if countAndMaterial[1] not in requiredMaterial:
        requiredMaterial[countAndMaterial[1]] = 0;
    requiredMaterial[countAndMaterial[1]] += countAndMaterial[0];
    return requiredMaterial;

def doReaction(currentMaterial, reactionMaterial, count):
    global reactions;
    global oreBought;

    #print(reactionMaterial, count)
    usedMaterialGroups = {}
    for i in reactions[reactionMaterial][0]:
        newCount = 0
        if i[1] == 'ORE':
            if oreBought + (i[0] * count) > 1000000000000:
                usedMaterialGroups['ORE'] = (1000000000000 - oreBought) // i[0];
                oreBought = 1000000000000 - oreBought;
            else:
                oreBought += i[0] * count;
        else:
            #if reactionMaterial == 'FUEL' and count == 1000:
            print(i[0], count, i[1]);
                #print(currentMaterial);
            print(currentMaterial[i[1]])
            print(reactions[i[1]][1]);
                #print(oreBought)
                #input();
            newCount = (((i[0] * count) - currentMaterial[i[1]]) // reactions[i[1]][1])
            if ((i[0] * count) - currentMaterial[i[1]]) % reactions[i[1]][1] != 0:
                newCount += 1
            returnedMaterialCount = math.inf;
            if newCount > 0:
                currentMaterial, returnedMaterialCount = doReaction(currentMaterial, i[1], newCount);
                print(currentMaterial);
                print(str(count) + " " + reactionMaterial + " => " + i[1]);
                print(newCount);
                print(oreBought)
                input();
                currentMaterial[i[1]] -= returnedMaterialCount;
            usedMaterialGroups[i[1]] = returnedMaterialCount // i[0]
    returnedMaterialGroupCount = math.inf
    for i in usedMaterialGroups:
        if usedMaterialGroups[i] < count:
            returnedMaterialGroupCount = usedMaterialGroups[i];
        if i == 'ORE':
            print(usedMaterialGroups, count);
    if count < returnedMaterialGroupCount:
        returnedMaterialGroupCount = count;
    currentMaterial[reactionMaterial] += reactions[reactionMaterial][1] * returnedMaterialGroupCount;
    if reactionMaterial == 'FUEL' and returnedMaterialGroupCount == 0:
        #print(reactions[reactionMaterial][1] * returnedMaterialGroupCount)
        print(currentMaterial['FUEL'])
        input();
    return currentMaterial, reactions[reactionMaterial][1] * returnedMaterialGroupCount;

inputStream = open("./input", "r");
inputStream = open("./inputTest", "r");




seperatedInput = inputStream.readlines();
halvedInput = [];
sanitisedInput = set();
for i in range(len(seperatedInput)):
    seperatedInput[i] = seperatedInput[i][:-1];
    halvedInput.append(re.split(" => ", seperatedInput[i]));
    halvedInput[i] = [re.split(", ", halvedInput[i][0]), halvedInput[i][1]]
    currentLine = [];
    for j in range(len(halvedInput[i][0])):
        currentLine.append(tuple(re.split(" ", halvedInput[i][0][j])))
        currentLine[j] = tuple([int(currentLine[j][0]), currentLine[j][1]])
    splitOutput = re.split(" ", halvedInput[i][1]);
    splitOutput = [int(splitOutput[0]), splitOutput[1]];
    sanitisedInput.add((tuple(currentLine), tuple(splitOutput)));
#print(sanitisedInput);
requiredMaterial = {};
allMaterials = set();
oreCreates = {};
countOutputOccurance = {}
reactions = {}
for i in sanitisedInput:
    if i[1][1] not in countOutputOccurance:
        countOutputOccurance[i[1][1]] = 0;
    countOutputOccurance[i[1][1]] += 1;
    reactions[i[1][1]] = (i[0], i[1][0])
    if i[1][1] == 'FUEL':
        for j in i[0]:
            requiredMaterial = addMaterial(requiredMaterial, j)
    for j in i[0]:
        if j[1] == 'ORE':
            if i[1][1] in oreCreates:
                print("o no");
            oreCreates[i[1][1]] = i[1][0];
        allMaterials.add(j[1])
allMaterials.remove('ORE');
#print(requiredMaterial);
#print()
#print(allMaterials);
allMaterialsImmediateSubsidaries = {};
for i in allMaterials:
    allMaterialsImmediateSubsidaries[i] = set()
    for j in sanitisedInput:
        if j[1][1] == i:
            for k in j[0]:
                allMaterialsImmediateSubsidaries[i].add(k[1]);
allMaterialsSubsidaries = {}
for i in allMaterialsImmediateSubsidaries:
    allMaterialsSubsidaries[i] = allMaterialsImmediateSubsidaries[i].copy();
oreCheck = False;
while not oreCheck:
    oreCheck = True;
    for i in allMaterialsSubsidaries:
        tempSet = set()
        for j in allMaterialsSubsidaries[i]:
            if j != 'ORE':
                for k in allMaterialsSubsidaries[j]:
                    tempSet.add(k);
        oldSet = allMaterialsSubsidaries[i].copy();
        for j in tempSet:
            allMaterialsSubsidaries[i].add(j);
        if oldSet != allMaterialsSubsidaries[i]:
            oreCheck = False;
#print(allMaterialsSubsidaries);
#print();
#print(allMaterialsImmediateSubsidaries);
#print();
#print(requiredMaterial);
#print();
#print(sanitisedInput);
currentMaterial = {};
oreBought = 0;
for i in allMaterials:
    currentMaterial[i] = 0;
currentMaterial['FUEL'] = 0;

currentMaterial, fuelReturned = doReaction(currentMaterial, 'FUEL', 1);
print(oreBought);

while oreBought / 1000000000000 < 0.9995:
    currentMaterial, fuelReturned = doReaction(currentMaterial, 'FUEL', 10000);

print(currentMaterial);
while True:
    currentMaterial, fuelReturned = doReaction(currentMaterial, 'FUEL', 1);
#for i in requiredMaterial:
    #while requiredMaterial[i] < currentMaterial[i]:
        #   currentMaterial = doReaction(currentMaterial, i)
print(oreBought);
