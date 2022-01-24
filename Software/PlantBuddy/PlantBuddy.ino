/*************************************************** 
  The coolest Robot to check your plants
    He will read the soil Moisture
    Temperature
    Humidity
    Light

  To check how good you treat your plant
 ****************************************************/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <BH1750.h>
#include "DHT.h"

#define echoPin 10 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 11 //attach pin D3 Arduino to pin Trig of HC-SR04


Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();
BH1750 lightMeter;
DHT dht(12, DHT22);


long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

int soilMoistureValue = 0;
long randNumber;
long randDelay;



int DebugLevel = 10; // Debug level for the serial output

int state = 0; // State of the Statemachine

// Setup
void setup() {
  Serial.begin(9600);
  Serial.println("Plant Budy Debug output");

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT

  matrix.begin(0x70);  // start the led matrix
  lightMeter.begin(); // start the light sensor
  dht.begin();  // start the tem sensor
}

// Main loop
void loop() {

  // Read the sensor values

  soilMoistureValue = analogRead(A0); // Read the moisture sensor
  float lux = lightMeter.readLightLevel(); // Read the light sensor 
  float hunidity = dht.readHumidity(); // Read the Humidity
  float temperature = dht.readTemperature(); // Read temperature as Celsius (the default)


  
  digitalWrite(trigPin, LOW);// Clears the trigPin condition
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);// Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  duration = pulseIn(echoPin, HIGH);// Reads the echoPin, returns the sound wave travel time in microseconds
  distance = duration * 0.034 / 2; // Calculating the distance // Speed of sound wave divided by 2 (go and back)


  //Debug output
  if(DebugLevel > 0){
    Serial.println("----");
    Serial.println(soilMoistureValue); 

    Serial.print("Light: " + String(lux) + "[LUX]" );
    // Serial.print("Humidity: " + String(hunidity) + "[%]");
    // Serial.print("Temperature: " + String(temperature) + "[°C]");
    // Serial.print("Distance: "+String(distance) + "[cm]");

  }

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

  switch (state)
  {
    case 0: // Init state
      state++;
      break;

    case 1: // Idle State

      // Check if it is dark
      if (lux < 1){
        state = 70;
      }
      else if(moistureLevel == 1){
        state = 10;
      }
      else if(moistureLevel == 2){
        state = 20;
      }
      else if(moistureLevel == 3){
        state = 30;
      }

      break; 

    case 10: // enough water

      randDelay = random(2500, 4000);
      drawSmiley(1, true, 1, int(randDelay));

      randNumber = random(70);

      if(randNumber < 50){
        // Blink with the eyes         
        drawSmiley(1, false, 1, 300); //Close both eyes
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

        drawHeart(2, 500); // Blink with an heart two times
        drawHeart(1, 300);
        drawHeart(2, 300);
        drawHeart(1, 300);
        drawHeart(2, 500);        
      }

      drawSmiley(1, true, 1, 500);
 
      state = 1;
      break;

    case 20: // medium water

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

      state = 1;
      break;

    case 30: // To much Water
      randDelay = random(2500, 4000);
      drawSmiley(1, true, 3, int(randDelay));
      drawSmiley(1, false, 3, 300);
      
      state = 1;
      break;

    case 70: // Get to sleep

      drawSmiley(1, false, 1, 800); //Close both eyes
      drawSmiley(1, true , 1, 200); //Open both eyes
      drawSmiley(1, false, 1, 800); //Close both eyes
      drawSmiley(11, true, 1, 400); //Open one eye

      drawSmiley(1, false, 5, 600); //Close both eyes
      drawSmiley(1, false, 2, 600); //Close both eyes

      drawSmiley(1, false, 5, 600); //Close both eyes
      //drawSmiley(1, false, 2, 1200); //Close both eyes

      drawSmiley(1, false, 8, 200); //Close both eyes
      drawSmiley(1, false, 9, 200); //Close both eyes      
      drawSmiley(1, false, 8, 200); //Close both eyes
      drawSmiley(1, false, 9, 200); //Close both eyes      


      drawSmiley(1, false, 5, 1200); //Close both eyes

      //drawSmiley(1, false, 2, 1200); //Close both eyes
      drawSmiley(1, false, 8, 200); //Close both eyes
      drawSmiley(1, false, 9, 200); //Close both eyes      
      drawSmiley(1, false, 8, 200); //Close both eyes
      drawSmiley(1, false, 9, 200); //Close both eyes
      drawSmiley(1, false, 2, 300); //Close both eyes

      state++;
      break;

    case 71: // sleeping
    
      matrix.clear(); // Clear the matrix to turn of the lights
      uint8_t emptyArray[8];
      emptyArray[0] = 0;
      emptyArray[1] = 0;
      emptyArray[2] = 0;
      emptyArray[3] = 0;
      emptyArray[4] = 0;
      emptyArray[5] = 0;
      emptyArray[6] = 0;
      emptyArray[7] = 0;
      matrix.drawBitmap(0, 0, emptyArray, 8, 8, LED_GREEN); // Set the requested layout on the Matrix
      matrix.writeDisplay(); // Draw the matrix

      // Wait for the light
      if(lux > 10){
        state++;
      }

      break;

    case 72: // Wake up


      drawSmiley(1, false, 5, 1400); //Close both eyes moan
      drawSmiley(1, false, 2, 500); //Close both eyes flat mouth
      drawSmiley(11, true, 2, 600); //Open one eyes flat mouth
      drawSmiley(1, false, 2, 600); //Close both eyes flat mouth
      drawSmiley(1, true , 2, 200); //Open both eyes smile
      drawSmiley(1, false , 2, 200); //Open both eyes smile
      drawSmiley(1, true , 2, 200); //Open both eyes smile
      drawSmiley(1, false , 1, 200); //Open both eyes smile


      state = 1;
      break;


    default:
      state = 1;
      break;
  }

}

