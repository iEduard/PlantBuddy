# PlantBuddy

Buddy that helps you out with your plants


## Hardware

- Raspberry Pi zero [shop]()
- Capacitive moisture sensor [shop](https://www.reichelt.de/entwicklerboards-feuchtesensor-bodenfeuchte--debo-cap-sens-p223620.html?&nbc=1)
- 8x8 Bicolor LED matrix [shop](https://www.reichelt.de/entwicklerboards-zweifarbige-led-matrix-debo-led-matrix-p235472.html?&nbc=1)
- BH1750 Digital light sensor [shop](https://www.reichelt.de/entwicklerboards-digitaler-lichtsensor-bh1750-debo-bh-1750-p224217.html?&nbc=1)
- Moisture Sensor 


### Moisture sensor

Capacitive moisture sensor with an analog output.


### Distance sensor



### LED Matrix

The used LED Matrix is from Adafruit: https://www.adafruit.com/product/902
It is an 8x8 Bi Color LED Matrix. So you can display three colors red, yellow and green.

The Adafruit implementation for python causes slow response for the matrix. You are only able to set pixel by pixel.
In order to improve the performance we use this Library to control the LED-Matrix. The ht16k33.py and the ht16k33matrixcolour.py Files are needed in order to function properly.

https://github.com/smittytone/HT16K33-Python

With this Library we also need the blinka library from Adafruit. To install the Library you can use pip.
But still needs the blinka library from Adafruit

> sudo pip3 install adafruit-blinka


### Light sensor

The Fritzing file was downloaded here:
http://omnigatherum.ca/wp/?p=338

Interresting Library found here: [Link](https://gist.github.com/oskar456/95c66d564c58361ecf9f)

Alternative will be from adafruit here: [Link](https://learn.adafruit.com/adafruit-bh1750-ambient-light-sensor/python-circuitpython)

### Temp Humidity Sensor

Using the DHT Library

Some Infos from websites
- [Link1](https://www.pi-shop.ch/temperatur-und-feuchtigkeitssensor)
- [Link2](https://learn.adafruit.com/dht/using-a-dhtxx-sensor)

Used library is from Adafruit: https://github.com/adafruit/Adafruit_CircuitPython_DHT


To Install the library use pip:

> pip3 install adafruit-circuitpython-dht

## Software

The Software is written in Python. 


### Install Dependencies






