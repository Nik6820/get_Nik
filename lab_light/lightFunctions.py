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

    fig = plt.figure(figsize=(10, 5), dpi=1000)

    plt.title('Интенсивность отражённого излучения\n' + '{} / {}'.format(lamp, surface))
    plt.xlabel('Относительный номер пикселя')
    plt.ylabel('Яркость')
    red=np.array(rgb[:,0])
    green=np.array(rgb[:,1])
    blue=np.array(rgb[:,2])
    luma=np.array(luma)
    plt.plot(red, label='красный канал')
    plt.plot(green, label='зеленый канал')
    plt.plot(blue, label='синий канал')
    plt.plot(luma, 'w', label='белый канал')
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

def GrafIntens(luma, plotName):
    white = luma[0]
    yellow = luma[1]
    red = luma[2]
    green = luma[3]
    blue = luma[4]
    n=[0]*len(white)
    k=142/67
    b=546-119*k
    for i in range(len(white)):
        n[i]=i*k+b
    n=np.array(n)
    fig = plt.figure(dpi=1000)
    plt.title('Интенсивность цветных поверхностей от длины волны')
    plt.xlabel('Длина волны, нм')
    plt.ylabel('Интенсивность, о.е.')
    plt.plot(n[25:200], white[25:200], label="белый", color="black")
    plt.plot(n[25:200], yellow[25:200], label="желтый", color="y")
    plt.plot(n[25:200], red[25:200], label="красный", color="r")
    plt.plot(n[25:200], green[25:200], label="зеленый", color="g")
    plt.plot(n[25:200], blue[25:200], label="синий", color="b")
    plt.legend()
    plt.grid(which='major', linestyle = "-", linewidth=0.3)
    plt.grid(which='minor', linestyle = "--", linewidth=0.1)
    plt.minorticks_on()
    plt.savefig(plotName)

def GrafAlbedo(luma, plotName):
    white = luma[0]
    yellow = luma[1]
    red = luma[2]
    green = luma[3]
    blue = luma[4]
    n=[0]*len(white)
    k=142/67
    b=546-119*k
    for i in range(len(white)):
        n[i]=i*k+b
    n=np.array(n)
    albedo_white = white[25:200]/white[25:200]
    albedo_yellow= yellow[25:200]/white[25:200]
    albedo_red = red[25:200]/white[25:200]
    albedo_green = green[25:200]/white[25:200]
    albedo_blue = blue[25:200]/white[25:200]
    fig = plt.figure(dpi=1000)
    plt.title('Альбедо цветных поверхностей от длины волны')
    plt.xlabel('Длина волны, нм')
    plt.ylabel('Альбедо, о.е.')
    plt.plot(n[25:200], albedo_white, label="белый", color="black")
    plt.plot(n[25:200], albedo_yellow, label="желтый", color="y")
    plt.plot(n[25:200], albedo_red, label="красный", color="r")
    plt.plot(n[25:200], albedo_green, label="зеленый", color="g")
    plt.plot(n[25:200], albedo_blue, label="синий", color="b")
    plt.legend()
    plt.grid(which='major', linestyle = "-", linewidth=0.3)
    plt.grid(which='minor', linestyle = "--", linewidth=0.1)
    plt.minorticks_on()
    plt.savefig(plotName)