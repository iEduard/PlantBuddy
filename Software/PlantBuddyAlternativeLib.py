import board
from ht16k33matrixcolour import HT16K33MatrixColour
import time
from enum import Enum

class Emoji(Enum):
    HEART_SMALL = 1
    HEART_BIG = 2

class PlantBuddy():


    def __init__(self, *args, **kwargs):
        """Class init"""

        self.i2c = board.I2C()
        self.matrix = HT16K33MatrixColour(self.i2c)


    def run(self):

        i2c = board.I2C()
        self.matrix = HT16K33MatrixColour(i2c)
        #matrix[row, coloumn]
        
        print("Hello World")

        #Clear
        self.matrix.clear().draw()
        time.sleep(0.9)


        #Fill LED
        #matrix.fill(matrix.COLOUR_YELLOW).draw()
        #time.sleep(0.9)

        # Clear the display
        #matrix.clear().draw()
        #time.sleep(0.9)

        #Fill LED
        #matrix.fill(matrix.COLOUR_GREEN).draw()
        #time.sleep(0.9)

        # Clear the display
        #matrix.clear().draw()
        #time.sleep(0.9)

        #Fill LED
        #matrix.fill(matrix.COLOUR_RED).draw()
        #time.sleep(0.9)

        #for x in range(8):
        #    matrix.plot(x, 0).plot(x, 7)
        #for y in range(1,7):
        #    matrix.plot(0, y).plot(7, y)

        self.matrix.clear()
        self.matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
        time.sleep(0.3)

        self.matrix.clear()
        self.matrix.plot(1, 0).plot(1, 1).plot(2, 0).plot(2, 1).draw()
        time.sleep(0.3)    

        self.matrix.clear()
        self.matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
        time.sleep(0.3)

        self.matrix.clear()
        self.matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
        time.sleep(0.3)

        self.matrix.clear()
        self.matrix.plot(1, 0).plot(1, 1).plot(2, 0).plot(2, 1).draw()
        time.sleep(0.3)    

        self.matrix.clear()
        self.matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
        time.sleep(0.3)


        #matrix.draw()

        #matrix.plot(1, 1, matrix.COLOUR_GREEN).draw()
        self.matrix.clear()

        print("Hello Raspberry Pi")


    def __drawEmoji(self, emoji):
        """
        Draw the requested emoji
        """

        #Clear the display


        #Define the emoji
        if (Emoji.HEART_SMALL == emoji):

            self.matrix.plot(1, 1, self.matrix.COLOUR_RED).draw()

        elif (Emoji.HEART_BIG == emoji):
            self.matrix.plot(1, 1, self.matrix.COLOUR_RED).draw()

        #Draw the emoji
        self.matrix.draw()

    def __animation(self):
        """
        Animate the given pattern with the given duration
        """
        False

if __name__ == '__main__':

    #Init the buddy
    buddy = PlantBuddy()

    #Wake up... buddy wake up :-)     
    buddy.run()