void drawHeart(int heartSize,  int delayTime){

  uint8_t heart[8] = {0,0,0,0,0,0,0,0};;
  matrix.clear(); // First of clear the matrix

  switch (heartSize)
  {
  case 1:
    // Large heart 
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
    heart[2] = B00101000;
    heart[3] = B01111100;
    heart[4] = B01111100;
    heart[5] = B00111000;
    heart[6] = B00010000;
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

  uint8_t smiley[] = {0,0,0,0,0,0,0,0};
  matrix.clear(); // First of clear the matrix

  switch (eyes)
  {
    case 1:
      // center_center
      if (eyesOpened){
        smiley[1] = B01100110;
      }
      smiley[2] = B01100110;
      break;

    case 2:
      // center_left
      if (eyesOpened)
      {
        smiley[1] = B11001100;
      }
      smiley[2] = B11001100;
      break;

    case 3:
      // center_right
      if (eyesOpened)
      {
        smiley[1] = B00110011;
      }
      smiley[2] = B00110011;
      break;

    case 4:
      // center_up
      if (eyesOpened)
      {
        smiley[0] = B01100110;
      }
      smiley[1] = B01100110;
      break;

    case 5:
      // left_up
      if (eyesOpened)
      {
        smiley[0] = B11001100;
      }
      smiley[1] = B11001100;
      break;

    case 6:
      // right_up
      if (eyesOpened)
      {
        smiley[0] = B00110011;
      }
      smiley[1] = B00110011;
      break;


    case 7:
      // center_down
      if (eyesOpened)
      {
        smiley[2] = B01100110;
      }
      smiley[3] = B01100110;
      break;

    case 8:
      // left_down
      if (eyesOpened)
      {
        smiley[2] = B11001100;
      }
      smiley[3] = B11001100;
      break;

    case 9:
      // center_down
      if (eyesOpened)
      {
        smiley[2] = B00110011;
      }
      smiley[3] = B00110011;
      break;

    case 10:
      // right_down
      if (eyesOpened)
      {
        smiley[2] = B00110011;
      }
      smiley[3] = B00110011;
      break;


    case 11:
      // center right blink
      smiley[1] = B01100000;
      smiley[2] = B01100110;
      break;

    default:
      // confused_opened
      smiley[0] = B00110000;
      smiley[1] = B00110110;
      smiley[2] = B00000110;
      break;
  }

  switch (mouth)
  {
    case 1:
      // Smile
      smiley[5] = B01000010;
      smiley[6] = B00111100;
      break;

    case 2:
      // ----
      smiley[5] = B01111110;
      break;

    case 3:
      // Sad
      smiley[5] = B00111100;
      smiley[6] = B01000010;
      break;

    case 4:
      // Kiss
      smiley[4] = B00001010;
      smiley[5] = B00000100;
      smiley[6] = B00001010;
      break;

    case 5:
      // Open
      smiley[4] = B00111100;
      smiley[5] = B01000010;
      smiley[6] = B00111100;
      break;

    case 6:
      // Tongue_out
      smiley[5] = B01000010;
      smiley[6] = B00111100;
      smiley[7] = B00001100;
      break;

    case 7:
      // Tongue_out flaot mouth
      smiley[6] = B01111110;
      smiley[7] = B00001100;
      break;

    case 8:
      // -±-±-
      smiley[4] = B00101000;
      smiley[5] = B01111110;
      smiley[6] = B00010100;
      break;

    case 9:
      // ±-±-
      smiley[4] = B00010100;
      smiley[5] = B01111110;
      smiley[6] = B00101000;
      break;


    default:
      // confused_opened
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