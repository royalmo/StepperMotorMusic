from gpiozero import LED, Button
from threading import Thread
from time import sleep

def blink():
    global blinking
    while True:
        if blinking:
            led.on()
            sleep(.5)
            led.off()
            sleep(.5)
        else:
            led.on()
            sleep(1)

def main():
    dis.on()
    global blinking
    blinking = True
    Thread(target=blink).start()
    while True:
        stop.wait_for_press()
        stop.wait_for_release()
        dis.off()
        blinking = False
        stop.wait_for_press()
        stop.wait_for_release()
        dis.off()
        blinking = True

led = LED(17)
dis = LED(12)
stop = Button(19)

if __name__ == "__main__":
    main()
