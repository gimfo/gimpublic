import time
import RPi.GPIO as GPIO
import datetime
import pygame
import threading
import random
from rpi_ws281x import PixelStrip, Color
from Adafruit_LED_Backpack import SevenSegment

# LED-Strip konfiguration
LED_COUNT = 64        # Anzahl der Pixel
LED_PIN = 12          # GPIO-Pin, andem das Modul angeschlossen ist
LED_FREQ_HZ = 800000  # LED-Signal-Frequenz
LED_DMA = 10          # DMA-Kanal, der zur Generierung des Signals verwendet wird
LED_BRIGHTNESS = 10   # Helligkeitseinstellung
LED_INVERT = False    # Signal-Invertierung
LED_CHANNEL = 0       # Setze auf 1, falls die GPIOs 13, 19, 41, 45 oder 53 verwendet werden

pygame.mixer.init()

segment = SevenSegment.SevenSegment(address=0x70)
heart = [1,6,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,50,51,52,53,59,60]

buzzer_pin = 18
shake_pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(shake_pin, GPIO.OUT)
GPIO.setwarnings(False)


print("STRG+C zum beenden druecken")

now = datetime.datetime.now()
hour = now.hour
minute = now.minute
second = now.second

segment.clear()
segment.set_digit(0, int(hour / 10))
segment.set_digit(1, hour % 10)
segment.set_digit(2, int(minute / 10))
segment.set_digit(3, minute % 10)
segment.set_colon(2)
segment.write_display()
time.sleep(1)

class RGB_Matrix:

    def __init__(self):

        # LED-Strip konfiguration
        self.LED_COUNT = 64        # Anzahl der Pixel
        self.LED_PIN = 12          # GPIO-Pin, andem das Modul angeschlossen ist
        self.LED_FREQ_HZ = 800000  # LED-Signal-Frequenz
        self.LED_DMA = 10          # DMA-Kanal, der zur Generierung des Signals verwendet wird
        self.LED_BRIGHTNESS = 10   # Helligkeitseinstellung
        self.LED_INVERT = False    # Signal-Invertierung
        self.LED_CHANNEL = 0       # Setze auf 1, falls die GPIOs 13, 19, 41, 45 oder 53 verwendet werden

        self.RIGHT_BORDER = [7,15,23,31,39,47,55,63]
        self.LEFT_BORDER = [0,8,16,24,32,40,48,56]

    # Funktonen zur LED-Animation definieren
    def clean(self,strip):
        # Alle LEDs ausschalten
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()


    def wheel(self,pos):
        """Erzeugen von Regenbogenfarben ueber die Positionen 0-255."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self,strip, wait_ms=20, iterations=1):
        """Regenbogen-Effekt auf allen LEDs"""
        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, self.wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChase(self,strip, color, wait_ms=50, iterations=10):
        """Lauflichtanimation"""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)


    def demo(self,strip):
        self.theaterChase(strip, Color(127, 127, 127))  # Weisses Lauflicht
        self.theaterChase(strip, Color(127, 0, 0))  # Rotes Lauflicht
        self.theaterChase(strip, Color(0, 0, 127))  # Blaues Lauflicht

        self.rainbow(strip)

        self.clean(strip)

    def run(self):
        # NeoPixel-Objekt erstellen
        strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Bibliothek initialisieren
        strip.begin()
        try:
            print('Teste Animationen...')
            for i in range(3):
                self.demo(strip)
            while True:
                for i in heart:
                    strip.setPixelColor(i,Color(255,0,0))
                strip.show()
        except KeyboardInterrupt:
             self.clean(strip)


def count_down(times):
    segment.clear()
    segment.set_digit(0, times)
    segment.set_digit(1, times)
    segment.set_digit(2, times)
    segment.set_digit(3, times)
    segment.write_display()
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(0.5)

def cleanup():

    GPIO.cleanup()

def delay(times):
   time.sleep(times/500.0)

def colorWipe(strip, color, wait_ms=50):
    """Farben pixelweise ueber die LEDs schieben"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
segment.begin()


try:
    while True:
        for i in range(4,-1,-1):
            count_down(i)
        break
    segment.clear()
    segment.write_display()
    colorWipe(strip,Color(0,0,0),0)
    GPIO.output(buzzer_pin,GPIO.HIGH)
    GPIO.output(shake_pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer_pin,GPIO.LOW)
    GPIO.output(shake_pin,GPIO.LOW)

    pygame.mixer.music.load('1.mp3')
    pygame.mixer.music.play()
    matrix = RGB_Matrix()
    matrix.run()

except KeyboardInterrupt:
    colorWipe(strip,Color(0,0,0),0)
    segment.clear()
    segment.write_display()
    pygame.mixer.music.stop()
    GPIO.output(buzzer_pin,GPIO.LOW)
