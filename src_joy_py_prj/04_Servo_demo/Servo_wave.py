# -*- coding: utf-8 -*-
#!/usr/bin/env python
import threading
import time
import sys
import RPi.GPIO as GPIO
import smbus
import math
import datetime

# Setze GPIO-Modus
GPIO.setmode(GPIO.BCM)

class Servo:
    def __init__( self, pin, direction ):

        GPIO.setup( pin, GPIO.OUT )
        self.pin = int( pin )
        self.direction = int( direction )
        self.servo = GPIO.PWM( self.pin, 50 )
        self.servo.start(0.0)

    def cleanup( self ):
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    def currentdirection( self ):
        return self.direction

    def _henkan( self, value ):
        return 0.05 * value + 7.0

    def setdirection( self, direction, speed ):
        for d in range( self.direction, direction, int(speed) ):
            self.servo.ChangeDutyCycle( self._henkan( d ) )
            self.direction = d
            time.sleep(0.1)
            self.servo.ChangeDutyCycle( self._henkan( direction ) )
            self.direction = direction


def moveServo():
    servo_pin = 19
    s = Servo(servo_pin,0)
    for i in range(14):
        print("Drehe nach links...")
        s.setdirection( 100, 80 )
        #10
        time.sleep(1)
        print("Drehe nach rechts...")
        s.setdirection( -100, -80 )
        time.sleep(1)
    s.cleanup()

def main():
    moveServo()


try:
    servo_pin = 19
    s = Servo(servo_pin,0)
    for i in range(14):
        print("Drehe nach links...")
        s.setdirection( 100, 80 )
        #10
        time.sleep(1)
        print("Drehe nach rechts...")
        s.setdirection( -100, -80 )
        time.sleep(1)
    s.cleanup()

except KeyboardInterrupt:
    s.cleanup()
