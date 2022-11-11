import RPi.GPIO as GPIO
import time
from rpi_ws281x import PixelStrip, Color

# LED-Strip konfiguration
LED_COUNT = 64        # Anzahl der Pixel
LED_PIN = 12          # GPIO-Pin, andem das Modul angeschlossen ist
LED_FREQ_HZ = 800000  # LED-Signal-Frequenz
LED_DMA = 10          # DMA-Kanal, der zur Generierung des Signals verwendet wird
LED_BRIGHTNESS = 10   # Helligkeitseinstellung
LED_INVERT = False    # Signal-Invertierung
LED_CHANNEL = 0       # Setze auf 1, falls die GPIOs 13, 19, 41, 45 oder 53 verwendet werden

tilt_pin = 22
# setze GPIO Modus
GPIO.setmode(GPIO.BCM)
GPIO.setup(tilt_pin, GPIO.IN)

def colorWipe(strip, color, wait_ms=50):
    """Farben pixelweise ueber die LEDs schieben"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

sprite_number_left = [24,17,10,3,33,42,51,25,26,27,28,29,30]
sprite_number_right = [31,22,13,4,38,45,52,30,29,28,27,26,25]
sprite_number_del_left = [3,10,17,24,33,42,51]
sprite_number_del_right = [4,13,22,31,38,45,52]

colorWipe(strip,Color(0,0,0),10)
try:
    while True:
        if(GPIO.input(tilt_pin) == True):
            for i in sprite_number_del_right:
                strip.setPixelColor(i,Color(0,0,0))
            for i in sprite_number_left:
                strip.setPixelColor(i,Color(255,0,0))
            strip.show()
        else:
            for i in sprite_number_del_left:
                strip.setPixelColor(i,Color(0,0,0))
            for i in sprite_number_right:
                strip.setPixelColor(i,Color(0,255,0))
            strip.show()
except KeyboardInterrupt:
    colorWipe(strip,Color(0,0,0),10)
    GPIO.cleanup()
