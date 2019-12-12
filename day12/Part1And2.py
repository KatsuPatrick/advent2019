import math

def applyGravity(position, velocity):#
    newVelocity = {}
    newVelocityDelta = {}
    for i in velocity:
        newVelocityDelta[i] = [0, 0, 0]
        for j in velocity:
            updatedVelocity = []
            if i != j:
                for k in range(len(velocity[i])):
                    if position[i][k] < position[j][k]:
                        updatedVelocity.append(1);
                    elif position[i][k] > position[j][k]:
                        updatedVelocity.append(-1);
                    else:
                        updatedVelocity.append(0);
                for l in range(len(newVelocityDelta[i])):
                    newVelocityDelta[i][l] += updatedVelocity[l];
    for i in newVelocityDelta:
        newVelocity[i] = []
        for j in range(len(newVelocityDelta[i])):
            newVelocity[i].append(newVelocityDelta[i][j] + velocity[i][j]);
    return newVelocity;

def applyVelocity(position, velocity):
    for i in position:
        for j in range(len(position[i])):
            position[i][j] += velocity[i][j];
    return position;

def calculateTotalEnergy(position, velocity):
    totalEnergy = 0
    for i in position:
        totalPotential = 0
        for j in position[i]:
            totalPotential += abs(j);
        totalKinetic = 0
        for j in velocity[i]:
            totalKinetic += abs(j);
        totalEnergy += totalPotential * totalKinetic;
    return totalEnergy;

startPosition = {}
startPosition["Io"] =[9, 13, -8];
startPosition["Europa"] = [-3, 16, -17];
startPosition["Ganymede"] = [-4, 11, -10];
startPosition["Callisto"] = [0, -2, -2];

#startPosition["Io"] =[-1, 0, 2];
#startPosition["Europa"] = [2, -10, -7];
#startPosition["Ganymede"] = [4, -8, 8];
#startPosition["Callisto"] = [3, 5, -1];

#startPosition["Io"] =[-8, -10, 0];
#startPosition["Europa"] = [5, 5, 10];
#startPosition["Ganymede"] = [2, -7, 3];
#startPosition["Callisto"] = [9, -8, -3];

startVelocity = {}
startVelocity["Io"] = [0, 0 ,0];
startVelocity["Europa"] = [0, 0 ,0];
startVelocity["Ganymede"] = [0, 0 ,0];
startVelocity["Callisto"] = [0, 0 ,0];

time = 0;
position = startPosition.copy();
velocity = startVelocity.copy();
totalEnergy = calculateTotalEnergy(position, velocity)

firstRepeat0 = None
firstRepeat1 = None
firstRepeat2 = None

#while time < 1000:
while firstRepeat0 == None or firstRepeat1 == None or firstRepeat2 == None:
    velocity = applyGravity(position, velocity)

    position = applyVelocity(position, velocity)

    time += 1

    totalEnergy = calculateTotalEnergy(position, velocity);

    if firstRepeat0 == None:
        coordRepeat = True;
        for i in velocity:
            if velocity[i][0] != startVelocity[i][0]:
                coordRepeat = False;
            if position[i][0] != startPosition[i][0]:
                coordRepeat = False;
        if coordRepeat == True:
            firstRepeat0 = time;

    if firstRepeat1 == None:
        coordRepeat = True;
        for i in velocity:
            if velocity[i][1] != startVelocity[i][1]:
                coordRepeat = False;
            if position[i][1] != startPosition[i][1]:
                coordRepeat = False;
        if coordRepeat == True:
            firstRepeat1 = time;

    if firstRepeat2 == None:
        coordRepeat = True;
        for i in velocity:
            if velocity[i][2] != startVelocity[i][2]:
                coordRepeat = False;
            if position[i][2] != startPosition[i][2]:
                coordRepeat = False;
        if coordRepeat == True:
            firstRepeat2 = time;
    if time == 1000:
        print("Total energy in system at Time " + str(time) + ": " + str(totalEnergy));

print("First instance of the universe repeating: Time " + str(firstRepeat0 * firstRepeat1 * firstRepeat2))
