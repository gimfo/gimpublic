import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import time
import math
GPIO.setmode(GPIO.BCM)

TRIG = 16
ECHO = 26

class LCDModule():

    def __init__(self):
        # Spalten und Reihen des LCD definieren
        self.address = 0x21
        self.lcd_columns = 16
        self.lcd_rows = 2
        # LCD initialisieren
        self.lcd = LCD.Adafruit_CharLCDBackpack(address=self.address)
    def turn_off(self):
        # Hintergrundbeleuchtung ausschalten
        self.lcd.set_backlight(1)
    def turn_on(self):
        # Hintergrundbeleuchtung einschalten
        self.lcd.set_backlight(0)
    def clear(self):
        # LCD-Ausgabe loeschen
        self.lcd.clear()
    def write_lcd(self,text):
        # LCD einschalten
        self.turn_on()
        time.sleep(0.05)
        # Nachricht ausgeben
        self.lcd.message(text)
        time.sleep(0.05)


def distance():
    global TRIG
    global ECHO


    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)



    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_end = 0
    pulse_start = 0

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


try:
    lcd_screen = LCDModule()
    while True:
        a = distance()
        GPIO.output(TRIG, False)

        lcd_screen.write_lcd(text="Distanz:\n%scm           " % a)
        time.sleep(0.05)
except KeyboardInterrupt:
        GPIO.cleanup()
        lcd_screen.clear()
        lcd_screen.turn_off()
