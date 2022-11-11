import RPi.GPIO as GPIO
import time
import os
import Adafruit_CharLCD as LCD

# Definitionen
motion_pin = 23
lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
lcd.set_backlight(0)

# setze GPIO-Modus
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin, GPIO.IN)

class LCDModule():

    def __init__(self):
        # Definiere Spalten und Reihen
        self.address = 0x21
        self.lcd_columns = 16
        self.lcd_rows = 2
        # Initialisiere LCD
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
        self.turn_on()
        time.sleep(0.1)
        # Nachricht auf LCD ausgeben
        self.lcd.message(text)
        time.sleep(3)
        self.clear()
        time.sleep(0.1)
        self.turn_off()

# LCD-Modul definieren
lcd_screen = LCDModule()
lcd_screen.clear()
try:
    while True:
       if(GPIO.input(motion_pin) == 0):
             lcd.message("Pruefe...\n                ")
       elif(GPIO.input(motion_pin) == 1):
             lcd_screen.clear()
             lcd.message("Nehme auf...")
             ts = int(time.time())
             os.system("ffmpeg -t 7 -f v4l2 -framerate 60 -video_size 1280x720 -i /dev/video0 /home/pi/Videos/%s.avi"%ts)
             lcd_screen.clear()
             lcd.message("Aufgenommen")
             time.sleep(1)
             lcd_screen.turn_off()
             os.system("vlc /home/pi/Videos/%s.avi"%ts)
             break
       time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd_screen.turn_off()
