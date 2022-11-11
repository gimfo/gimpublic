import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD

lcd_columns = 16
lcd_rows    = 2
# LCD initialisieren
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
lcd.set_backlight(0)

# Sound-Pin definieren
sound_pin = 24
# GPIO-Modus setzen
GPIO.setmode(GPIO.BCM)
GPIO.setup(sound_pin, GPIO.IN)

class LCDModule():

    def __init__(self):
        # Spalten und Reihen fuer das LCD definieren
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
        # Ausgabe auf dem LCD loeschen
        self.lcd.clear()

    def write_lcd(self,text):
        # LCD einschalten
        self.turn_on()
        time.sleep(0.1)
        # Nachricht ausgeben
        self.lcd.message(text)
        time.sleep(3)
        # Ausgabe loeschen
        self.clear()
        time.sleep(0.1)
        # LCD ausschalten
        self.turn_off()

# LCD-Modul definieren
lcd_screen = LCDModule()

try:
    while True:
        # Pruefe ob ein Geraeusch erkannt wurde
        if(GPIO.input(sound_pin) == True):
            message = 'Hallo'
            lcd.message(message)
            for i in range(lcd_columns-len(message)):
                time.sleep(0.5)
                lcd.move_right()
            for i in range(lcd_columns-len(message)):
                time.sleep(0.5)
                lcd.move_left()
            # Hintergrundbeleuchtung ausschalten
            time.sleep(2)
            lcd.clear()

    else:
        # Schalte LCD aus, wenn kein Geraeusch erkannt wurde
        lcd_screen.clear()
        lcd_screen.turn_off()
except KeyboardInterrupt:
    lcd_screen.clear()
    lcd_screen.turn_off()
    GPIO.cleanup()
