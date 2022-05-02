import board
from ht16k33matrixcolour import HT16K33MatrixColour
import threading
import time
from enum import Enum
import random
from environment import Environment



class State(Enum):

    INIT = 0
    ASLEEP = 1
    WAKE_UP = 2
    AWAKE = 3
    NORMAL = 5
    COLD = 10
    HOT = 11
    THURSTY = 20
    DROWNING = 21
    EXIT = 9999

class Emoji(Enum):
    HEART_SMALL = 1
    HEART_BIG = 2
    SMILE_LOOK_CENTER = 3
    SMILE_LOOK_LEFT = 4
    SMILE_LOOK_RIGHT = 5
    SMILE_BLINK = 6
    KISS = 7
    YAWNING_CLOSED_EYES = 8
    YAWNING_OPENED_EYES = 9
    FLAT_CLOSED_EYES = 10
    FLAT_OPENED_EYES = 11
    SMILE_BLINK_TONGUE_OUT = 12

class Animation(Enum):
    HEART_BEAT = 1
    LOOK_LEFT_RIGHT_BLINK = 2
    LOOK_LEFT_RIGHT_KISS = 3
    RANDOM_BLINK = 4
    WAKE_UP = 5
    FALL_ASLEEP = 6
    SLEEP = 7
    LOOK_LEFT_RIGHT_TONGUE_OUT = 8
    ROLE_FACE = 9
    SWEATING = 10


