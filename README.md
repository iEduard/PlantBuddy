# PlantBuddy

Buddy that helps you out with your plants


## Hardware


- Arduino Nano
- Capacitive moisture sensor
- 8x8 Bicolor LED matrix 
- BH1750 Digital light sensor



### LED Matrix

LED Matrix from Adafruit: https://www.adafruit.com/product/902

In order to improve the performance we use this Library to control the LED-Matrix. The ht16k33.py and the ht16k33matrixcolour.py Files are needed in order to function properly.

https://github.com/smittytone/HT16K33-Python

With this Library we also need the blinka library from Adafruit. To install the Library you can use pip.
But still needs the blinka library from Adafruit

> sudo pip3 install adafruit-blinka



### Light Sensor

The Fritzing file was downloaded here:
http://omnigatherum.ca/wp/?p=338

Library reference
https://www.arduino.cc/reference/en/libraries/bh1750/


### Temp Humidity Sensor

Using the DHT Library

Examples here: https://learn.adafruit.com/dht/using-a-dhtxx-sensor

Used library is from Adafruit: https://github.com/adafruit/Adafruit_CircuitPython_DHT
To Install the library use pip

> pip3 install adafruit-circuitpython-dht

## Software



### Install Dependencies









