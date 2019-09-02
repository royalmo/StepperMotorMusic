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

        ult.append([0, 0, 0, 1, 0])
        return ult

def crearfitx(l, ubi):
    fout = open(ubi, "x")
    for line in l:
        fout.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " + str(line[4]) + "\n")


sequence = read_midifile("C:/Users/royal/Desktop/smm/HB.mid")
l = convert_midi(sequence)
d1 = generateDict(l, 0)
d2 = generateDict(l, 1)
f = crearllista(d1, d2)
crearfitx(f, "C:/Users/royal/Desktop/smm/HB_conv.txt")
print("done!")
