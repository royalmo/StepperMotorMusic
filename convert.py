from midi import read_midifile

def convert_midi(sequence):
    sequence = fin.readlines()
    fin.close()
    tempo = 1
    lprincipal = []
    for line in sequence:
        if "NoteOnEvent" in line:
            pos = line.find("(")
            substr = line[pos+1:-3]
            laux = substr.split(",")
            l = []
            for element in laux:
                if "=" in element:
                    if "[" in element:
                        l = l + [int(element.split("=")[1][1:])]
                    else:
                        l = l + [int(element.split("=")[1])]
                else:
                    l = l + [int(element[1:-1])]
            lprincipal.append(l)
    return lprincipal

def generateDict(l, nummotor):
    d = {}
    i = 0
    for element in l:
        if element[1] == nummotor:
            i = i + element[0]
            if element[3] != 0:
                d[i] = element[2]
            else:
                d[i] = 0
    return d

def crearllista(d1, d2):
        res = []
        keys = []
        for k in d1:
            keys.append(k)
        for k in d2:
            if k not in keys:
                keys.append(k)
        for k in keys:
            res.append([k, d1.get(k, "n"), d2.get(k, "n"), 0, k])
        i = 0
        ult = []
        for line in res:
            if line[1] == "n" and i > 0:
                line[1] = res[i-1][1]
            elif line[1] == "n":
                line[1] = 0
            if line[2] == "n" and i > 0:
                line[2] = res[i-1][2]
            elif line[2] == "n":
                line[2] = 0
            ult.append(line)
            i += 1

        t = 0
        s = 0
        res = ult
        ult = []

        for line in res:
            s = line[0]
            line[0] = line[0] - t
            t = s
            ult.append(line)

        pitches = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32258, 30303, 28571, 27027, 25641, 24390, 22727, 21739, 20408, 19230, 18182, 17241, 16129, 15385, 14493, 13699, 12821, 12195, 11494, 10753, 10204, 9615, 9091, 8547, 8130, 7634, 7194, 6803, 6410, 6061, 5714, 5405, 5102, 4808, 4545, 4292, 4049, 3817, 3610, 3401, 3215, 3030, 2865, 2703, 2551, 2410, 2273, 2146, 2024, 1912, 1805, 1704, 1608, 1517, 1433, 1351, 1276, 1203, 1136, 1073, 1012, 955, 902, 851, 803, 758, 716, 676, 638, 602, 568, 536, 506, 478, 451, 426, 402, 379, 358, 338, 315, 301, 284, 268, 253, 239, 225, 213, 201, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        res = ult
        ult = []

        for line in res:
            line[1] = pitches[line[1]]
            line[2] = pitches[line[2]]
            ult.append(line)

        ult.append([0, 0, 0, 1, 0])
        return ult

def crearfitx(l, ubi):
    fout = open(ubi, "x")
    for line in l:
        fout.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "\n")
    fout.close()


def convert_midifile(ubi1, ubi2):
    sequence = read_midifile(ubi1)
    l = convert_midi(sequence)
    d1 = generateDict(l, 0)
    d2 = generateDict(l, 1)
    f = crearllista(d1, d2)
    crearfitx(f, ubi2)
