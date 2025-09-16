import RPi.GPIO as IO
import time

led = 26
state=0
period=1

IO.setmode(IO.BCM)
IO.setup(led, IO.OUT)

while True:
    IO.output(led, state)
    state = not state
    time.sleep(period) 