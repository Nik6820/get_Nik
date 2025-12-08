import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt, medfilt

# Читаем данные из файла
df = pd.read_csv('mil_n.csv')

# Извлекаем данные
time = df['Время[c]'].values
voltage = df['Напряжение[В]'].values

# Рассчитываем частоту дискретизации
fs = 1 / np.mean(np.diff(time))

# Функция для фильтра Баттерворта
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# КОМБИНИРОВАННЫЙ ФИЛЬТР
# 1. Медианный фильтр для удаления выбросов
voltage_median = medfilt(voltage, kernel_size=7)

# 2. Фильтр Баттерворта для удаления высокочастотного шума
voltage_clean = butter_lowpass_filter(voltage_median, cutoff=15, fs=fs, order=4)

# Детектирование пиков на очищенном сигнале
peaks, properties = find_peaks(voltage_clean, height=1.15, distance=200, prominence=0.003)
peak_times = time[peaks]
peak_voltages = voltage_clean[peaks]

# Вычисляем интервалы R-R
rr_intervals = np.diff(peak_times)

# Настройка стиля
plt.style.use('default')
plt.rcParams['figure.figsize'] = [14, 6]
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# Создание графика
fig, ax = plt.subplots(figsize=(14, 6))

# Очищенный сигнал
ax.plot(time, voltage_clean, color='#2E86AB', linewidth=1.5, 
        label=f'Очищенный сигнал пульса', zorder=1)

# Отметки пиков
ax.scatter(peak_times, peak_voltages, color='#E63946', s=40, zorder=3,
          edgecolors='white', linewidth=1.5,
          label=f'R-зубцы ({len(peaks)} шт.)')


# Настройки графика
ax.set_title('Сигнал пульса Миланы (до физ.нагрузки)', 
             fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Время (с)', fontsize=16)
ax.set_ylabel('Напряжение (В)', fontsize=16)
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Легенда с дополнительной информацией
if len(rr_intervals) > 0:
    avg_rr = np.mean(rr_intervals)
    bpm = 60 / avg_rr
    legend_text = (f'Очищенный сигнал пульса\n'
                   f'R-зубцы: {len(peaks)} шт.\n'
                   f'Средний R-R: {avg_rr:.3f} с\n'
                   f'ЧСС: {bpm:.1f} уд/мин')
else:
    legend_text = f'Очищенный сигнал пульса\nR-зубцы: {len(peaks)} шт.'

ax.legend([ax.lines[0], ax.collections[0]], 
          ['Очищенный сигнал пульса', 
           f'R-зубцы ({len(peaks)} шт.)\nПульс: {60/np.mean(rr_intervals):.1f} уд/мин' if len(rr_intervals) > 0 else f'R-зубцы ({len(peaks)} шт.)'],
          loc='upper right', fontsize=12, framealpha=0.9)

# Улучшаем внешний вид осей
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(0.5)

plt.tight_layout()
plt.show()

# Вывод статистики в консоль
print("="*60)
print("📊 РЕЗУЛЬТАТЫ АНАЛИЗА ПУЛЬСА")
print("="*60)
print(f"Общее время записи: {time[-1]:.2f} с")
print(f"Обнаружено R-зубцов: {len(peaks)}")
print(f"Интервалов R-R: {len(rr_intervals)}")
print()

if len(rr_intervals) > 0:
    print("📈 ИНТЕРВАЛЫ R-R (секунды):")
    for i, interval in enumerate(rr_intervals, 1):
        print(f"  {i:3d}. {interval:.4f} с")
    print()
    
    print("📊 СТАТИСТИКА:")
    print(f"  Средний интервал R-R:     {np.mean(rr_intervals):.4f} с")
    print(f"  Стандартное отклонение:   {np.std(rr_intervals):.4f} с")
    print(f"  Минимальный интервал:     {np.min(rr_intervals):.4f} с")
    print(f"  Максимальный интервал:    {np.max(rr_intervals):.4f} с")
    print(f"  Размах:                   {np.ptp(rr_intervals):.4f} с")
    print()
    
    print("❤️ ЧАСТОТА СЕРДЕЧНЫХ СОКРАЩЕНИЙ:")
    print(f"  ЧСС: {60/np.mean(rr_intervals):.1f} уд/мин")
    print(f"  Вариабельность (CV): {(np.std(rr_intervals)/np.mean(rr_intervals)*100):.2f}%")
    
    # Оценка регулярности ритма
    cv = np.std(rr_intervals)/np.mean(rr_intervals)*100
    if cv < 5:
        rhythm = "регулярный"
    elif cv < 10:
        rhythm = "умеренно нерегулярный"
    else:
        rhythm = "нерегулярный"
    print(f"  Ритм: {rhythm}")
    
print("="*60)
