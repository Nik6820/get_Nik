import RPi.GPIO as IO
import time

DAC=[16,20,21,25,26,17,27,22]
period=1
value=3.3

def d2b(n):
    return [int(element) for element in bin(n)[2:].zfill(8)]

def voltage_to_number(V):
    if not(0.0 <= V <= value):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{value:.2f} В)")
        print("устанавливаем 0.0")
        return 0
    return int(255*V/3.3)


IO.setmode(IO.BCM)
IO.setup(DAC, IO.OUT)
IO.output(DAC, 0)
try:
    while True:
        try:
            Volt=float(input("Введите напряжение в вольтах: "))
            nV=voltage_to_number(Volt)
            state=d2b(nV)
            print(f"Число на вход ЦАП {nV}, ,биты {state}")
            for i in DAC:
                IO.output(i, state[DAC.index(i)])
            time.sleep(period)
        except:
            print("Вы ввели не число")
        
finally:
    IO.output(DAC, 0)
    IO.cleanup()



