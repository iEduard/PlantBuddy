/*************************************************** 
  The coolest Robot to check your plants
    He will read the soil Moisture
    Temperature
    Humidity
    Light

  To check how good you treat your plant
 ****************************************************/


int soilMoistureValue = 0;



int DebugLevel = 10; // Debug level for the serial output

// Setup
void setup() {
  Serial.begin(9600);
  Serial.println("Plant Budy Debug output");
}

// Main loop
void loop() {

  // Read the sensor values

  soilMoistureValue = analogRead(A0); // Read the moisture sensor

  //Debug output
  if(DebugLevel > 0){
    Serial.println("----");
    Serial.println(soilMoistureValue); 
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



}