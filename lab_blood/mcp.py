import RPi.GPIO as IO
import time
import mcp3021_driver as mcp
import adc_plot as plt
import numpy as np

adc = mcp.MCP3021(5.16)
time_values = []
voltage_values = []
duration = 12
try:
    start_time=time.time()
    now_time=time.time()
    while now_time-start_time<duration:
        now_time=time.time()
        voltage_values.append(adc.get_voltage())
        time_values.append(now_time-start_time)
    plt.plot_voltage_vs_time(time_values, voltage_values, 5.18)
    data = np.column_stack((time_values, voltage_values))
    np.savetxt('kar_f.csv',
			data,
			delimiter=',',
			fmt='%.4f',
			header='Время[c],Напряжение[В]',
			comments='',
			encoding='utf-8')
finally:
        adc.deinit()


