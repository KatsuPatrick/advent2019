import math

def containsAdjacent(i):
    stringI = str(i);
    if (stringI[0] == stringI[1] and stringI[1] != stringI[2]) or (stringI[1] == stringI[2] and stringI[0] != stringI[1] and stringI[2] != stringI[3]) or (stringI[2] == stringI[3] and stringI[1] != stringI[2] and stringI[3] != stringI[4]) or (stringI[3] == stringI[4] and stringI[2] != stringI[3] and stringI[4] != stringI[5]) or (stringI[4] == stringI[5] and stringI[4] != stringI[3]):
        return True;
    return False;

def neverDecreases(i):
    stringI = str(i);
    if int(stringI[0]) <= int(stringI[1]) and int(stringI[1]) <= int(stringI[2]) and int(stringI[2]) <= int(stringI[3]) and int(stringI[3]) <= int(stringI[4]) and int(stringI[4]) <= int(stringI[5]):
        return True;
    return False;

i = 123257;
j = 647015;
count = 0;
while i < j:
    if len(str(i)) == 6 and containsAdjacent(i) and neverDecreases(i):
        count += 1;
    i += 1;
print(count)
