import board
import time
from enum import Enum
import random
import buddy
import plant

class PlantBuddyApp():


    def __init__(self, *args, **kwargs):
        """Class init"""

        #Get the i2c object
        self.i2c = board.I2C()        

        #init the Buddy 

        self.plant = plant.Plant(self.i2c)

        self.buddy = buddy.Buddy(self.i2c, self.plant)


    def run(self):

        self.active = True
        
        print("Start")
        self.buddy.run()
        self.plant.run()
        
        #Clear
        while self.active:

            print("Temp: {:.1f} C    humidity: {}% ".format( self.plant.temperature, self.plant.humidity))
            print("Light: {:.2f} lux".format(self.plant.illuminance))
            time.sleep(8.0)

            #Wait untill the end of time
            False

        print("Done")

        #Set the state back to false
        self.plantStateSwitch = False

if __name__ == '__main__':

    #Init the buddy
    plantBuddyApp = PlantBuddyApp()

    #Wake up... buddy wake up :-)     
    plantBuddyApp.run()