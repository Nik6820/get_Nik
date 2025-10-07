import time
import mcp4725_driver as mcp
import signal_generator as sig

amplitude = 4
sig_freq = 5
sampl_freq = 1000

try:
    dc = mcp.MCP4725(5.17, 0x61, True)

    while True:
        try:

            fx=sig.get_triangle_wave_amplitude(sig_freq, time.time())
            dc.set_voltage(fx*amplitude)
            sig.wait_for_sampling_period(sampl_freq)
        except ValueError:
                print("Не число!\n") 

finally:
    dc.deinit()