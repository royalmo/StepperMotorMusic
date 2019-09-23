from midi import read_midifile
import sys

def convert_midi(sequence):
    tempo = 1
    lprincipal = []
    separated = sequence.split('\n')
    for line in separated:
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
                    l = l + [int(element[1:])]
            lprincipal.append(l)
    return lprincipal

def generateDict(l, nummotor):
    d = {}
    i = 0
    k = 0
    b = False
    for element in l:
        if element[1] == nummotor:
            i = i + element[0]
            if element[3] != 0:
                d[i] = element[2]
            else:
                if k != 0:
                    if l[k-1][3] != 0:
                        d[i] = l[k-1][2]
                        b = True
                if b == False:
                    d[i] = 0
        k = k + 1
        b = False
    return d

def crearllista(d1, d2):
        res = []
        keys = []
        for k in d1:
            keys.append(k)
        for k in d2:
            if k not in keys:
                keys.append(k)
        keys.sort()
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

        pitches = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32058, 30103, 28371, 26827, 25441, 24190, 22527, 21539, 20208, 19030, 17982, 17041, 15929, 15185, 14293, 13499, 12621, 11995, 11294, 10553, 10004, 9415, 8891, 8347, 7930, 7434, 6994, 6603, 6210, 5961, 5914, 5205, 5802, 4608, 4345, 4092, 3949, 3717, 3510, 3301, 3115, 2920,   2700, 2503, 2300, 2120, 2000, 1900, 1800, 1675, 1560, 1480, 1400, 1325, 1245, 1175, 1100, 1030, 960, 900, 842, 785, 727, 675, 640, 600, 565, 530, 495, 465, 435, 410, 391, 353, 340, 320, 303, 284, 258, 238, 215, 201, 184, 168, 153, 139, 125, 113, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

        res = ult
        ult = []

        for line in res:
            line[1] = pitches[line[1]]
            line[2] = pitches[line[2]]
            ult.append(line)

        ult.append([0, 0, 0, 1, 0])
        return ult

def crearfitx(l, ubi):
    fout = open(ubi, "w")
    for line in l:
        fout.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "\n")
    fout.close()


def convert_midifile(ubi1, ubi2):
    sequence = str(read_midifile(ubi1))
    l = convert_midi(sequence)
    d1 = generateDict(l, 0)
    d2 = generateDict(l, 1)
    f = crearllista(d1, d2)
    crearfitx(f, ubi2)

convert_midifile(str(sys.argv[1]), str(sys.argv[2]))
