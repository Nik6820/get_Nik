import time
import signal_generator as sig
import r2r_class as r2r

amplitude = 3
sig_freq = 20
sampl_freq = 1000


try:
    dc = r2r.R2R_DAC([16,20,21,25,26,17,27,22], 3.2*255/256, True)

    while True:
        try:

            fx=sig.get_sin_wave_amplitude(sig_freq, time.time())
            dc.set_voltage(fx*amplitude)
            sig.wait_for_sampling_period(sampl_freq)
        except ValueError:
                print("Не число!\n") 

finally:
    dc.deinit()