import RPi.GPIO as IO
import time

def d2b(n):
    return [int(element) for element in bin(n)[2:].zfill(8)]


DAC=[8,11,7,1,0,5,12,6]
period=1

IO.setmode(IO.BCM)
IO.setup(DAC, IO.OUT)
IO.output(DAC, 0)

while True:
    num=float(input())
    V=int(255*num/3.3)
    state=d2b(V)
    for i in DAC:
        IO.output(i, state[DAC.index(i)])
    time.sleep(period)

