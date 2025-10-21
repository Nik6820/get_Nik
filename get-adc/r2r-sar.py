import RPi.GPIO as IO
import time
import r2r_adc as r2r
import adc_plot as plt

adc = r2r.R2R_ADC(3.29)
time_values = []
voltage_values = []
duration = 3.0
try:
    start_time=time.time()
    now_time=time.time()
    while now_time-start_time<duration:
        now_time=time.time()
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(now_time-start_time)
    plt.plot_voltage_vs_time(time_values, voltage_values, 3.29)
    plt.plot_sampling_period_hist(time_values)
finally:
        adc.deinit()