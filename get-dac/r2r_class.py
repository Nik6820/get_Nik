import RPi.GPIO as IO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        IO.setmode(IO.BCM)
        IO.setup(self.gpio_bits, IO.OUT, initial = 0)
    
    def deinit(self):
        IO.output(self.gpio_bits, 0)
        IO.cleanup()
    
    def set_number(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    
    def set_voltage(self, V):
        if not(0.0 <= V <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{self.dynamic_range:.2f} В)")
            print("устанавливаем 0.0")
            V = 0
        nV=int(255*V/self.dynamic_range)
        v_ar = self.set_number(nV)
        for i in self.gpio_bits:
                IO.output(i, v_ar[self.gpio_bits.index(i)])


if __name__ == "__main__":
    try:
        dac = R2R_DAC([16,20,21,25,26,17,27,22], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Не число!\n") 

    finally:
        dac.deinit()            