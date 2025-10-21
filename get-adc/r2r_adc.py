import RPi.GPIO as IO
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time=compare_time
        self.bits_gpio=[26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio=21
        IO.setmode(IO.BCM)
        IO.setup(self.bits_gpio, IO.OUT, initial = 0)
        IO.setup(self.comp_gpio, IO.IN)

    def deinit(self):
        IO.output(self.bits_gpio, 0)
        IO.cleanup()

    def set_number(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    
    def number_to_dac(self, N):
        v_ar = self.set_number(N)
        for i in self.bits_gpio:
                IO.output(i, v_ar[self.bits_gpio.index(i)])
    def sequental_counting_adc(self):
        for i in range(256):
            self.number_to_dac(i)
            if (IO.input(self.comp_gpio)>0):
                break
        time.sleep(self.compare_time)
        return i
    def get_sc_voltage(self):
        return self.sequental_counting_adc()/255*self.dynamic_range
    def successive_approximation_adc(self):
        self.right=256
        self.left=0
        while(self.right-self.left)>1:
            self.mid=int((self.right+self.left)/2)
            self.number_to_dac(self.mid)
            if IO.input(self.comp_gpio)>0:
                self.right=self.mid
            else:
                self.left=self.mid
        time.sleep(self.compare_time)
        return self.left
    def get_sar_voltage(self):
        return self.successive_approximation_adc()/255*self.dynamic_range
    


if (__name__ == "__main__"):
    try:
        adc=R2R_ADC(3.29)
        while True:
            #V=adc.get_sc_voltage()
            V=adc.get_sar_voltage()
            print(V)
            
    finally:
        adc.deinit()

