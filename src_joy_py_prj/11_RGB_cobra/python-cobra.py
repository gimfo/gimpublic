# Python Cobra Game
# Modified by Joy-IT for Joy-Pi Note Software - SIMAC Electronics GmbH - www.joy-it.net
# Original Autor: Tayfun ULU - https://github.com/tayfunulu/SnakeGame
# For LCS NeoPixel library used.
# https://github.com/jgarff/rpi_ws281x
# Autor of Library : Jeremy Garff
import time, curses, thread, random
import spidev
from rpi_ws281x import PixelStrip, Color

spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 1000000

# Auslesen der Daten ueber SPI
def ReadChannel(channel):
    adc = spi.xfer2([1, (8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# Kanaele definieren
x_channel = 1
y_channel = 0
delay = 0.15

# auf Joystick reagieren
def klavyeden ( threadName,bir):
    global ek_x
    global ek_y
    global timing
    try:
        screen = curses.initscr()
        curses.cbreak()
        curses.echo()
        screen.keypad(True)
        while True:
            x_value = ReadChannel(x_channel)
            y_value = ReadChannel(y_channel)

            if x_value > 650:
                # Links
                if not ek_x==1:
                    ek_y=0
                    ek_x=-1
                    timing=False
            if x_value < 400:
                # Rechts
                if not ek_x==-1:
                    ek_y=0
                    ek_x=1
                    timing=False
            if y_value > 650:
                # Hoch
                if not ek_y==1:
                    ek_y=-1
                    ek_x=0
                    timing=False
            if y_value < 400:
                # Runter
                if not ek_y==-1:
                    ek_y=1
                    ek_x=0
                    timing=False
    
    finally:
        curses.echo()
        curses.cbreak()
        curses.endwin()

def writer_point (strip,list,color):
    for i in list:
        strip.setPixelColor(i,color)

# ausgabe auf der matrix loeschen
def clear_lcd (strip,color=Color(0,0,0)):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,color)

# gameover overlay und punktezahl ausgeben
def game_over(strip,point):
    # matrix loeschen
    clear_lcd(strip)
    strip.show()
    time.sleep(1)

    # roter screen
    clear_lcd(strip,Color(0,100,0))
    strip.show()
    time.sleep(1)

    clear_lcd(strip,Color(76,35,9))
    face=[0,1,2,5,6,7,8,9,14,15,16,23,24,31,32,39,40,42,45,47,48,49,54,55,56,57,58,59,60,61,62,63]
    mot=[18,26,27,28,29,21]

    clear_lcd(strip,Color(0,0,0))

    # characters
    second_one = [12,20,28,36,44]
    second_two =[12,13,14,22,28,29,30,36,44,45,46]
    second_three =[12,13,14,20,28,29,30,36,44,45,46]
    second_four =[13,20,21,22,30,38,46]
    second_five=[12,13,14,20,28,29,30,38,44,45,46]
    second_six=[12,13,14,20,22,28,29,30,38,46]
    second_seven=[12,20,28,36,44,45,46]
    second_eight=[12,13,14,20,22,28,29,30,36,38,44,45,46]
    second_nine=[12,20,28,29,30,36,38,44,45,46]
    second_zero=[12,13,14,20,22,28,30,36,38,44,45,46]

    first_one=[9,17,25,33,41]
    first_two=[8,9,10,18,24,25,26,32,40,41,42]
    first_three=[8,9,10,16,24,25,26,32,40,41,42]
    first_four=[9,16,17,18,26,34,42]
    first_five=[8,9,10,16,24,25,26,34,40,41,42]
    first_six=[8,9,10,16,18,24,25,26,34,42]
    first_seven=[8,16,24,32,40,41,42]
    first_eight=[8,9,10,16,18,24,25,26,32,34,40,41,42]
    first_nine=[8,16,24,25,26,32,34,40,41,42]
    first_zero=[8,9,10,16,18,24,26,32,34,40,41,42]

    # Punktestand anzeigen
    '''
    if point > 9 :
        first_digit=int(str(point)[1])
        second_digit=int(str(point)[0])
    else :
        first_digit = point
        second_digit = 0

    if second_digit ==1:
        writer_point(strip,second_one,Color(0,50,0))
    elif second_digit == 2 :
        writer_point(strip,second_two,Color(0,50,0))
    elif second_digit == 3:
        writer_point(strip,second_three,Color(0,50,0))
    elif second_digit == 4:
        writer_point(strip,second_four,Color(0,50,0))
    elif second_digit == 5:
        writer_point(strip,second_five,Color(0,50,0))
    elif second_digit == 6:
        writer_point(strip,second_six,Color(0,50,0))
    elif second_digit == 7:
        writer_point(strip,second_seven,Color(0,50,0))
    elif second_digit == 8:
        writer_point(strip,second_eight,Color(0,50,0))
    elif second_digit == 9:
        writer_point(strip,second_nine,Color(0,50,0))

    if first_digit == 1:
        writer_point(strip,first_one,Color(0,50,0))
    elif first_digit == 2:
        writer_point(strip,first_two,Color(0,50,0))
    elif first_digit == 3:
        writer_point(strip,first_three,Color(0,50,0))
    elif first_digit == 4:
        writer_point(strip,first_four,Color(0,50,0))
    elif first_digit == 5:
        writer_point(strip,first_five,Color(0,50,0))
    elif first_digit == 6:
        writer_point(strip,first_six,Color(0,50,0))
    elif first_digit == 7:
        writer_point(strip,first_seven,Color(0,50,0))
    elif first_digit == 8:
        writer_point(strip,first_eight,Color(0,50,0))
    elif first_digit == 9:
        writer_point(strip,first_nine,Color(0,50,0))
    else :
        writer_point(strip,first_zero,Color(0,50,0))'''

    strip.show()

# LED-Matrix Konfiguration:
LED_COUNT      = 64      # Anzahl der Pixel
LED_PIN        = 18      # GPIO Pin
LED_FREQ_HZ    = 800000  # Signalfrequenz
LED_DMA        = 5       # DMA-Kanal
LED_BRIGHTNESS = 155     # Helligkeit
LED_INVERT     = False   # Invertierungseinstellung

if __name__ == '__main__':
    # Matrix-Objekt erstellen
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    print ('Press Ctrl-C to quit.')

    global ek_x
    global ek_y
    global timing

    ek_x = 0
    ek_y = 1

    ex_x_2=ex_x=x=3
    ex_y_2=ex_y=y=3

    x_rand=random.randint(-1,1)
    y_rand=random.randint(-1,1)

    # Zufaelligen Punkt erstellen
    yem_x = random.randint(0,7)
    yem_y = random.randint(0,7)

    # Steuerung
    if ( x==yem_x and y==yem_y):
        yem_x = random.randint(0,7)
        yem_y = random.randint(0,7)

    liste_x = []
    liste_y = []

    # Thread zur Steuerung erstellen
    thread.start_new_thread( klavyeden, ("Thread-1",'' ))

    try :
        while True:
            liste_x.append(x)
            liste_y.append(y)

            sil_x=liste_x.pop(0)
            sil_y=liste_y.pop(0)

            if ( x==yem_x and y==yem_y):
                liste_x.append(x)
                liste_y.append(y)

                yem_x = random.randint(0,7)
                yem_y = random.randint(0,7)

                yeni = True
                while yeni:
                    yeni = False
                    for i in range(0,len(liste_x)):
                        if ( yem_x==liste_x[i] and yem_y==liste_y[i]):
                            yem_x = random.randint(0,7)
                            yem_y = random.randint(0,7)
                            yeni = True
                            pass
            x = x + ek_x
            y = y + ek_y

            if x==-1 :
                x = 7
            if x==8 :
                x = 0
            if y==-1 :
                y = 7
            if y==8 :
                y = 0

            strip.setPixelColor(yem_y*8+yem_x, Color(0,100,0))
            strip.setPixelColor(y*8+x, Color(80,0,0))
            strip.setPixelColor(sil_y*8+sil_x, Color(0,0,0))

            for i in range(0,len(liste_x)):
                strip.setPixelColor(liste_y[i]*8+liste_x[i], Color(30,0,0))
            strip.show()
            time.sleep(400/1000.0)
            timing = True

            for i in range(0,len(liste_x)):
                if ( x==liste_x[i] and y==liste_y[i]):
                    game_over(strip,(len(liste_x)+1))
                    quit ()

    except (KeyboardInterrupt, SystemExit):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
