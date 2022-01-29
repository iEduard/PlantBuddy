import board
from ht16k33matrixcolour import HT16K33MatrixColour
import time

def main():

    i2c = board.I2C()
    matrix = HT16K33MatrixColour(i2c)
    #matrix[row, coloumn]
    
    print("Hello World")

    #Clear
    matrix.clear().draw()
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

    matrix.clear()
    matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
    time.sleep(0.3)

    matrix.clear()
    matrix.plot(1, 0).plot(1, 1).plot(2, 0).plot(2, 1).draw()
    time.sleep(0.3)    

    matrix.clear()
    matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
    time.sleep(0.3)

    matrix.clear()
    matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
    time.sleep(0.3)

    matrix.clear()
    matrix.plot(1, 0).plot(1, 1).plot(2, 0).plot(2, 1).draw()
    time.sleep(0.3)    

    matrix.clear()
    matrix.plot(1, 1).plot(1, 2).plot(2, 1).plot(2, 2).draw()
    time.sleep(0.3)


    #matrix.draw()

    #matrix.plot(1, 1, matrix.COLOUR_GREEN).draw()


    print("Hello Raspberry Pi")


if __name__ == '__main__':

    #Start the main program
    main()