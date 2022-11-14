import RPi.GPIO as GPIO
import time
def buzz(vPinBuzzer):
    GPIO.output(vPinBuzzer, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(vPinBuzzer, GPIO.LOW)
