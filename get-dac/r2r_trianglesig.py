import RPi.GPIO as IO
import time

def d2b(n):
    return [int(element) for element in bin(n)[2:].zfill(8)]


DAC=[8,11,7,1,0,5,12,6]
period=0.005

IO.setmode(IO.BCM)
IO.setup(DAC, IO.OUT)
IO.output(DAC, 0)

while True:
    for j in range(256):
        state=d2b(j)
        for i in DAC:
            IO.output(i, state[DAC.index(i)])
        time.sleep(period)
    for j in range(255, -1, -1):
        state=d2b(j)
        for i in DAC:
            IO.output(i, state[DAC.index(i)])
        time.sleep(period)