class Buddy():


    def __init__(self, i2c:board.I2C, **kwargs):
        """Class init"""

        self.matrix = HT16K33MatrixColour(i2c)
        
        #Init the State machine
        self.state = State.INIT
        self.plantState  = State.HOT #Init the plant state to normal


    def run(self):
        
        print("Buddy wake up...")

        #Create a task and run it // , daemon=True
        self.deamonThread = threading.Thread(target=self.__stateMachine)
        self.deamonThread.start()

        print("Buddy is up and awake")

    def updatePlantState(self, state:State):
        """
        Send the Plant State to the plant buddy
        ----
        state is the plant state as PlantState Enum  
        """
        #safe the state to the local variable
        self.plantState = state

    def getState(self):
        """
        Gett thr current state of the Plant Buddy
        ---
        Will return the State as an BuddyState Enum
        """
        return self.state

    def __stateMachine(self):
        """
        State machnie of the plant buddy
        -----
        Should be running in an seperated thread
        All the transitions between the state will be done here
        """
        while not (self.state == State.EXIT):
            
            if(self.state == State.INIT):

                print("State == Init")
                #Do init stuff
                self.matrix.clear().draw()

                #Switch state to wake up
                self.state = State.WAKE_UP

            elif(self.state == State.WAKE_UP):
                
                print("State == WAKE UP")
                #Perform the wake up animation
                self.__animation(Animation.WAKE_UP)

                #Switch to state awake
                self.state = State.AWAKE

            elif(self.state == State.AWAKE):

                print("State == Awake")
                #Perform the wake up animation
                self.plantStateSwitch = False

                animationSelector = random.randrange(100)

                if (self.plantState != State.NORMAL):
                    self.state = self.plantState

                elif(animationSelector < 75):
                    self.__animation(Animation.RANDOM_BLINK)
                elif(animationSelector < 85):
                    self.__animation(Animation.LOOK_LEFT_RIGHT_TONGUE_OUT)
                elif(animationSelector < 90):
                    self.__animation(Animation.ROLE_FACE)
                elif(animationSelector < 95):
                    self.__animation(Animation.LOOK_LEFT_RIGHT_BLINK)
                elif(animationSelector < 100):
                    self.__animation(Animation.LOOK_LEFT_RIGHT_KISS)

            elif(self.state == State.COLD):
                #To cold for the plant
                print("State == Cold")
                time.sleep(1)
                False #Performe the animation for to cold
                
                self.state = State.AWAKE
            
            elif(self.state == State.HOT):
                #To hot for the plant
                print("State == Hot")

                self.__animation(Animation.SWEATING)
                self.state = State.AWAKE

            elif(self.state == State.THURSTY):
                #To less water for the plant
                print("State == Thursty")
                time.sleep(1)
                False 
                self.state = State.AWAKE

            elif(self.state == State.DROWNING):
                #To much water
                print("State == Drowning")
                time.sleep(1)
                False
                self.state = State.AWAKE


            self.plantStateSwitch = False


    def __drawEmoji(self, emoji:Emoji):
        """
        Draw the requested emoji
        """
        #Clear the icon 
        icon = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

        #Define the emoji
        if (Emoji.HEART_SMALL == emoji):
            icon = b"\x00\x00\x00\x18\x00\x3C\x00\x1E\x00\x3C\x00\x18\x00\x00\x00\x00" 

        elif (Emoji.HEART_BIG == emoji):
            icon = b"\x00\x30\x00\x78\x00\x7C\x00\x3E\x00\x3E\x00\x7C\x00\x78\x00\x30" 

        elif (Emoji.SMILE_LOOK_CENTER == emoji):
            icon = b"\x00\x00\x64\x00\x62\x00\x02\x00\x02\x00\x62\x00\x64\x00\x00\x00"

        elif (Emoji.SMILE_LOOK_LEFT == emoji):
            icon = b"\x60\x00\x64\x00\x02\x00\x02\x00\x62\x00\x62\x00\x04\x00\x00\x00"

        elif (Emoji.SMILE_LOOK_RIGHT == emoji):
            icon = b"\x00\x00\x04\x00\x62\x00\x62\x00\x02\x00\x02\x00\x64\x00\x60\x00"

        elif (Emoji.SMILE_BLINK == emoji):
            icon =  b"\x00\x00\x24\x00\x22\x00\x02\x00\x02\x00\x22\x00\x24\x00\x00\x00"

        elif (Emoji.KISS == emoji):
            icon = b"\x00\x00\x60\x00\x60\x00\x00\x00\x00\x0A\x20\x04\x20\x0A\x00\x00"

        elif(Emoji.YAWNING_CLOSED_EYES == emoji):
            icon = b"\x00\x00\x24\x00\x2A\x00\x0A\x00\x0A\x00\x2A\x00\x24\x00\x00\x00"

        elif(Emoji.YAWNING_OPENED_EYES == emoji):
            icon = b"\x00\x00\x64\x00\x6A\x00\x0A\x00\x0A\x00\x6A\x00\x64\x00\x00\x00"

        elif(Emoji.FLAT_CLOSED_EYES == emoji):
            icon = b"\x00\x00\x24\x00\x24\x00\x04\x00\x04\x00\x24\x00\x24\x00\x00\x00"

        elif(Emoji.FLAT_OPENED_EYES == emoji):
            icon = b"\x00\x00\x64\x00\x64\x00\x04\x00\x04\x00\x64\x00\x64\x00\x00\x00"

        elif(Emoji.SMILE_BLINK_TONGUE_OUT == emoji):
            icon = b"\x00\x00\x64\x00\x62\x00\x02\x00\x00\x03\x20\x03\x24\x00\x00\x00"

        self.__drawIcon(icon)

    def __drawIcon(self, icon):

        #Clear the display
        self.matrix.clear()

        self.matrix.set_icon(icon)
        #Draw the emoji
        self.matrix.draw()

    def __animation(self, animation:Animation):
        """
        Animate the given pattern with the given duration
        -----
        animation : Pass through the requestet animation via Animation Enum
        """

        if (Animation.WAKE_UP == animation):

            #Animate the wake up.
            self.__drawEmoji(Emoji.FLAT_CLOSED_EYES)
            time.sleep(0.8)
            self.__drawEmoji(Emoji.YAWNING_CLOSED_EYES)
            time.sleep(0.6)
            self.__drawEmoji(Emoji.FLAT_CLOSED_EYES)
            time.sleep(0.5)
            self.__drawEmoji(Emoji.YAWNING_CLOSED_EYES)
            time.sleep(0.7)
            self.__drawEmoji(Emoji.FLAT_CLOSED_EYES)
            time.sleep(0.2)
            self.__drawEmoji(Emoji.FLAT_OPENED_EYES)
            time.sleep(0.2)
            self.__drawEmoji(Emoji.FLAT_CLOSED_EYES)
            time.sleep(0.2)
            self.__drawEmoji(Emoji.FLAT_OPENED_EYES)
            time.sleep(0.7)
            self.__drawEmoji(Emoji.YAWNING_OPENED_EYES)
            time.sleep(0.8)
            self.__drawEmoji(Emoji.FLAT_OPENED_EYES)
            time.sleep(0.7)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)

        elif (Animation.HEART_BEAT == animation):
            #Animate an Heart Beat
            self.__drawEmoji(Emoji.HEART_SMALL)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.HEART_BIG)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.HEART_SMALL)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.HEART_BIG)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.HEART_SMALL)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.HEART_BIG)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.HEART_SMALL)
            time.sleep(0.3)

        elif (Animation.LOOK_LEFT_RIGHT_BLINK == animation):
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_LEFT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_RIGHT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_BLINK)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)

        elif (Animation.LOOK_LEFT_RIGHT_TONGUE_OUT == animation):
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_LEFT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_RIGHT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_BLINK_TONGUE_OUT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)

        elif (Animation.LOOK_LEFT_RIGHT_KISS == animation):
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_LEFT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_RIGHT)
            time.sleep(0.3)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.5)
            self.__drawEmoji(Emoji.KISS)
            time.sleep(0.5)
            self.__animation(Animation.HEART_BEAT)

        elif (Animation.RANDOM_BLINK == animation):

            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)

            #Define a random time before blinking
            sleepTime = random.uniform(3, 6)
            time.sleep(sleepTime)

            self.__drawEmoji(Emoji.SMILE_BLINK)
            time.sleep(0.4)
            self.__drawEmoji(Emoji.SMILE_LOOK_CENTER)
            time.sleep(0.3)

        elif (Animation.ROLE_FACE == animation):
            # Role the complete face.

            _sleepTime = 0.2
            _icon = b"\x00\x00\x64\x00\x62\x00\x02\x00\x02\x00\x62\x00\x64\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x64\x00\x62\x00\x02\x00\x02\x00\x62\x00\x64\x00\x00\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x62\x00\x02\x00\x02\x00\x62\x00\x64\x00\x00\x00\x00\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x02\x00\x02\x00\x62\x00\x64\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x02\x00\x62\x00\x64\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x62\x00\x64\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x64\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x00\x62\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x00\x62\x00\x02\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x00\x00\x00\x00\x00\x00\x64\x00\x62\x00\x02\x00\x02\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x00\x00\x00\x00\x64\x00\x62\x00\x02\x00\x02\x00\x62\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x00\x00\x64\x00\x62\x00\x02\x00\x02\x00\x62\x00\x64\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)

        elif (Animation.SWEATING == animation):
            # Sweating face

            _sleepTime = 0.2

            _icon = b"\x00\x00\x64\x00\xEA\x80\x08\x03\x08\x03\x6A\x00\x64\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\xE4\x80\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x80\x80\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x40\x40\x64\x00\x6A\x00\x08\x03\x08\x03\x2A\x00\x24\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x20\x20\x24\x00\x2A\x00\x08\x03\x08\x03\x2A\x00\x24\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x10\x10\x24\x00\x2A\x00\x08\x03\x88\x83\x2A\x00\x24\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x08\x08\x24\x00\x2A\x00\x08\x03\x08\x03\xEA\x80\x64\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x04\x04\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\xE4\x80\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x02\x02\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x80\x80"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x01\x01\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x40\x40"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x20\x20"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x10\x10"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x64\x00\x6A\x00\x08\x03\x08\x03\x6A\x00\x64\x00\x08\x08"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x64\x00\x6A\x00\x08\x03\x08\x03\x2A\x00\x24\x00\x04\x04"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x24\x00\x2A\x00\x08\x03\x08\x03\x2A\x00\x24\x00\x02\x02"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x24\x00\x2A\x00\x08\x03\x08\x03\x2A\x00\x24\x00\x01\x01"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)
            _icon = b"\x00\x00\x64\x00\x6A\x00\x08\x03\x08\x03\x2A\x00\x24\x00\x00\x00"
            self.__drawIcon(_icon)
            time.sleep(_sleepTime)