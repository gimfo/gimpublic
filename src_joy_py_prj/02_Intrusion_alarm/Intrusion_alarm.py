import RPi.GPIO as GPIO
import time

buzzer_pin = 18
# Sound-Pin definieren
pir_pin = 23

# GPIO-Modus setzen
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    while True:
        # Pruefe ob ein Geraeusch erkannt wurde
        if(GPIO.input(pir_pin) == True):
            # Aktiviere Buzzer
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            # Deaktiviere Buzzer
            GPIO.output(buzzer_pin, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
