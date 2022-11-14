import RPi.GPIO as GPIO
import time
def initBuzz(vPinBuzzer):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(vPinBuzzer, GPIO.OUT)

def buzz(vPinBuzzer):
    GPIO.output(vPinBuzzer, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(vPinBuzzer, GPIO.LOW)
