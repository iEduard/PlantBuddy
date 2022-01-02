/*************************************************** 
  This is a library for our I2C LED Backpacks

  Designed specifically to work with the Adafruit LED Matrix backpacks 
  ----> http://www.adafruit.com/products/872
  ----> http://www.adafruit.com/products/871
  ----> http://www.adafruit.com/products/870

  These displays use I2C to communicate, 2 pins are required to 
  interface. There are multiple selectable I2C addresses. For backpacks
  with 2 Address Select pins: 0x70, 0x71, 0x72 or 0x73. For backpacks
  with 3 Address Select pins: 0x70 thru 0x77

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

void setup() {
  Serial.begin(9600);
  Serial.println("8x8 LED Matrix Test");
  // matrix.begin(0x70);  // pass in the address
}

static const uint8_t PROGMEM
  smile_bmp[] =
  { B00111100,
    B01000010,
    B10100101,
    B10000001,
    B10100101,
    B10011001,
    B01000010,
    B00111100 },
  neutral_bmp[] =
  { B00111100,
    B01000010,
    B10100101,
    B10000001,
    B10111101,
    B10000001,
    B01000010,
    B00111100 },
  frown_bmp[] =
  { B00111100,
    B01000010,
    B10100101,
    B10000001,
    B10011001,
    B10100101,
    B01000010,
    B00111100 };

void loop() {

  Serial.println("----");

  // Read the analog value
  int moistureLevel = 3;

  switch(moistureLevel)
  {
    case 1:
      // enough water
      drawSmiley(1, true, 1);
      delay(500);

      drawSmiley(10, true, 1);
      delay(500);

      drawSmiley(1, true, 1);
      delay(500);

      drawSmiley(10, true, 4);
      delay(500);
 
      break;

    case 2:
      // medium water
      drawSmiley(1, true, 2);
      delay(800);
 
      drawSmiley(1, false, 2);
      delay(500);

      break;

    case 3:
      // Not enough water
      drawSmiley(1, true, 3);
      delay(800);

      drawSmiley(1, false, 3);
      delay(500);
 
      break;

    default:

      break;

  }  


}


void drawSmiley(int eyes, bool eyesOpened, int mouth) {
  // Draw the smiley with eyes and mouth definition

  uint8_t smiley[8];
  //matrix.clear(); // First of clear the matrix

  if(eyes == 1 && mouth == 1 && eyesOpened)
  {
    Serial.println("😀");
  }
  else if(eyes == 1 && mouth == 2 && eyesOpened)
  {
    Serial.println("😐");
  }
  else if(eyes == 1 && mouth == 2 && !eyesOpened)
  {
    Serial.println("😑");
  }
  else if(eyes == 1 && mouth == 3 && eyesOpened)
  {
    Serial.println("🙁");
  }
  else if(eyes == 1 && mouth == 3 && !eyesOpened)
  {
    Serial.println("😔");
  }
  else if(eyes == 10 && mouth == 1 && eyesOpened)
  {
    Serial.println("😉");
  }
  else if(eyes == 10 && mouth == 4 && eyesOpened)
  {
    Serial.println("😘");
  }


  switch (eyes)
  {
    case 1:
      // center_center
      smiley[0] = B00000000;
      if (eyesOpened)
      {
        smiley[1] = B01100110;
      }
      smiley[2] = B01100110;
      smiley[3] = B00000000;
      break;

    case 2:
      // center_left
      smiley[0] = B00000000;
      if (eyesOpened)
      {
        smiley[1] = B11001100;
      }
      smiley[2] = B11001100;
      smiley[3] = B00000000;
      break;

    case 3:
      // center_right
      smiley[0] = B00000000;
      if (eyesOpened)
      {
        smiley[1] = B00110011;
      }
      smiley[2] = B00110011;
      smiley[3] = B00000000;
      break;

    case 4:
      // center_up
      if (eyesOpened)
      {
        smiley[0] = B01100110;
      }
      smiley[1] = B01100110;
      smiley[2] = B00000000;
      smiley[3] = B00000000;
      break;

    case 5:
      // left_up
      if (eyesOpened)
      {
        smiley[0] = B11001100;
      }
      smiley[1] = B11001100;
      smiley[2] = B00000000;
      smiley[3] = B00000000;
      break;

    case 6:
      // right_up
      if (eyesOpened)
      {
        smiley[0] = B00110011;
      }
      smiley[1] = B00110011;
      smiley[2] = B00000000;
      smiley[3] = B00000000;
      break;


    case 7:
      // center_down
      smiley[0] = B00000000;
      smiley[1] = B00000000;
      if (eyesOpened)
      {
        smiley[2] = B01100110;
      }
      smiley[3] = B01100110;
      break;

    case 8:
      // left_down
      smiley[0] = B00000000;
      smiley[1] = B00000000;
      if (eyesOpened)
      {
        smiley[2] = B11001100;
      }
      smiley[3] = B11001100;
      break;

    case 9:
      // center_down
      smiley[0] = B00000000;
      smiley[1] = B00000000;
      if (eyesOpened)
      {
        smiley[2] = B00110011;
      }
      smiley[3] = B00110011;
      break;

    case 10:
      // center right blink
      smiley[0] = B00000000;
      smiley[1] = B00000000;
      smiley[2] = B00110000;
      smiley[3] = B00110011;
      break;

    default:
      // confused_opened
      smiley[0] = B00110000;
      smiley[1] = B00110110;
      smiley[2] = B00000110;
      smiley[3] = B00000000;
      break;
  }

  switch (mouth)
  {
    case 1:
      // Smile
      smiley[4] = B00000000;
      smiley[5] = B01000010;
      smiley[6] = B00111100;
      smiley[7] = B00000000;
      break;

    case 2:
      // ----
      smiley[4] = B00000000;
      smiley[5] = B00000000;
      smiley[6] = B01111110;
      smiley[7] = B00000000;
      break;

    case 3:
      // Sad
      smiley[4] = B00000000;
      smiley[5] = B00111100;
      smiley[6] = B01000010;
      smiley[7] = B00000000;
      break;

    case 4:
      // Kiss
      smiley[4] = B00010101;
      smiley[5] = B00001110;
      smiley[6] = B00010101;
      smiley[7] = B00000000;
      break;

    default:
      // confused_opened
      smiley[4] = B00000000;
      smiley[5] = B01000000;
      smiley[6] = B00011000;
      smiley[7] = B00000010;
      break;
  }

  //matrix.drawBitmap(0, 0, smiley, 8, 8, LED_GREEN); // Set the requested layout on the Matrix
  //matrix.writeDisplay(); // Draw the matrix

}