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
    global act
    while True:
        if act[0] != 0:
            sm1.on()
            sm1.off()
            sleep(float(act[0]) / 1000000)

def step2():
    global act
    while True:
        if act[1] != 0:
            sm2.on()
            sm2.off()
            sleep(float(act[1]) / 1000000)

def getpiches():
    pitches = []
    with open('/home/pi/StepperMotorMusic/pitches.txt', 'r') as all_piches:
        for line in all_piches:
            pitches.append(int(line[:-1]))
    return pitches

def getlines(location):
    with open(location, 'r') as song:
        lines = []
        for line in song:
            line = line[:-1]
            lines.append(line.split())
    return lines

def play_song(location):
    global act
    values = [0, 0, 0, 0]
    exit = 0
    i = 0
    timer = 0
    lines = getlines(location)
    pitches = getpiches()
    while exit == 0:
        i = i + 1
        values = lines[i]
        act = [pitches[int(values[1])], pitches[int(values[2])]]
        if stop.is_pressed:
            act = [0, 0]
            exit = 1
        if values[3] == '1':
            act = [0, 0]
            exit = 2
        if int(values[0]) > 0:
            sleep(float(values[0]) / 1000000)
    if exit == 1:
        return i
    else:
        return 0

sm1 = LED(5)
sm2 = LED(6)
stop = Button(2)

act = [0, 0]

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
print ( play_song("/home/pi/StepperMotorMusic/saves/sweetchildofmine.txt") )
