import RPi.GPIO as GPIO
import dht11
import time
import Adafruit_CharLCD as LCD

# GPIOs initialisieren
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

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
        self.clear()
        # Nachricht ausgeben
        self.lcd.message(text)

# LCD-Modul definieren
lcd_screen = LCDModule()

instance = dht11.DHT11(pin=4)

try:
    while True:
        result = instance.read()
        if result.is_valid():
            lcd_screen.write_lcd(text=('Temp. = {0:0.1f}*c\nFeucht. = {1:0.1f}%\n'.format(result.temperature,result.humidity)))
            print("Temperatur: %-3.1f C" % result.temperature)
            print("Feuchtigkeit: %-3.1f %%" % result.humidity)

except KeyboardInterrupt:
    lcd_screen.turn_off()
    GPIO.cleanup()
