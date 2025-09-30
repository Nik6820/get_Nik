import RPi.GPIO as IO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_freq, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_freq = pwm_freq
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        IO.setmode(IO.BCM)
        IO.setup(self.gpio_pin, IO.OUT)
        self.pwm=IO.PWM(self.gpio_pin, self.pwm_freq)
        duty=0
        self.pwm.start(duty)

    def deinit(self):
        IO.output(self.gpio_pin, 0)
        IO.cleanup()

    def set_voltage(self, V):
        if not(0.0 <= V <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{self.dynamic_range:.2f} В)")
            print("устанавливаем 0.0")
            V = 0
        duty=int(100*V/self.dynamic_range)
        self.pwm.ChangeDutyCycle(duty)


if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Не число!\n") 

    finally:
        dac.deinit()    