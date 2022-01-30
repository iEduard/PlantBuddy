import board
from ht16k33matrixcolour import HT16K33MatrixColour
import threading
import time
from enum import Enum
import random
import plant



class State(Enum):

    INIT = 0
    ASLEEP = 1
    WAKE_UP = 2
    AWAKE = 3
    EXIT =9999

class Emoji(Enum):
    HEART_SMALL = 1
    HEART_BIG = 2
    SMILE_LOOK_CENTER = 3
    SMILE_LOOK_LEFT = 4
    SMILE_LOOK_RIGHT = 5
    SMILE_BLINK = 6
    KISS = 7
    YAWNING_CLOSED_EYES = 8
    YAWNING_OPEND_EYES = 9
    FLAT_CLOSED_EYES = 10
    FLAT_OPEND_EYES = 11
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
    
class Buddy():


    def __init__(self, i2c:board.I2C, **kwargs):
        """Class init"""

        self.matrix = HT16K33MatrixColour(i2c)
        
        #Init the State machine
        self.state = State.INIT


    def run(self):
        
        print("Buddy wake up...")

        #Create a task and run it // , daemon=True
        self.deamonThread = threading.Thread(target=self.__stateMachine)
        self.deamonThread.start()

        print("Buddy is up and awake")

    def updateState(self, state:plant.State):
        """
        Send the Plant State to the plant buddy
        ----
        state is the plant state as PlantState Enum  
        """

        #Check if the state has changed
        if (self.plantState != state):
            self.plantStateSwitch = True

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

                #Clear
                while not self.plantStateSwitch:

                    animationSelector = random.randrange(100)

                    if(animationSelector < 60):
                        self.__animation(Animation.RANDOM_BLINK)
                    elif(animationSelector < 80):
                        self.__animation(Animation.LOOK_LEFT_RIGHT_TONGUE_OUT)
                    elif(animationSelector < 95):
                        self.__animation(Animation.LOOK_LEFT_RIGHT_BLINK)
                    elif(animationSelector < 100):
                        self.__animation(Animation.LOOK_LEFT_RIGHT_KISS)


            self.plantStateSwitch = False


    def __drawEmoji(self, emoji:Emoji):
        """
        Draw the requested emoji
        """

        #Clear the display
        self.matrix.clear()

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

        elif(Emoji.YAWNING_OPEND_EYES == emoji):
            icon = b"\x00\x00\x64\x00\x6A\x00\x0A\x00\x0A\x00\x6A\x00\x64\x00\x00\x00"

        elif(Emoji.FLAT_CLOSED_EYES == emoji):
            icon = b"\x00\x00\x24\x00\x24\x00\x04\x00\x04\x00\x24\x00\x24\x00\x00\x00"

        elif(Emoji.FLAT_OPEND_EYES == emoji):
            icon = b"\x00\x00\x64\x00\x64\x00\x04\x00\x04\x00\x64\x00\x64\x00\x00\x00"

        elif(Emoji.SMILE_BLINK_TONGUE_OUT == emoji):
            icon = b"\x00\x00\x64\x00\x62\x00\x02\x00\x00\x03\x20\x03\x24\x00\x00\x00"

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
            self.__drawEmoji(Emoji.FLAT_OPEND_EYES)
            time.sleep(0.2)
            self.__drawEmoji(Emoji.FLAT_CLOSED_EYES)
            time.sleep(0.2)
            self.__drawEmoji(Emoji.FLAT_OPEND_EYES)
            time.sleep(0.7)
            self.__drawEmoji(Emoji.YAWNING_OPEND_EYES)
            time.sleep(0.8)
            self.__drawEmoji(Emoji.FLAT_OPEND_EYES)
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