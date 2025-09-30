import RPi.GPIO as IO
import time
import math

def get_sin_wave_amplitude(freq, time):
    y = math.sin(2 * math.pi * freq * time)
    return (y+1)/2
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)