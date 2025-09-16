import RPi.GPIO as IO
import time

def d2b(n):
    return [int(element) for element in bin(n)[2:].zfill(8)]


leds=[24,22,23,27,17,25,12,16]
num=0
butup=9
butdn=10
period = 0.2

IO.setmode(IO.BCM)
IO.setup(leds, IO.OUT)
IO.setup(butup, IO.IN)
IO.setup(butdn, IO.IN)
IO.output(leds, 0)

while True:
    if IO.input(butup):
        num+=1
        if (num>255):
            num=255
        print(num, d2b(num))
        time.sleep(period)
    if IO.input(butdn):
        num-=1
        if (num<0):
            num=0
        print(num, d2b(num))
        time.sleep(period)
    state=d2b(num)[::-1]
    #print(state)
    for i in leds:
        IO.output(i, state[leds.index(i)])
    time.sleep(period)

