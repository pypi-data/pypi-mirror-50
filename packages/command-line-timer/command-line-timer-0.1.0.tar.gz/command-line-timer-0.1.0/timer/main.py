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

class Bcolors:
    """console colors"""
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;212m'
    PALEYELLOW = '\033[38;5;228m'
    PALEBLUE = '\033[38;5;111m'

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
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write("\r"+timeformat)
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    """format current time of day"""
    now = datetime.datetime.now()
    hour = now.hour
    ampm = "AM"
    if (hour > 12) :
        hour = hour - 12
        ampm = "PM"
    if (now.minute < 10) :
        minute = "0"+str(now.minute)
    else:
        minute = str(now.minute)
    if (now.second < 10):
        second = "0"+str(now.second)
    else:
        second = str(now.second)
    rightnow = Bcolors.PALEYELLOW+str(hour)+":"+minute+":"+second+" "+ampm+Bcolors.ENDC
    sys.stdout.write(Bcolors.OKGREEN+"\rtimer ended"+Bcolors.ENDC+" at "+rightnow+"\n")
    """play music"""
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

if __name__ == "__main__":
    main()
