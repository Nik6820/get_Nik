import smbus as i2c
class MCP4725:
    def __init__(self, dynamic_range, address = 0X61, verbose = False):
        self.bus = i2c.SMBus(1)
        self.address = address
        self.verbose = verbose
        self.dynamic_range=dynamic_range
        self.wm = 0
        self.pds = 0


    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые значения")
        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
        first_byte = self.wm | self.pds | number >> 8
        second_byte = number& 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, V):
        if not(0.0 <= V <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{self.dynamic_range:.2f} В)")
            print("устанавливаем 0.0")
            V = 0
        nV=int(4095*V/self.dynamic_range)
        self.set_number(nV)
        
if __name__ == "__main__":
    try:
        dac = MCP4725(5.17, 0x61, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Не число!\n") 

    finally:
        dac.deinit()      
