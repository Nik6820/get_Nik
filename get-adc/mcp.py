import RPi.GPIO as IO
import time
import mcp3021_driver as mcp
import adc_plot as plt

adc = mcp.MCP3021(5.18)
time_values = []
voltage_values = []
duration = 3.0
try:
    start_time=time.time()
    now_time=time.time()
    while now_time-start_time<duration:
        now_time=time.time()
        voltage_values.append(adc.get_voltage())
        time_values.append(now_time-start_time)
    plt.plot_voltage_vs_time(time_values, voltage_values, 5.18)
    plt.plot_sampling_period_hist(time_values)
finally:
        adc.deinit()