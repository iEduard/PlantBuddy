import board
from adafruit_ht16k33.matrix import Matrix8x8x2

i2c = board.I2C()
matrix = Matrix8x8x2(i2c)


matrix[0, 0] = matrix.LED_RED
matrix[1, 4] = matrix.LED_GREEN
matrix[2, 7] = matrix.LED_YELLOW
matrix[3, 0] = matrix.LED_OFF


print("Hello World")