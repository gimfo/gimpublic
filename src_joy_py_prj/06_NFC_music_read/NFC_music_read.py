import socket
import time
import signal
from pirc522 import RFID
import Adafruit_CharLCD as LCD
import pygame
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
# MP3-Player initialisieren
pygame.mixer.init()
NUMBERS = [
    ('0',0),
    ('1',1),
    ('2',2),
    ('3',3),
    ('4',4),
    ('5',5),
    ('6',6),
    ('7',7),
    ('8',8),
    ('9',9),
    ('10',10)
]
run = True
rdr = RFID()
util = rdr.util()
util.debug = False

lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
lcd.set_backlight(0)

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
        # Ausgabe loeschen
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
lcd_screen.clear()

def end_read(signal,frame):
    try:
        global run
        run = False
    except KeyboardInterrupt:
        rdr.cleanup()
        pygame.mixer.music.stop()

signal.signal(signal.SIGINT, end_read)

lcd_screen.clear()
lcd.message("Pruefe...")

while run:
    rdr.wait_for_tag()
    (error, data) = rdr.request()

    if not error:
        print("[-] Karte erkannt: " + format(data, "02x"))
    (error, uid) = rdr.anticoll()
    if not error:
        # Karte gefunden - lese Block 4
        print("[-] Karten-UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        util.set_tag(uid)
        util.auth(rdr.auth_b, CARD_KEY)
        util.read_out(4)
        (error, data) = rdr.read(4)
    if data is None:
        print('Daten der Karte konnte nicht ausgelesen werden!')
        continue
            # Pruefe den Block-Header der Karte
    if data[0:4] != [78, 85, 77, 0]:
        print('Karte mit falschen Daten beschrieben!')
        continue
    number_id = data[4]
    for number in NUMBERS:
        if number[1] == number_id:
            number_name = number[0]
            break
            print('Zahl gefunden!')
    print('Zahlenwert: {0}'.format(number_name))
    try:
        lcd_screen.clear()
        lcd.message("%s.mp3"%number_name)
        time.sleep(1)
        lcd_screen.turn_off()
        pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
        pygame.mixer.music.play()
    except KeyboardInterrupt:
        time.sleep(1)
        lcd_screen.turn_off()
        continue
