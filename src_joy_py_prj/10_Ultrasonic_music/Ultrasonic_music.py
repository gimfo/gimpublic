import RPi.GPIO as GPIO
import time
from rpi_ws281x import PixelStrip, Color
import math
import random

# LED-Strip konfiguration
LED_COUNT = 64        # Anzahl der Pixel
LED_PIN = 12          # GPIO-Pin, andem das Modul angeschlossen ist
LED_FREQ_HZ = 800000  # LED-Signal-Frequenz
LED_DMA = 10          # DMA-Kanal, der zur Generierung des Signals verwendet wird
LED_BRIGHTNESS = 10   # Helligkeitseinstellung
LED_INVERT = False    # Signal-Invertierung
LED_CHANNEL = 0       # Setze auf 1, falls die GPIOs 13, 19, 41, 45 oder 53 verwendet werden

# setze GPIO-Modus
GPIO.setmode(GPIO.BCM)
tonePin = 18
GPIO.setup(tonePin,GPIO.OUT)
a = 0
TRIG = 16
ECHO = 26
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def tone(pin,pitch,duration):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(tonePin,GPIO.OUT)
	if pitch == 0:
	    delay(duration)
	    return
	p = GPIO.PWM(tonePin,pitch)
	p.start(30)
	delay(duration)
	p.stop()
	delay(2)

def delay(times):
   time.sleep(times/500.0)

def colorWipe(strip, color, wait_ms=50):
    """Farben pixelweise ueber die LEDs schieben"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def distance():
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

def if_dis(number1,number2,light,pitch,duration):
    global a
    if a > number1 and a <= number2:
        colorWipe(strip,Color(0,0,0),0)
        for i in light:
            strip.setPixelColor(i,Color(red,green,blue))
        strip.show()
        tone(tonePin, pitch,duration)



strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()



light_8 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_7 = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_6 = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_5 = [24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_4 = [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_3 = [40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_2 = [48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_1 = [56,57,58,59,60,61,62,63]


colorWipe(strip,Color(0,0,0),0)

try:
    while True:
        a = distance()
        red = random.randint(10,254)
        green = random.randint(10,254)
        blue = random.randint(10,254)
        if_dis(0,5,light_1,262,50)
        if_dis(5,10,light_2,294,50)
        if_dis(10,15,light_3,330,50)
        if_dis(15,20,light_4,349,50)
        if_dis(20,25,light_5,392,50)
        if_dis(25,30,light_6,440,50)
        if_dis(30,35,light_7,494,50)
        if_dis(35,40,light_8,0,50)
        if a > 40 or a < 0:
            colorWipe(strip,Color(0,0,0),0)
            tone(tonePin, 0, 50)
except KeyboardInterrupt:
    tone(tonePin, 0, 50)
    colorWipe(strip,Color(0,0,0),10)
    GPIO.cleanup()
