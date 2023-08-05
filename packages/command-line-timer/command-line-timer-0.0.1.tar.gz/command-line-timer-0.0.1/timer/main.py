#!/usr/bin/env python
import argparse
import time
import datetime
import sys
import pygame
import signal
import os
import pkg_resources

"""handle control C"""
def signal_handler(sig, frame):
    print('\ntimer cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    """countdown from the total seconds to zero then play a cucaracha horn"""
    version = pkg_resources.require("command-line-timer")[0].version
    """parse arguments from command line"""
    parser = argparse.ArgumentParser(description='count down from x', prog='timer')
    parser.add_argument("time", help="amount of time to count down from. Example hh:mm:ss or mm:ss or just ss")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()

    """convert hh:mm:ss to seconds"""
    multiply = 1
    input = args.time.split(":")
    seconds = 0
    for block in reversed(input) :
        seconds = seconds + int(block)*multiply
        multiply = multiply*60

    """load audio file"""
    audio_file = "cuca.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(0.3)
    os.system("date")
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write("\r"+timeformat)
        sys.stdout.flush()
        time.sleep(1)
        t -= 1
    """format current time of day"""
    now = datetime.datetime.now()
    hour = now.hour
    ampm = "am"
    if (hour > 12) :
        hour = hour - 12
        ampm = "pm"
    if (now.minute < 10) :
        minute = "0"+str(now.minute)
    else :
        minute = str(now.minute)
    rightnow = str(hour)+":"+minute+" "+ampm
    sys.stdout.write("\rtimer ended at "+rightnow+"\n")
    """play music"""
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

if __name__ == "__main__":
    main()
