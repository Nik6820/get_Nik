import matplotlib.pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10,6))
    plt.plot(time, voltage)
    plt.xlabel("Время")
    plt.ylabel("Напряжение")
    plt.grid(True, which="major", linestyle="-")
    plt.grid(True, which="minor", linestyle="--", linewidth=0.5)
    plt.ylim(0, max_voltage)
    plt.minorticks_on()
    plt.show()
def plot_sampling_period_hist(time):
    sampling_periods=[]
    for i in range(len(time)-1):
        sampling_periods.append(time[i+1]-time[i])
    plt.figure(figsize=(10,6))
    plt.hist(sampling_periods)
    plt.title("Распределение количества измерений по их продолжительности")
    plt.xlabel("Время")
    plt.ylabel("Количество измерений")
    plt.xlim(0, 0.06)
    plt.grid(True, which="major", linestyle="-")
    plt.grid(True, which="minor", linestyle="--", linewidth=0.5)
    plt.minorticks_on()
    plt.show()