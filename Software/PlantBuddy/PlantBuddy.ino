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
int soilMoistureValue = 0;
long randNumber;
long randDelay;
void setup() {
  Serial.begin(9600);
  Serial.println("8x8 LED Matrix Test");
  matrix.begin(0x70);  // pass in the address
}

void loop() {

  Serial.println("----");
  soilMoistureValue = analogRead(A0);
  Serial.println(soilMoistureValue);
  // Read the analog value
  int moistureLevel = 1;

  if((600 > soilMoistureValue) & (soilMoistureValue > 430)){
    moistureLevel = 2; // Dry
  }
  else if((430 > soilMoistureValue) & (soilMoistureValue > 350)){
    moistureLevel = 1; // Wet
  }
  else if((350 > soilMoistureValue) & (soilMoistureValue > 0)){  
    moistureLevel = 3; // Water
  }
moistureLevel = 1;
  switch(moistureLevel)
  {
    case 1:
      // enough water
      randDelay = random(2500, 4000);
      drawSmiley(1, true, 1, int(randDelay));

      randNumber = random(70);

      if(randNumber < 50){
        // Blink with the eyes         
        drawSmiley(1, false, 1, 300);
      }
      else if(randNumber < 60){
        drawSmiley(2, true, 1, 400);
        drawSmiley(1, true, 1, 100);
        drawSmiley(3, true, 1, 400);
      }
      else if(randNumber < 65){
        drawSmiley(2, true, 1, 400);
        drawSmiley(1, true, 1, 100);
        drawSmiley(3, true, 1, 400);
        drawSmiley(1, true, 1, 500);
        drawSmiley(1, true, 6, 600);// Tongeue out
      }
      else if(randNumber < 70){         
        drawSmiley(1, false, 1, 300); // Blink with the eyes
        drawSmiley(1, true, 1, 300);
        drawSmiley(1, false, 1, 300);
        drawSmiley(1, true, 1, 300);
        drawSmiley(11, true, 4, 700); // Kiss

        drawHeart(2, 300); // Blink with an heart two times
        drawHeart(1, 300);
        drawHeart(2, 300);
        drawHeart(1, 300);        
      }

      drawSmiley(1, true, 1, 500);
 
      break;

    case 2:
      // medium water
      randDelay = random(2500, 4000);
      drawSmiley(1, true, 2, int(randDelay));

      randNumber = random(70);

      if(randNumber < 50){
        // Blink with the eyes         
        drawSmiley(1, false, 2, 300);
      }
      else if(randNumber < 60){
        drawSmiley(2, true, 2, 400);
        drawSmiley(1, true, 2, 100);
        drawSmiley(3, true, 2, 400);
      }
      else if(randNumber < 65){
        // Tongeue out          
        drawSmiley(2, true, 2, 400);
        drawSmiley(1, true, 2, 100);
        drawSmiley(3, true, 2, 400);
        drawSmiley(1, true, 2, 500);
        drawSmiley(1, true, 7, 600);
      }
      else if(randNumber < 70){
        // Role eith the eyes
        drawSmiley(8, true, 2, 100);
        drawSmiley(5, true, 2, 100);
        drawSmiley(4, true, 2, 100);
        drawSmiley(6, true, 2, 100);
        drawSmiley(3, true, 2, 100);
        drawSmiley(10, true, 2, 100);
        drawSmiley(1, true, 2, 100);

        drawSmiley(1, false, 2, 300);
      }

      drawSmiley(1, true, 2, 500);
      break;

    case 3:
      // To much Water
      randDelay = random(2500, 4000);
      drawSmiley(1, true, 3, int(randDelay));
      drawSmiley(1, false, 3, 300);
      break;

    default:

      break;

  }  


}

void drawHeart(int heartSize,  int delayTime){

  uint8_t heart[8];
  matrix.clear(); // First of clear the matrix


  switch (heartSize)
  {
  case 1:
    // Large heart 
    heart[0] = B00000000;
    heart[1] = B01100110;
    heart[2] = B11111111;
    heart[3] = B11111111;
    heart[4] = B11111111;
    heart[5] = B01111110;
    heart[6] = B00111100;
    heart[7] = B00011000;

    break;

  case 2:
    // Smal heart
    heart[0] = B00000000;
    heart[1] = B00000000;
    heart[2] = B00101000;
    heart[3] = B01111100;
    heart[4] = B01111100;
    heart[5] = B00111000;
    heart[6] = B00010000;
    heart[7] = B00000000;

    break;

  default:
    break;
  }


  matrix.drawBitmap(0, 0, heart, 8, 8, LED_RED); // Set the requested layout on the Matrix
  matrix.writeDisplay(); // Draw the matrix

  // Delay the next step   
  delay(delayTime);


}

void drawSmiley(int eyes, bool eyesOpened, int mouth, int delayTime) {
  // Draw the smiley with eyes and mouth definition

  uint8_t smiley[8];
  matrix.clear(); // First of clear the matrix

  switch (eyes)
  {
    case 1:
      // center_center
      smiley[0] = B00000000;
      if (eyesOpened){
        smiley[1] = B01100110;
      }
      else{
        smiley[1] = B00000000;
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
      // right_down
      smiley[0] = B00000000;
      smiley[1] = B00000000;
      if (eyesOpened)
      {
        smiley[2] = B00110011;
      }
      smiley[3] = B00110011;
      break;


    case 11:
      // center right blink
      smiley[0] = B00000000;
      smiley[1] = B01100000;
      smiley[2] = B01100110;
      smiley[3] = B00000000;
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
      smiley[4] = B00001010;
      smiley[5] = B00000100;
      smiley[6] = B00001010;
      smiley[7] = B00000000;
      break;

    case 5:
      // Open
      smiley[4] = B00111100;
      smiley[5] = B01000010;
      smiley[6] = B00111100;
      smiley[7] = B00000000;
      break;

    case 6:
      // Tongue_out
      smiley[4] = B00000000;
      smiley[5] = B01000010;
      smiley[6] = B00111100;
      smiley[7] = B00001100;
      break;

    case 7:
      // Tongue_out flaot mouth
      smiley[4] = B00000000;
      smiley[5] = B00000000;
      smiley[6] = B01111110;
      smiley[7] = B00001100;
      break;

    default:
      // confused_opened
      smiley[4] = B00000000;
      smiley[5] = B01000000;
      smiley[6] = B00011000;
      smiley[7] = B00000010;
      break;
  }

  matrix.drawBitmap(0, 0, smiley, 8, 8, LED_GREEN); // Set the requested layout on the Matrix
  matrix.writeDisplay(); // Draw the matrix

  // Delay the next step   
  delay(delayTime);

}