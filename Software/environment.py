from enum import Enum
import board
import adafruit_dht
import time
import threading
import smbus
from bh1750 import BH1750

try:
    # Used only for typing
    from typing import Union
except ImportError:
    pass

class State(Enum):
    HOT = 1
    COLD = 2
    DRAWNING = 3


class Environment():

    def __init__(self, i2c:board.I2C, **kwargs):
        """
        Constructor of the plant class
        """

        # Initial the dht device, with data pin connected to:
        self._tempAndHumiditySensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)

        #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
        bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
        self._lightSensor = BH1750(bus)

        self._temperature_c = 0.0
        self._humidity = 0.0
        self._illuminance = 0.0


    def run(self):
        """
        Get the environment data
        """
        self._readSensors = True

        #Create a task and run it // , daemon=True
        self._sensorDeamonThread = threading.Thread(target=self.__sensorDeamon)
        self._sensorDeamonThread.start()

    def __sensorDeamon(self):
        """
        Read all the sensor values at once and store them to parameters
        """
        while self._readSensors:
            try:
                # read the temperature and _humidity sensor
                self._temperature_c = self._tempAndHumiditySensor.temperature
                self._humidity = self._tempAndHumiditySensor._humidity
                #print("Temp: {:.1f} C    humidity: {}% ".format( self._temperature_c, self._humidity))

                # Read the light sensor
                self._lightSensor.set_sensitivity(255)
                self._illuminance = self._lightSensor.measure_low_res()
                #print("Light: {:.2f} lux".format(self._illuminance))
                time.sleep(4)

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
            except Exception as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
    
    @property
    def temperature(self) -> Union[int, float, None]:
        """reads available last temperature. 
        """

        return self._temperature_c

    @property
    def humidity(self) -> Union[int, float, None]:
        """reads available last humidity. 
        """
    
        return self._humidity

    @property
    def illuminance(self) -> Union[int, float, None]:
        """reads available last illuminance. 
        """
    
        return self._illuminance

