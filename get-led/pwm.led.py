import RPi.GPIO as IO
import time

led=26
period=0.02

IO.setmode(IO.BCM)
IO.setup(led, IO.OUT)

pwm=IO.PWM(led, 200)
duty=0
pwm.start(duty)

while True:
    pwm.ChangeDutyCycle(duty)
    time.sleep(period)
    duty+=1
    if duty>100:
        duty=0