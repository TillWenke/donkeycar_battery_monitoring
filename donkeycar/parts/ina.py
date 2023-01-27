import time

class INA:
    def __init__(self, addr=0x41, poll_delay=0.0166):
        import board
        import busio
        import adafruit_ina219
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_ina219.INA219(i2c, addr)
        
        self.on = True
        self.poll_delay = poll_delay
        self.voltage = 0.
        self.current = 0.
        self.power = 0.
        
    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)
            
    def poll(self):
        try:
            self.voltage = self.sensor.bus_voltage
            self.current = self.sensor.current
            self.power = self.sensor.power
        except:
            print('failed to read INA219!!')
            
    def run_threaded(self):
        return self.voltage, self.current, self.power

    def run(self):
        self.poll()
        return self.voltage, self.current, self.power

    def shutdown(self):
        self.on = False
