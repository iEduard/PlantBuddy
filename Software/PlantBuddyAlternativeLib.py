import board
from ht16k33matrixcolour import HT16K33MatrixColour
import time
from enum import Enum

class Emoji(Enum):
    HEART_SMALL = 1
    HEART_BIG = 2
    SMILE_LOOK_CENTER = 3
    SMILE_LOOK_LEFT = 4
    SMILE_LOOK_RIGHT = 5
    SMILE_BLINK = 6
    KISS = 7


class Animation(Enum):
    HEART_BEAT = 1
    LOOK_LEFT_RIGHT_BLINK = 2
    LOOK_LEFT_RIGHT_KISS = 3


class PlantBuddy():


    def __init__(self, *args, **kwargs):
        """Class init"""

        self.i2c = board.I2C()
        self.matrix = HT16K33MatrixColour(self.i2c)


    def run(self):

        i2c = board.I2C()
        self.matrix = HT16K33MatrixColour(i2c)
        #matrix[row, coloumn]
        
        print("Start")

        #Clear
        self.__animation(Animation.LOOK_LEFT_RIGHT_KISS)

        #self.__animation(Animation.HEART_BEAT)

        print("Done")


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
            self.matrix.set_icon(icon)

        elif (Emoji.HEART_BIG == emoji):

            icon = b"\x00\x30\x00\x78\x00\x7C\x00\x3E\x00\x3E\x00\x7C\x00\x78\x00\x30" 
            self.matrix.set_icon(icon)

        elif (Emoji.SMILE_LOOK_CENTER == emoji):

            icon = b"\x00\x00\x64\x00\x62\x00\x02\x00\x02\x00\x62\x00\x64\x00\x00\x00"
            self.matrix.set_icon(icon)

        elif (Emoji.SMILE_LOOK_LEFT == emoji):

            icon = b"\x60\x00\x64\x00\x02\x00\x02\x00\x62\x00\x62\x00\x04\x00\x00\x00"
            self.matrix.set_icon(icon)

        elif (Emoji.SMILE_LOOK_RIGHT == emoji):

            icon = b"\x00\x00\x04\x00\x62\x00\x62\x00\x02\x00\x02\x00\x64\x00\x60\x00"
            self.matrix.set_icon(icon)

        elif (Emoji.SMILE_BLINK == emoji):

            icon =  b"\x00\x00\x24\x00\x22\x00\x02\x00\x02\x00\x22\x00\x24\x00\x00\x00"
            self.matrix.set_icon(icon)

        elif (Emoji.KISS == emoji):

            icon = b"\x00\x00\x60\x00\x60\x00\x00\x00\x00\x0A\x20\x04\x20\x0A\x00\x00"
            self.matrix.set_icon(icon)


        #Draw the emoji
        self.matrix.draw()

    def __animation(self, animation:Animation):
        """
        Animate the given pattern with the given duration
        """
        False
        if (Animation.HEART_BEAT == animation):
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
            time.sleep(0.3)
            self.__drawEmoji(Emoji.KISS)
            time.sleep(0.3)
            self.__animation(Animation.HEART_BEAT)

if __name__ == '__main__':

    #Init the buddy
    buddy = PlantBuddy()

    #Wake up... buddy wake up :-)     
    buddy.run()