#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
import spidev
import os

# Spalten und Reihen des LCD definieren
lcd_columns = 16
lcd_rows    = 2

# LCD initialisieren
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# SPI Bus oeffnen
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

class ButtonMatrix():

    def __init__(self):

        self.calculated = ""

        GPIO.setmode(GPIO.BCM)

        # Channel setzen
        self.key_channel = 4
        self.delay = 0.1

        self.adc_key_val = [30,90,160,230,280,330,400,470,530,590,650,720,780,840,890,960]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

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

    def ReadChannel(self,channel):
        # Funktion um die SPI-Daten aus dem MCP3008 Chip auszulesen
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
        btnIndex = int(btnIndex)
        btnIndex = self.indexes[btnIndex]
        # Rechnerfunktion aufrufen
        self.calculate(btnIndex)
        print("button %s pressed" % btnIndex)
        # verhindere nah beieinander liegende Tastendruecke
        time.sleep(.3)
        return self.calculated

    def calculate(self,btnIndex):
        btnIndex = int(btnIndex)
        # Zahlen
        if(btnIndex == 1):
            self.calculated = self.calculated + "7"
        elif(btnIndex == 2):
            self.calculated = self.calculated + "8"
        elif(btnIndex == 3):
            self.calculated = self.calculated + "9"
        elif(btnIndex == 5):
            self.calculated = self.calculated + "6"
        elif(btnIndex == 6):
            self.calculated = self.calculated + "5"
        elif(btnIndex == 7):
            self.calculated = self.calculated + "4"
        elif(btnIndex == 9):
            self.calculated = self.calculated + "1"
        elif(btnIndex == 10):
            self.calculated = self.calculated + "2"
        elif(btnIndex == 11):
            self.calculated = self.calculated + "3"
        elif(btnIndex == 13):
            self.calculated = self.calculated + "0"
        # Reset
        elif(btnIndex == 14):
            self.calculated = ""
        # Funktionen
        elif(btnIndex == 4):
            self.calculated = self.calculated + "*"
        elif(btnIndex == 8):
            self.calculated = self.calculated + "/"
        elif(btnIndex == 12):
            self.calculated = self.calculated + "+"
        elif(btnIndex == 16):
            self.calculated = self.calculated + "-"
        elif(btnIndex == 15):
            # Berchnung
            self.calculated = str(eval(self.calculated))
        return self.calculated

class LCDModule():

    def __init__(self):
        # LCD initialisieren
        self.address = 0x21
        self.lcd_columns = 16
        self.lcd_rows = 2
        self.lcd = LCD.Adafruit_CharLCDBackpack(address=self.address)

    def turn_off(self):
        # Hintergrundbeleuchtung ausschalten
        self.lcd.set_backlight(1)

    def turn_on(self):
        # Hintergrundbeleuchtung einschalten
        self.lcd.set_backlight(0)

    def clear(self):
        # Ausgabe auf dem LCD-Bildschirm loeschen
        self.lcd.clear()

    def write_lcd(self,text):
        # LCD einschalten
        self.turn_on()
        time.sleep(0.1)
        # nachricht ausgeben
        self.lcd.message(text)
        time.sleep(3)
        # Anzeige loeschen
        self.clear()
        time.sleep(0.1)
        # LCD ausschalten
        self.turn_off()

# LCD-Modul definieren
lcd_screen = LCDModule()





# Buttonmatrix initialisieren
buttons = ButtonMatrix()
# LCD-Beleuchtung ausschalten
lcd.set_backlight(0)

try:
    while True:
            # Knopfdruck ueber SPI abrufen
            adc_key_value = buttons.GetAdcValue()
            key = buttons.GetKeyNum(adc_key_value)
            if key != buttons.oldkey:
                time.sleep(0.05)
                adc_key_value = buttons.GetAdcValue()
                key = buttons.GetKeyNum(adc_key_value)
                if key != buttons.oldkey:
                    oldkey = key
                    if key >= 0:
                        # Button wurde gedrueckt - aktiviere entsprechende Funktion
                        calculated = buttons.activateButton(key)
                        print(calculated)
                        # LCD loeschen, bevor neue Werte angzeigt werden
                        lcd.clear()
                        # Ergebnis auf dem LCD ausgeben
                        lcd.message(calculated)
            time.sleep(buttons.delay)

except KeyboardInterrupt:
    lcd_screen.clear()
    lcd_screen.turn_off()
    GPIO.cleanup()
