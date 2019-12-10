import math;

inputStream = open("./input", "r");
#inputStream = open("./testInput", "r");
#inputStream = open("./testInput2", "r");
seperatedInput = inputStream.readlines();
sanitisedInput = []
for i in seperatedInput:
    sanitisedInput.append(i[:]);

gridOfAsteroids = set();

for i in range(0, len(sanitisedInput)):
    notI = len(sanitisedInput) - 1 - i
    for j in range(0, len(sanitisedInput[notI])):
        if sanitisedInput[notI][j] == "#":
            gridOfAsteroids.add(tuple((j, notI)))

gridOfAnglesCovered = {};
maxAsteroidsDetected = 0
maxAsteroidsDetectedAsteroid = None
gridOfAnglesSave = None
for i in gridOfAsteroids:
    gridOfAnglesCovered = {};
    for j in gridOfAsteroids:
        if i != j:
            gcd = None;
            gcd = math.gcd(j[0] - i[0], j[1] - i[1])
            if (int((j[0] - i[0]) / gcd), int((j[1] - i[1]) / gcd)) not in gridOfAnglesCovered:
                gridOfAnglesCovered[(int((j[0] - i[0]) / gcd), int((j[1] - i[1]) / gcd))] = {((j[0], j[1]))}
            else:
                gridOfAnglesCovered[(int((j[0] - i[0]) / gcd), int((j[1] - i[1]) / gcd))].add((j[0], j[1]));
    if len(gridOfAnglesCovered) > maxAsteroidsDetected:
        maxAsteroidsDetected = len(gridOfAnglesCovered);
        maxAsteroidsDetectedAsteroid = i;
        gridOfAnglesSave = gridOfAnglesCovered.copy()



gridOfAnglesCovered = gridOfAnglesSave;

#print(gridOfAnglesCovered)
anglesDict = {}
for i in gridOfAnglesCovered:
    #print(i);
    if i[1] == 0:
        if i[0] >= 0:
            anglesDict[math.degrees(math.pi/2)] = ((i[0], i[1]), len(gridOfAnglesCovered[(i[0], i[1])]));
        else:
            anglesDict[math.degrees((3/2)*math.pi)] = ((i[0], i[1]), len(gridOfAnglesCovered[(i[0], i[1])]));
    else:
        angle = math.degrees(math.atan(i[0]/i[1]))
        if i[1] < 0:
            angle += 180
        elif i[0] < 0:
            angle += 360
        angle = angle + 180
        if angle >= 360:
            angle = angle - 360
        if angle == 0:
            angle = 360;
        anglesDict[360 - angle] = ((i[0], i[1]), len(gridOfAnglesCovered[(i[0], i[1])]));

#print(anglesDict);
orderedAngles = []
for i in anglesDict:
    orderedAngles.append(i);
orderedAngles.sort()



#for i in orderedAngles:
    #print((gridOfAnglesCovered[anglesDict[i][0]]))

position = 0
loop = 1
hitCount = 0
hitNumber = 330
while hitCount < hitNumber:
    if anglesDict[orderedAngles[position]][1] >= loop:
        hitCount += 1;
        print(str(hitCount) + ": " + str(gridOfAnglesCovered[anglesDict[orderedAngles[position]][0]]))
        if hitCount == hitNumber:
            break;
    position += 1
    if position >= len(orderedAngles):
        position = 0
        loop += 1
        print("loop")
print("The " + str(hitNumber) + "th asteroid to be destroyed is on the line " + str(gridOfAnglesCovered[    anglesDict[orderedAngles[position]][0]    ]) + ", " + str(loop) + " from the asteroid at " + str(maxAsteroidsDetectedAsteroid));
