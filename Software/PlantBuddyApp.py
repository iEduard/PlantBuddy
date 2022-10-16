import board
import time
from enum import Enum
import random
from buddy import Buddy
from environment import Environment
from plantSensors import PlantSensors

class PlantBuddyApp():


    def __init__(self, *args, **kwargs):
        """Class init"""

        #Get the i2c object
        self.i2c = board.I2C()        

        #init the Buddy 

        #self.environment = Environment(self.i2c)
        self.plantSensors = PlantSensors("./Settings/PlantSensors.json")
        self.buddy = Buddy(self.i2c)


    def run(self):

        self.active = True
        
        print("Start")
        self.buddy.run()
        self.plantSensors.run()
        #self.environment.run()
        
        #Clear
        while self.active:

            #print("Temp: {:.1f} C    humidity: {}% ".format( self.environment.temperature, self.environment.humidity))
            #print("Light: {:.2f} lux".format(self.environment.illuminance))
            time.sleep(8.0)

            #Wait untill the end of time
            False

        print("Done")

        #Set the state back to false
        self.environmentStateSwitch = False


if __name__ == '__main__':

    #Init the buddy
    plantBuddyApp = PlantBuddyApp()

    #Wake up... buddy wake up :-)     
    plantBuddyApp.run()