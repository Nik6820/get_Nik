import RPi.GPIO as IO
import time

led = 26
sunsensor=6
state=0
period=0.2

IO.setmode(IO.BCM)
IO.setup(led, IO.OUT)
IO.setup(sunsensor, IO.IN)

while True:
    state = not IO.input(sunsensor)
    IO.output(led, state)
    time.sleep(period) 