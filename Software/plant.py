from enum import Enum
import board
import adafruit_dht
import time
import threading
import smbus
from bh1750 import BH1750

class State(Enum):
    HOT = 1
    COLD = 2
    DRAWNING = 3


class Plant():

    def __init__(self, i2c:board.I2C, **kwargs):
        """
        Constructor of the plant class
        """

        # Initial the dht device, with data pin connected to:
        self.tempAndHumiditySensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)

        #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
        bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
        self.lightSensor = BH1750(bus)

    def run(self):
        """
        Startin the plan observation with all the sensors
        """
        self.readSensors = True

        #Create a task and run it // , daemon=True
        self.sensorDeamonThread = threading.Thread(target=self.__sensorDeamon)
        self.sensorDeamonThread.start()

    def __sensorDeamon(self):
        """
        """
        while self.readSensors:
            try:
                # read the temperature and humidity sensor
                self.temperature_c = self.tempAndHumiditySensor.temperature
                self.humidity = self.tempAndHumiditySensor.humidity
                print("Temp: {:.1f} C    Humidity: {}% ".format( self.temperature_c, self.humidity))

                # Read the light sensor
                self.lightSensor.set_sensitivity(255)
                self.illuminance = self.lightSensor.measure_low_res()
                print("Light: {:.2f} lux".format(self.illuminance))
                time.sleep(1)

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
            except Exception as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
                #self.tempAndHumiditySensor.exit()
                #raise error

            time.sleep(2.0)    
