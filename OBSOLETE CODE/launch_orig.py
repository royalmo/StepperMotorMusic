from time import sleep
from subprocess import check_output
from threading import Thread
from gpiozero import LED, Button

def ena_and_blink():
    led = LED(17)
    dis = LED(12)
    led.on()
    dis.on()
    sleep(4.75)
    dis.off()
    sleep(0.25)
    dis.on()
    while True:
        if check_output("sudo iw dev wlan0 station dump", shell=True) == b'':
            dis.off()
            led.off()
            sleep(.450)
            led.on()
            sleep(.450)
        else:
            led.on()
            dis.off()  #ENABLE LATER
            sleep(.900)

def step1():
    nota1 = 0
    while True:
        with open('/home/pi/smm/playing.txt', 'r') as notes:
            nota1 = int(notes.readlines()[0].rstrip()) #He doesnt found anything
        if nota1 != 0:
            sm1.on()
            sm1.off()
            sleep((float(nota1[0]) / 1000000) - 0.000001)

def step2():
    nota2 = 0
    while True:
        with open('/home/pi/smm/playing.txt', 'r') as notes:
            nota2 = int(notes.readlines()[1].rstrip())
        if nota2 != 0:
            sm2.on()
            sm2.off()
            sleep((float(nota2[1]) / 1000000) - 0.000001)

def getpiches():
    pitches = []
    with open('/home/pi/smm/pitches.txt', 'r') as all_piches:
        for line in all_piches:
            pitches.append(line[:-1])
    return pitches

def getlines(location):
    with open(location, 'r') as song:
        lines = []
        for line in song:
            line = line[:-1]
            lines.append(line.split())
    return lines

def play_song(location):
    sm1_pitch = '0'
    sm2_pitch = '0'
    values = [0, 0, 0, 0]
    exit = 0
    i = 0
    lines = getlines(location)
    pitches = getpiches()
    while exit == 0:
        i = i + 1
        values = lines[i]
        sm1_pitch = pitches[int(values[1])]
        sm2_pitch = pitches[int(values[2])]
        with open('/home/pi/smm/playing.txt', 'w') as f:
            f.write(str(sm1_pitch) + '\n' + str(sm2_pitch) + '\n')
        if stop.is_pressed:
            with open('/home/pi/smm/playing.txt', 'w') as f:
                f.write('0\n0\n')
            exit = 1
        if values[3] == '1':
            with open('/home/pi/smm/playing.txt', 'w') as f:
                f.write('0\n0\n')
            exit = 2
        if int(values[0]) != 0:
            sleep((float(values[0]) / 1000000) - 0.000001)
    if exit == 1:
        return i
    else:
        return 0

sm1 = LED(5)
sm2 = LED(6)
stop = Button(2)

with open('/home/pi/smm/playing.txt', 'w') as f:
    f.write('0\n0')

enafunction = Thread(target=ena_and_blink)
enafunction.start()

sleep(4.75)
for i in range(0, 400):
  sm1.on()
  sm2.on()
  sm1.off()
  sm2.off()
  sleep(.0005)

s1 = Thread(target=step1)
s1.start()

s2 = Thread(target=step2)
s2.start()

sleep(10)
print ( play_song("/home/pi/smm/transformed/sweetchildofmine.txt") )
