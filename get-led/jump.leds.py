import RPi.GPIO as IO
import time

leds=[16,12,25,17,27,23,22,24]
period=0.1

IO.setmode(IO.BCM)
IO.setup(leds, IO.OUT)
IO.output(leds, 0)
while True:
    for fl in leds:
        IO.output(fl, 1)
        time.sleep(period)
        IO.output(fl, 0)
    for rl in leds[6:0:-1]:
        IO.output(rl, 1)
        time.sleep(period)
        IO.output(rl, 0)