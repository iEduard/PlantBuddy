import board
from adafruit_ht16k33.matrix import Matrix8x8x2
import time

def main():

    i2c = board.I2C()
    matrix = Matrix8x8x2(i2c)
    #matrix[row, coloumn]
    
    print("Hello World")

    smiley(matrix, "Smile")
    time.sleep(0.4)
    smiley(matrix, "Closed")
    time.sleep(0.4)
    smiley(matrix, "Smile")
    time.sleep(0.4)
    smiley(matrix, "Closed")
    time.sleep(0.4)
    smiley(matrix, "Smile")



    print("Hello Raspberry Pi")


def smiley(matrix, smileyType):
    """
    """
    matrix.fill(0)

    if (smileyType == "Smile"):
        leftEye(matrix, "open_center", "left")
        leftEye(matrix, "open_center", "right")
    elif (smileyType == "Closed"):
        leftEye(matrix, "closed_center", "left")
        leftEye(matrix, "closed_center", "right")
    elif (smileyType == "Blink"):
        leftEye(matrix, "closed_center", "left")
        leftEye(matrix, "open_center", "right")

def leftEye(matrix, eye, leftOrRight):
    """
    """
    offset = 0

    if (leftOrRight == "left"):
        offset = 0
    elif (leftOrRight == "right"):
        offset = 4

    if (eye == "open_center"):
        matrix[0, offset + 0] = matrix.LED_OFF
        matrix[0, offset + 1] = matrix.LED_OFF
        matrix[0, offset + 2] = matrix.LED_OFF
        matrix[0, offset + 3] = matrix.LED_OFF

        matrix[1, offset + 0] = matrix.LED_OFF
        matrix[1, offset + 1] = matrix.LED_GREEN
        matrix[1, offset + 2] = matrix.LED_GREEN
        matrix[0, offset + 3] = matrix.LED_OFF

        matrix[2, offset + 0] = matrix.LED_OFF
        matrix[2, offset + 1] = matrix.LED_GREEN
        matrix[2, offset + 2] = matrix.LED_GREEN
        matrix[2, offset + 3] = matrix.LED_OFF

        matrix[3, offset + 0] = matrix.LED_OFF
        matrix[3, offset + 1] = matrix.LED_OFF
        matrix[3, offset + 2] = matrix.LED_OFF
        matrix[3, offset + 3] = matrix.LED_OFF

    elif(eye == "closed_center"):

        matrix[0, offset + 0] = matrix.LED_OFF
        matrix[0, offset + 1] = matrix.LED_OFF
        matrix[0, offset + 2] = matrix.LED_OFF
        matrix[0, offset + 3] = matrix.LED_OFF

        matrix[1, offset + 0] = matrix.LED_OFF
        matrix[1, offset + 1] = matrix.LED_OFF
        matrix[1, offset + 2] = matrix.LED_OFF
        matrix[0, offset + 3] = matrix.LED_OFF

        matrix[2, offset + 0] = matrix.LED_OFF
        matrix[2, offset + 1] = matrix.LED_GREEN
        matrix[2, offset + 2] = matrix.LED_GREEN
        matrix[2, offset + 3] = matrix.LED_OFF

        matrix[3, offset + 0] = matrix.LED_OFF
        matrix[3, offset + 1] = matrix.LED_OFF
        matrix[3, offset + 2] = matrix.LED_OFF
        matrix[3, offset + 3] = matrix.LED_OFF

if __name__ == '__main__':

    #Start the main program
    main()