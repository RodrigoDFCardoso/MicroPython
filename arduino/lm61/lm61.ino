void setup() {
  // Inicialize o monitor serial
  Serial.begin(9600);
}

void loop() {
  // Leia a tensão no pino A0
  int sensorValue = analogRead(A0);
  
  // Converta a tensão em temperatura em graus Celsius
  float voltage = (sensorValue / 1023.0) * 5.0;  // Tensão de referência de 5V no Arduino
  float temperatureC = (voltage - 0.5) * 100.0;  // Fórmula de conversão

  // Exiba a temperatura no monitor serial
  Serial.print("Temperatura (C): ");
  Serial.println(temperatureC);

  // Aguarde um curto período de tempo antes da próxima leitura
  delay(1000);
}
