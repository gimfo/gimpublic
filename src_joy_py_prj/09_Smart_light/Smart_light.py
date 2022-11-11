import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import smbus
import time
from rpi_ws281x import PixelStrip, Color

 # Revision fuer den Bus-Treiber pruefen
if(GPIO.RPI_REVISION == 1):
    bus = smbus.SMBus(0)
else:
    bus = smbus.SMBus(1)

# LED-Strip konfiguration
LED_COUNT = 64        # Anzahl der Pixel
LED_PIN = 12          # GPIO-Pin, andem das Modul angeschlossen ist
LED_FREQ_HZ = 800000  # LED-Signal-Frequenz
LED_DMA = 10          # DMA-Kanal, der zur Generierung des Signals verwendet wird
LED_BRIGHTNESS = 10   # Helligkeitseinstellung
LED_INVERT = False    # Signal-Invertierung
LED_CHANNEL = 0       # Setze auf 1, falls die GPIOs 13, 19, 41, 45 oder 53 verwendet werden

buzzer_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)


class LCDModule():

    def __init__(self):
        # Spalten und Reihen des LCD-Display definieren
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

class LightSensor():

    def __init__(self):

        # Datenblatt-Konstanten definieren
        self.DEVICE = 0x5c # I2C-Adresse
        self.POWER_DOWN = 0x00 # Inaktiver Zustand
        self.POWER_ON = 0x01 # Einschalten
        self.RESET = 0x07 # Datenregisterwert zuruecksetzen

        # Starte Messung mit 4lx Aufloesung - typischerweise 16ms
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        # Starte Messung mit 1lx Aufloesung - typischerweise 120ms
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Starte Messung mit 0.5lx Aufloesung - typischerweise 120ms
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Starte Messung mit 1lx Aufloesung - typischerweise 120ms
        # Sensor wird nach der Messung automatisch ausgeschaltet
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Starte Messung mit 0.5lx Aufloesung - typischerweise 120ms
        # Sensor wird nach der Messung automatisch ausgeschaltet
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Starte Messung mit 1lx Aufloesung - typischerweise 120ms
        # Sensor wird nach der Messung automatisch ausgeschaltet
        self.ONE_TIME_LOW_RES_MODE = 0x23

    def convertToNumber(self, data):
        # Umwandlung von 2-Byte-Datensaetzen in Dezimalzahl
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self):
        data = bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)


def buzz():
    # Ton ueber Buzzer ausgeben
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer_pin, GPIO.LOW)

def RGB_on():
    for i in range(64):
            strip.setPixelColor(i,Color(255,255,255))
    strip.show()

def RGB_off():
    for i in range(64):
            strip.setPixelColor(i,Color(0,0,0))
    strip.show()



strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Bibliothek initialisieren
strip.begin()

# Licht-Sensor definieren
sensor = LightSensor()
# LCD-Modul definieren
lcd_screen = LCDModule()
# Niedrigen Helligkeitswert definieren
low_light = 40

try:
    while True:
        sensor_data = sensor.readLight()
        a = int(sensor_data)
        lcd_screen.write_lcd(text="Licht-Level:\n%s lux             " % a)
        print("Licht-Level : " + str(int(sensor.readLight())) + " lux                       ")
        if(sensor_data < 40):
            # Lichtwert zu niedrig - aktiviere Buzzer
            RGB_on()
        else:
            RGB_off()
        time.sleep(0.5)
except KeyboardInterrupt:
    lcd_screen.clear()
    lcd_screen.turn_off()
    GPIO.cleanup()
