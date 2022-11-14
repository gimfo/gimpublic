# Import des librairies
import time
import adafruit_character_lcd.character_lcd_i2c as LCD
import board
import RPi.GPIO as GPIO
from JoyPiNote import LightSensor
import ress_cap
from ress_cap import buzz
#Préparation du buzzer Pin 18
buzzer_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
# Création de l'objet light_sensor
light_sensor = LightSensor()
# Création de l'objet LCD
i2c = board.I2C()
lcd = LCD.Character_LCD_I2C(i2c, 16, 2, address=0x21)
# Paramétrage de l'alarme
low_light = 40


try:
    while True:
        sensor_data = light_sensor.readLight()

        lcd.message = "Light level:\n                  "

        lcd.message = "Light level:\n%s lx" % round(sensor_data, 2)

        if(sensor_data < low_light):
            buzz(buzzer_pin)

        time.sleep(0.5)

except KeyboardInterrupt:
    lcd.clear()
    lcd.backlight = False
    GPIO.cleanup()
