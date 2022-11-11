# -*- coding: utf-8 -*-
#!/usr/bin/env python
import threading
import time
import sys
import RPi.GPIO as GPIO
import smbus
import math
import datetime

# GPIO-Modus setzen
GPIO.setmode(GPIO.BCM)

class Stepmotor:

    def __init__(self):
        # Pins definieren
        self.pin_A = 5
        self.pin_B = 6
        self.pin_C = 13
        self.pin_D = 25
        self.interval = 0.0011

        # Pins als Ausgabe konfigurieren
        GPIO.setup(self.pin_A,GPIO.OUT)
        GPIO.setup(self.pin_B,GPIO.OUT)
        GPIO.setup(self.pin_C,GPIO.OUT)
        GPIO.setup(self.pin_D,GPIO.OUT)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)
        GPIO.output(self.pin_D, False)

    def Step1(self):
        GPIO.output(self.pin_D, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)

    def Step2(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_C, False)

    def Step3(self):
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_C, False)

    def Step4(self):
        GPIO.output(self.pin_B, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)

    def Step5(self):
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)

    def Step6(self):
        GPIO.output(self.pin_A, True)
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)

    def Step7(self):
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)

    def Step8(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_A, False)

    def turn(self,count):
        for i in range (int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def turnSteps(self, count):
        # Drehe um n Schritte
        for i in range (count):
            self.turn(1)

    def turnDegrees(self, count):
        # Drehe um n Grad
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        # Drehung um Distanzwert
        self.turn(round(512*dist/(2*math.pi*rad),0))


def step():
    print("Bewegung gestartet!")
    motor = Stepmotor()
    print("360 Grad Drehung")
    for i in range(7):
        motor.turnDegrees(360)
    print("Bewegung angehalten")

def main():
    step()


try:
    if __name__ == "__main__":
        number_name = 2
        main()


except KeyboardInterrupt:
    GPIO.cleanup()
