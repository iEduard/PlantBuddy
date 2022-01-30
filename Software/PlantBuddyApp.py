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
        self.buddy = buddy.Buddy(self.i2c)

        self.plant = plant.Plant()

    def run(self):

        self.active = True
        
        print("Start")
        self.buddy.run()


        #Clear
        while self.active:

            #Wait untill the end of time
            False


        print("Done")

    def __state(self):
        """
        State machnie of the plant buddy
        -----
        Should be running in an seperated thread
        All the transitions between the state will be done here
        """





        if(self.state == BuddyState.INIT):
            #Do init stuff
            self.matrix.clear().draw()

            #Switch state to wake up
            self.state = BuddyState.WAKE_UP

        elif(self.state == BuddyState.WAKE_UP):

            #Perform the wake up animation
            self.__animation(Animation.WAKE_UP)

            #Switch to state awake
            self.state = BuddyState.AWAKE

        elif(self.state == BuddyState.AWAKE):

            #Perform the wake up animation
            self.plantStateSwitch = False

            #Clear
            while not self.plantStateSwitch:

                animationSelector = random.randrange(100)

                if(animationSelector < 80):
                    self.__animation(Animation.RANDOM_BLINK)
                elif(animationSelector < 95):
                    self.__animation(Animation.LOOK_LEFT_RIGHT_BLINK)
                elif(animationSelector < 100):
                    self.__animation(Animation.LOOK_LEFT_RIGHT_KISS)





        #Set the state back to false
        self.plantStateSwitch = False

if __name__ == '__main__':

    #Init the buddy
    plantBuddyApp = PlantBuddyApp()

    #Wake up... buddy wake up :-)     
    plantBuddyApp.run()