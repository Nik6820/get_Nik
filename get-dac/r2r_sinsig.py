import RPi.GPIO as IO
import time
import math

def d2b(n):
    return [int(element) for element in bin(n)[2:].zfill(8)]


DAC=[8,11,7,1,0,5,12,6]
period=0.00005

IO.setmode(IO.BCM)
IO.setup(DAC, IO.OUT)
IO.output(DAC, 0)
x=0
while True:
    x+=0.01
    y=(math.sin(x)+1)/2
    V=int(y*255)
    state=d2b(V)
    for i in DAC:
        IO.output(i, state[DAC.index(i)])
    time.sleep(period)