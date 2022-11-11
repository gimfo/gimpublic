#!/usr/bin/env python
# Author: Tony DiCola
# Copyright (c) 2015 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import signal
import time
from pirc522 import RFID
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import spidev
import sys

# Definiere Spalten und Reihen des LCD Displays
lcd_columns = 16
lcd_rows    = 2

# Initialisiere LCD-Display
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# SPI-Bus oeffnen
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

class ButtonMatrix():

    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        # Kanaele definieren
        self.key_channel = 4
        self.delay = 0.1

        self.adc_key_val = [30,90,160,230,280,330,400,470,530,590,650,720,780,840,890,960]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

        '''
        self.indexes = {
            12:1,
            13:2,
            14:3,
            15:4,
            10:5,
            9:6,
            8:7,
            11:8,
            4:9,
            5:10,
            6:11,
            7:12,
            0:13,
            1:14,
            2:15,
            3:16
        }
        '''
        self.indexes = {
                12:7,
                13:8,
                14:9,
                15:6,
                10:6,
                9:5,
                8:4,
                11:8,
                4:1,
                5:2,
                6:3,
                7:12,
                0:13,
                1:14,
                2:15,
                3:16
        }


    def ReadChannel(self,channel):
        # Funktion zum Auslesen der SPI-Daten aus dem MCP3008-Chip
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def GetAdcValue(self):
        adc_key_value = self.ReadChannel(self.key_channel)
        return adc_key_value

    def GetKeyNum(self,adc_key_value):
        for num in range(0,16):
            if adc_key_value < self.adc_key_val[num]:
                return num
        if adc_key_value >= self.num_keys:
            num = -1
            return num

    def activateButton(self, btnIndex):
        # Index ueber SPI abrufen
        btnIndex = int(btnIndex)
        btnIndex = self.indexes[btnIndex]
        print("button %s pressed" % btnIndex)
        # verhindere, dass Tastendruecke zu nah beieinander liegen
        time.sleep(.3)
        return btnIndex

# Initialisiere Buttonmatrix
buttons = ButtonMatrix()
# Aktiviere LCD-Hintergrundbeleuchtung
lcd.set_backlight(0)

# LCD-Ausgabe loeschen
lcd.clear()

try:
    input = raw_input
except NameError:
    pass

CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

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
    ('9',9)
]

run = True
rdr = RFID()
util = rdr.util()
util.debug = False

def end_read(signal,frame):
    global run
    run = False
    rdr.cleanup()

signal.signal(signal.SIGINT, end_read)

print("Starte...")

# Schritt 1 - Auf Karte warten
print('== Schritt 1 =========================')
print('Halte die Karte auf das Lesegeraet...')

while run:
    rdr.wait_for_tag()
    (error, data) = rdr.request()
    if not error:
        print("[-] Karte erkannt: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("[-] Karten-UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print('==============================================================')
        print('ACHTUNG: KARTE NICHT ENTFERNEN!')
        print('==============================================================')
        print('')

        print('== Schritt 2 =========================')
        print('Waehle eine Zahl, die auf die Karte geschrieben werden soll.')

        lcd.clear()
        lcd.message("Waehle eine Zahl...")

        number_choice = None
        while number_choice is None:
            # rufe Tastendruck ueber SPI ab
            adc_key_value = buttons.GetAdcValue()
            key = buttons.GetKeyNum(adc_key_value)
            if key != buttons.oldkey:
                time.sleep(0.05)
                adc_key_value = buttons.GetAdcValue()
                key = buttons.GetKeyNum(adc_key_value)
                if key != buttons.oldkey:
                    oldkey = key
                    if key >= 0:
                        # Knopf wurde gedrueckt - aktiviere entsprechende Funktion
                        number_choice = buttons.activateButton(key)
                        # loesche LCD-Ausgabe
                        lcd.clear()
                        if(number_choice <= 10 and number_choice >= 0):
                            # sZeige Wert auf LCD
                            lcd.message("Zahl: %s" % number_choice)
                        else:
                            lcd.message("Falsche Zahl...")
        try:
            number_choice = int(number_choice)
        except ValueError:
            # Eingabe war keine Zahl
            print('Achtung! Fehlerhafte Eingabe!')
            continue
        # Pruefe ob die Eingabe im richtigen Bereich liegt
        if not (0 <= number_choice < len(NUMBERS)):
            print('Achtung! Block-Zahl muss zwischen 0 und {0} liegen!'.format(len(NUMBERS)-1))
            continue

        # Block ausgewaehlt - pruefe Name und ID
        number_name, number_id = NUMBERS[number_choice]
        print('Deine Auswahl: {0}'.format(number_name))
        print('')

        time.sleep(1.5)

        # Bestaetigung
        print('== Schritt 3 =========================')
        print('Bestaetige die Beschreibung der Karte:')
        print('Zahl: {0}'.format(number_name))
        print('Warte auf Bestaetigung... (Y oder N)')
        # Bestaetigungstext auf LCD anzeigen
        lcd.clear()
        lcd.message("Zahl %s \nbestaetigen..." % number_name)
        choice = None
        while choice is None:
            # rufe Tastendruck ueber SPI ab
            adc_key_value = buttons.GetAdcValue()
            key = buttons.GetKeyNum(adc_key_value)
            if key != buttons.oldkey:
                time.sleep(0.05)
                adc_key_value = buttons.GetAdcValue()
                key = buttons.GetKeyNum(adc_key_value)
                if key != buttons.oldkey:
                    oldkey = key
                    if key >= 0:
                        # Button wurde gedrueckt
                        choice = buttons.activateButton(key)
                        lcd.clear()
                        if(choice != 16):
                            lcd.message('Fehlgeschlagen!')
                            time.sleep(1.5)
                            lcd.clear()
                            # Hintergrundbeleuchtung ausschalten
                            lcd.set_backlight(1)
                            # Programm verlassen
                            sys.exit(0)
                        else:
                            print("Beschreibe Karte... (KARTE NICHT ENTFERNEN!)")
                            util.set_tag(uid)
                            util.auth(rdr.auth_b, CARD_KEY)
                            util.rewrite(4, [None, None, 0x69, 0x24, 0x40])

                            data = bytearray(16)
                            data[0:4] = b'NUM'
                            data[4]   = number_id & 0xFF
                            util.rewrite(4, data)
                            print('Karte erfolgreich beschrieben! Karte kann nun entfernt werden.')
                            lcd.clear()
                            lcd.message('Erfolgreich!')
                            time.sleep(1.5)
                            lcd.clear()
                            lcd.set_backlight(1)
                            run = False
