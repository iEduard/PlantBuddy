from enum import Enum
import board
import adafruit_dht
import time
import threading

class State(Enum):
    HOT = 1
    COLD = 2
    DRAWNING = 3


class Plant():

    def __init__(self, *args, **kwargs):
        """
        Constructor of the plant class
        """

        # Initial the dht device, with data pin connected to:
        self.tempAndHumiditySensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)


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
                # Print the values to the serial port
                temperature_c = self.tempAndHumiditySensor.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = self.tempAndHumiditySensor.humidity
                print(
                    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                        temperature_f, temperature_c, humidity
                    )
                )

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                self.tempAndHumiditySensor.exit()
                raise error

            time.sleep(2.0)    
