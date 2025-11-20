import numpy as np
import matplotlib.pyplot as plt
import imageio
from cycler import cycler
from scipy.signal import find_peaks


def readIntensity(photoName, plotName, lamp, surface):
    photo = imageio.imread(photoName)
    x1=260
    y1=480
    x2=465  
    y2=610
    background = photo[x1:y1, x2:y2, 0:3].swapaxes(0, 1)

    cut = photo[x1:y1, x2:y2, 0:3].swapaxes(0, 1)
    rgb = np.mean(cut, axis=(0))
    luma = 0.2989 * rgb[:, 0] + 0.5866 * rgb[:, 1] + 0.1144 * rgb[:, 2]

    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

    fig = plt.figure(figsize=(10, 5), dpi=200)

    plt.title('Интенсивность отражённого излучения\n' + '{} / {}'.format(lamp, surface))
    plt.xlabel('Относительный номер пикселя')
    plt.ylabel('Яркость')
    red=np.array(rgb[:,0])
    green=np.array(rgb[:,1])
    blue=np.array(rgb[:,2])
    luma=np.array(luma)
    plt.plot(red, label=['r'])
    plt.plot(green, label=['g'])
    plt.plot(blue, label=['b'])
    plt.plot(luma, 'w', label='I')
    plt.legend()
    peaks, _ = find_peaks(luma, height=20, width=5)
    plt.imshow(background, origin='lower')
    plt.grid(which='major', linestyle = "-", linewidth=0.3)
    plt.grid(which='minor', linestyle = "--", linewidth=0.1)
    plt.minorticks_on()

    plt.savefig(plotName)
    print(f"Фото: {photoName} Найдено пиков: {len(peaks)}")
    for i, peak in enumerate(peaks):
        print(f"Пик {i+1}: позиция {peak}, интенсивность {luma[peak]:.2f}")
    return luma
