import os
import time

os.system("lxterminal --title=detection --geometry=70x30+0+0 -e 'bash -c \"sudo python python-cobra.py; exec bash\"'")

while True:
    time.sleep(1)
