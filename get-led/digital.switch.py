import RPi.GPIO as IO
import time

led = 26
button=13
state=0
period=0.2

IO.setmode(IO.BCM)
IO.setup(led, IO.OUT)
IO.setup(button, IO.IN)

while True:
    if IO.input(button):
        state = not state
        IO.output(led, state)
        time.sleep(period) 