import math;

inputStream = open("./input", "r");
#inputStream = open("./testInput", "r");
seperatedInput = inputStream.readlines();
sanitisedInput = []
for i in seperatedInput:
    sanitisedInput.append(i[:]);
#print(sanitisedInput)

gridOfAsteroids = set();

for i in range(0, len(sanitisedInput)):
    #print(sanitisedInput[i])
    for j in range(0, len(sanitisedInput[i])):
        #print(j);
        if sanitisedInput[i][j] == "#":
            gridOfAsteroids.add(tuple((j, i)))

#print(len(gridOfAsteroids));
gridOfAnglesCovered = set();
maxAsteroidsDetected = 0
for i in gridOfAsteroids:
    gridOfAnglesCovered = set();
    for j in gridOfAsteroids:
        if i != j:
            gcd = None;
            gcd = math.gcd(j[0] - i[0], j[1] - i[1])
            gridOfAnglesCovered.add(((j[0] - i[0]) / gcd, (j[1] - i[1]) / gcd));
    if len(gridOfAnglesCovered) > maxAsteroidsDetected:
        maxAsteroidsDetected = len(gridOfAnglesCovered);
print(maxAsteroidsDetected);
